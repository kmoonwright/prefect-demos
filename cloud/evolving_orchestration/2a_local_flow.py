from prefect import task, Flow
from prefect.storage import Local
from prefect.run_configs import LocalRun
from prefect.engine.executors.dask import LocalDaskExecutor


@task
def extract():
    """Get a list of data"""
    return [i for i in range(1, 100)]


@task
def transform(datum):
    """Multiply the input by 10"""
    return datum * 10


@task
def load(data):
    """Print the data to indicate it was received"""
    print("Here's your data: {}".format(data))


with Flow(
    "ETL",
    storage=Local(),
    run_config=LocalRun(env={"SOME_VAR": "value"}),
    executor=LocalDaskExecutor(scheduler="threads", num_workers=3),
) as flow:
    e = extract()
    t = transform.map(e)
    l = load(t)
