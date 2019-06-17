import graphene
import json
from datetime import datetime
import uuid
# if query has multiple field then to resolve then create a class


class User(graphene.ObjectType):
    id = graphene.ID(default=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())


class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())

    def resolve_users(self, info, limit=None):
        return [
            User(id='1', username="bob", created_at=datetime.now()),
            User(id='2', username="alice", created_at=datetime.now()),
            User(id='3', username="psyther", created_at=datetime.now()),
        ][:limit]


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        user = User(username=username)
        # we can remove created_at from here and use it in User class
        # same with the id field
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(
    '''
    mutation {
        createUser(username: "jeff"){
           user{
            id
            username
            createdAt
           }
        }
    }
    '''
)
dictResults = json.dumps(dict(result.data.items()), indent=4)
print(dictResults)


