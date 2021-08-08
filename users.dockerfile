FROM frostming/pdm:1.6.4
SHELL ["/bin/bash", "-c"] 

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH '/usr/local/lib/python3.9/site-packages/pdm/pep582'
ENV DJANGO_SUPERUSER_USERNAME 'onlinejudge'
ENV DJANGO_SUPERUSER_PASSWORD 'onlinejudge'
ENV DJANGO_SUPERUSER_EMAIL  'onlinejudge@mail.com.br'
ENV PRODUCTION 'PRODUCTION'

# install dependencies
COPY . /usr/src/app
RUN ls /usr/src/app
RUN pdm install
EXPOSE 8000

CMD ["./run_users.sh"]
