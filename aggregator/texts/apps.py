from django.apps import AppConfig


class TextsConfig(AppConfig):
    name = 'texts'

    def ready(self):
        import texts.signals
