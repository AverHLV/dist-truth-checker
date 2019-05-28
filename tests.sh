#!/bin/bash

coverage run -a gateway/manage.py test texts.tests
coverage run -a gateway/manage.py test texts_admin.tests
coverage run -a topic_modeling/manage.py test api.tests
coverage run -a seo_analysis/manage.py test api.tests
coverage report

sudo pip install --user codecov && codecov -t $CODECOV_TOKEN