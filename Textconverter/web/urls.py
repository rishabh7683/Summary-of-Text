
from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'web'

urlpatterns=[

    path('about/',views.about,name='about'),
]
