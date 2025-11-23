from django.shortcuts import render

# Create your views here.
# ChatAppApi/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from LivreApp.models import Livre
from AvisApp.utils import get_recommended_books_for_user


@csrf_exempt
def chatbot_api(request):
    """
    Very simple JSON API for the SmartLibrary chatbot.
    It reads a user message and returns a text reply.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        message = data.get('message', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    if not message:
        return JsonResponse({
            'reply': "I didn’t receive any text. Please type a question about books or the library 😊"
        })

    user = request.user if request.user.is_authenticated else None
    lower = message.lower()

    # 1) Recommendations
    if ('recommend' in lower) or ('suggest' in lower) or ('advice' in lower) or ('advise' in lower):
        books = get_recommended_books_for_user(user, limit=5)
        if not books:
            reply = (
                "I don’t have enough information yet to recommend books.\n"
                "Try rating a few books first, and I’ll be able to give you better suggestions 😉"
            )
        else:
            lines = [f"- {b.title} — {b.author}" for b in books]
            intro = "Here are some books I recommend for you:\n" if user else \
                    "Here are some popular books:\n"
            reply = intro + "\n".join(lines)
        return JsonResponse({'reply': reply})

    # 2) Search: "search <keyword>"
    if lower.startswith('search '):
        query = message.split(' ', 1)[1]
        books = Livre.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query),
            available=True
        )[:5]

        if not books:
            reply = f"I couldn’t find any book for “{query}”."
        else:
            lines = [f"- {b.title} — {b.author}" for b in books]
            reply = f"Here is what I found for “{query}”:\n" + "\n".join(lines)
        return JsonResponse({'reply': reply})

    # 3) Help / default answer
    help_text = (
        "I can help you with:\n"
        "- Recommending books → type: “recommend some books”\n"
        "- Searching a book → type: “search Harry Potter”\n"
    )
    reply = (
        "Thanks for your message! I am still a simple chatbot for now 🤖.\n\n"
        + help_text
    )
    return JsonResponse({'reply': reply})
