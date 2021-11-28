FROM docker.io/nginx


RUN mkdir /usr/share/nginx/html/static
COPY static /usr/share/nginx/html/static
COPY default.conf /etc/nginx/conf.d/default.conf