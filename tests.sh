#!/bin/bash

python gateway/manage.py makemigrations
python topic_modeling/manage.py makemigrations
python seo_analysis/manage.py makemigrations

python gateway/manage.py migrate
python topic_modeling/manage.py migrate
python seo_analysis/manage.py migrate

python gateway/manage.py test
python topic_modeling/manage.py test
python seo_analysis/manage.py test

coverage run -a gateway/manage.py test
coverage run -a topic_modeling/manage.py test
coverage run -a seo_analysis/manage.py test
coverage report