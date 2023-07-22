import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Note
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from .exceptions import NotOwnerException

User = get_user_model()

class NoteType(DjangoObjectType):
    class Meta:
        model = Note

class UserType(DjangoObjectType):
    class Meta:
        model = User   
        fields = ["username"]     
        
class CreateNoteMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        content = graphene.String()   
    
    note = graphene.Field(NoteType)    
    
    @permissions_checker([IsAuthenticated])
    def mutate(self, info, title, content):
        note = Note(title = title, content = content, user = info.context.user)
        note.save()
        return CreateNoteMutation(note = note)

class DeleteNoteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    
    message = graphene.String()      
    
    @permissions_checker([IsAuthenticated])
    def mutate(self, info, id):
        note = Note.objects.get(id = id)
        if note.user.id != info.context.user.id:
            raise NotOwnerException
        note.delete()      
        return DeleteNoteMutation(message = "Note deleted succesfuly")      

class UpdateNoteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()
    
    note = graphene.Field(NoteType)      

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, id, title, content):
        note = Note.objects.get(id = id)
        if note.user.id != info.context.user.id:
            raise NotOwnerException
        note.title = title
        note.content = content
        note.save()      
        return UpdateNoteMutation(note = note)  
         
class Query(graphene.ObjectType):
    notes = graphene.List(NoteType)
    note = graphene.Field(NoteType, id = graphene.ID())
    
    @permissions_checker([IsAuthenticated])
    def resolve_notes(self, info, **kwargs):
        return Note.objects.filter(user = info.context.user.id)
    
    @permissions_checker([IsAuthenticated])
    def resolve_note(self, info, id):
        note = Note.objects.get(id = id)
        if note.user.id != info.context.user.id:
            raise NotOwnerException
        return note
    
class Mutation(graphene.ObjectType):
    create_note = CreateNoteMutation.Field()    
    delete_note = DeleteNoteMutation.Field()
    update_note = UpdateNoteMutation.Field()