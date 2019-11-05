import pandas as pd
import itertools
import re
# User Input for Dataset
file_name = input("Enter file name: ")
# Reading file into Dataframe
Data = pd.read_csv(file_name, sep='\t', lineterminator='\n', header=None)
# Appending "Gx_" to each item where x is column number
for i in range(len(Data.columns)):
    Data[i] = 'G' + str(i + 1) + "_" + Data[i].astype(str)
# User Input for Support
Support = int(input("Enter Support Percentage: "))
Support = Support / 100 * len(Data)
print("Support is set to be ",int(Support),"%")
freq_set = set()
l = len(Data.columns)
# Extracting unique items from each column
for i in range(l):
    d = Data[i]
    for j in d:
        if j not in freq_set:
            freq_set.add(j)
# Creating a superset of each row of the given dataset for comparison with frequent itemsets
Superset = []
for i in range(len(Data)):
    Superset.append(set(Data.iloc[i]))
# Function to generate all combinations of lengths 1,2,3,4,.. etc.
# itertools.combinations returns a list of possible combinations of desired length
def allcombinations(items, c):
    combinations = itertools.combinations(items, c)
    return [set(i) for i in list(combinations)]
# Initializing s as 0 for calculating total number of frequent itemsets of all lengths
s = 0
final_list=[]
for i in range(1, l):
    # Getting combinations for each length
    candidates = allcombinations(freq_set, i)
    set_ap = []
# Count frequency of each combination present in the superset and storing those that have greater value than support provided by user
    for k in candidates:
        sup_count = 0
        for j in Superset:
            if k.issubset(j):
                sup_count = sup_count + 1
        if sup_count >= Support:
            set_ap.append(k)
            final_list.append(k)
# Exiting the loop if no new itemsets are found for a particular length
    if len(set_ap) == 0:
        break
    else:
        print("number of length-" + str(i), "frequent itemsets: " + str(len(set_ap)))
        s += len(set_ap)
    # Storing unique values of the itemsets for sending as input to combinations calculator
    freq_set = set()
    for i in set_ap:
        for j in i:
            if j not in freq_set:
                freq_set.add(j)
print("number of all lengths frequent itemsets: ", s)
print("Final list of frequent itemsets: ")
for f in final_list:
    print(f)
# User Input for Confidence
conf = int(input("Enter confidence Percentage: "))
conf = conf / 100 * len(Data)
print("Minimum Confidence is set to be ",int(conf),"%")
conf=conf/100
# Generating Assosiation Rules from Frequent itemsets
rules = []
for i in range(0, len(final_list)):
    count = []
    for items in final_list[i]:
        count.append(items)
    # To ignore Frequent items of length 1
    if len(count)>1:
        # For each item of length 2, generate two candidate rules by swapping RHS and LHS
        if len(count)==2:
            for k in final_list[i]:
                sup_count = 0
                rhs = 0
                k = {k}
                for j in Superset:
                    if final_list[i].issubset(j):
                        sup_count = sup_count + 1
                    if k.issubset(j):
                        rhs = rhs + 1
                # Computing Confidence for each rule
                final_conf = sup_count/rhs
                #print(final_conf,k,"-->",str(final_list[i]-k),"Sup:", sup_count," rhs:",rhs)
                # Check if candidate rule has confidence greater than or equal to minconf 
                if final_conf>=conf:
                    #print(final_conf,k)
                    rule_form = str(k) + "-->" + str(final_list[i]-k)
                    rules.append(rule_form)
        else:
            # For Frequent itemsets having length greater than 3
            cand = []
            # Generate all possible combinations of LHS
            for c in range(1,len(count)):
                cand = cand + allcombinations(final_list[i],c)
            # Check confidence for each combination of LHS
            for k in cand:
                sup_count = 0
                lhs = 0
                for j in Superset:
                    if final_list[i].issubset(j):
                        sup_count = sup_count + 1
                    if k.issubset(j):
                        lhs = lhs + 1
                final_conf = sup_count/lhs
                #print(final_conf,k,"-->",str(final_list[i]-k))
                # Check if candidate rule has confidence greater than or equal to minconf 
                if final_conf>=conf:
                    rule_form = str(k) + "-->" + str(final_list[i]-k)
                    rules.append(rule_form)
