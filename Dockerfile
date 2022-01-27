FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /usr/src/webapp

COPY ./requirments.txt ./

RUN pip install -r requirments.txt

COPY ./ ./
