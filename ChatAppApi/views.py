# ChatAppApi/views.py
import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from LivreApp.models import Livre
from AvisApp.utils import get_recommended_books_for_user

from google import genai


# Create Gemini client using API key from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # Optionnel : tu peux juste logguer ça en prod
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set. "
        "Please set it before running the server."
    )

client = genai.Client(api_key=GEMINI_API_KEY)


def call_gemini(prompt: str) -> str:
    """
    Call Gemini 2.5 Flash with a text prompt and return the response text.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        # response.text contient le texte concaténé de la réponse
        return (response.text or "").strip()
    except Exception as e:
        # En prod : logger l'erreur
        return f"Sorry, I had an issue contacting the AI service: {e}"


@csrf_exempt
def chatbot_api(request):
    """
    JSON API for SmartLibrary chatbot using Gemini 2.5 Flash.
    The frontend (chat.html) sends a user message, we:
      - enrich it with context (recommendations / search results)
      - send a single prompt to Gemini
      - return the AI's answer as 'reply' in JSON
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

    # --------- 1) Optional: get recommendations if user asks for them ----------
    recommended_books = None
    if "recommend" in lower or "suggest" in lower or "advice" in lower or "advise" in lower:
        recommended_books = list(get_recommended_books_for_user(user, limit=5))

    # --------- 2) Optional: search books if user types "search ..." ----------
    search_results = None
    search_query = None
    if lower.startswith("search "):
        search_query = message.split(" ", 1)[1]
        search_results = list(
            Livre.objects.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(description__icontains=search_query),
                available=True
            )[:5]
        )

    # --------- 3) Build a rich prompt for Gemini ----------
    context_lines = [
        "You are SmartLibrary, a helpful virtual librarian for an online bookstore / library.",
        "Always answer in clear, friendly English.",
        "",
        f"User message: {message}",
        "",
    ]

    if recommended_books:
        context_lines.append("Based on this user's history, here are some recommended books:")
        for b in recommended_books:
            context_lines.append(f"- {b.title} — {b.author}")
        context_lines.append("")

    if search_results is not None:
        # user explicitly did a search
        context_lines.append(f"The user searched for: {search_query}")
        if search_results:
            context_lines.append("Here are books in the catalog matching this search:")
            for b in search_results:
                context_lines.append(f"- {b.title} — {b.author}")
        else:
            context_lines.append("No books were found in the catalog for this search.")
        context_lines.append("")

    context_lines.append(
        "Use the information above to answer the user naturally. "
        "If you suggest specific books, try to pick from the list I provided when possible. "
        "Keep the answer reasonably short and focused on books or the library context."
    )

    full_prompt = "\n".join(context_lines)

    # --------- 4) Call Gemini and return the answer ----------
    ai_reply = call_gemini(full_prompt)

    return JsonResponse({'reply': ai_reply})
