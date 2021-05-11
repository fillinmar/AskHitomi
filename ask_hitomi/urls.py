from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('new/', views.new_questions, name='new_questions'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('question/<int:pk>/', views.question_page, name='question_page'),
    path('tag/<str:tag>/', views.tag_questions, name='tag_questions'),
    path('settings/', views.settings, name='settings'),
    path('ask/', views.ask_question, name='ask_question'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('', views.new_questions, name='root'),
]
