from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
import datetime

def index(request):
    #now = datetime.datetime.now()
    return render(request, 'index.html', {})
    #html = "<html><body>It is now %s.</body></html>" % now
    #return HttpResponse(html)


def chat(request):
    user_param = request.GET['user']
    if request.method == 'GET' and user_param:
        request.session['user'] = user_param
        return render(request, 'chat.html', {'user' : user_param})
    return HttpResponseNotFound('<h1>Page not found</h1>')