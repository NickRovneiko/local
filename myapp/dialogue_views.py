from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import Dialogue
from asgiref.sync import sync_to_async
import asyncio

from .telegram_client import telegram_client, start_telegram_client

async def fetch_dialogues():
    await start_telegram_client()
    async for dialog in telegram_client.iter_dialogs():
        await sync_to_async(Dialogue.objects.update_or_create, thread_sensitive=True)(
            dialogue_id=dialog.id,
            defaults={'name': dialog.name, 'is_added': False}
        )
    await telegram_client.disconnect()

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




