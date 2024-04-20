
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from .models import Dialogue



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