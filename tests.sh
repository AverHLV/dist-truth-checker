#!/bin/bash

coverage run -a gateway/manage.py test texts.tests
coverage run -a gateway/manage.py test texts_admin.tests
coverage run -a topic_modeling/manage.py test api.tests
coverage run -a seo_analysis/manage.py test api.tests
coverage report

pip install --user codecov && codecov -t d86457a1-1b31-47a2-b10a-1505f6b10a19