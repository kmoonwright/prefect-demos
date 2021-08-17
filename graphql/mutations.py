import datetime
import prefect

client = prefect.Client()

# Adding parameters to a create_flow_run API call
client.graphql(
    """
    mutation {
        create_flow_run(
            input: {
                flow_id: "<MY_FLOW_ID>",
                parameters: "{\"<TASK_NAME>\": \"<TASK_VALUE>\"}"
            }
        ) {
            id
        }
    }
    """
)

# Adding a DateClock to a create_flow_run API call
client.graphql(
    """
    mutation {
        create_flow_run(
            input: {
                flow_id: "<MY_FLOW_ID>",
                parameters: "{\"<TASK_NAME>\": \"<TASK_VALUE>\"}",
                scheduled_start_time: "<DATETIME_OBJECT>"
            }
        ) {
            id
        }
    }
    """
)

# Schedule a flow run via API Call
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
client.create_flow_run(
    flow_id="<FLOW_ID>",
    scheduled_start_time=tomorrow,
)

# Delete a Flow Run by ID
client.graphql(
    """
    mutation {
        delete_flow_run(input: {flow_run_id: "<FLOW_ID>"}) {
            success,
            error
        }
    }
    """
)

# Set flow run label
client.graphql(
    """
    mutation {
        set_flow_group_labels_input(
            input: {
                flow_group_id: "<FLOW_GROUP_ID>",
                labels: "MY_LABEL"
            }
        ) {
            success,
            error
        }
    }
    """
)

# Create a Cloud Hook for a Flow Version Group
callback_url = "<CALLBACK_URL>"
client.graphql(
    f"""
    mutation {{
        create_cloud_hook(
            input: {{
                type: SLACK_WEBHOOK,
                name: "GlobalSlackHook",
                version_group_id: null,
                states: ["Failed", "Triggerfailed", "Timedout"],
                config: "{{\\"url\\": \\"{callback_url}\\"}}"                    
        }} ) {{
        id
        }}
    }}
    """
)

flow_run_id = prefect.context.get("flow_run_id")
set_flow_run_state = client.graphql(
    query="""
        mutation SetFlowRunStates($flowRunId: UUID!, $state: JSON!) {
            set_flow_run_states(
                input: {
                states: [{ flow_run_id: $flowRunId, state: $state }]
                }
            ) {
                states {
                id
                status
                message
                }
            }
        }
    """,
    variables={
        "flowRunId": flow_run_id,
        "state": {"type": "Finished"}
    }
)

advanced_query = client.graphql(
    """
    query {
        flow_run(
            where: {_and: [{flow: {name: {_eq: "meta_datapull"}}}, {state: {_eq: "Success"}}, 
                {labels: {_has_key: "prod"}}, {parameters: {_contains: {dataset: consumer_dataset}}}]}
            order_by: {end_time: desc}
            limit: 1
        ) {
            name
            state
            end_time
        }
    }
    """
)