from pytz import utc
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from mekoros.system.database import client
from . import jobs
from mekoros.settings import APSCHEDULER_NAME


def run_background_scheduler():
    jobstores = {'default': MongoDBJobStore(client=client, database=APSCHEDULER_NAME)}
    scheduler = BackgroundScheduler(jobstores=jobstores, timezone=utc)
    scheduler.start()
    jobs.remove_jobs(scheduler)
    jobs.add_jobs(scheduler)
    return scheduler