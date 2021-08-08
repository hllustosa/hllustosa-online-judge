FROM frostming/pdm:1.6.4
SHELL ["/bin/bash", "-c"] 

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH '/usr/local/lib/python3.9/site-packages/pdm/pep582'
ENV PRODUCTION 'PRODUCTION'
ENV PYTHONSANDBOX 'PYTHONSANDBOX'

# install dependencies
COPY . /usr/src/app
RUN pdm install
RUN pip3 install pyseccomp
EXPOSE 8000

CMD ["python", "runner/main.py"]