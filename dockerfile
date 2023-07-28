FROM python:3.10

RUN apt-get -y update

# install google chrome
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`-1_amd64.deb \
  && apt install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb

# install chromedriver
RUN apt-get install -yqq unzip curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# upgrade pip
RUN pip install --upgrade pip

# install selenium
RUN pip install selenium requests Pillow python-dotenv debugpy

RUN useradd selenium; mkdir /home/selenium; chown selenium:selenium /home/selenium

USER selenium

WORKDIR /app
# CMD ["python", "-m", "debugpy", "--listen", "localhost:5678", "--wait-for-client", "send_screeen.py"]