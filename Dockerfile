FROM python:3.7.4-slim

RUN adduser --disabled-password custoom
WORKDIR /home/custoom

ENV PATH="/home/custoom/.local/bin:$PATH" \
    _PIP_VERSION="20.2.2"

RUN apt-get update \
      && apt-get install -q -y --no-install-recommends \
      git \
      libboost-dev \
      gcc \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade \
      pip==${_PIP_VERSION}

COPY boot.sh ./
RUN chmod +x boot.sh
ENV FLASK_APP custoom.py

COPY app app
COPY albums albums
COPY credentials credentials
COPY migrations migrations
COPY utils utils
COPY custoom.py config.py settings.yaml ./
COPY Pipfile.lock Pipfile.lock
COPY Pipfile Pipfile
RUN chown -R custoom:custoom ./

USER custoom
RUN pip install --user pipenv
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]

