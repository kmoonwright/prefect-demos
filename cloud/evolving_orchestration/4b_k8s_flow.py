from prefect import task, Flow
from prefect.storage import GitHub
from prefect.run_configs import KubernetesRun
from prefect.engine.executors.dask import DaskExecutor


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


# Some configuration is required, see https://docs.prefect.io/orchestration/flow_config/overview.html
with Flow(
    "ETL",
    storage=GitHub(
        repo="<my_github_org/repo_name>",
        path="src/flow.py",
        secrets=["<GITHUB_ACCESS_TOKEN>"],
    ),
    run_config=KubernetesRun(
        cpu_request=2, cpu_limit=3, image="prefecthq/prefect:all_extras"
    ),
    executor=DaskExecutor(
        cluster_class="dask_cloudprovider.aws.FargateCluster",
        adapt_kwargs={"maximum": 10},
    ),
) as flow:
    e = extract()
    t = transform.map(e)
    l = load(t)
