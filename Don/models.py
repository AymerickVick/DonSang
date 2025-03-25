# Don/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Donneur(models.Model):
    id = models.AutoField(primary_key=True)
    date_remplissage = models.DateField(default=timezone.now)
    date_naissance = models.DateField()
    niveau_etude = models.CharField(max_length=50)
    genre = models.CharField(max_length=10, choices=[
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('Autre', 'Autre'),
    ])
    situation_matrimoniale = models.CharField(max_length=20)
    profession = models.CharField(max_length=50)
    arrondissement_residence = models.CharField(max_length=50)
    quartier_residence = models.CharField(max_length=50)
    age = models.IntegerField(editable=False)
    poids = models.FloatField(null=True, blank=True)
    est_eligible = models.BooleanField(default=False)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Lien avec l'utilisateur

    def save(self, *args, **kwargs):
        today = timezone.now().date()
        self.age = today.year - self.date_naissance.year - ((today.month, today.day) < (self.date_naissance.month, self.date_naissance.day))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Donneur {self.id}"

class ConditionsSante(models.Model):
    donneur = models.OneToOneField(Donneur, on_delete=models.CASCADE, related_name='conditionssante')
    raison_non_eligibilite = models.CharField(max_length=255, blank=True, null=True)
    taille = models.FloatField(null=True, blank=True)
    poids = models.FloatField(null=True, blank=True)
    maladie_chronique = models.CharField(max_length=3, choices=[
        ('Oui', 'Oui'),
        ('Non', 'Non'),
    ], default='Non')
    dernier_don = models.DateField(null=True, blank=True)
    porteur_hiv = models.BooleanField(default=False)
    porteur_hbs = models.BooleanField(default=False)
    porteur_hcv = models.BooleanField(default=False)
    opere = models.BooleanField(default=False)
    drepanocytaire = models.BooleanField(default=False)
    diabetique = models.BooleanField(default=False)
    hypertendu = models.BooleanField(default=False)
    asthmatique = models.BooleanField(default=False)
    cardiaque = models.BooleanField(default=False)
    tatoue = models.BooleanField(default=False)
    date_tatouage = models.DateField(null=True, blank=True)
    scarifie = models.BooleanField(default=False)
    date_scarification = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Conditions de {self.donneur}"

class AutresRaisons(models.Model):
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    raison_supplementaire = models.TextField()

    def __str__(self):
        return f"Raison pour {self.donneur}"