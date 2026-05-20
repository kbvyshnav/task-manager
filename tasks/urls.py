
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('tasks/',views.task_list,name='task_list'),

     #dynamic URL's
    #path('tasks/<int:task_id>/',views.task_detail,name='task_detail'),
]