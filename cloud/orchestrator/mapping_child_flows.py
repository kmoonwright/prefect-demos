# From Chris/Nicholas
from prefect import task, Flow, Parameter, unmapped
from prefect.tasks import StartFlowRun
from typing import List

@task
def taskA() -> List[int]: 
  return [1, 2, 3]

@task
def create_parameter_payload(result, param):
    return {'blah': param, 'resultId': result}

with Flow("Mapping Parameters Flow") as flow:
    my_results = taskA()
    flow_run_task = StartFlowRun()
    param = Parameter("My Parameter Value")

    params = create_parameter_payload.map(param=unmapped(param), result=my_results)
    flow_run_task.map(flow_name=unmapped('DownstreamFlow'), parameters=params)