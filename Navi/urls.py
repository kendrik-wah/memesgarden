from django.urls import path, re_path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
	
	# main screen
    re_path(r'^$', views.index, name='index'),
    path('home', views.home, name='homepage'),
    path('about', views.about, name='about'),

    # log-in flow
    path('register', views.register, name='register'),
    path('authenticate', views.authenticate, name='authenticate'),

    # task screen
    path('tasks', views.tasks, name='tasks'),
    path('your_tasks', views.your_tasks, name='your_tasks'),
    path('accept_tasks', views.accept_tasks, name='accept_tasks'),
    path('create_tasks', views.create_tasks, name='create_tasks'),
    path('request_tasks', views.request_tasks, name='request_tasks'),

    # rewards screen
    path('rewards', views.rewards, name='rewards'),
    path('your_rewards', views.your_rewards, name='your_rewards'),
    path('claim_rewards', views.claim_rewards, name='claim_rewards'),

    # plants screen
    path('plants', views.plants, name='plants'),
    path('your_plants', views.your_plants, name='your_plants'),
    path('request_add_plant', views.request_add_plant, name='request_add_plant'),
    path('add_plant', views.add_plant, name='add_plant')
]