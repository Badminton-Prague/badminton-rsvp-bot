from django.http import HttpResponse

def index(request):
    return HttpResponse("Telegram bot is running in the background.")