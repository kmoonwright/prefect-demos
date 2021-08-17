import random
import pendulum
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from prefect import task, Flow
from prefect.schedules import Schedule
from prefect.schedules.clocks import CronClock
from prefect.storage import Docker
from prefect.tasks.notifications.slack_task import SlackTask
from prefect.tasks.secrets import PrefectSecret

# req = requests.get("https://personaldevelopfit.com/motivational-quotes/")
# content = BeautifulSoup(req.content, features="lxml")
# quote_ordered_list = content.find("ol")
# quote_list = [x.text for x in quote_ordered_list.find_all("strong")]

@task
def get_content():
    req = requests.get("https://personaldevelopfit.com/motivational-quotes/")
    return req.content

@task
def get_quote_list(content):
    content = BeautifulSoup(content, 'html.parser')
    quote_list = content.find_all("strong")
    return [quote.text for quote in quote_list]

@task
def get_random_quote(quote_list):
    random_index = random.randint(0, 499)
    return quote_list[random_index]

post_to_slack = SlackTask()

with Flow(
    "motivational-flow",
    schedule=Schedule(
        clocks=[CronClock("0 8 * * 1-5",
        start_date=pendulum.now(tz="US/Pacific"))]
    ),
    storage=Docker(
        registry_url="kmoonwright",
        image_name="flows",
        image_tag="motivational-flow",
        python_dependencies=["bs4", "lxml", "requests"]
    ),
) as flow:
    content = get_content()
    quote_list = get_quote_list(content)
    random_quote = get_random_quote(quote_list)
    post_to_slack(message=random_quote)

flow.register(project_name="Motivation")