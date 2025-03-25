# Don/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('ajout-utilisateur/', views.ajout_utilisateur, name='ajout_utilisateur'),
    path('liste-utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('modifier-utilisateur/<int:user_id>/', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('supprimer-utilisateur/<int:user_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('ajout-donneur/', views.ajout_donneur, name='ajout_donneur'),
    path('liste-donneurs/', views.liste_donneurs, name='liste_donneurs'),
    path('detail-donneur/<int:donneur_id>/', views.detail_donneur, name='detail_donneur'),
    path('modifier-donneur/<int:donneur_id>/', views.modifier_donneur, name='modifier_donneur'),
    path('supprimer-donneur/<int:donneur_id>/', views.supprimer_donneur, name='supprimer_donneur'),
    path('tableau-bord/', views.tableau_bord, name='tableau_bord'),
    path('verifier-eligibilite/', views.verifier_eligibilite, name='verifier_eligibilite'),
    path('verifier-eligibilite/<int:donneur_id>/', views.verifier_eligibilite, name='verifier_eligibilite_donneur'),
    path('tableau-eligibilite/', views.tableau_eligibilite, name='tableau_eligibilite'),
]