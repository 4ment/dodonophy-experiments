#!/usr/bin/env python

# plot the final log SIWAE value as the number of mixtures changes
import os
import re
import sys

import matplotlib.pyplot as plt
import numpy as np

# from matplotlib.ticker import ticker


# extract the SIWAE values
siwae = []
std = []
n_mixtures = []
print(sys.argv[1:])
for file in sys.argv[1:]:
    # ELBO estimated from many final samples
    with open(file, "r") as f:
        lines = f.read().splitlines()
        line_siwae = lines[-3]
        this_siwae = -float(line_siwae.split()[-1])
        # this_siwae = float(lines[-2].strip())
        this_std = 0.0

    siwae.append(this_siwae)
    std.append(this_std)
    a = os.path.split(file)[-2]
    boost = re.search(r"b(\d+)", file).group(1)
    n_mixtures.append(int(boost))

x = np.argsort(n_mixtures)
siwae = np.array(siwae)[x]
n_mixtures = np.array(n_mixtures)[x]

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(6, 4)
ax.set_position([0.16, 0.11, 0.83, 0.88])
# ax.annotate("B", (0.05, 0.85), xycoords="figure fraction", fontsize="18")
plt.errorbar(n_mixtures, siwae, yerr=std, fmt="ko-")
plt.xlabel("Number of mixtures")
plt.ylabel("log SIWAE")
# plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

plt.savefig("boosts_SIWAE.jpg", format="jpg")
plt.savefig("boosts_SIWAE.eps", format="eps", dpi=1200)
# plt.show()
