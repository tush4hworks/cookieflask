FROM python:3.7

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        nginx \
        vim \
        unzip

RUN apt-get install --no-install-recommends -y \
    libpangocairo-1.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libcups2 \
    libgbm-dev \
    libdrm2 \
    libxss1 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libgtk-3-0

RUN rm -rf /var/lib/apt/lists/*

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip


WORKDIR /cookieflask
COPY . /cookieflask
RUN pip install -r requirements.txt
RUN cp nginx.conf /etc/nginx/nginx.conf
RUN chown -R www-data:www-data /var/www/
CMD service nginx restart ; uwsgi -s /tmp/cookieflask.sock --chmod-socket=777 --env HOME=/var/www --uid www-data --gid www-data --manage-script-name --mount /=app:app --processes 4 --threads 2 --http-timeout 30 --socket-timeout 30
