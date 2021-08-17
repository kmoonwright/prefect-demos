import prefect

client = prefect.Client()


# Query with individual string fields
client.graphql({"query": {"flow": {"id", "name"}}})

# Query with a full GraphQL String
client.graphql(
    """
    query{
        project(where: {name: {_ilike: "%r%"}}){
            name
        }
    }
    """
)

# Query using the WHERE clause
client.graphql(
    """
    query {
        flow_run_state(
            where: {
                state: {_eq: "Failed"}
            }
        ) 
        {
        message,
        state,
        }
    }
    """
)

client.graphql(
    """
    query {
        flow_run_state {
            created
            flow_run {
                created,
                task_runs {
                    created
                }
            }
        }
    }
    """
)

# Query for Flow Group ID
client.graphql(
    """
    query {
        flow(where: {
            name: {_eq: "%s"}
            project: {  name : {_eq: "%s"}}
        }) {
            id
            flow_group_id
        }
    }
    """
)

# Query for Flow ID based on flow & project name
client.graphql(
    """
    query {
        flow (
            where: {
                name: {_eq: <FLOW_NAME>}
                project: {
                    name: {_eq: <PROJECT_NAME>}
                }
            }
        ){
            id,
            name,
            version,
            project {
                name
            }
        }
    }
    """
)

# Query for task runs that failed
client.graphql(
    """
    query {
        task_run(
            where: {
                state: {_eq: "Failed"},
                flow_run_id: {_eq: "<FLOW_ID>"},
            }
        ) {
            task {
                name
            },
            created,
            end_time,
        }
    }
    """
)

# Get project name at runtime
get_project_name = client.graphql(
    """
    query {
        flow_run_by_pk(id: {_eq: "<FLOW_RUN_ID>"}) {
            flow {
                project {
                    name,
                    id,
                }
            }
        }
    }
    """
)

# Get last 10 flow runs of a flow (by ID) and their final state
get_project_name = client.graphql(
    """
    query {
        flow_run(
            where: {
                flow_id: {_eq:"<FLOW_ID>"}
            }
            order_by: {updated: desc}
            limit: 10
        ) {
            id
            state
            name
            scheduled_start_time
        }
    }
"""
)

# Get the last Successful Flow Run by name regardless of version
get_last_successful_flow_run = client.graphql(
    """
    query {
        flow(
            where: {
                name: {_eq: "<FLOW_NAME>"}
            }
            limit:1
        ) {
            flow_runs(
                where: {
                    state: {_eq: "Success"}
                }
                order_by: {updated: desc}
                limit: 1
            ) {
                name
                state
                end_time
            }
        }
    }
    """
)

get_last_successful_flow_run2 = client.graphql(
    """
    query {
        flow_run(
            where: {_and: [
                {flow: {name: {_eq: "<FLOW_NAME>"}}}, 
                {state: {_eq: "Success"}}
            ]}
            order_by: {end_time: desc}
            limit: 1
        ) {
            name
            id
            state
            state_message
            created
            end_time
            version
        }
    }
    """
)

# Get the ID for a Flow's latest version
get_latest_version_of_flow_id = client.graphql(
    """
    query {
        flow(where: { name: { _eq: "<FLOW_NAME>"} } 
            order_by: {version: desc}
            limit: 1
        ) {
            name
            id
            version
        }
    }
    """
)

# Get a count for successful task runs between the timestamps
# _gt == greater than, _gte == greater or equal to, _lt == less than
get_successful_task_runs = client.graphql(
    """
    query {
        task_run_state_aggregate(
            where:{
                state:{ _eq:"Success"} 
                timestamp: { _gt: "2021-02-01", _lt:"2021-02-02"}
            }
        ) {  
        aggregate {count}  
        }
    }
    """
)

# Get logs for a flow run by id
get_flow_logs = client.graphql(
    """
    query {
        log(where:{flow_run_id: {_eq: "<FLOW_RUN_ID>"}}) {
            message
            timestamp
            id
            level
        }
    }
    """
)
get_flow_logs2 = client.graphql(
    """
    query {
        flow_run(where: {id: {_eq: "<FLOW_RUN_ID>"}}) {
            logs {
                created
                info
                name
                message
                timestamp
            }
        }
    }
    """
)