FROM python:3.10

RUN pip install flask transformers torch

WORKDIR /
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
COPY . .

CMD ["flask", "run"]