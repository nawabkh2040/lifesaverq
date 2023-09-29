from django.shortcuts import render, HttpResponse ,redirect


def index(request):
     return render(request, 'emergency/index.html')
     # return HttpResponse("Hello")

def privacy_Policy(request):
     return render(request, 'emergency/privacy_policy.html')

def contact(request):
     return render(request, 'emergency/contact_us.html')

def about_me(request):
     return render(request, 'emergency/about_me.html')