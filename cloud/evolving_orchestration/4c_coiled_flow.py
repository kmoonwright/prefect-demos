import coiled
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


coiled.create_software_environment(
    name="gpu-env4",
    container="gpuci/miniconda-cuda:10.2-runtime-ubuntu18.04",
    conda={
        "channels": ["conda-forge", "defaults", "fastchan"],
        "dependencies": [
            "python==3.8.5",
            "pytorch",
            "torchvision",
            "cudatoolkit=10.2",
            "prefect",
            "fastai",
            "scikit-image",
            "numpy",
            "dask",
            "bokeh>=0.13.0",
            "dask-cuda",
            "prefect",
            "pandas",
        ],
    },
)

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
        cluster_class=coiled.Cluster,
        cluster_kwargs={
            "software": "my_account/gpu-env4",
            "n_workers": 2,
            "shutdown_on_close": True,
            "name": "prefect-executor",
            "worker_memory": "4 GiB",
            "worker_gpu": 1,
            "backend_options": {"spot": False},
        },
    ),
) as flow:
    e = extract()
    t = transform.map(e)
    l = load(t)
