"""character_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from character_manager_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path("create_character", views.create_character),
    path("characters", views.load_characters),
    path("character/<int:c_id>", views.character_self),
    path("character/edit_character", views.edit_character),
    path("character/check", views.check),
    path("character/skill_check", views.skill_check),
    path("character/save_proficiency", views.save_proficiency),
    path("character/get_html_weapon", views.get_html_weapon),
    path("character/get_html_item", views.get_html_item),
    path("character/save_weapon", views.save_weapon),
    path("character/roll_weapon_damage", views.roll_weapon_damage),
    path("character/save_item", views.save_item)
    
]
