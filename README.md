# Truth checking distributed service

![coverage](https://img.shields.io/codecov/c/github/AverHLV/dist-truth-checker.svg) ![build_status](https://img.shields.io/gitlab/pipeline/AverHLV/dist-truth-checker/dev.svg) [![Documentation Status](https://readthedocs.org/projects/dist-truth-checker/badge/?version=latest)](https://dist-truth-checker.readthedocs.io/en/latest/?badge=latest)


A set of services that calculates some parameters of news articles in order to determine their veracity.

## Services

- Aggregator: client interface, texts managing and gathering checking results;
- Topic modeling: computing similarity of article headline and text;
- SEO analysis: calculating most common SEO text processing metrics and evaluating them.

## Technologies

Python 3.7, Django, rest framework, aiohttp, nltk, scikit-learn, scikit-fuzzy.