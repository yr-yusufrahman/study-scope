from django.apps import AppConfig


class PredictorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predictor'

    def ready(self):
        # Quiz generation uses rake-nltk; punkt_tab is required on fresh installs.
        from predictor.helpers.ensure_nltk import ensure_nltk_data

        ensure_nltk_data()
