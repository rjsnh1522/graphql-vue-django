# Self and info values
import graphene
import json
from datetime import datetime
import uuid
# if query has multiple field then to resolve then create a class


class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()


class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return 'http://cloudnary.com/{}/{}'.format(self.username, self.id)


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


class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title, content):
        if info.context.get('is_anonymous'):
            raise Exception('Not authenticated')
        post = Post(title=title, content=content)
        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(
    '''
    query {
        users{
            id
            username
            avatarUrl
        }
    }
    ''',
    context={'is_anonymous': False}
    # variable_values={'title': 'Post Title', 'content': 'Post content'}
)
dictResults = json.dumps(dict(result.data.items()), indent=4)
print(dictResults)

# variable data type passed in mutation must match with defined in the arguments
# use exclamation mark to mark field as required
# $title: String, $content: String
# title: $username, content: $content

# dynamic mutation
# mutation($username: String) {
#     createUser(username: $username){
#     user
# {
#     id
# username
# createdAt
# }
# }
# }


# dynamic query
# query
# getUsersQuery($limit: Int){
#     users(limit: $limit){
#     id
# username
# createdAt
# }
# }
