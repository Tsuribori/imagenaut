FROM python:3.5
ENV PYTHONBUFFERED 1

RUN mkdir -p /opt/services/imagenaut/src

COPY requirements.txt /opt/services/imagenaut/src
RUN pip install -r /opt/services/imagenaut/src/requirements.txt

WORKDIR /opt/services/imagenaut/src

COPY . /opt/services/imagenaut/src
RUN cd imagenaut && python manage.py collectstatic --settings=imagenaut.settings.production_settings --no-input

EXPOSE 8000

CMD ["gunicorn", "--chdir", "imagenaut", "--bind", ":8000", "--env", "DJANGO_SETTINGS_MODULE=imagenaut.settings.production_settings", "imagenaut.wsgi:application"]
