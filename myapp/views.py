from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from .models import Dialogue, Message
import datetime

from .dialogs import get_messages_by_dialogue_id, fetch_dialogues  # Импорт fetch_dialogues

from asgiref.sync import sync_to_async
from datetime import datetime

# Функция для вызова снаружи
@sync_to_async
def get_dialogues():
    return list(Dialogue.objects.filter(is_added=True))

@sync_to_async
def create_or_update_dialogue(dialogue_data):
    Dialogue.objects.update_or_create(
        dialogue_id=dialogue_data['dialogue_id'],
        defaults={'name': dialogue_data['name']}
    )

async def save_dialogues_to_db():
    dialogues = await fetch_dialogues()
    for dialogue_data in dialogues:
        await create_or_update_dialogue(dialogue_data)

@sync_to_async
def save_message(data, dialogue):
    if data.get('text') is None or data.get('text').strip() == "":
        data['text'] = "No message text provided"

    Message.objects.update_or_create(
        message_id=data['message_id'],
        defaults={
            'user_id': data['user_id'],
            'date': data['date'],
            'text': data['text'],
            'dialogue': dialogue
        }
    )

@sync_to_async
def get_last_message_date(dialogue):
    last_message = Message.objects.filter(dialogue=dialogue).order_by('-date').first()
    if last_message:
        return last_message.date
    return None

async def fetch_and_save_messages(request):
    dialogues = await get_dialogues()
    for dialogue in dialogues:
        last_message_date = await get_last_message_date(dialogue)
        if last_message_date:
            last_message_date = last_message_date.replace(tzinfo=None)  # Убираем информацию о временной зоне
        messages_data = await get_messages_by_dialogue_id(dialogue.dialogue_id, last_message_date)
        for data in messages_data:
            await save_message(data, dialogue)
    return JsonResponse({'status': 'success', 'message': 'Messages have been updated successfully.'})

@csrf_exempt
async def load_dialogues(request):
    await save_dialogues_to_db()
    return JsonResponse({'status': 'success', 'message': 'Dialogues have been loaded successfully.'})

def show_dialogues(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('dialogue_ids')
        if selected_ids:
            Dialogue.objects.filter(dialogue_id__in=selected_ids).update(is_added=True)
        return redirect('show_dialogues')

    dialogues = Dialogue.objects.all()
    added_dialogues = dialogues.filter(is_added=True)
    return render(request, 'select_dialogues.html', {
        'dialogues': dialogues,
        'added_dialogues': added_dialogues
    })

def search_dialogues(request):
    search_query = request.GET.get('search', '').strip()
    dialogues = Dialogue.objects.filter(name__icontains=search_query)[:10]  # Ограничиваем количество результатов
    html = render_to_string('search_results.html', {'dialogues': dialogues})
    return HttpResponse(html)

@csrf_exempt
def add_dialogue(request):
    dialogue_id = request.POST.get('dialogue_id')
    dialogue = Dialogue.objects.get(dialogue_id=dialogue_id)
    dialogue.is_added = True
    dialogue.save()
    return JsonResponse({'status': 'success', 'name': dialogue.name})

def get_recent_messages(request):
    dialogue_id = request.GET.get('dialogue_id')
    messages = Message.objects.filter(dialogue__dialogue_id=dialogue_id).order_by('-date')[:20]
    messages_html = render_to_string('recent_messages.html', {'messages': messages})
    return HttpResponse(messages_html)

@csrf_exempt
def delete_dialogue(request):
    if request.method == 'POST':
        dialogue_id = request.POST.get('dialogue_id')
        dialogue = Dialogue.objects.filter(dialogue_id=dialogue_id)
        if dialogue.exists():
            dialogue.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Dialogue not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

from django.db.models import Q
from django.utils.html import escape

@csrf_exempt
def search_messages(request):
    search_query = request.GET.get('search', '').strip()
    if search_query:
        messages = Message.objects.filter(Q(text__icontains=search_query))[:50]  # Ограничиваем количество результатов
        for message in messages:
            message.text = escape(message.text).replace(search_query, f'<span class="highlight">{search_query}</span>')
        html = render_to_string('message_search_results.html', {'messages': messages})
        return HttpResponse(html)
    return HttpResponse('')
