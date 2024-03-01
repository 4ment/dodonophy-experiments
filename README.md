# dodonaphy-experiments

[![Docker Image CI](https://github.com/4ment/dodonaphy-experiments/actions/workflows/docker-image.yml/badge.svg)](https://github.com/4ment/dodonaphy-experiments/actions/workflows/docker-image.yml)

This repository contains the pipeline and data sets supporting the results of the following article:

Macaulay M and Fourment M. Differentiable Phylogenetics via Hyperbolic Embeddings with Dodonaphy. [arXiv:2309.11732](https://arxiv.org/abs/2309.11732)

## Dependencies
You will need to install [nextflow](https://www.nextflow.io) to run the pipeline. For ease of use the pipeline can be set up with either the package manager [conda](https://conda.io) or [docker](https://www.docker.com). Singularity is another option for running the pipeline on an HPC.

## Download pipeline

    git clone http://github.com/4ment/dodonaphy-experiments.git
    cd dodonaphy-experiments/
    chmod +x bin/*.py

## Pipeline without docker/singularity

### Installing dependencies with conda
    conda env create -f environment.yml
    git clone http://github.com/mattapow/hydraPlus.git
    pip install hydraPlus/
    git clone http://github.com/mattapow/dodonaphy.git
    pip install dodonaphy/

### Running the pipeline

    nextflow run main.nf

## Pipeline with docker or singularity
There is no need to install dependencies with docker or singularity.

### Running the pipeline with docker

    nextflow run main.nf -profile docker

## Running the pipeline with singularity with PBS

    nextflow -C configs/uts.config run main.nf -profile singularity

Since the pipeline will take weeks to run to completion one should use a high performance computer. Examples of configuration files for pbspro and slurm can be found in the [configs](configs/) folder.