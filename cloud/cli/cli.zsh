"""
prefect run is designed to make the transition from local execution to running with a Cloud or Server backend seamless. 
Previously, when developing, you needed to define your flow then call flow.run() at the bottom; then, to test the flow, 
you'd run python my_flow_file.py; then, when the flow is ready to be pushed to Cloud, you'd change your flow.run() call 
to flow.register(\"project\") and go to the UI to start a flow run. With prefect register (introduced in 0.14.13) and 
prefect run, you can drop this cruft from your flow. Limiting your flow files to the definition of your flow and using 
the CLI to perform actions on that definition means you don't have to edit your flow to change how it is run.
prefect run will take an import or file path to run a flow locally; this replaces using flow.run(). For example, the 
following will run the file, extract the flow object, and call flow.run() for you:
"""
# KEY CLI COMMANDS
# Replaces flow.run():
prefect run --path sdlc_v15/hello_name.py
prefect run --path sdlc_v15/hello_name.py --param name=Marvin

# Replaces flow.register():
prefect register --path sdlc_v15/hello_name.py --project example


# SAMPLE SDLC WITH CLI
# Running the flow locally:
prefect run --path sdlc_v15/hello_name.py

# Login to Prefect Cloud
prefect auth login --key <MY_KEY>
prefect auth list-tenants
prefect auth switch-tenants --slug <MY_SLUG>

# Create a project & register a flow to it
prefect create project "My Project" --skip-if-exists
prefect register --path sdlc_v15/hello_name.py --project My Project
# If watch is set, the specified paths and modules will be monitored 
# and registration re-run upon changes.
prefect register --path sdlc_v15/hello_name.py --project My Project --watch

# Run registered flow with the backend by flow name and watch execution
prefect run --name "Hello Good Lookin" --label prod --label demo-flows
prefect run --name "Hello Good Lookin" --watch
# Run registered flow and execute locally without an agent, must be registered
prefect run --name "Hello Good Lookin" --execute
# Run registered flow and pipe flow run id to another program
prefect run -n "Hello Good Lookin" --quiet | post_run.sh