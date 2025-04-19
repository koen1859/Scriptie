import math

import matplotlib.pyplot as plt
import numpy as np


def find_beta(lengths, area):
    b, x, y = [], [], []
    b_hat_n = {}

    for n in sorted(lengths.keys()):
        b_n = []
        for length in lengths[n]:
            b.append(length / math.sqrt(n * area))
            b_n.append(length / math.sqrt(n * area))
            x.append(n)
            y.append(length)
            b_hat_n[n] = sum(b_n) / len(b_n)
    b_hat = np.mean(b)

    return x, y, b_hat, b_hat_n


def results(lengths, x, y, b_hat, area):
    sorted_keys = sorted(lengths.keys())
    line = [b_hat * math.sqrt(n * area) for n in sorted_keys]
    errors = [line[sorted_keys.index(x[i])] - y[i] for i in range(len(x))]
    MAE = np.mean(np.mean(np.abs(errors)) / line)

    return line, errors, MAE


def scatterplot(lengths, x, y, b_hat, area, filename):
    line = [b_hat * math.sqrt(n * area) for n in sorted(lengths.keys())]

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


def errorsplot(lengths, x, y, b_hat, area, filename):
    sorted_keys = sorted(lengths.keys())
    line = [b_hat * math.sqrt(n * area) for n in sorted_keys]
    errors = [line[sorted_keys.index(x[i])] - y[i] for i in range(len(x))]

    plt.figure(figsize=(20, 15))
    plt.hist(errors, label="Prediction errors", alpha=0.6)
    plt.xlabel("Predictio error (m)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.title("Histogram of TSP path length prediction errors")
    plt.savefig(f"plots/{filename}")
