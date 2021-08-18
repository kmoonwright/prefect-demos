![Prefect Logo](/images/prefect-logo-full-gradient.svg)
# Prefect Demos
A collection of demos scripts and progressive tutorials demonstrating the features and funtionality of the Prefect Core workflow engine and Prefect Cloud orchestration.

## What is Prefect?
[Prefect](http://prefect.io) is a data engineering framework and workflow orchestration technology for your Python jobs - a means to unite the efforts of data engineers, analysts, and DevOps engineers.

The open source module, [Prefect Core](https://github.com/PrefectHQ/prefect), contains a common set of components and semantics to create dynamic workflows as graph structures, which can be scheduled/monitored/configured using the a backend API: either an instance of [Prefect Server](https://docs.prefect.io/orchestration/server/overview.html) or the managed [Prefect Cloud](https://cloud.prefect.io). 

## Key Terminology
* Task: An individual unit of computation
* Flow: A collection of tasks in a graph structure
* TaskRun: An instance of a Task
* FlowRun: An instance of a Flow
* Agent: A lightweight process that polls the scheduler API for new or incomplete FlowRuns and allows you to orchestration workflows across heterogeneous environments
* Flow Metadata: Structure of dependencies between tasks and various configurations attached to aspects of your flow (Parameters, Scheduling, Retry Logic, Caching, etc...)

## Navigation
#### Core Directory
![Prefect Core Logo](/images/prefect-core-logo.svg)
* Evolving ETL - Progressive data pipelines with increasing Prefect functionality, using multiple versions of Prefect Core
* Snippets - Various snippets exemplifying different functionality

#### Cloud Directory
![Prefect Cloud Logo](/images/prefect-cloud-logo-white.f7c8b5e3.svg)
* Evolving Orchestration - Progressive data pipelines with increasing Prefect orchestration functionality, demonstrating the combinations of flow level configurations (storage, run_config, executor)
* Orchestrator - Patterns and functionality for running a flow-of-flows, using multiple versions of Prefect Core
* CLI - Various useful CLI commands for usage with Prefect +0.15.0

#### GraphQL
* Queries - Common queries/syntax to retrieve metadata from Prefect's GraphQL API
* Mutations - Common mutations/syntax to retrieve metadata from Prefect's GraphQL API

#### Sales
* Demos - Demonstration scripts used in sales meetings and presentations

## Links
* [Prefect](http://prefect.io)
* [Prefect Documentation](http://docs.prefect.io)
* [Prefect Core Documentation](https://docs.prefect.io/core/)
* [Prefect Cloud Documentation](https://docs.prefect.io/orchestration/)
* [Prefect API Documentation](https://docs.prefect.io/api/latest/)