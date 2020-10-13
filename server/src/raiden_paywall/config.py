from os import environ

from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import cpu_count
from subprocess import Popen

from raiden_paywall.tasks import database_update_payments 

from raiden_paywall.flask_raiden import RaidenNode

sched = None

from flask import Flask

def on_starting(server):
    # FIXME does this have to be global?
    global sched

    # TODO get rid of flask creation here and read config file manually
    # only create to get the config
    app = Flask(__name__)
    app.config.from_envvar("RAIDEN_PAYWALL_SETTINGS")

    raiden = RaidenNode.from_config(app.config)

    sched = BackgroundScheduler(timezone="UTC")
    sched.start()
    sched.add_job(database_update_payments, kwargs={'raiden': raiden}, id="update_payments", coalesce=True, max_instances=1, trigger='interval', seconds=0.5)
