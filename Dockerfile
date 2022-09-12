FROM python:3.10


WORKDIR /root

COPY . .


RUN python -m venv /opt/venv
ENV VIRTUAL_ENV /opt/venv
ENV PATH $VIRTUAL_ENV/bin:$PATH


RUN pip install -U pip setuptools wheel
RUN pip install -r requirements.txt


