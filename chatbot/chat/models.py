from django.db import models
from django.utils import timezone

class Conversation(models.Model):
    titre = models.CharField(max_length=100, default="Nouvelle conversation")
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titre

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    contenu = models.TextField()
    est_utilisateur = models.BooleanField(default=True)  # True pour l'utilisateur, False pour le bot
    date_envoi = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.conversation.titre} - {'Utilisateur' if self.est_utilisateur else 'Bot'}"