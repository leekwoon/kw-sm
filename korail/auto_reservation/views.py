from django.shortcuts import render
from django.http import JsonResponse
from korail2 import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def note(request):
    return render(request, 'note.md')

def history(request):
    return render(request, 'history.md')

def reservation(request):
    TRAIN_TYPE = [
        ('05','전체(ALL)'),
        ('00','KTX'),
        ('01','새마을호(SAEMAEUL)'),
        ('02','무궁화호(MUGUNGHWA)'),
        ('03','통근열차(TONGGEUN)'),
        ('04','누리로(NURIRO)'),
        ('06','공항직통(AIRPORT)'),
        ('07','KTX-산천(KTX_SANCHEON)'),
        ('08','ITX-새마을(ITX_SAEMAEUL)'),
        ('09','ITX-춘천(ITX_CHEONGCHUN)'),
    ]

    HOURS = range(0,24)

    MINUTES = range(0,60)

    PASSENGERS = range(0,10)

    retdic = {
        'TRAIN_TYPE': TRAIN_TYPE,
        'HOURS': HOURS,
        'MINUTES': MINUTES,
        'PASSENGERS': PASSENGERS
    }
    return render(request, 'reservation.html', retdic)

def auth(request):
    ID = request.POST['id']
    PW = request.POST['pw']
    adult_passenger = int(request.POST['adult_passenger'])
    child_passenger = int(request.POST['child_passenger'])
    senior_passenger = int(request.POST['senior_passenger'])
    print(ID,PW,adult_passenger,child_passenger,senior_passenger)
    korail = Korail(ID, PW, auto_login=False)
    if(korail.login() == False):
        return JsonResponse({'auth':'fail'})
    return JsonResponse({'auth':'success'})

def search(request):
    ID = request.POST['id']
    PW = request.POST['pw']
    adult_passenger = int(request.POST['adult_passenger'])
    child_passenger = int(request.POST['child_passenger'])
    senior_passenger = int(request.POST['senior_passenger'])
    dep = request.POST['dep']
    arr = request.POST['arr']
    train_type = request.POST['train_type']
    datepicker = request.POST['datepicker']
    hour = str(request.POST['hour'])
    minute = str(request.POST['min'])
    search_all = request.POST['search_all']
    no_seat = request.POST['no_seat']

    print('search_all',search_all)

    date = '20'+datepicker[-2:]+datepicker[:2]+datepicker[3:5]
    if len(hour) == 1:
    	hour = '0'+hour
    if len(minute) == 1:
    	minute = '0'+minute

    time = hour+minute+'00'
    korail = Korail(ID, PW, auto_login=False)


    NO_SEAT = True if no_seat == 'true' else False

    if search_all == 'true':
    	trains = korail.search_train_allday(dep, arr, date, time, include_no_seats=NO_SEAT)
    else:
        trains = korail.search_train(dep, arr, date, time, include_no_seats=NO_SEAT)

    retdic = {
        'result': [str(train) for train in trains]
    }
    return JsonResponse(retdic)