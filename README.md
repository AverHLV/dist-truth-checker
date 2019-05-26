## Truth checking distributed service

A set of services that calculate some parameters of news articles in order to determine their veracity.

# Services

- Gateway: client interface, aggregating texts and gathering checking results;
- Topic modeling: computing similarity of article headline and text;
- SEO analysis: calculating most common SEO text processing metrics and evaluating them.

# Technologies

Python 3.7, Django, rest framework, aiohttp, nltk, scikit-learn, scikit-fuzzy.