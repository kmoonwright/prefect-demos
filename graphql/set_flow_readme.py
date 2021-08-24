# ATM Setting a Flow ReadME is only available via GQL

mutation = """
mutation($input: set_flow_group_description_input!) {
   set_flow_group_description(input: $input) {
      success
   } 
}
"""

from prefect import Client

client = Client()

client.graphql(
    mutation,
    variables=dict(
        input=dict(description="<README_MARKDOWN>", flow_group_id="<FLOW_GROUP_ID>")
    ),
)
