import graphene
from .models import Track, Like
from graphene_django import DjangoObjectType
from users.schema import UserType
from graphql import GraphQLError

class TrackType(DjangoObjectType):
    class Meta:
        model = Track


class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType)
    likes = graphene.List(LikeType)

    def resolve_tracks(self, info):
        return Track.objects.all()

    def resolve_likes(self, info):
        return Like.objects.all()

class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, **kwargs):
        title = kwargs.get('title')
        description = kwargs.get('description')
        url = kwargs.get('url')
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Log in to add a track')
        track = Track(title=title, description=description, url=url, posted_by=user)
        track.save()
        return CreateTrack(track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, **kwargs):
        track_id = kwargs.get('track_id')
        title = kwargs.get('title')
        url = kwargs.get('url')
        description = kwargs.get('description')

        user = info.context.user
        track = Track.objects.get(id=track_id)
        if track.posted_by != user:
            raise Exception('Not permitted to update this track')
        track.title = title
        track.description = description
        track.url = url
        track.save()

        return UpdateTrack(track=track)


class DeleteTrack(graphene.Mutation):
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if track.posted_by != user:
            raise GraphQLError("You can not delete this track")
        track.delete()
        return DeleteTrack(track_id=track_id)


class CreateLike(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login first')

        track = Track.objects.get(id=track_id)
        if not track:
            raise GraphQLError('Track not found')

        Like.objects.create(user=user, track=track)
        return CreateLike(user=user, track=track)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_like = CreateLike.Field()
