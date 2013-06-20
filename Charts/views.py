#NMCharts/Charts
from django.http import HttpResponse, HttpResponseRedirect
from django import forms 
from django.template import Context
from Results import *
from TurnMove import *
from django.shortcuts import render
from django.utils import simplejson

class VolumeForm(forms.Form):
    network = forms.CharField(max_length=100)
    host = forms.CharField(max_length=64)
    user = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64)
    links = forms.CharField(max_length=200)
    start = forms.IntegerField(min_value=0)
    end = forms.IntegerField(max_value=10800)

class TurnMoveForm(forms.Form):
    network = forms.CharField(max_length=100)
    host = forms.CharField(max_length=64)
    user = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64)
    simvat = forms.CharField(max_length=64)
    links = forms.CharField(max_length=200)

class TravelTimeForm(forms.Form):
    network = forms.CharField(max_length=100)
    host = forms.CharField(max_length=64)
    user = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64)
    start = forms.IntegerField(min_value=0)
    end = forms.IntegerField(max_value=10800)

def hellocharts(request):
    return render(request, 'charts.html')
    
def basetest(request):
    return render(request, 'base.html')
  
def turnMoveInfo(request):
    form = TurnMoveForm()
    return render(request, 'turnmoveinfo.html', {'form': form})
    
def travelTimeInfo(request):
    form = TravelTimeForm()
    return render(request, 'traveltimeinfo.html', {'form': form})
    
def volumeCountsInfo(request):
    form = VolumeForm()
    return render(request, 'volumeinfo.html', {'form': form})
  
def preTurnMove(request):
    
    if request.method == 'POST':
        form = TurnMoveForm(request.POST)
        if form.is_valid():
            network = form.cleaned_data['network']
            host = form.cleaned_data['host']
            user = form.cleaned_data['user']
            pwd = form.cleaned_data['password']
            simvat = form.cleaned_data['simvat']
            links = form.cleaned_data['links']
        try: 
            c = login(host, user, pwd, network)
        except:
            return HttpResponseRedirect('/charts/dberror/')
        try:
            context = {'network': network, 'host': host, 'user': user, 
                       'pwd': pwd, 'simvat': simvat, 'links': links}
            return render(request, 'turnmove.html', context)              
        except:
            return HttpResponseRedirect('/charts/error/')
    else:
        form = TurnMoveForm()
    return render(request, 'turnmoveinfo.html', {'form': form})

def preVolume(request):
    if request.method == 'POST':
        form = VolumeForm(request.POST)
        if form.is_valid():
            network = form.cleaned_data['network']
            host = form.cleaned_data['host']
            user = form.cleaned_data['user']
            pwd = form.cleaned_data['password']
            links = form.cleaned_data['links']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
        try:
            c = login(host, user, pwd, network)
            c.close()
        except:
            return HttpResponseRedirect('/charts/dberror/')
        try:
            context = {'network': network, 'host': host, 'user': user, 
                       'pwd': pwd, 'start': start, 'end': end, 'links': links}
            
            return render(request, 'volume.html', context)
        except:
            return HttpResponseRedirect('/charts/error/')
    else:
        form = VolumeForm()
    return render(request, 'volumeinfo.html', {'form': form})
 
def preTravelTime(request):
    if request.method == 'POST':
        form = TravelTimeForm(request.POST)
        if form.is_valid():
            network = form.cleaned_data['network']
            host = form.cleaned_data['host']
            user = form.cleaned_data['user']
            pwd = form.cleaned_data['password']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
        try:
            c = login(host, user, pwd, network)
            c.close()
        except:
            return HttpResponseRedirect('/charts/dberror/')
        try: 
            context = {'network': network, 'host': host, 'user': user, 
                       'pwd': pwd, 'start': start, 'end': end}
            return render(request, 'traveltime.html', context)
        except:
            return HttpResponseRedirect('/charts/error/')
    else:
        form = TravelTimeForm()
    return render(request, 'traveltimeinfo.html', {'form': form})


def loadvolume(request, network, host, pwd, user, links, start, end):
    c = login(host, user, pwd, network)
    d = login(host, user, pwd, network)
    numlinks = [int(x) for x in links.split(',')]
    start = int(start)
    end = int(end)
    volumes = compVolume(c, d, network, start, end, numlinks)
    chartdata = simplejson.dumps(volumes)
    c.close()
    d.close()
    return HttpResponse(chartdata, mimetype='application/json')

def loadtraveltime(request, network, host, pwd, user, start, end):
    start = int(start)
    end = int(end)
    c = login(host, user, pwd, network)
    times = getCorridorTimes(c, network, start, end)
    chartdata = simplejson.dumps(times)
    c.close()
    return HttpResponse(chartdata, mimetype='application/json')

def loadturnmove(request, network, host, pwd, user, links):
   
    turns = {}
    moves = {}
    numlinks = links.split(',')
    #HARDCODED....CHANGE IN FUTURE
    simvat = '/Users/Carlos/CTR/nmc_results_module/NMCharts/NMCharts/sim.vat'
    c = login(host, user, pwd, network)
    mmap = movemap()
    mmap = loadfile(simvat, mmap)
    for link in numlinks:
        link = int(link)
        moves = mmap.movesFromLink(link) 
        for x in moves:
            setDirection(x, c)
            temp = x.getInfo()
            turns[temp["id"]] = temp
    c.close()
    data = {"data": turns, "networks": network, "link": numlinks}
    rjson = simplejson.dumps(data)
    return HttpResponse(rjson, mimetype='application/json')