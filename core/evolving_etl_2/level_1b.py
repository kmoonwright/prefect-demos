from random import randrange
from prefect import Task, Flow

# Task definitions with Imperative API, useful for pre-built tasks
class Extract(Task):
    def run(self):
        return randrange(1, 100)

class Transform(Task):
    def run(self, data):
        return data * 10

class Load(Task):
    def run(self, data):
        print(f"\nHere's your data: {data}")

# Instantiate tasks
e = Extract()
t = Transform()
l = Load()

flow = Flow("Evolving ETL")

# Set task dependencies with flow method
flow.set_dependencies(t, keyword_tasks={'data': e})
flow.set_dependencies(l, keyword_tasks={'data': t})

# Rather than flow.run(), utilize the CLI to run flow in a Python process:
# prefect run -p core/evolving_etl_2/level_1b.py