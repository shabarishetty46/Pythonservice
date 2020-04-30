# Base image
FROM python:3.6

# Create app directory
WORKDIR /app

# Install app dependencies
COPY packages.txt ./


# pip to install requests and urllib3

RUN pip install -r packages.txt

COPY *  /app/


EXPOSE 8080

# command to get the metrics

CMD [ "python", "pythonservice.py"]
