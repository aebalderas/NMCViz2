#for pydoc
import sys
sys.path.append('/Users/Carlos')
sys.path.append('/Users/Carlos/nmc/')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nmc.settings")


from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.db import models
from django import forms
from django.utils import simplejson 
import psycopg2

from network.models import Network

class NewNetworkForm(forms.Form):
    """
    test test!!
    """
    name = forms.CharField(max_length = 64)
    host = forms.CharField(max_length = 64)
    user = forms.CharField(max_length = 64)
    password = forms.CharField(max_length = 64)
    database = forms.CharField(max_length = 64)

def network(request):
    dbs = []
    for d in Network.objects.all():
        dbs.append(d.name)
    return render(request, 'network.html', {"databases": dbs})

def load_data(request, network_name, start, interval, terminate):
    
    network = Network.objects.get(name=network_name)
    
    dbc = psycopg2.connect(host=network.host, user=network.user, password=network.password, database=network.database)
    cursor = dbc.cursor()
    
    sql = 'select linkid, from_sec, to_sec, flow_15min as volume, v_over_c from compute_v_over_c(%s,%s,%s) a,links b,bus_route c,bus_route_link d  where b.id=a.linkid and d.link=b.id and c.id=d.route order by from_sec;' % (interval, start, terminate)
    try:
        cursor.execute(sql)
    except Exception, e:
        error_str = e.args[0]
        result = {'status': 'Database error: %s' % error_str}
    else:  
        time_data = []
        last_time = None
        last_timestep = None
       
        for row in cursor:
            
            if row[1] != last_time:
                
                if last_timestep != None:
                    time_data.append(last_timestep)
                    
                last_time = row[1]
                    
                last_timestep = {'linkids': [], 'start': row[1], 'end': row[2], 'volume': [], 'v_over_c': []}
            
            last_timestep['linkids'].append(row[0])
            last_timestep['volume'].append(row[3])
            last_timestep['v_over_c'].append(row[4])
            
        if last_timestep != None:
            time_data.append(last_timestep)
            
        result = {'status': 'OK', 'attributes': ['volume', 'v_over_c'], 'data': time_data}
        
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

def visualize(request, name):

    try:
        network = Network.objects.get(name=name)
    except:
        return HttpResponseRedirect('error/Unable to identify network: %s' % name) 
    else:
        if network == None:
            return HttpResponseRedirect('error/Unable to identify network: %s' % name) 

    try:
        network.load()
    except:
        return HttpResponseRedirect('error/Unable to load network: %s' % name)
    
    args = {}
    args['name'] = name
    args['nodes'] = network.nodes
    args['nodetypes'] = network.nodetypes.split(',')
    args['links'] = network.links
    args['linktypes'] = network.linktypes.split(',')
    args['busroutes'] = network.busroutes
    #return render(request, 'visualize.html', args)
    return render(request, 'UIupdate.html', args)

def network_error(request, errormsg):    
    return render(request, 'database_open_error.html', {"errormsg": errormsg})

def network_ok(request):
    return render(request, 'database_open_ok.html')

def new_network(request):
    if request.method == 'POST':
        form = NewNetworkForm(request.POST)
        if form.is_valid():
            name     = form.cleaned_data['name']
            host     = form.cleaned_data['host']
            user     = form.cleaned_data['user']
            password = form.cleaned_data['password']
            database = form.cleaned_data['database']
        try:
            dbconnection = psycopg2.connect(host=host, user=user, password=password, database=database)
        except:
            return HttpResponseRedirect('error/Unable to access database')
        else:
            try:
                network = Network.objects.get(name=name)
                network.host = host
                network.user = user
                network.password = password
                network.database = database
            except:
                network = Network.objects.create_network(name, host, user, password, database)
            network.save()
            return HttpResponseRedirect('ok')
    else:
        form = NewNetworkForm()

    return render(request, 'new_network.html', { 'form': form, })
