import imp
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required



@login_required(login_url='/')
def chat(request):
    context={}
    return render(request,'chat.html')