#!/usr/bin/env python

import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import StrMethodFormatter

if len(sys.argv) > 2:
    df = pd.concat(
        [pd.read_csv(f, names=["program", "dataset", "lnl"]) for f in sys.argv[1:]]
    )
else:
    df = pd.read_csv(sys.argv[1])

df = df.pivot(index="dataset", columns="program", values="lnl")
df = df.reindex(sorted(df.columns, reverse=True), axis=1)
df = df.sort_index(ascending=True)

# Create subplots
fig, ax = plt.subplots()

# Plot trendlines for each column
jitter = 0.01
for i, data_label in enumerate(df.index.values):
    x_jitter = (i - 3.5) * jitter
    ax.scatter(
        np.arange(len(df.columns.values)) + x_jitter,
        df.iloc[i] - df.iat[i, 0],
        label=data_label,
    )

# Add grid and legend
ax.legend()
ax.grid()
ax.set_yscale("symlog", linthresh=1)

# Set labels and title
ax.set_ylabel("Log Likelihood Difference", fontsize=14)
ax.set_xticks(np.arange(len(df.columns.values)))
ax.set_xticklabels(df.columns.values, rotation=0, ha="center")

ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
ax.tick_params(axis="both", which="major", labelsize=12)
plt.tight_layout()

plt.savefig("ml_performance.jpg", format="jpg")
plt.savefig("ml_performance.eps", format="eps", dpi=1200)
# plt.show()
