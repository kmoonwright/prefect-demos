from flow_to_register import flow

# Signature:
# flow.register(
#     project_name: str = None,
#     build: bool = True,
#     labels: List[str] = None,
#     set_schedule_active: bool = True,
#     version_group_id: str = None,
#     no_url: bool = False,
#     idempotency_key: str = None,
#     **kwargs: Any,
# ) -> Union[str, NoneType]
# Docstring:
# Register the flow with Prefect Cloud; if no storage is present on the Flow, the default
# value from your config will be used and initialized with `**kwargs`.

# Args:
#     - project_name (str, optional): the project that should contain this flow.
#     - build (bool, optional): if `True`, the flow's environment is built
#         prior to serialization; defaults to `True`
#     - labels (List[str], optional): a list of labels to add to this Flow's environment;
#         useful for associating Flows with individual Agents; see
#         http://docs.prefect.io/orchestration/agents/overview.html#flow-affinity-labels
#     - set_schedule_active (bool, optional): if `False`, will set the schedule to
#         inactive in the database to prevent auto-scheduling runs (if the Flow has a
#         schedule).  Defaults to `True`. This can be changed later.
#     - version_group_id (str, optional): the UUID version group ID to use for versioning
#         this Flow in Cloud; if not provided, the version group ID associated with this
#         Flow's project and name will be used.
#     - no_url (bool, optional): if `True`, the stdout from this function will not
#         contain the URL link to the newly-registered flow in the Cloud UI
#     - idempotency_key (str, optional): a key that, if matching the most recent
#         registration call for this flow group, will prevent the creation of
#         another flow version and return the existing flow id instead.
#     - **kwargs (Any): if instantiating a Storage object from default settings, these
#         keyword arguments will be passed to the initialization method of the default
#         Storage class

# Returns:
#     - str: the ID of the flow that was registered


# Examples
# flow.register(project_name="Cloud Configuration Examples")

# flow.register(project_name="Cloud Configuration Examples", labels=["docker_agent_1"])

flow.register(
    project_name="Cloud Configuration Examples", idempotency_key=flow.serialized_hash()
)

# flow.register(project_name="Cloud Configuration Examples", build=False)
