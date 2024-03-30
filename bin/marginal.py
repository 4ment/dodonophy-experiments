#!/usr/bin/env python

import os
import re
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def estimate_marginal_importance(filename):
    likelihoods, priors, jacobians, variational_weights = read_vbis(filename)
    n = len(likelihoods)

    log_estimated_marginal_sum = 0.0
    log_samples = likelihoods + priors + jacobians - variational_weights
    log_estimated_marginal_sum = np.logaddexp.reduce(log_samples)

    log_estimated_marginal = log_estimated_marginal_sum - np.log(n)
    return log_estimated_marginal


def count_lines(filename):
    with open(filename, "r", encoding="UTF-8") as file:
        count = sum(1 for _ in file)
    return count


def read_vbis(filename):
    with open(filename, "r", encoding="UTF-8") as file:
        line_count = count_lines(filename)
        if line_count == 0:
            return None

        likelihood = np.zeros((line_count))
        prior = np.zeros((line_count))
        variational_weight = np.zeros((line_count))
        jacobian = np.zeros((line_count))

        for i, line in enumerate(file):
            match = re.search(r"&lnL=(-?\d+\.\d+)", line)
            if match:
                likelihood[i] = float(match.group(1))

            match = re.search(r"&lnPr=(-?\d+\.\d+)", line)
            if match:
                prior[i] = float(match.group(1))

            match = re.search(r"&lnQ=(-?\d+\.\d+)", line)
            if match:
                variational_weight[i] = float(match.group(1))

            match = re.search(r"&lnJac=(-?\d+\.\d+)", line)
            if match:
                jacobian[i] = float(match.group(1))

    nonzero_indices = np.nonzero(likelihood)

    return (
        likelihood[nonzero_indices],
        prior[nonzero_indices],
        jacobian[nonzero_indices],
        variational_weight[nonzero_indices],
    )


def compute_marginal_for_files(filenames):
    marginal_values = []

    for filename in filenames:
        if os.path.isfile(filename):
            marginal = estimate_marginal_importance(filename)
            if marginal is not None:
                marginal_values.append(marginal)
        else:
            marginal_values.append(None)
            # raise FileExistsError(filename)

    return marginal_values


def plot_over_booots(filenames):
    # plot the estimated marginal for different number of boosts
    boost_numbers = list(range(1, len(filenames) + 1))
    marginal_values = compute_marginal_for_files(filenames)

    for filename, marginal in zip(filenames, marginal_values):
        a = os.path.split(filename)[-2]
        boost = re.search(r"b\d", a).group(0)
        print(f"Boosts{boost[1:]}: -> marginal: {marginal}")

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(4, 4)
    ax.set_position([0.20, 0.11, 0.79, 0.88])
    plt.rcParams.update({"font.size": 11})
    plt.plot(boost_numbers, marginal_values, marker="o", color="k")
    plt.xlabel("Boosts (K)")
    plt.ylabel("Estimated Marginal Probability")
    plt.show()


def print_over_ds(filenames):
    # print the estimated marginal for different data sets
    marginal_values = compute_marginal_for_files(filenames)
    data = {}
    for filename, marginal in zip(filenames, marginal_values):
        ds = re.search(r"DS\d", filename).group(0)
        print(f"{ds}: -> marginal: {marginal}")
        data[ds] = [marginal]

    df = pd.DataFrame(data, index=["Dodonaphy"])
    df = df.reindex(sorted(df.columns), axis=1).to_latex()
    with open("table1.tex", "w") as fp:
        fp.write(df)
    print(df)


if __name__ == "__main__":
    print_over_ds(sys.argv[1:])
    # plot_over_booots(sys.argv[1:])
