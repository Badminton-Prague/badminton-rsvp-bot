import asyncio
import json
from django.http import HttpResponse
from .bot import set_webhook, run_bot


def index(request):
    if request.method == 'POST':
        data = request.body
        telegram_update = json.loads(data.decode('utf-8'))
        asyncio.run(run_bot(telegram_update))
        return HttpResponse("ok")
    else:
        webhook_url = f'https://{request.META.get("HTTP_HOST", "")}'
        asyncio.run(set_webhook(webhook_url))
        return HttpResponse(f'We have set the webhook url to {webhook_url}')