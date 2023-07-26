import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Note
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from .exceptions import NotOwnerException
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, OrderingFilter, CharFilter
from .utils import convert_graphqlid_to_int
from django.db.models import Q

User = get_user_model()

class NoteFilter(FilterSet):
    search = CharFilter(method='filter_by_title_or_content')
    class Meta:
        model = Note
        fields = {
            'title': ('contains',),
            'content': ('contains',),
        }
    order_by = OrderingFilter(
        fields=(
        ('created_at', 'created_at'),
        ),
        field_labels={
        'created_at': 'created_at',
        }
    )
    def filter_by_title_or_content(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))

class NoteType(DjangoObjectType):
    class Meta:
        model = Note
        interfaces = (graphene.relay.Node,)
        
class NoteConnections(graphene.relay.Connection):
    class Meta:
        node = NoteType   
    
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
        num_id = convert_graphqlid_to_int(id)
        note = Note.objects.get(id = num_id)
        if note.user.id != info.context.user.id:
            raise NotOwnerException
        note.delete()      
        return DeleteNoteMutation(message = "Note deleted succesfully")      

class BulkDeleteNotesMutation(graphene.Mutation):
    class Arguments:
        ids = graphene.List(graphene.ID, required=True)
    
    message = graphene.String()      
    
    @permissions_checker([IsAuthenticated])
    def mutate(self, info, ids):
        """
        -ids is a string like: ['Tm90ZVR5cGU6OTQ=,Tm90ZVR5cGU6OTI=,Tm90ZVR5cGU6OTE=']
        -so i convert ids to a list with list(ids) to obtains something like ['Tm90ZVR5cGU6OTQ=,Tm90ZVR5cGU6OTI=,Tm90ZVR5cGU6OTE=']
        -then i take ids[0] -> 'Tm90ZVR5cGU6OTQ=,Tm90ZVR5cGU6OTI=,Tm90ZVR5cGU6OTE='
        -split them and save in a list to iterate the ids, recovery the note and delete it
        """
        ids_list = str(list(ids)[0]).split(",") 
        for id in ids_list:
            num_id = convert_graphqlid_to_int(id)
            note = Note.objects.get(id = num_id)
            if note.user.id != info.context.user.id:
                raise NotOwnerException
            note.delete()      
        return DeleteNoteMutation(message = "Notes deleted succesfully")       

class UpdateNoteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()
    
    note = graphene.Field(NoteType)      

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, id, title, content):
        num_id = convert_graphqlid_to_int(id)
        note = Note.objects.get(id = num_id)
        if note.user.id != info.context.user.id:
            raise NotOwnerException
        note.title = title
        note.content = content
        note.save()      
        return UpdateNoteMutation(note = note)  
         
class Query(graphene.ObjectType):
    notes = DjangoFilterConnectionField(NoteType, filterset_class = NoteFilter)
    note = graphene.Field(NoteType, id = graphene.ID())
    
    @permissions_checker([IsAuthenticated])
    def resolve_notes(self, info, **kwargs):
        return Note.objects.filter(user = info.context.user.id)
    
    @permissions_checker([IsAuthenticated])
    def resolve_note(self, info, id):
        num_id = convert_graphqlid_to_int(id)
        note = Note.objects.get(id = num_id)
        if note.user.id != info.context.user.id:
            raise NotOwnerException
        return note
    
class Mutation(graphene.ObjectType):
    create_note = CreateNoteMutation.Field()    
    delete_note = DeleteNoteMutation.Field()
    bulk_delete_notes = BulkDeleteNotesMutation.Field()
    update_note = UpdateNoteMutation.Field()