FROM python:3.8

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

# add current directory to python path
ENV PYTHONPATH "${PYTHONPATH}:/."

CMD ["python", "src/run.py"]