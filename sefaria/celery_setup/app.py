from celery import Celery
from mekoros.celery_setup.config import generate_config_from_env

app = Celery('mekoros')
app.conf.update(**generate_config_from_env())
app.autodiscover_tasks(packages=['mekoros.helper.llm'])
