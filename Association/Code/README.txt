README

Install python 3.7.4 version, pandas and itertools

Run the submitted python file in Command prompt. Keep the file associationruletestdata.txt in the same folder as the python file in order to avoid giving full path when prompted for filename.

Example:

python3 Part-2.py


- User prompt for input dataset. Enter the filename along with path.
- User prompt for Support value. Enter Support.
  Generated Frequent item-sets along with count are displayed.
- User prompt for Confidence value. Enter Confidence.
  Association rules for the specified Support and Confidence are displayed.
- User prompt for queries. Specify queries as per the template format
  Corresponding query results with count are displayed.

Queries format:
Type in queries as per format given in Template.pdf

Examples:

asso_rule.template1("RULE", "ANY", ['G59_Up'])
asso_rule.template1("RULE", "NONE", ['G59_Up'])
asso_rule.template1("RULE", 1, ['G59_Up', 'G10_Down'])
asso_rule.template1("HEAD", "ANY", ['G59_Up'])
asso_rule.template1("HEAD", "NONE", ['G59_Up'])
asso_rule.template1("HEAD", 1, ['G59_Up', 'G10_Down'])
asso_rule.template1("BODY", "ANY", ['G59_Up'])
asso_rule.template1("BODY", "NONE", ['G59_Up'])
asso_rule.template1("BODY", 1, ['G59_Up', 'G10_Down'])
asso_rule.template2("RULE", 3)
asso_rule.template2("HEAD", 2)
asso_rule.template2("BODY", 1)
asso_rule.template3("1or1", "HEAD", "ANY", ['G10_Down'], "BODY", 1, ['G59_Up'])
asso_rule.template3("1and1", "HEAD", "ANY", ['G10_Down'], "BODY", 1, ['G59_Up'])
asso_rule.template3("1or2", "HEAD", "ANY", ['G10_Down'], "BODY", 2)
asso_rule.template3("1and2", "HEAD", "ANY", ['G10_Down'], "BODY", 2)
asso_rule.template3("2or2", "HEAD", 1, "BODY", 2)
asso_rule.template3("2and2", "HEAD", 1, "BODY", 2)


 