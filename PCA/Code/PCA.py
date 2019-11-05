import pandas as pd
import numpy as np
import math
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pylab as pl
print("Enter the text filename with it's whole path")
path = input()

def pca(path):
    df = pd.read_fwf(path)
    df = pd.read_csv(path, delimiter="\t")
    df.to_csv('a.csv', encoding='utf-8', index=False)
    print(df.head(5))

    row, col = df.shape
    print("Row: ", row)
    print("Col: ", col)

    X = df.iloc[:, 0:col - 1].values
    y = df.iloc[:, col - 1].values

    a = np.unique(y)
    l = len(a)
    print("unique no. of values in last column: ", l)
    print(a)

    #X_std = StandardScaler().fit_transform(X)
    #X_std=preprocessing.normalize(X)
    X_std = X - X.mean()
    cov_mat = np.cov(X_std.T)
    eig_vals, eig_vecs = np.linalg.eig(cov_mat)


    # Sort the (eigenvalue, eigenvector) tuples from high to low
    # Make a list of (eigenvalue, eigenvector) tuples
    eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:, i]) for i in range(len(eig_vals))]

    # Sort the (eigenvalue, eigenvector) tuples from high to low
    eig_pairs.sort(key=lambda tup: tup[0])
    eig_pairs.reverse()

    matrix_w = np.hstack((eig_pairs[0][1].reshape(col - 1, 1),
                          eig_pairs[1][1].reshape(col - 1, 1)))

    Y = X_std.dot(matrix_w)

    colors = ['blue', 'orange', 'green', 'red', 'hotpink', 'y', 'cyan', 'purple', 'pink', 'yellow', 'gold',
              'lightcoral', 'salmon', 'yellowgreen', 'greenyellow', 'olive', 'gray', 'navy']

    plt.figure(figsize=(12, 7))

    for c, i, target_name in zip(colors, a, a):
        pl.scatter(Y[y == i, 0], Y[y == i, 1], c=c, label=target_name)

    pl.xlabel('Principal Component 1')
    pl.ylabel('Principal Component 2')
    pl.legend()
    pl.savefig('PCA.png')
    pl.title('PCA')
    pl.show()

pca(path)
print("Exiting...")
exit(0)
##C:/Users/malin/Desktop/d.txt