#!/bin/bash
echo $GW_SECRET | base64 -d > /builds/AverHLV/dist-truth-checker/gateway/config/secret.json
echo $SEO_SECRET | base64 -d > /builds/AverHLV/dist-truth-checker/seo_analysis/config/secret.json
echo $TM_SECRET | base64 -d > /builds/AverHLV/dist-truth-checker/topic_modeling/config/secret.json

coverage run -a gateway/manage.py test
coverage run -a topic_modeling/manage.py test
coverage run -a seo_analysis/manage.py test
coverage report