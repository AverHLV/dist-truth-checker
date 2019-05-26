from django.core.exceptions import ImproperlyConfigured
from unipath import Path

try:
    # base paths

    base_dir = Path(__file__).absolute().ancestor(2)
    secret_filename = base_dir.child('config').child('secret.json')
    lda_models_path = base_dir.child('api').child('models')
    ref_messages_path = base_dir.child('api').child('json').child('reference_messages.json')

except IOError as e:
    raise ImproperlyConfigured('Path error: {0}'.format(e))

logger_name = 'custom'

# api.models

message_id_length = 32
headline_max_length = 150
text_max_length = 1500
status_threshold = 0.2

# api.lda

load_encoding = 'utf8'
