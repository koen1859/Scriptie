import math
import matplotlib.pyplot as plt

def find_beta(lengths):
    A = 2959.68 * 1000000
    b, x, y = [], [], []

    for n, lengths_list in lengths.items():
        for length in lengths_list:
            b.append(length / math.sqrt(n * A))
            x.append(n)
            y.append(length)
    b_hat = sum(b) / len(b)

    return x, y, b_hat

def scatterplot(lengths, x, y, b_hat):
    A = 2959.68 * 1000000
    line = [b_hat * math.sqrt(n * A) for n in lengths.keys()]

    plt.figure(figsize = (20,15))
    plt.scatter(x, y, label="Simulated values", alpha = 0.6)
    plt.plot(lengths.keys(), line, label=f"Estimated line b = {b_hat:.2f}")
    plt.xlabel("n (number of locations)")
    plt.ylabel("y (TSP path length (m))")
    plt.legend()
    plt.title("Scatterplot of TSP path lengths with estimated line y = b * sqrt(n * A)")
    plt.savefig("plots/scatter.png")
    plt.show()
