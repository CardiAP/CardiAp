[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/CardiAP/CardiAp/HEAD?urlpath=%2Fvoila%2Frender%2FCardiAP.ipynb)

CardiAP
=======


Copyright © `2020-2021 ` `Velez Rueda, Garcia Smith, Sommese`



> Python Server for performing biomedical images analysis

You can run the web version of CardiAP using Binder server

# Live server
This project is hosted in Binder. You can launch [CardiAP here](https://mybinder.org/v2/gh/CardiAP/CardiAp/HEAD?urlpath=%2Fvoila%2Frender%2FCardiAP.ipynb) 

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

# Run
```bash
$ voila CardiAP.ipynb
# start with live reload
$ voila CardiAP.ipynb  --autoreload=True
```

After using CardiAP locally, you can deactivate the env by doing:
```bash
$ deactivate
```
