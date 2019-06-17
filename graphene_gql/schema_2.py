import graphene
import json
from datetime import datetime
# if query has multiple field then to resolve then create a class


class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    created_at = graphene.DateTime()


class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())

    def resolve_users(self, info, limit=None):
        return [
            User(id='1', username="bob", created_at=datetime.now()),
            User(id='2', username="alice", created_at=datetime.now()),
            User(id='3', username="psyther", created_at=datetime.now()),
        ][:limit]


schema = graphene.Schema(query=Query)

result = schema.execute(
    '''
    {
        users {
            id
            username
            createdAt
        }
    }
    '''
)
dictResults = json.dumps(dict(result.data.items()), indent=4)
print(dictResults)

# schema should in camelCase or
# if you want to use snake case then set auto_camelcase=False in schema
