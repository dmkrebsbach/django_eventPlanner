from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Event
import bcrypt
import datetime
import pytz

def index(request):
    return render(request, "watchParty/index.html")

def registration(request):
    if request.method == "POST":

        errors = User.objects.registrationValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")

        newUser = User.objects.create(
            firstName = request.POST["firstName"],
            lastName = request.POST["lastName"],
            email = request.POST["email"],
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()),
        )
        newUser.save()
        request.session["id"]=newUser.id
        request.session["firstName"]=newUser.firstName
    return redirect("/dashboard")

def login(request):
    if request.method == "POST":

        errors = User.objects.loginValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")

        user = User.objects.get(email=request.POST['loginEmail'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print("User Password Matches")
            request.session["id"]=user.id
            request.session["firstName"]=user.firstName
            return redirect("/dashboard")
        else:
            print('*'*50, '\n',"User Password Match Fails", '\n', '*'*50)
            return redirect("/")

def dashboard(request):
    if "id" in request.session:
        print("user is in session")
        thisUser = User.objects.get(id=request.session['id'])
        context = {
            'user': User.objects.get(id=thisUser.id),
            'userEvents': User.objects.get(id=thisUser.id).events.all(),
            'allEvents' : Event.objects.exclude(attendees=thisUser),
            'hostEvents' : Event.objects.filter(host=thisUser).count(),
            'attendeeCount' : Event.objects.filter(attendees=thisUser).count()
        }
        
        return render(request, "watchParty/dashboard.html", context)
    return redirect ("/")

def newShow(request):

    return render(request, "watchParty/new-show.html")

def createEvent(request):
    if "id" in request.session:
        if request.method == "POST":
            thisUser = User.objects.get(id=request.session["id"])
        newEvent = Event.objects.create(
            title = request.POST["title"],
            genre = request.POST["genre"],
            eventDate = request.POST["eventDate"],
            location = request.POST["location"],
            host = thisUser,
            )
        newEvent.attendees.add(thisUser)    ## this line includes the host as an attendee
        newEvent.save()
        return redirect("/dashboard")
    return redirect ("/")

def viewEvent(request, eventId):
    if "id" in request.session:
        print('*'*50, '\n',"User Viewed This Event", '\n', '*'*50)
        context = {
                'event': Event.objects.get(id=eventId),
                'eventAttendees': Event.objects.get(id=eventId).attendees.all(), 
            }
        return render(request, "watchParty/view-show.html", context)
    return redirect ("/")

def joinEvent(request, eventId):
    if "id" in request.session:
        thisUser = User.objects.get(id=request.session["id"])
        print("user requested to join event")
        joinEvent = Event.objects.get(id=eventId)
        joinEvent.attendees.add(thisUser)
        joinEvent.save()
        print("user joined this event")
        return redirect("/dashboard")
    return redirect ("/")

def leaveEvent(request, eventId):
    if "id" in request.session:
        thisUser = User.objects.get(id=request.session["id"])
        print("this user wants to leave this event")
        leaveEvent = Event.objects.get(id=eventId)
        leaveEvent.attendees.remove(thisUser)
        leaveEvent.save()
        print("user left this event")
        return redirect("/dashboard")
    return redirect ("/")

def cancelEvent(request, eventId):
    if "id" in request.session:
        thisUser = User.objects.get(id=request.session["id"])
        print("this host wants to leave this event")
        cancelEvent = Event.objects.get(id=eventId).delete()
        print("user cancelled this event")
        return redirect("/dashboard")
    return redirect ("/")












def logout(request):
    request.session.clear()
    return redirect("/")