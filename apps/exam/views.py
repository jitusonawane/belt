from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import User , Trip , Group
# Create your views here.

def logincheck(session):
    if 'id' not in session:
        return False
    return True    

def index(request):
    if logincheck(request.session):
        return redirect('/travel')
    else:
        return render(request, 'exam/index.html')

def register(request):
    errors  = User.objects.reg_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():            
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        print "here"
        rg = User.objects.get(email = request.POST['email'])
        request.session['id'] = rg.id   
        return redirect('/travel')


def login(request):    
    errors  = User.objects.login_valiator(request.POST)
    if len(errors):              
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:        
        lg =  User.objects.get(email = request.POST['email'])
        request.session['id'] = lg.id
        return redirect('/travel')


def logout(request):
    del request.session['id']
    return redirect('/')
  

def travel(request):    
    if logincheck(request.session):
        userid = User.objects.get(id=request.session['id'])        
        other_trip = Trip.objects.exclude(user=userid)
        mine_trip = Trip.objects.filter(user=userid)
        
        context = {
            'mine_trip':mine_trip, 
            'other_trip':other_trip
            }
                    
        return render(request, 'exam/travel.html', context)
    else:
        return redirect('/')


def add_trip(request):
    
        return render(request, 'exam/add_trip.html')

def your_trip(request):
    userid = User.objects.get(id=request.session['id'])
    if request.method == "POST":
        destination = request.POST['destination']
        plan = request.POST['plan']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        new_trip=Trip.objects.create(user=userid, destination=destination, plan=plan, start_date=start_date, end_date=end_date)        
        other_trip = Trip.objects.exclude(user=userid)
        context = {
            'new_trip': new_trip, 
            'other_trip': other_trip
            }        
    return redirect('/travel', context)


def join_trip(request, id):
    user = User.objects.get(id=request.session['id'])
    trip_id = Trip.objects.get(id=id)
    trip_attend_by = Trip.objects.filter(user=user)
    trip_owner_by = Group.objects.filter(guest=user)
    owner = trip_id.user.id
    trip_mem = Group.objects.filter(trip=trip_id)    
    group = Group.objects.filter(guest=user)   
    if request.POST['submit'] == 'Join':
        for group in trip_mem:
            if user.id == group.guest.id:               
                messages.info(request, 'you were same  trip!')                
                return redirect('/detail/' + id)
        new_guest = Group.objects.create(guest=user, trip=trip_id, )
        context = {
            'new_guest' : new_guest
        }
    return redirect('/travel' , context)


def detail(request, id):       
    trip_id = Trip.objects.filter(id=id)
    mem = Group.objects.filter(trip=id)
    context={
        'trip_id':trip_id, 
        'mem':mem
        }
    return render(request, 'exam/detail.html', context)