print("Total number of rules generated: ",len(rules))
print("Rules:")
for r in rules:
    print(r)
# Split the Rules as Head and Body
head = []
body = []
for i in rules:
    lhs,rhs = i.split("-->")
    head.append(lhs)
    body.append(rhs)


# Function for TEMPLATE 1
def Template1(arg1, arg2, arg3):
    # Store the final queried rules
    temp = []
    if arg1 == "RULE":
        if arg2 == "ANY":
            # Traversing through all the rules and storing the rule that contains the query items
            for i in range(0, len(rules)):
                for arg in arg3:
                    if arg in rules[i]:
                        temp.append(rules[i])
        elif arg2 == "NONE":
            # Making two copies of the rules to avoid issues while deleting rules containg each item(item1, item2...)
            t = rules.copy()
            a = rules.copy()
            for arg in arg3:
                for i in t:
                    if arg in i:
                        a.remove(i)
                t = a.copy()
            temp = t.copy()
        elif arg2 == 1:
            r = []
            # Saving all the rules containing any of the items(May include the rules with all the items which needs to be removed)
            for arg in arg3:
                for i in range(0, len(rules)):
                    if arg in rules[i]:
                        r.append(rules[i])
            # Removing the rules containing all the items
            new_rule = r.copy()
            for i in r:
                flag = 0
                for arg in arg3:
                    if arg in i:
                        flag += 1
                if flag != 1:
                    new_rule.remove(i)
            temp = new_rule.copy()
        elif type(arg2) == int:
            # For more than one combinations
            if (len(arg3) < arg2):
                print("Invalid Input")
            elif len(arg3) == arg2:
                # no exclusions required
                for r in rules:
                    f = 1
                    for arg in arg3:
                        if arg not in r:
                            f = 0
                    if f == 1:
                        temp.append(r)
            else:
                # Find combinations of size arg2(Number of elements to be present in the rule)
                combinations = allcombinations(arg3, arg2)
                for comb in combinations:
                    # Create the list of elements to be excluded if present in the rule
                    List = list(set(arg3) - set(comb))
                    for r in rules:
                        f = 1
                        for c in comb:
                            if c not in r:
                                f = 0
                        if f == 1:
                            a = 1
                            for l in List:
                                if l in r:
                                    a = 0
                            if a == 1:
                                # Append the rule if it does not contain the element from the exclusion list and contains number of items required
                                temp.append(r)
        else:
            print("Invalid Input")

    elif arg1 == "HEAD":
        if arg2 == "ANY":
            # Traversing through all the rules and storing the rule that contains the query items in it's head
            for i in range(0, len(head)):
                for arg in arg3:
                    if arg in head[i]:
                        temp.append(rules[i])
        elif arg2 == "NONE":
            # Making two copies of the rules to avoid issues while deleting rules/heads containg each item(item1, item2...)
            t = head.copy()
            a = head.copy()
            new_rules = rules.copy()
            new_rules1 = rules.copy()
            for arg in arg3:
                for i in range(0, len(t)):
                    if arg in t[i]:
                        a.remove(t[i])
                        new_rules1.remove(new_rules[i])
                t = a.copy()
                new_rules = new_rules1.copy()
            temp = new_rules.copy()
        elif arg2 == 1:
            h = []
            r = []
            # Saving all the rules/heads containing any of the items(May include the rules with all the items which needs to be removed)
            for arg in arg3:
                for i in range(0, len(head)):
                    if arg in head[i]:
                        r.append(rules[i])
                        h.append(head[i])
            h1 = h.copy()
            r1 = r.copy()
            if len(arg3) == 1:
                temp = r1.copy()
            else:
                # Removing the rules/heads containing all the items
                for i in range(0, len(h)):
                    flag = 0
                    for arg in arg3:
                        if arg in h[i]:
                            flag += 1
                    if flag != 1:
                        h1.remove(h[i])
                        r1.remove(r[i])
                temp = r1.copy()
        elif type(arg2) == int:
            # For more than one combination
            if (len(arg3) < arg2):
                print("Invalid Input")
            elif len(arg3) == arg2:
                # No exclusions required
                for h in range(0, len(head)):
                    f = 1
                    for arg in arg3:
                        if arg not in head[h]:
                            f = 0
                    if f == 1:
                        temp.append(rules[h])
            else:
                # Find combinations of size arg2(Number of elements to be present in head)
                combinations = allcombinations(arg3, arg2)
                for comb in combinations:
                    # Create the list of elements to be excluded if present in the head
                    List = list(set(arg3) - set(comb))
                    for i in range(0, len(head)):
                        f = 1
                        for c in comb:
                            if c not in head[i]:
                                f = 0
                        if f == 1:
                            a = 1
                            for l in List:
                                if l in head[i]:
                                    a = 0
                            if a == 1:
                                # Append the rule if it does not contain the element from the exclusion list and contains number of items required
                                temp.append(rules[i])
        else:
            print("Invalid Input")
    elif arg1 == "BODY":
        if arg2 == "ANY":
            # Traversing through all the rules and storing the rule that contains the query items in it's body
            for i in range(0, len(body)):
                for arg in arg3:
                    if arg in body[i]:
                        temp.append(rules[i])
        elif arg2 == "NONE":
            # Making two copies of the rules to avoid issues while deleting rules/bodies containg each item(item1, item2...)
            t = body.copy()
            a = body.copy()
            new_rules = rules.copy()
            new_rules1 = rules.copy()
            for arg in arg3:
                for i in range(0, len(t)):
                    if arg in t[i]:
                        a.remove(t[i])
                        new_rules1.remove(new_rules[i])
                t = a.copy()
                new_rules = new_rules1.copy()
            temp = new_rules.copy()
        elif arg2 == 1:
            b = []
            r = []
            # Saving all the rules/bodies containing any of the items(May include the rules with all the items which needs to be removed)
            for arg in arg3:
                for i in range(0, len(body)):
                    if arg in body[i]:
                        r.append(rules[i])
                        b.append(body[i])
            b1 = b.copy()
            r1 = r.copy()
            if len(arg3) == 1:
                temp = r1.copy()
            else:
                # Removing the rules/bodies containing all the items
                for i in range(0, len(b)):
                    flag = 0
                    for arg in arg3:
                        if arg in b[i]:
                            flag += 1
                    if flag != 1:
                        b1.remove(b[i])
                        r1.remove(r[i])
                temp = r1.copy()
        elif type(arg2) == int:
            # For more than one combination
            if (len(arg3) < arg2):
                print("Invalid Input")
            elif len(arg3) == arg2:
                # No exclusions required
                for i in range(0, len(body)):
                    f = 1
                    for arg in arg3:
                        if arg not in body[i]:
                            f = 0
                    if f == 1:
                        temp.append(rules[i])
            else:
                # Find combinations of size arg2(Number of elements to be present in body)
                combinations = allcombinations(arg3, arg2)
                for comb in combinations:
                    # Create the list of elements to be excluded if present in body
                    List = list(set(arg3) - set(comb))
                    for i in range(0, len(body)):
                        f = 1
                        for c in comb:
                            if c not in body[i]:
                                f = 0
                        if f == 1:
                            a = 1
                            for l in List:
                                if l in body[i]:
                                    a = 0
                            if a == 1:
                                # Append the rule if it does not contain the element from the exclusion list and contains number of items required
                                temp.append(rules[i])
        else:
            print("Invalid Input")
    # Removing Duplicates
    temp = list(dict.fromkeys(temp))
    # Returning queried list of rules
    return temp
