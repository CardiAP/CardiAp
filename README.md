[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CardiAP/CardiAp/HEAD?urlpath=%2Fvoila%2Frender%2FCardiAP.ipynb)

CardiAP
=======


Copyright © `2020-2021 ` `Velez Rueda, Garcia Smith, Sommese`



> Python Server for performing biomedical images analysis


# Live server
You can run the web version of CardiAP using Binder server. 
You can launch [CardiAP here](https://mybinder.org/v2/gh/CardiAP/CardiAp/HEAD?urlpath=%2Fvoila%2Frender%2FCardiAP.ipynb) 

# Running CardiAP using docker

You can easily run CardiAP using [Docker](https://docs.docker.com/desktop/install/windows-install/) by running:

```bash
docker run -it --rm --net host ajvelezrueda/cardiap
```


# Installing CardiAP locally

```bash
# clone the repository
git clone https://github.com/CardiAP/CardiAp.git

# Create and active a virtual env
$ virtualenv .venv

# activate the env
$ . .venv/bin/activate

# install dependencies
$ pip3 install -r requirements.txt 
```

# Run it locally

```bash
$ voila CardiAP.ipynb
# start with live reload
$ voila CardiAP.ipynb  --autoreload=True
```

After using CardiAP locally, you can deactivate the env by doing:
```bash
$ deactivate
```

# Building docker image
```bash
docker build . -f Dockerfile -t ajvelezrueda/cardiap
```
