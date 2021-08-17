from random import randrange
from prefect import task, Flow

# Task Definitions
@task
def extract():
    return randrange(1, 100)

@task
def transform(data):
    return data * 10

@task
def load(data):
    print(f"\nHere's your data: {data}")

# Flow Definition for task dependencies
with Flow("Evolving ETL") as flow:
    e = extract()
    t = transform(e)
    l = load(t)

# Rather than flow.run(), utilize the CLI to run flow in a Python process:
# prefect run -p core/evolving_etl_2/level_1.py