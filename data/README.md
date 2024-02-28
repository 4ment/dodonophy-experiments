@@ -0,0 +1,44 @@
# Running Dodonaphy VI on a cluster
This folder is self contained for running dodonaphy using a pbs script. Input alignments are in ds<x>/data/DS.nex and the treefile from iqtree (ds1 has the log to see how it was generated). The file DS.fasta is a translation of DS.nex for bito/BEAGLE. Currently our results run for 200 epochs, I've set it here to run for 2000 epochs.

1. First install dodonaphy in a conda environment.
2. Edit line 11 of the file `run_dodo_vi.pbs` to for the name of your conda environement.
3. Submit the following batch job for all datasets.
```bash
qsub run_dodo_vi.pbs
```

## What could go wrong
1. Time or memory may be an issue, so I set them high.
2. Try deleting the line with the --use_bito if it's not working.
3. If re-running anything:
  a) you can change the line "PBS -J 1-8", to say "PBS -J 7-8" if only needing to do a few
  b) Dodnaphy won't overwrite output files. Either delete what you had or add a suffix string to the folder it writes in e.g. `--suffix rerun1`.
It's possible that ds7 and ds8 won't finish at all, but may have already saved some samples from the final variational distribution, which can be read by the post-processing scrips.

# Running Dodonaphy Maximum likelihood on a cluster
I've also added a pbs script for running maximum likelihood. Currently our results run for 2000 epochs. DS1 takes 3 hours, DS4 takes 26 hours, and actually the rest didn't finish. I wrote a script
```bash
qsub run_dodo_ml.pbs
```
to try and get DS 5-8 to finish at 2000 epochs. These start from the bionj tree in the data folder.

## Post processing Maximum Likelihood
If that finished, then it should be a simple matter of manually updating the values for Dodonaphy in the file https://github.com/mattapow/vi-fig-scripts/blob/main/ml_performance.py to recreate figure 2. To get the Dodonaphy+ results, optimise the tree found by Dodonaphy with fixed topology using IQTREE. I think this requires changing the mape.t file to newick. I haven't got an automated way to do this. Then:
```bash
cd ds1/hmap/nj/None/bionj/lr2_tau5_n2000_k2_d3
iqtree -s data/DS.nex -te mape.nwk -m GTR+FO --prefix dodo_iq -T AUTO
```

# Post processing Variational Inference
The mattapow/vi-fig-scripts repo can generate what we need.
1. For table 1, the script https://github.com/mattapow/vi-fig-scripts/blob/main/marginal.py will print the values required. The main function is right at the bottom. Configure [line 94](https://github.com/mattapow/vi-fig-scripts/blob/main/marginal.py#L94) to point to this current directory i.e. `./revised-run-2024`.
2. For figure 3a,
  - Edit https://github.com/mattapow/vi-fig-scripts/blob/main/split_lengths_prepare.py:
    a) line 43 to the current directory `revised-run-2024`
    b) line 45: remove the "boosts" and the last string for the directory name will be different
    c) line 47-48: edit to the path one OneDrive where the MrBayes runs are.
  - This will save the split lengths to a tmp directory.
  - Then run https://github.com/mattapow/vi-fig-scripts/blob/main/split_lengths_plot.py to generate figure 3a
3. For figure 3b,
  - Edit https://github.com/mattapow/vi-fig-scripts/blob/main/tree_length.py on lines 17 and 19 for the paths. Line 19 could be made redundant since we're not changing the number of boosts.
