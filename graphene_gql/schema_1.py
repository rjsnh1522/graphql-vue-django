import graphene
import json

class Query(graphene.ObjectType):
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return "world"

    def resolve_is_admin(self, info):
        return True

schema = graphene.Schema(query=Query)

result = schema.execute(
    '''
    {
        isAdmin
    }
    '''
)
dictResults = dict(result.data.items())
print(dictResults)

# schema should in camelCase or
# if you want to use snake case then set auto_camelcase=False in schema
