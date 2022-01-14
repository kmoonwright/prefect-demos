from inspect import Parameter
import prefect
from prefect import task, Flow, Parameter
from prefect.storage import GitHub

@task
def hello_task(name):
    logger = prefect.context.get("logger")
    logger.info(name)
    return "Done!"

with Flow("Github Storage") as flow:
    name = Parameter(default="Kyle")
    hello_task(name)


flow.storage = GitHub(
    repo="kmoonwright/prefect-demos",
    path="sales/github_storage.py",
    access_token_secret="GITHUB_ACCESS_TOKEN"
)

flow.register(project_name="Test")