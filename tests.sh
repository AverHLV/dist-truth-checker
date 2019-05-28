#!/bin/bash

python gateway/manage.py test
python topic_modeling/manage.py test
python seo_analysis/manage.py test

coverage run -a gateway/manage.py test
coverage run -a topic_modeling/manage.py test
coverage run -a seo_analysis/manage.py test
coverage report