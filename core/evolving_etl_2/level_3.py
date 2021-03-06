from datetime import datetime, timedelta
from random import randrange, sample
from prefect import task, Flow, Parameter, case, context
from prefect.engine.results import LocalResult
from prefect.triggers import all_successful, any_failed, some_successful

# Custom state handler for task logging
def log_state(task, old_state, new_state):
    if new_state.is_successful():
        logger = context.get("logger")
        logger.info(f"\nTask {task} finished in state: {new_state}\n")
    return new_state

# Task definitions with Functional API, adding task level configurations
length = Parameter(name="length", default=3)

@task(max_retries=3, retry_delay=timedelta(seconds=5), state_handlers=[log_state])
def extract(length):
    return sample(range(100), length)

@task(result=LocalResult(dir="~/Desktop/results", location="{flow_name}/{task_name}/{scheduled_start_time}"))
def transform(data):
    return data * 10

@task(trigger=some_successful(at_least=1, at_most=8))
def load(data):
    print(f"\nHere's your data: {data}")

# Schedule object consisting of two clocks
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock

clock1 = IntervalClock(
    start_date=datetime.now() + timedelta(seconds=5),
    interval=timedelta(hours=1),
    parameter_defaults={"length": 6}
)
clock2 = IntervalClock(
    start_date=datetime.now() + timedelta(seconds=15),
    interval=timedelta(hours=1),
    parameter_defaults={"length": 50}
)

schedule = Schedule(clocks=[clock1, clock2])

# Flow Definition for task dependencies in with block
with Flow("Evolving ETL", schedule=schedule) as flow:
    # Case blocks for our Parameter task
    with case(length, 6):
        e = extract(length)
        t = transform.map(e)
        l = load(t)

    with case(length, 50):
        e = extract(length)
        t = transform.map(e)
        t2 = transform.map(t)
        l = load(t2)

# Rather than flow.run(), utilize the CLI to run flow in a Python process:
# prefect run -p core/evolving_etl_2/level_3.py