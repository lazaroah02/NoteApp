from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/api/', include('authentication_api.urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True))),
]


