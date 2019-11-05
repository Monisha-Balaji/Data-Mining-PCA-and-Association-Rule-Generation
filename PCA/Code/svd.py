import csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler

print("Enter the text filename with it's whole path")
path = input()
def svd(path):
    df = pd.read_fwf(path)
    df = pd.read_csv(path, delimiter="\t")
    df.to_csv('a.csv', encoding='utf-8', index=False)

    row, col = df.shape
    print("Row: ", row)
    print("Col: ", col)

    X = df.iloc[:, 0:col - 1].values
    y = df.iloc[:, col - 1].values
    a = np.unique(y)
    l = len(a)
    print("unique no. of values in last column: ", l)
    print(a)

    X_scaled = StandardScaler().fit_transform(X)

    svd = TruncatedSVD(n_components=2)
    Y_fitted = svd.fit_transform(X_scaled)

    colors = ['blue', 'orange', 'green', 'red', 'hotpink', 'y', 'cyan', 'purple', 'pink', 'yellow', 'gold',
              'lightcoral', 'salmon', 'yellowgreen', 'greenyellow', 'olive', 'gray', 'navy']

    for labels, columns in zip(a, colors):
        plt.scatter(Y_fitted[y == labels, 0], Y_fitted[y == labels, 1], label=labels)

    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.legend(loc='best')
    plt.title("SVD", fontsize=20)
    plt.savefig('svd.png')
    plt.show()


svd(path)
print("Exiting...")
exit(0)