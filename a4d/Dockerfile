FROM python:3.12.2-alpine3.18

#Upgrade pip
RUN python -m pip install --upgrade pip

#Update all packages
RUN rm -rf /var/cache/apk/* && rm -rf /tmp/*
RUN apk update

# install packeges run install mysqlclient and uwsgi
RUN apk add linux-headers
RUN apk add --virtual build-deps gcc python3-dev musl-dev
RUN apk add --no-cache mariadb-dev

# install deploy requirements for python
COPY ./deploy_requirements.txt /app/deploy_requirements.txt
WORKDIR /app
RUN pip install -r deploy_requirements.txt

# install requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy the app
COPY . /app

EXPOSE 8000
ENTRYPOINT python manage.py migrate;python manage.py collectstatic --no-input;uwsgi  --uid nobody --gid nogroup --http 0.0.0.0:8000 --module a4d.wsgi
