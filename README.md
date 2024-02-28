# dodonaphy-experiments

[![Docker Image CI](https://github.com/4ment/dodonaphy-experiments/actions/workflows/docker-image.yml/badge.svg)](https://github.com/4ment/dodonaphy-experiments/actions/workflows/docker-image.yml)

This repository contains the pipeline and data sets supporting the results of the following article:

Macaulay M and Fourment M. Differentiable Phylogenetics via Hyperbolic Embeddings with Dodonaphy. [arXiv:2309.11732](https://arxiv.org/abs/2309.11732)

## Dependencies
You will need to install [nextflow](https://www.nextflow.io) and [docker](https://www.docker.com) to run this benchmark.
Docker is not required but it is highly recommended to use it due to the numerous dependencies.

## Installation

    git clone 4ment/dodonaphy-experiments.git

## Running the pipeline with docker

    nextflow run 4ment/dodonaphy-experiments -profile docker

Since the pipeline will take weeks to run to completion one should use a high performance computer. Examples of configuration files for pbspro and slurm can be found in the [configs](configs/) folder.