from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from models import *
from TagRank import getCountForTags
import tags_extraction
import json
import datetime
import recom

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
    return tags_extraction.extractTagsWithScore(message)

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
        tag_list = sorted([[tag.name, tag.score] for tag in tags], reverse=True)
        tagsWithCount = getCountForTags(tag_list)
        totalResponse = []
        for tagWithCount in tagsWithCount:
            totalResponse.append(get_recommendations(tagWithCount, coordinates))
        json_output = json.dumps(totalResponse[0])
        return HttpResponse(json_output)
    return HttpResponse('Okay!')

def get_recommendations(tagWithCount, coordinates):
    print tagWithCount
    print coordinates
    return recom.fetch_recommendation(tagWithCount, coordinates)