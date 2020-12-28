
FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
#CMD ["main.py"]
ENTRYPOINT ["python3", "main.py"]
CMD ["all"]

