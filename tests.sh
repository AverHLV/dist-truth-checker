#!/bin/bash

coverage run -a aggregator/manage.py test texts.tests
coverage run -a aggregator/manage.py test texts_admin.tests
coverage run -a topic_modeling/manage.py test api.tests
coverage run -a seo_analysis/manage.py test api.tests
coverage report

codecov -t $CODECOV_TOKEN