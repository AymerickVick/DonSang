# Don/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Donneur, ConditionsSante
from .forms import DonneurForm, ConditionsSanteForm
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Vue de connexion
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue, {username} !")
                return redirect('liste_donneurs')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Erreur dans le formulaire.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vue de déconnexion
def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')

# Vue pour ajouter un utilisateur
@login_required
def ajout_utilisateur(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur ajouté avec succès !")
            return redirect('liste_utilisateurs')
        else:
            messages.error(request, "Erreur lors de l'ajout de l'utilisateur.")
    else:
        form = UserCreationForm()
    return render(request, 'ajout_utilisateur.html', {'form': form})

# Vue pour lister les utilisateurs
@login_required
def liste_utilisateurs(request):
    utilisateurs = User.objects.all()
    return render(request, 'liste_utilisateurs.html', {'utilisateurs': utilisateurs})

# Vue pour modifier un utilisateur
@login_required
def modifier_utilisateur(request, user_id):
    utilisateur = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=utilisateur)
        if form.is_valid():
            form.save()
            messages.success(request, "Utilisateur modifié avec succès !")
            return redirect('liste_utilisateurs')
        else:
            messages.error(request, "Erreur lors de la modification.")
    else:
        form = UserCreationForm(instance=utilisateur)
    return render(request, 'modifier_utilisateur.html', {'form': form, 'utilisateur': utilisateur})

# Vue pour supprimer un utilisateur
@login_required
def supprimer_utilisateur(request, user_id):
    utilisateur = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        utilisateur.delete()
        messages.success(request, "Utilisateur supprimé avec succès !")
        return redirect('liste_utilisateurs')
    return render(request, 'supprimer_utilisateur.html', {'utilisateur': utilisateur})

# Vues existantes (inchangées sauf ajout de @login_required où nécessaire)
@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def ajout_donneur(request):
    if request.method == 'POST':
        donneur_form = DonneurForm(request.POST)
        conditions_form = ConditionsSanteForm(request.POST)
        if donneur_form.is_valid() and conditions_form.is_valid():
            donneur = donneur_form.save(commit=False)
            donneur.utilisateur = request.user  # Associe l'utilisateur connecté
            donneur.save()
            conditions = conditions_form.save(commit=False)
            conditions.donneur = donneur
            conditions.save()
            messages.success(request, "Donneur ajouté avec succès !")
            return redirect('liste_donneurs')
        else:
            messages.error(request, "Erreur lors de l'enregistrement.")
    else:
        donneur_form = DonneurForm()
        conditions_form = ConditionsSanteForm()
    return render(request, 'ajout_donneur.html', {
        'donneur_form': donneur_form,
        'conditions_form': conditions_form
    })

@login_required
def liste_donneurs(request):
    donneurs = Donneur.objects.all()
    total_donneurs = donneurs.count()
    donneurs_femmes = donneurs.filter(genre='F').count()
    donneurs_hommes = donneurs.filter(genre='M').count()
    return render(request, 'liste_donneurs.html', {
        'donneurs': donneurs,
        'total_donneurs': total_donneurs,
        'donneurs_femmes': donneurs_femmes,
        'donneurs_hommes': donneurs_hommes
    })

@login_required
def detail_donneur(request, donneur_id):
    donneur = get_object_or_404(Donneur, id=donneur_id)
    try:
        conditions = donneur.conditionssante
    except ConditionsSante.DoesNotExist:
        conditions = None
    return render(request, 'detail_donneur.html', {
        'donneur': donneur,
        'conditions': conditions
    })

@login_required
def modifier_donneur(request, donneur_id):
    donneur = get_object_or_404(Donneur, id=donneur_id)
    try:
        conditions = donneur.conditionssante
    except ConditionsSante.DoesNotExist:
        conditions = None

    if request.method == 'POST':
        donneur_form = DonneurForm(request.POST, instance=donneur)
        conditions_form = ConditionsSanteForm(request.POST, instance=conditions)
        if donneur_form.is_valid() and conditions_form.is_valid():
            donneur_form.save()
            conditions = conditions_form.save(commit=False)
            conditions.donneur = donneur
            conditions.save()
            messages.success(request, "Donneur modifié avec succès !")
            return redirect('liste_donneurs')
        else:
            messages.error(request, "Erreur lors de la modification.")
    else:
        donneur_form = DonneurForm(instance=donneur)
        conditions_form = ConditionsSanteForm(instance=conditions)

    return render(request, 'modifier_donneur.html', {
        'donneur_form': donneur_form,
        'conditions_form': conditions_form,
        'donneur': donneur
    })

@login_required
def supprimer_donneur(request, donneur_id):
    donneur = get_object_or_404(Donneur, id=donneur_id)
    if request.method == 'POST':  # Changé de GET à POST pour sécurité
        donneur.delete()
        messages.success(request, "Donneur supprimé avec succès !")
        return redirect('liste_donneurs')
    return render(request, 'supprimer_donneur.html', {'donneur': donneur})

