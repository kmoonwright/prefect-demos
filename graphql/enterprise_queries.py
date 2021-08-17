import prefect

client = prefect.Client()


# Query with individual string fields
client.graphql(
    """
    query{
        log(
            where: {
                object_table: {_eq: "user"}, 
                is_audit_log: {_eq: true}}
        ) {
            message
            timestamp
            tenant {id, name}
        }
    }
    """
)

