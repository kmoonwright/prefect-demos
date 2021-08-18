from typing import List

from prefect import Flow, Parameter, task
from prefect.engine.results import LocalResult
from prefect.tasks.prefect import create_flow_run, get_task_run_result

"""
Code example for passing task results between child flows using the 
dependent flows pattern (Orchestrator pattern) for Prefect +0.15.0.
"""

# Child Flow
@task(result=LocalResult())
def create_some_data(length: int):
    return list(range(length))

with Flow("child") as child_flow:
    data_size = Parameter("data_size", default=5)
    data = create_some_data(data_size)

# Parent flow
@task(log_stdout=True)
def transform_and_show(data: List[int]) -> List[int]:
    print(f"Got: {data!r}")
    new_data = [x + 1 for x in data]
    print(f"Created: {new_data!r}")
    return new_data

with Flow("parent") as parent_flow:
    child_run_id = create_flow_run(
        flow_name=child_flow.name, parameters=dict(data_size=10)
    )
    # Passing task results from child flow using get_task_run_result API
    child_data = get_task_run_result(child_run_id, "create_some_data-1")
    transform_and_show(child_data)