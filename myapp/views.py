#views.py
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from .models import Dialogue, Message
import datetime

from .one_dialog import get_messages_by_dialogue_id

from asgiref.sync import sync_to_async



@sync_to_async
def get_dialogues():
    return list(Dialogue.objects.filter(is_added=True))

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

@sync_to_async
def get_dialogues():
    return list(Dialogue.objects.filter(is_added=True))

async def fetch_and_save_messages(request):
    dialogues = await get_dialogues()
    for dialogue in dialogues:
        messages_data = await get_messages_by_dialogue_id(dialogue.dialogue_id)
        for data in messages_data:
            await save_message(data, dialogue)
    return JsonResponse({'status': 'success', 'message': 'Messages have been updated successfully.'})

@sync_to_async
def save_message(data, dialogue):
    # Проверяем, что поле 'text' не является None или пустой строкой
    if data.get('text') is None or data.get('text').strip() == "":
        data['text'] = "No message text provided"  # Заполнение значения по умолчанию, если текст отсутствует

    Message.objects.update_or_create(
        message_id=data['message_id'],
        defaults={
            'user_id': data['user_id'],
            'date': data['date'],
            'text': data['text'],
            'dialogue': dialogue
        }
    )

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