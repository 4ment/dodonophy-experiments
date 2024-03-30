#!/usr/bin/env python

import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

# Step 1: Read the data from the CSV file into a pandas DataFrame
df = pd.read_csv(sys.argv[1])

# Step 2: Create the scatter plot for complete data points
fig = plt.figure(figsize=(4, 4))
fig.gca().set_position([0.19, 0.11, 0.80, 0.88])

complete_df = df.dropna(how="any")

alpha1_complete = (
    complete_df["Mean_Edge_Length_MB1"] / complete_df["Mean_Edge_Length_MB1"].max()
) ** 0.25
for x, y, dx, dy, alpha in zip(
    complete_df["Mean_Edge_Length_MB1"],
    complete_df["Mean_Edge_Length_Dodonaphy"],
    complete_df["Std_Edge_Length_MB1"],
    complete_df["Std_Edge_Length_Dodonaphy"],
    alpha1_complete,
):
    plt.errorbar(
        x, y, xerr=dx, yerr=dy, linestyle="None", color="gray", alpha=0.5 * alpha
    )
    plt.scatter(x, y, color="black", alpha=alpha)


plot_both_runs = False
if plot_both_runs:
    alpha2_complete = (
        complete_df["Mean_Edge_Length_MB2"] / complete_df["Mean_Edge_Length_MB2"].max()
    ) ** 0.25
    for x, y, dx, dy, alpha in zip(
        complete_df["Mean_Edge_Length_MB2"],
        complete_df["Mean_Edge_Length_Dodonaphy"],
        complete_df["Std_Edge_Length_MB2"],
        complete_df["Std_Edge_Length_Dodonaphy"],
        alpha2_complete,
    ):
        plt.errorbar(
            x, y, xerr=dx, yerr=dy, linestyle="None", color="gray", alpha=0.5 * alpha
        )
        plt.scatter(x, y, color="red", alpha=alpha)
    plt.scatter(None, None, label="MB1", color="black", marker="o")
    plt.scatter(None, None, label="MB2", color="red", marker="o")
else:
    plt.errorbar(
        None, None, None, None, label="True Inclusions", color="black", marker="o"
    )

# plt.errorbar(df['Mean_Edge_Length_MB2'], df['Mean_Edge_Length_Dodonaphy'], xerr=df['Std_Edge_Length_MB2'], yerr=df['Std_Edge_Length_Dodonaphy'], linestyle='None', color='gray', alpha=0.5)
# plt.errorbar(df['Mean_Edge_Length_MB2'], df['Mean_Edge_Length_Dodonaphy'], xerr=df['Std_Edge_Length_MB2'], yerr=df['Std_Edge_Length_Dodonaphy'], linestyle='None', color='gray', alpha=0.5)
# plt.scatter(df['Mean_Edge_Length_MB1'], df['Mean_Edge_Length_Dodonaphy'], label='MB1', color='blue')
# plt.scatter(df['Mean_Edge_Length_MB2'], df['Mean_Edge_Length_Dodonaphy'], label='MB2', color='blue')
# sns.kdeplot(x=df['Mean_Edge_Length_MB1'], y=df['Mean_Edge_Length_Dodonaphy'], cmap='viridis', fill=True)


# Step 3: Identify and plot the missing data points on the x-axis
missing_x = df[df["Mean_Edge_Length_Dodonaphy"].isna()]["Mean_Edge_Length_MB1"]
plt.scatter(
    missing_x, np.zeros_like(missing_x), color="burlywood", marker="o", alpha=0.2
)
plt.scatter(
    None,
    None,
    None,
    None,
    label="False Omissions",
    color="burlywood",
    marker="o",
)

# Step 4: Identify and plot the missing data points on the y-axis
missing_y = df[df["Mean_Edge_Length_MB1"].isna()]["Mean_Edge_Length_Dodonaphy"]
plt.scatter(np.zeros_like(missing_y), missing_y, color="plum", marker="o", alpha=0.2)
plt.scatter(None, None, None, None, label="False Inclusions", color="plum", marker="o")

x = (0, df["Mean_Edge_Length_MB1"].max())
plt.plot(x, x, color="k")
handles = [
    Line2D([0], [0], linestyle="none", color="r", marker="d", label="Internal Split"),
    Line2D([0], [0], linestyle="none", color="b", marker="o", label="Leaf Split"),
]

plt.xlabel("Edge Lengths MrBayes")
plt.ylabel("Edge Lengths Dodonaphy")
plt.legend()
# plt.tight_layout()

path_save_jpeg = "split_lengths.jpg"
plt.savefig(path_save_jpeg, format="jpg")

# high resolution eps, to be converted to tif
path_save_eps = "split_lengths.eps"
plt.savefig(path_save_eps, format="eps", dpi=1200)
# plt.show()