#Function for Template 2
def Template2(arg_1,arg_2):
    temp = []
    if arg_1 == "RULE":
        #Traversing through all the rules
        for i in range(0,len(rules)):
            #Retreiving strings within single quotes and storing it in a list
            s = re.findall(r"'(.*?)'",rules[i])
            #If length of the list is greater than the 2nd argument(Count) given by user then add the rule to temp
            if len(s) >= arg_2:
                temp.append(rules[i])
    elif arg_1 == "HEAD":
        #Traversing through all the heads
        for i in range(0,len(head)):
             #Retreiving strings within single quotes and storing it in a list
            s = re.findall(r"'(.*?)'",head[i])
            #If length of the list is greater than the 2nd argument(Count) given by user then add the rule to temp
            if len(s) >= arg_2:
                temp.append(rules[i])
    elif arg_1 == "BODY":
        #Traversing through all the bodies
        for i in range(0,len(body)):
            #Retreiving strings within single quotes and storing it in a list
            s = re.findall(r"'(.*?)'",body[i])
            #If length of the list is greater than the 2nd argument(Count) given by user then add the rule to temp
            if len(s) >= arg_2:
                temp.append(rules[i])
    else:
            print("Invalid Input")
    #Returning queried list of rules
    return temp
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
#Function for Template 3
def Template3(arg):
    if arg[0]=="1or1":
        #Quering for two Queries from Template1
        list1=Template1(arg[1],arg[2],arg[3])
        list2=Template1(arg[4],arg[5],arg[6])
        #Merging the lists
        final_list=list1+list2
        #Removing Duplicates
        final_list = list(dict.fromkeys(final_list))
    elif arg[0]=="1and1":
        #Quering for two Queries from Template1
        list1=Template1(arg[1],arg[2],arg[3])
        list2=Template1(arg[4],arg[5],arg[6])
        #Finding intersection of two lists
        final_list = intersection(list1,list2)
    elif arg[0]=="1or2":
        #Quering for two Queries from Template1 and Template 2
        list1=Template1(arg[1],arg[2],arg[3])
        list2=Template2(arg[4],arg[5])
        #Merging the lists
        final_list=list1+list2
        #Removing Duplicates
        final_list = list(dict.fromkeys(final_list))
    elif arg[0]=="1and2":
        #Quering for two Queries from Template1 and Template 2
        list1=Template1(arg[1],arg[2],arg[3])
        list2=Template2(arg[4],arg[5])
        #Finding intersection of two lists
        final_list = intersection(list1,list2)
    elif arg[0]=="2or2":
        #Quering for two Queries from Template2
        list1=Template2(arg[1],arg[2])
        list2=Template2(arg[3],arg[4])
        #Merging the lists
        final_list=list1+list2
        #Removing Duplicates
        final_list = list(dict.fromkeys(final_list))
    elif arg[0]=="2and2":
        #Quering for two Queries from Template2
        list1=Template2(arg[1],arg[2])
        list2=Template2(arg[3],arg[4])
        #Finding intersection of two lists
        final_list = intersection(list1,list2)
    #Returning queried list of rules    
    return final_list
while True:
    #User Input for Queries
    Query= input("Enter Query Or \"exit\" for Exiting: ")
    if Query == "exit":
        break
    if("template1" in Query):
        Query=Query.replace("asso_rule.template1","")
        #Split and store the query arguments in an array
        arg=eval(Query)
        print("Query: ", Query)
        final_list=Template1(arg[0],arg[1],arg[2])
    elif("template2" in Query):
        Query=Query.replace("asso_rule.template2","")
        #Split and store the query arguments in an array
        arg=eval(Query)
        print("Query: ", Query)
        final_list=Template2(arg[0],arg[1])
    elif("template3" in Query):
        Query=Query.replace("asso_rule.template3","")
        #Split and store the query arguments in an array
        arg=eval(Query)
        print("Query: ", Query)
        final_list=Template3(arg)
    print("Count:",len(final_list))
    print("Rules Queried:")
    for r in final_list:
        print(r)