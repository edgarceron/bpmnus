# Dockerfile
FROM python:3.7-buster

RUN apt-get update && apt-get install nginx vim gunicorn -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN cd /opt/app/ && git clone https://github.com/edgarceron/bpmnus
WORKDIR /opt/app/bpmnus
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN chown -R www-data:www-data /opt/app

EXPOSE 8020
STOPSIGNAL SIGTERM
RUN chmod 755 /opt/app/bpmnus/start_server.sh
CMD ["./start_server.sh"]