
# Nginx configuration

Created to test an Nginx configuration that will properly serve static files
and redirect other requests to gunicorn when running in production.

This configuration seems to work.

```conf
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    root   /usr/share/nginx/html;

    location / {
        proxy_pass http://192.168.0.148:8000; # Django or Gunicorn
    }

    location /static/ {
        root   /usr/share/nginx/html; # Location of static files.
    }
}
```

## Build

To build this configuration I used buildah altough docker should also work.

    buildah build .

