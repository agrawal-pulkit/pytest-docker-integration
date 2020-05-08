FROM python:3.7
WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python3-dev
RUN apt-get install -y default-libmysqlclient-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]


