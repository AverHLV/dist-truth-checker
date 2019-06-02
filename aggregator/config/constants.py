from django.core.exceptions import ImproperlyConfigured
from unipath import Path
from os import environ

try:
    # base paths

    base_dir = Path(__file__).absolute().ancestor(2)
    secret_filename = base_dir.child('config').child('secret.json')

    # texts.checker paths

    lang_info_path = base_dir.child('texts').child('json').child('language_info.json')
    stopwords_path = base_dir.child('texts').child('json').child('stopwords.json')

except IOError as e:
    raise ImproperlyConfigured('Path error: {0}'.format(e))

logger_name = 'custom'

# texts.models

message_id_length = 32
headline_max_length = 150
headline_min_length = 40
text_max_length = 1500
text_min_length = 200
text_preview_length = 140

# texts.views

texts_count = 40

# texts.checker

load_encoding = 'utf8'

# texts.arclient

timeout = 20

if environ['DJANGO_SETTINGS_MODULE'] == 'config.settings.production':
    services = {
        'tm': 'http://165.22.195.65:8000',
        'seo': 'http://165.22.205.17:8000'
    }

else:
    services = {
        'tm': 'http://127.0.0.1:7000',
        'seo': 'http://127.0.0.1:7001'
    }

# texts_admin.models

token_bytes = 32
token_length = token_bytes * 2
