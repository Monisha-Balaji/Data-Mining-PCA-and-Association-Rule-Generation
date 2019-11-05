import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from sklearn.manifold import TSNE

print("Enter the text filename with it's whole path")
path = input()
def tsne(path):
    #df = pd.read_fwf(path)
    df = pd.read_csv(path, delimiter="\t")
    #df.to_csv('a.csv', encoding='utf-8', index=False)

    row, col = df.shape
    print("Row: ", row)
    print("Col: ", col)

    X = df.iloc[:, 0:col - 1].values
    y = df.iloc[:, col - 1].values

    a = np.unique(y)
    l = len(a)
    print("unique no. of values in last column: ", l)
    print(a)

    tsne = TSNE(n_components=2, random_state=0)
    X_2d = tsne.fit_transform(X)

    colors = ['blue', 'orange', 'green', 'red', 'hotpink', 'y', 'cyan', 'purple', 'pink', 'yellow', 'gold',
              'lightcoral', 'salmon', 'yellowgreen', 'greenyellow', 'olive', 'gray', 'navy']

    plt.figure(figsize=(10, 7))

    for c, i, target_name in zip(colors, a, a):
        pl.scatter(X_2d[y == i, 0], X_2d[y == i, 1], c=c, label=target_name)

    pl.xlabel('Component 1')
    pl.ylabel('Component 2')
    pl.legend()
    pl.title('TSNE')
    pl.savefig('TSNE.png')
    pl.show()

tsne(path)
print("Exiting...")
exit(0)