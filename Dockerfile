# Dockerfile
FROM python:3.7-buster

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/static
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/bpmnus
WORKDIR /opt/app/bpmnus
COPY requirements.txt .
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
COPY . .
COPY buildfiles/nginx.default /etc/nginx/sites-available/default
RUN chown -R www-data:www-data /opt/app

EXPOSE 8020
STOPSIGNAL SIGTERM
RUN chmod 777 /opt/app/bpmnus/buildfiles/start_server.sh
RUN chmod 777 /opt/app/bpmnus/buildfiles/wait-for-it.sh
CMD ["/opt/app/bpmnus/buildfiles/start_server.sh"]