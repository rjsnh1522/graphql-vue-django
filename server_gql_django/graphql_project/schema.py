import graphene
import graphql_jwt

from tracks.schema import Query as tracks_query
from tracks.schema import Mutation as tracks_mutation
from users.schema import Mutation as users_mutation
from users.schema import Query as user_query


class Query(user_query,
            tracks_query,
            graphene.ObjectType):
    pass


class Mutation(users_mutation,
               tracks_mutation,
               graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

