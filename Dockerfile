FROM python:2.12

WORKDIR /app

COPY requirements.txt .
RUN pip install

COPY . /app

EXPOSE

ENTRYPOINT ["entrypoint.sh"]
