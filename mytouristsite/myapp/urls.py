"""
URL configuration for mytouristsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('mostra_itinerario/<str:name>/<str:place>/<int:duration>/', views.mostra_itinerario, name='mostra_itinerario'),
    path('rispondi_domanda/<str:place>/', views.rispondi_domanda, name='rispondi_domanda'),
    path('pagina_punteggio/<int:punteggio>/', views.pagina_punteggio, name='pagina_punteggio'),

]

