import datetime
import pendulum
import requests

from prefect import task, Flow, Parameter, case
from prefect.tasks.secrets import PrefectSecret
from prefect.tasks.notifications.slack_task import SlackTask
from prefect.artifacts import create_link
from prefect.storage import GitHub
from prefect.run_configs import LocalRun
from prefect.schedules import Schedule
from prefect.schedules.clocks import CronClock

# TASK DEFINITIONS
# Parameter Task takes a value at runtime
name = Parameter(name="NAME PARAMETER", default="world!")

@task(log_stdout=True)
def hello(name):
    print(f"Hello {name}")

with Flow("My Label Hierarchy Test") as flow:
    hello(name)

flow.storage = GitHub(
    repo="kmoonwright/prefect-demos",
    path="sales/label_hierarchy.py",
    access_token_secret="GITHUB_ACCESS_TOKEN"
)

flow.run_config = LocalRun(
    labels=["MY_RUN_CONFIG_LABEL"]
)


# REGISTRATION TO PREFECT CLOUD
flow.register(project_name="Test", labels=["MY_REGISTRATION_LABEL"])