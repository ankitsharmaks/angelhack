from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from models import *
import json
import datetime

def store_tag(group_name, tag_str, score):
    group, created = Group.objects.get_or_create(name = group_name)
    if created:
        group.save()
    tags = group.tag_set.all()
    found = False
    for tag_model in tags:
        if tag_model.name == tag_str:
            found = True
            tag_model.score += score
            tag_model.save()
    if not found:
        new_tag_model = Tag(group = group, name = tag_str, score = score)
        new_tag_model.save()

def index(request):
    #now = datetime.datetime.now()
    return render(request, 'index.html', {})
    #html = "<html><body>It is now %s.</body></html>" % now
    #return HttpResponse(html)


def chat(request):
    user_param = request.GET['user']
    group_param = request.GET['group']
    location_param = request.GET['location']
    if request.method == 'GET' and user_param and group_param and location_param:
        request.session['user'] = user_param
        group, created = Group.objects.get_or_create(name = group_param)
        if created:
            group.save()
        user, created = User.objects.get_or_create(name=user_param, location=location_param, group=group)
        if created:
            user.save()
        return render(request, 'chat.html', {'user' : user_param, 'group' : group_param})
    return HttpResponseNotFound('<h1>Page not found</h1>')

def tags(request):
    group_param = request.GET['group']
    if request.method == 'GET' and group_param:
        group, created = Group.objects.get_or_create(name = group_param)
        print group.name
        if created:
            group.save()
        tags = group.tag_set.all()
        tag_list = [tag.name for tag in tags]
        return HttpResponse(json.dumps(tag_list))
    return HttpResponseNotFound('<h1>Page not found</h1>')

@csrf_exempt
def message(request):
    if request.method == 'POST':
        print(request.POST['message'])
        print(request.POST['user'])
        print(request.POST['group'])
        tagsWithScore = getTagsWithScore(request.POST['message'])
        for tagWithScore in tagsWithScore:
            store_tag(request.POST['group'], tagWithScore[0], tagWithScore[1])
    return HttpResponse('Okay!')

def getTagsWithScore(message):
    return [['indian',1.5],['cheap',0.5],['chinese',2.5]]

@csrf_exempt
def recommendations(request):
    if request.method == 'GET':
        group_param = request.GET['group']
        group, created = Group.objects.get_or_create(name = group_param)
        if created:
            group.save()
        users = group.user_set.all()
        coordinates = []
        for user in users:
            coordinates.append(user.location)
        tags = group.tag_set.all()
        tag_list = sorted([[tag.score, tag.name] for tag in tags])
        return HttpResponse(get_recommendations([tag_list[-1][1]], coordinates))
    return HttpResponse('Okay!')



def get_recommendations(tags, coordinates):
    print tags
    print coordinates
    return '[{"rating": 4.5, "name": "14 Carrot Taco Stand", "business_id": "14-carrot-taco-stand-seattle", "image_url": "http://s3-media3.fl.yelpcdn.com/bphoto/zdMx1mpcAttXklY-_dmcDA/ms.jpg", "yelp_url": "http://www.yelp.com/biz/14-carrot-taco-stand-seattle", "categories": [["Food Stands", "foodstands"], ["Mexican", "mexican"]]}, {"rating": 3.0, "name": "Little Water Cantina", "business_id": "little-water-cantina-seattle", "image_url": "http://s3-media4.fl.yelpcdn.com/bphoto/ZFZd-5Hsgr4hVZ9IWfAiKw/ms.jpg", "yelp_url": "http://www.yelp.com/biz/little-water-cantina-seattle", "categories": [["Mexican", "mexican"]]}, {"rating": 4.5, "name": "Tacos Chukis", "business_id": "tacos-chukis-seattle", "image_url": "http://s3-media3.fl.yelpcdn.com/bphoto/qxFr4q5vKzct8XxBxNTawQ/ms.jpg", "yelp_url": "http://www.yelp.com/biz/tacos-chukis-seattle", "categories": [["Mexican", "mexican"]]}, {"rating": 4.0, "name": "Mezcaleria Oaxaca", "business_id": "mezcaleria-oaxaca-seattle", "image_url": "http://s3-media4.fl.yelpcdn.com/bphoto/e3kRkjjPnrgE4dxCsdAngw/ms.jpg", "yelp_url": "http://www.yelp.com/biz/mezcaleria-oaxaca-seattle", "categories": [["Mexican", "mexican"]]}, {"rating": 4.0, "name": "Guanaco\'s Tacos Pupuseria", "business_id": "guanacos-tacos-pupuseria-seattle", "image_url": "http://s3-media3.fl.yelpcdn.com/bphoto/l01yTX3uvTfH98qOjwU9GA/ms.jpg", "yelp_url": "http://www.yelp.com/biz/guanacos-tacos-pupuseria-seattle", "categories": [["Mexican", "mexican"], ["Salvadoran", "salvadoran"]]}, {"rating": 4.0, "name": "Red Star Taco Bar", "business_id": "red-star-taco-bar-seattle", "image_url": "http://s3-media3.fl.yelpcdn.com/bphoto/LjCGPYa_Wd4Wcj_08HAg4g/ms.jpg", "yelp_url": "http://www.yelp.com/biz/red-star-taco-bar-seattle", "categories": [["Mexican", "mexican"]]}]'

