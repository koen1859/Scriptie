import math

import matplotlib.pyplot as plt
import numpy as np


def find_beta(lengths, area):
    A = area * 1000000
    b, x, y = [], [], []
    b_hat_n = {}

    for n in sorted(lengths.keys()):
        b_n = []
        for length in lengths[n]:
            b.append(length / math.sqrt(n * A))
            b_n.append(length / math.sqrt(n * A))
            x.append(n)
            y.append(length)
            b_hat_n[n] = sum(b_n) / len(b_n)
    b_hat = sum(b) / len(b)

    return x, y, b_hat, b_hat_n


def scatterplot(lengths, x, y, b_hat, area, filename):
    A = area * 1000000
    line = [b_hat * math.sqrt(n * A) for n in sorted(lengths.keys())]

    plt.figure(figsize=(20, 15))
    plt.scatter(np.log(x), np.log(y), label="Simulated values", alpha=0.6)
    plt.plot(
        np.log(sorted(lengths.keys())),
        np.log(line),
        label=f"Estimated line b = {b_hat:.2f}",
    )
    plt.xlabel("n (number of locations (log scale))")
    plt.ylabel("y (TSP path length (m) (log scale))")
    plt.legend()
    plt.title("Scatterplot of TSP path lengths with estimated line y = b * sqrt(n * A)")
    plt.savefig(f"plots/{filename}")
    plt.show()


def errorsplot(lengths, x, y, b_hat, area, filename):
    A = area * 1000000
    sorted_keys = sorted(lengths.keys())
    line = [b_hat * math.sqrt(n * A) for n in sorted_keys]
    errors = [line[sorted_keys.index(x[i])] - y[i] for i in range(len(x))]

    plt.figure(figsize=(20, 15))
    plt.scatter(x, errors, label="Prediction errors", alpha=0.6)
    plt.xlabel("n (number of locations)")
    plt.ylabel("Error (TSP path length (m))")
    plt.legend()
    plt.title("Scatterplot of TSP path length prediction errors")
    plt.savefig(f"plots/{filename}")
    plt.show()
