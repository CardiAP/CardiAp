FROM python:3.8-bullseye

RUN apt-get update && \
    apt-get install libgl1-mesa-glx -y && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY assets assets
COPY lib lib
COPY CardiAP.ipynb CardiAP.ipynb

EXPOSE 5000

ENTRYPOINT ["voila",  "--port=5000", "--no-browser",  "--Voila.ip='0.0.0.0'", "CardiAP.ipynb"]