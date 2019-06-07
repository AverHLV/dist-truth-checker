FROM python:3.7.3

EXPOSE 8000
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 0

RUN pip install --no-cache-dir uwsgi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /dist-truth-checker && mkdir /dist-truth-checker/topic_modeling
WORKDIR /dist-truth-checker/topic_modeling

CMD ["bash"]