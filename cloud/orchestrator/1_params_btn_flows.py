import prefect
from prefect import Flow, task
from prefect import Parameter
from prefect.tasks.prefect.flow_run import StartFlowRun

"""
Code example for passing Parameters between child flows using the 
dependent flows pattern (Orchestrator pattern) for Prefect >0.15.0
"""
# Child Flow
@task
def child_flow_test(data):
    logger = prefect.context.get("logger")
    logger.info(f"Your data is: {data}")
    return data
    
with Flow("Child Flow") as child_flow:
    child_param = Parameter("Child Parameter", default="test")
    child_flow_test(child_param)

child_flow.register(project_name="test-flows")


# Parent flow
@task
def get_param_val(data):
    logger = prefect.context.get("logger")
    logger.info(f"Your Parent param val is: {data}")
    return {"Child Parameter": data}

start_child_flow = StartFlowRun(flow_name="Child Flow", project_name="test-flows", wait=True)

with Flow("Parent Flow") as parent_flow:
    my_param = Parameter("Passing it down", default="THIS IS FROM THE PARENT")
    param_val = get_param_val(my_param)
    child_flow_1 = start_child_flow(upstream_tasks=[my_param], parameters=param_val)

parent_flow.register(project_name="test-flows")
