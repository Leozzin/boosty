FROM python:3.8

RUN mkdir /app
COPY . /app 
RUN apt-get update \
&& apt-get install git -y 
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt install build-essential -y \
&& apt-get install manpages-dev -y
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN rm -rf /usr/local/lib/python3.8/site-packages/chatterbot/utils
RUN rm -rf /usr/local/lib/python3.8/site-packages/chatterbot/adapters

EXPOSE 8000

CMD ["python3","manage.py", "runserver", "0.0.0.0:8000"]