FROM python:3.9 as dev

# set work directory
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install pandas
RUN pip install -r requirements.txt --no-cache-dir --upgrade

COPY ./ ./

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod 777 /entrypoint.sh

ENTRYPOINT ["sh","/entrypoint.sh"]
