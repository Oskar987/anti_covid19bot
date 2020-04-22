FROM python:3.7
COPY /requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r /app/requirements.txt
COPY . /app
CMD python /app/setup.py