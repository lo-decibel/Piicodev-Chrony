FROM geoffh1977/chrony
RUN apk add python3 py3-pip \
  && pip install piicodev ntplib pythonping \
  && apk del py3-pip
RUN sed -i '/# Run Chrony Daemon/apython3 \/piicodev\/main.py &' /usr/local/bin/start.sh