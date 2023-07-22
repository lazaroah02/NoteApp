import graphene

import notes_api.schema
import authentication_api.schema

class Query(authentication_api.schema.Query, notes_api.schema.Query, graphene.ObjectType):
    pass

class Mutation(authentication_api.schema.Mutation, notes_api.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query = Query, mutation = Mutation)