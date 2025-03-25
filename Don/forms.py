# forms.py
from django import forms
from .models import Donneur, ConditionsSante

class DonneurForm(forms.ModelForm):
    class Meta:
        model = Donneur
        fields = ['date_remplissage', 'date_naissance', 'niveau_etude', 'genre', 'situation_matrimoniale', 'profession', 'arrondissement_residence', 'quartier_residence', 'poids']
        widgets = {
            'date_remplissage': forms.DateInput(attrs={'type': 'date'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'genre': forms.Select(choices=[
                ('M', 'Masculin'),
                ('F', 'Féminin'),
                ('Autre', 'Autre'),
            ]),
        }

class ConditionsSanteForm(forms.ModelForm):
    class Meta:
        model = ConditionsSante
        fields = ['poids', 'taille', 'maladie_chronique', 'dernier_don', 'porteur_hiv', 'porteur_hbs', 'porteur_hcv', 'opere', 'drepanocytaire', 'diabetique', 'hypertendu', 'asthmatique', 'cardiaque', 'tatoue', 'date_tatouage', 'scarifie', 'date_scarification']
        widgets = {
            'dernier_don': forms.DateInput(attrs={'type': 'date'}),
            'date_tatouage': forms.DateInput(attrs={'type': 'date'}),
            'date_scarification': forms.DateInput(attrs={'type': 'date'}),
            'maladie_chronique': forms.Select(choices=[
                ('Oui', 'Oui'),
                ('Non', 'Non'),
            ]),
            'porteur_hiv': forms.CheckboxInput(),
            'porteur_hbs': forms.CheckboxInput(),
            'porteur_hcv': forms.CheckboxInput(),
            'opere': forms.CheckboxInput(),
            'drepanocytaire': forms.CheckboxInput(),
            'diabetique': forms.CheckboxInput(),
            'hypertendu': forms.CheckboxInput(),
            'asthmatique': forms.CheckboxInput(),
            'cardiaque': forms.CheckboxInput(),
            'tatoue': forms.CheckboxInput(),
            'scarifie': forms.CheckboxInput(),
        }