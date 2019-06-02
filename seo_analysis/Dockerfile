FROM python:3.7.3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 0

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uwsgi

RUN mkdir /dist-truth-checker
WORKDIR /dist-truth-checker

RUN git init
RUN git remote add origin https://github.com/AverHLV/dist-truth-checker.git
RUN git config core.sparsecheckout true
RUN echo "seo_analysis/*" >> .git/info/sparse-checkout

RUN mkdir /dist-truth-checker/seo_analysis
RUN mkdir /dist-truth-checker/seo_analysis/config
COPY uwsgi.ini /dist-truth-checker/seo_analysis
COPY config/secret.json /dist-truth-checker/seo_analysis/config
COPY seo_db /dist-truth-checker/seo_analysis/
WORKDIR /dist-truth-checker/seo_analysis/

EXPOSE 8000

CMD ["bash"]