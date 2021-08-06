FROM frostming/pdm
SHELL ["/bin/bash", "-c"] 

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH '/usr/local/lib/python3.9/site-packages/pdm/pep582'

# install dependencies
COPY . /usr/src/app
RUN pdm install
EXPOSE 8000

CMD ["python", "users/manage.py", "runserver", "0.0.0.0:8000"]
