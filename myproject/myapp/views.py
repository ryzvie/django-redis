import json

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import DataCivil, DataGroup, DataStatus

from django.template import loader

from django.contrib.auth import authenticate, login
# Create your views here.
def index(request):
    context = {}
    

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            msg = "error login account, cek your account"
            return render(request, "home/login.html", {"msg": msg})

    html_template = loader.get_template("home/login.html")
    return HttpResponse(html_template.render(context, request))



def dashboard(request):
    context = {}
    context['users'] = User.objects.all()
    context['status'] = DataStatus.objects.all()
    context['group'] = DataGroup.objects.all()

    html_template = loader.get_template("page/dashboard.html")
    return HttpResponse(html_template.render(context, request))
