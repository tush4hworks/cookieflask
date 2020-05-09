Current Flask server is standalone and isn't recommended for high traffic production environments.

Below are guidelines to use uWSGI + nginx as an alternate.

In /etc/nginx/nginx.conf, have this section:

server {
        listen 5001;
        location / {
            try_files $uri @app;
        }
        location @app {
            include uwsgi_params;
            uwsgi_pass unix:///tmp/cookieflask.sock;
        }
        }
        
In Dockerfile, instead of flask run, start nginx, uwsgi process.

RUN apt-get install -y nginx
#override nginx conf from local
RUN cp nginx.conf /etc/nginx/nginx.conf
CMD service nginx restart ; uwsgi -s /tmp/cookieflask.sock --chmod-socket=777 --uid www-data --gid www-data --manage-script-name --mount /=app:app --processes 4 --threads 2
