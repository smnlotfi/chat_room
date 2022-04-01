from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate
from django.http import JsonResponse


# Create your views here.


def main(request,*args,**kwargs):
    if request.user.is_authenticated:
            return redirect('/chat')
    msg=""
    if (request.POST or None):
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:  
            login(request,user)
            return redirect('/chat')
        else:
            msg='username or password is incorect!'

    context={
        'msg':msg
    }
    return render(request,'login.html',context)

def login_function(request,*args,**kwargs):
    if (request.POST or None):
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:  
         login(request,user)
         loginresponse='true'
        else:
         loginresponse='false'

    response={
        'loginresponse':loginresponse
    }
    
    return JsonResponse(response)