@login_required
def verifier_eligibilite(request, donneur_id=None):
    donneurs = Donneur.objects.all()
    if donneur_id:
        donneur = get_object_or_404(Donneur, id=donneur_id)
        try:
            conditions = donneur.conditionssante
        except ConditionsSante.DoesNotExist:
            messages.error(request, "Conditions de santé manquantes.")
            return render(request, 'eligibilite.html', {
                'donneurs': donneurs,
                'donneur': donneur,
                'conditions': None,
                'resultat': None
            })
    else:
        donneur = None
        conditions = None

    if request.method == 'POST':
        donneur_id = request.POST.get('donneur_id')
        donneur = get_object_or_404(Donneur, id=donneur_id)
        try:
            conditions = donneur.conditionssante
        except ConditionsSante.DoesNotExist:
            messages.error(request, "Conditions de santé manquantes.")
            return render(request, 'eligibilite.html', {
                'donneurs': donneurs,
                'donneur': donneur,
                'conditions': None,
                'resultat': None
            })

        raisons = []
        today = date.today()
        if donneur.age < 18 or donneur.age > 65:
            raisons.append("Âge non éligible (18-65 ans).")
        if conditions.poids < 50:
            raisons.append("Poids insuffisant (< 50 kg).")
        if conditions.dernier_don:
            delta = today - conditions.dernier_don
            if donneur.genre == 'F' and delta.days < 120:
                raisons.append("Délai insuffisant (4 mois pour femmes).")
            elif donneur.genre == 'M' and delta.days < 90:
                raisons.append("Délai insuffisant (3 mois pour hommes).")
        if conditions.porteur_hiv or conditions.porteur_hbs or conditions.porteur_hcv or \
           conditions.opere or conditions.drepanocytaire or conditions.diabetique or \
           conditions.hypertendu or conditions.asthmatique or conditions.cardiaque or \
           conditions.maladie_chronique == 'Oui':
            raisons.extend(["Condition médicale incompatible"])
        if conditions.tatoue and conditions.date_tatouage and (today - conditions.date_tatouage).days < 365:
            raisons.append("Tatouage récent (< 12 mois).")
        if conditions.scarifie and conditions.date_scarification and (today - conditions.date_scarification).days < 365:
            raisons.append("Scarification récente (< 12 mois).")

        if not raisons:
            conditions.raison_non_eligibilite = "Éligible"
            donneur.est_eligible = True
            resultat = "Éligible pour le don de sang."
            messages.success(request, resultat)
        else:
            conditions.raison_non_eligibilite = "; ".join(raisons)
            donneur.est_eligible = False
            resultat = "Non éligible : " + conditions.raison_non_eligibilite
            messages.error(request, resultat)

        conditions.save()
        donneur.save()
        return render(request, 'eligibilite.html', {
            'donneurs': donneurs,
            'donneur': donneur,
            'conditions': conditions,
            'resultat': resultat
        })

    return render(request, 'eligibilite.html', {
        'donneurs': donneurs,
        'donneur': donneur,
        'conditions': conditions,
        'resultat': None
    })

@login_required
def tableau_eligibilite(request):
    donneurs = Donneur.objects.all()
    return render(request, 'tableau_eligibilite.html', {'donneurs': donneurs})

@login_required
def tableau_bord(request):
    donneurs = Donneur.objects.all()
    total_donneurs = donneurs.count()
    donneurs_hommes = donneurs.filter(genre='M').count()
    donneurs_femmes = donneurs.filter(genre='F').count()
    donneurs_autre = donneurs.filter(genre='Autre').count()
    donneurs_eligible = donneurs.filter(est_eligible=True).count()
    donneurs_non_eligible = total_donneurs - donneurs_eligible

    age_18_30 = donneurs.filter(age__gte=18, age__lte=30).count()
    age_31_45 = donneurs.filter(age__gte=31, age__lte=45).count()
    age_46_65 = donneurs.filter(age__gte=46, age__lte=65).count()
    age_plus_65 = donneurs.filter(age__gt=65).count()

    conditions = ConditionsSante.objects.all()
    total_conditions = conditions.count()
    maladies_chroniques = conditions.filter(maladie_chronique='Oui').count()
    porteurs_hiv = conditions.filter(porteur_hiv=True).count()
    porteurs_hbs = conditions.filter(porteur_hbs=True).count()
    porteurs_hcv = conditions.filter(porteur_hcv=True).count()
    drepanocytaires = conditions.filter(drepanocytaire=True).count()

    pourcentage_maladies_chroniques = (maladies_chroniques / total_conditions * 100) if total_conditions > 0 else 0

    genre_data = {
        'labels': ['Hommes', 'Femmes', 'Autre'],
        'data': [donneurs_hommes, donneurs_femmes, donneurs_autre],
        'colors': ['#3498db', '#e91e63', '#9b59b6']
    }
    eligibilite_data = {
        'labels': ['Éligibles', 'Non Éligibles'],
        'data': [donneurs_eligible, donneurs_non_eligible],
        'colors': ['#2ecc71', '#e74c3c']
    }
    age_data = {
        'labels': ['18-30 ans', '31-45 ans', '46-65 ans', 'Plus de 65 ans'],
        'data': [age_18_30, age_31_45, age_46_65, age_plus_65],
        'colors': ['#3498db', '#e91e63', '#2ecc71', '#f1c40f']
    }

    return render(request, 'tableau_bord.html', {
        'total_donneurs': total_donneurs,
        'donneurs_hommes': donneurs_hommes,
        'donneurs_femmes': donneurs_femmes,
        'donneurs_autre': donneurs_autre,
        'donneurs_eligible': donneurs_eligible,
        'donneurs_non_eligible': donneurs_non_eligible,
        'age_18_30': age_18_30,
        'age_31_45': age_31_45,
        'age_46_65': age_46_65,
        'age_plus_65': age_plus_65,
        'maladies_chroniques': maladies_chroniques,
        'pourcentage_maladies_chroniques': round(pourcentage_maladies_chroniques, 2),
        'porteurs_hiv': porteurs_hiv,
        'porteurs_hbs': porteurs_hbs,
        'porteurs_hcv': porteurs_hcv,
        'drepanocytaires': drepanocytaires,
        'genre_data': genre_data,
        'eligibilite_data': eligibilite_data,
        'age_data': age_data,
    })