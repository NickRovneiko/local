from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from asgiref.sync import sync_to_async
from telethon import TelegramClient

from .models import Dialogue

import asyncio

api_id = '21992840'
api_hash = 'da0843d28758f33ad168037e277f7bb0'

client = TelegramClient('anon', api_id, api_hash)

async def fetch_dialogues():
    await client.start()
    async for dialog in client.iter_dialogs():
        await sync_to_async(Dialogue.objects.update_or_create, thread_sensitive=True)(
            dialogue_id=dialog.id,
            defaults={'name': dialog.name, 'is_added': False}
        )
    await client.disconnect()

def trigger_fetch_dialogues(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_dialogues())
    return JsonResponse({"status": "Dialogues are being fetched"})

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