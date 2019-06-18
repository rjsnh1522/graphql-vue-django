import graphene
from .models import Track, Like
from graphene_django import DjangoObjectType
from users.schema import UserType
from graphql import GraphQLError
from django.db.models import Q
from django.conf import settings as s
from elasticsearch import Elasticsearch
import json


def elastic_connection():
    # pk = 54
    # es = Elasticsearch(hosts=s.ELASTIC)
    # elastic_data = es.get_source(index=s.ELASTIC_INDEX, doc_type=s.ELASTIC_DOC_TYPE, id=pk)
    js = {
      's1': "Section 1",
      's2': "Section 2",
      's3': "Section 3",
      's4': "Section 4"
    }
    return js


class ElasticType(graphene.ObjectType):
    # id = graphene.ID()
    # index = graphene.String()
    # found = graphene.String()
    # properties = graphene.JSONString()
    # _source =
    key = graphene.String()
    header = graphene.String()


class TrackType(DjangoObjectType):
    class Meta:
        model = Track


class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType, search=graphene.String())
    likes = graphene.List(LikeType)
    elastic = graphene.List(ElasticType)

    def resolve_elastic(self, info):
        sections = elastic_connection()
        sections_as_obj_list = []

        for key, value in sections.items():
            section = ElasticType(key, value)
            sections_as_obj_list.append(section)

        return sections_as_obj_list


    def resolve_tracks(self, info, search=None):

        if search:
            filter = (
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(url__icontains=search) |
                    Q(posted_by__username__icontains=search)

            )
            return Track.objects.filter(filter)
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
