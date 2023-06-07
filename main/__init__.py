from .celery import app as celery_app
# this is to ensure that the celery app is loaded when Django starts so that all these tasks will use it
__all__ = ['celery_app']
