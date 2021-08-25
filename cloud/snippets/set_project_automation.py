# Setting a Project level automation via GQL as a flow
from prefect import task, Flow, Parameter, unmapped
from prefect.tasks.secrets import PrefectSecret
from prefect import Client

# Start a python client
@task
def start_prefect_client(my_api_key, my_tenant_id):
    return Client(api_key=my_api_key, tenant_id=my_tenant_id)

# Query for low IDs in a project
@task
def query_project_flows(client, project_name):
    result = client.graphql(
        f"""
            query {{
                flow (
                    where: {{
                        project: {{
                            name: {{_eq: {project_name} }}
                        }}
                    }}
                ){{
                    flow_group_id
                }}
            }}
        """
    )
    # Returns flow ids for roject
    flow_objects = result["data"]["flow"]
    return [flow["flow_group_id"] for flow in flow_objects]

# Create the action - create_action
@task
def create_flow_automation(client, webhook_secret, message):
    action = client.graphql(
        f"""
        mutation {{
            create_action(input: {{
                config: {{
                    slack_notification: {{
                        webhook_url_secret: {webhook_secret},
                        message: {message}
                    }}
                }}
            }}) {{
                id
            }}
        }}
        """
    )
    # Returns automation UUID
    return action["data"]["create_action"]["id"]

# Set the action - create_flow_group_sla
@task
def set_flow_automations(client, sla_id, flow__group_id):
    action = client.graphql(
        f"""
        mutation {{
            create_flow_group_sla(input: {{
                flow_sla_config_id: {sla_id},
                flow_group_id: {flow__group_id}
            }}) {{
                id
            }}
        }}
        """
    )


with Flow("Configure Project Automations") as flow:
    API_KEY = PrefectSecret(name="API Key")
    TENANT_ID = PrefectSecret(name="TENANT ID")
    webhook_secret = PrefectSecret(name="SLACK_WEBHOOK_URL")
    project_name = Parameter(name="Project with flows")
    message = Parameter(name="Slack Message", default="AY YO THERE BE STUFF TO DO")

    client = start_prefect_client(API_KEY, TENANT_ID)
    flows = query_project_flows(client, project_name)
    automation = create_flow_automation(client, webhook_secret, message)

    set_flow_automations.map(
        client=unmapped(client), sla_id=unmapped(automation), flow__group_id=flows
    )
