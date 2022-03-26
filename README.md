# Fifa Data Challenge

This project does a quick data analysis of fifa data from a football game. This is a quick test project, so this code is
not production ready.

## How to run?

In order to run, please create a virtual env and run doing the following:

Linux/OSX:

```
python -m virutalenv venv
source venv/bin/activate
pip install -r requirements.txt
```

If you're using Windows, please run the following:

```
python -m virtualenv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

In order to run: 

```
python src/run.py
```

## How to build and run the image?

```
docker build -t fifa-data-challenge:latest .
docker run fifa-data-challenge:latest
```