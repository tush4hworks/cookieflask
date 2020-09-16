FROM python:3.7

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        nginx \
        vim \
        google-chrome-stable \
        unzip && \
    rm -rf /var/lib/apt/lists/*


RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip


WORKDIR /cookieflask
COPY . /cookieflask
RUN pip install -r requirements.txt
RUN cp nginx.conf /etc/nginx/nginx.conf
CMD service nginx restart ; uwsgi -s /tmp/cookieflask.sock --chmod-socket=777 --uid www-data --gid www-data --manage-script-name --mount /=app:app --processes 4 --threads 2
