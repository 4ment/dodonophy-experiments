FROM condaforge/miniforge3
LABEL "author"="Mathieu Fourment"
LABEL "company"="University of Technology Sydney"

RUN apt-get update && \
	apt-get install -y --no-install-recommends \
        build-essential \
		git \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/4ment/dodonaphy-experiments /dodonaphy-experiments
RUN sed -i '/nextflow/d' /dodonaphy-experiments/environment.yml
RUN conda env create -f /dodonaphy-experiments/environment.yml

RUN git clone https://github.com/mattapow/hydraPlus
RUN /opt/conda/envs/dodonaphy/bin/pip install hydraPlus/

RUN git clone https://github.com/mattapow/dodonaphy
RUN /opt/conda/envs/dodonaphy/bin/pip install dodonaphy/

RUN echo "source activate dodonaphy" > ~/.bashrc
ENV PATH /opt/conda/envs/dodonaphy/bin:$PATH
