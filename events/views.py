from django.shortcuts import render,redirect
from .models import events
from django.contrib import messages
from django.contrib.auth.models import User, auth
from datetime import datetime
from django.db import connection

from django.core.files.storage import FileSystemStorage

# Create your views here.
def home(request):
    return render(request, 'home.html')

def deleteall(request):
    events.objects.filter(user = request.user).delete()
    return redirect('addevent')


def deleteone(request,cid):
    events.objects.get(pk=cid).delete()
    evs = events.objects.filter(user = request.user)
    data = {'event1':evs}
    # return render(request, 'addevent.html', data)
    return redirect('addevent')

def addevent(request):
    if request.method == 'POST':
        starttime =request.POST['starttime']
        endtime=request.POST['endtime']
        print(starttime)
        name = request.POST['name']
        starttime = starttime+":00"
        endtime = endtime + ":00"
        st =datetime.strptime(starttime, '%H:%M:%S').time()
        et =datetime.strptime(endtime, '%H:%M:%S').time()
        if request.user.is_authenticated:
            event = events(user = request.user,name = name, starttime = st,endtime = et)
            event.save();
            print("event created")
            # event.query
            event1 = events.objects.filter(user = request.user)
            data = {'event1':event1}
            # print(type(event1))
            # for obj in event1:
            #     print(obj.name)
            #     print(obj.starttime)

            return render(request, 'addevent.html', data)
        else:
            messages.info(request, 'Please login to creat events')
            
            return redirect('login.html')
    else:
        event1 = events.objects.filter(user = request.user)
        data = {'event1':event1}
        return render(request, 'addevent.html',data)
    


def showtimetable(request):
    event = events.objects.filter(user = request.user)
    # write your code here:
    # for i in event:
    #     i.name
    #     i.starttime
    #     i.endtime
    
    
    
    
    data = {'event':event}

    return render(request, 'showtimetable.html', data)

    


