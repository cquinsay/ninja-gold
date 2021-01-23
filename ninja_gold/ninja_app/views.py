from django.shortcuts import render, redirect
import random
from datetime import datetime

GOLD_INCREMENTS = {
    'farm': (10,20),
    'cave': (5,10),
    'house': (2,5),
    'casino': (0,50),
}

def index(request):
    if not "gold" in request.session or "activities" not in request.session:
        request.session['gold'] = 0
        request.session['activities'] = []
    return render(request, 'index.html')

def reset(request):
    request.session.flush()
    return redirect('/')

def process_gold(request):
    if request.method == 'GET':
        return redirect('/')
    place_name = request.POST['place']
    place = GOLD_INCREMENTS[place_name]
    place_name_upper = place_name[0].upper() + place_name[1:]
    curr_gold = random.randint(place[0], place[1])
    now_formatted = datetime.now().strftime("%m/%d/%Y%I:%M%p")
    result = 'earn'

    message = f"Earned {curr_gold} from the {place_name_upper}! ({now_formatted})"

    if place_name == 'casino':
        if random.randint(0,1) > 0:
            message = f"Entered a {place_name} and lost {curr_gold} golds... Ouch...({now_formatted})"
            curr_gold = curr_gold * -1
            result = 'lose'
    
    request.session['gold'] += curr_gold

    request.session['activities'].append({"message": message, "result": result})
    return redirect('/')



# Create your views here.
