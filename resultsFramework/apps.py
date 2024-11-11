from django.apps import AppConfig


class ResultsframeworkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resultsFramework'
    def ready(self):
        import resultsFramework.signals