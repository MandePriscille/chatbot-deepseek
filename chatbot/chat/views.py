from openai import OpenAI
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from decouple import config
from .models import Conversation, Message

# Récupération de la clé API depuis les variables d'environnement
DEEPSEEK_API_KEY = config('DEEPSEEK_API_KEY')

# Initialisation du client OpenAI avec la clé API et l'URL de base
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def call_deepseek_api(message):
    """
    Envoie un message à l'API DeepSeek et retourne la réponse.

    :param message: Le message de l'utilisateur à envoyer à l'API.
    :return: La réponse de l'API ou un message d'erreur.
    """
    try:
        print(f"Message envoyé à DeepSeek : {message}")  # Debugging

        # Envoi du message à l'API DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": message.strip()},
            ],
            stream=False
        )

        # Retourne le contenu de la réponse
        return response.choices[0].message.content
    except Exception as e:
        # Log l'erreur et retourne un message d'erreur
        print(f"Erreur lors de l'appel à l'API DeepSeek1 : {str(e)}")  # Logging pour le débogage
        return f"Erreur lors de l'appel à l'API DeepSeek : {str(e)}"


def conversation_list(request):
    conversations = Conversation.objects.all()
    return render(request, "chatbot/conversation_list.html", {"conversations": conversations})

def conversation_create(request):
    if request.method == "POST":
        titre = request.POST.get("titre", "Nouvelle conversation").strip()
        conversation = Conversation.objects.create(titre=titre)
        return redirect(reverse("conversation_detail", args=[conversation.id]))
    return render(request, "chatbot/conversation_create.html")

def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.select_related("conversation").all()

    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        if user_message:
            Message.objects.create(conversation=conversation, contenu=user_message, est_utilisateur=True)
            bot_response = call_deepseek_api(user_message)
            Message.objects.create(conversation=conversation, contenu=bot_response, est_utilisateur=False)
        return redirect(reverse("conversation_detail", args=[conversation.id]))

    return render(request, "chatbot/conversation_detail.html", {"conversation": conversation, "messages": messages})

def conversation_delete(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.method == "POST":
        conversation.delete()
        return redirect(reverse("conversation_list"))
    return render(request, "chatbot/conversation_delete.html", {"conversation": conversation})


