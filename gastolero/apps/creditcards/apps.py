from django.apps import AppConfig


class CreditcardsConfig(AppConfig):
    name = 'creditcards'

    def ready(self):
        from . import signals  # noqa
