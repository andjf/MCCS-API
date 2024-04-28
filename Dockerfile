FROM python:3.11.3
ENV PYTHONUNBUFFERED True

# This is where the configuration files will be mounted
RUN mkdir -p /home/config

ENV APP_HOME /root
WORKDIR $APP_HOME

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --root-user-action=ignore --no-cache-dir -r requirements.txt

COPY ./app $APP_HOME/app

EXPOSE 8080
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8080"]
