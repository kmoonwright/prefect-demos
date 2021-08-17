from prefect import Flow, task
import prefect

@task
def inc(x):
   if x > 3:
       import time
       time.sleep(5)
       # Sleep for some of the map children so we can see sub starts
   return x + 1

@task
def sub(x):
    return x - 1

@task
def display(x):
    print(x)

with Flow("foo") as flow:
    display(sub.map(inc.map(range(5))))
    
# Use a parallel executor
flow.executor = prefect.executors.LocalDaskExecutor()
flow.run()