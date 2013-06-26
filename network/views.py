#import  numpy, pickle
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.db import models
from django import forms
from django.utils import simplejson 
import psycopg2, sqlite3
#from TDD import *
import os

from network.models import Network

class NewNetworkForm(forms.Form):
    database = forms.CharField(max_length = 64)
    host = forms.CharField(max_length = 64)
    user = forms.CharField(max_length = 64)
    password = forms.CharField(max_length = 64)


def network(request):
    dbs = []
    for d in Network.objects.all():
        dbs.append(d.database)
    return render(request, 'network.html', {"databases": dbs})

def load_origins(request, network, dataset):
    user, network = tuple(network.split('_', 1))
    try:
        db = sqlite3.connect('/var/opt/vtg/vista/%s/%s/%s' % (user, network, dataset))
        c = db.cursor()
        c.execute('select distinct(orig) from paths')
    except:
        return HttpResponse(simplejson.dumps({'status': 'No such dataset as %s in %s' % (dataset, network)}), mimetype='application/json')
    
    r = {'status': 'OK', 'name': dataset, 'origins': [i[0] for i in c]}
    rjson = simplejson.dumps(r)
    return HttpResponse(rjson, mimetype='application/json')

def load_destinations(request, network, dataset, origin):
    user, network = tuple(network.split('_', 1))
    try:
        dbname = '/var/opt/vtg/vista/%s/%s/%s' % (user, network, dataset)
        db = sqlite3.connect(dbname)
        c = db.cursor()
        sql = 'select distinct(dest) from paths where orig in (%s)' % origin
        c.execute(sql)
    except:
        return HttpResponse(simplejson.dumps({'status': 'No such dataset as %s in %s' % (dataset, network)}), mimetype='application/json')
    
    r = {'status': 'OK', 'name': dataset, 'destinations': [i[0] for i in c]}
    rjson = simplejson.dumps(r)
    return HttpResponse(rjson, mimetype='application/json')

    
def load_paths(request, network, dataset, interval, origin, destination):
    user, network = tuple(network.split('_', 1))
    try:
        db = sqlite3.connect('/var/opt/vtg/vista/%s/%s/%s' % (user, network, dataset))
        c = db.cursor()
        sql = 'select cast((time / %s) as int) as tstep, count(*), max(elapsed), path from paths where orig in (%s) and dest in (%s) group by tstep, orig, dest, path order by tstep' % (interval, origin, destination)
        c.execute(sql)
    except:
        return HttpResponse(simplejson.dumps({'status': 'No such dataset as %s in %s' %  (dataset, network)}), mimetype='application/json')

    timesteps = []
    current_timestep_links = {}
    current_timestep_tstep = -1
    for i in c:
        if i[0] != current_timestep_tstep:
            if current_timestep_tstep >= 0:
                timesteps.append(current_timestep_links)
            current_timestep_links = {}
            current_timestep_tstep = i[0]
        for link in i[3].split(','):
            if current_timestep_links.has_key(link) == False:
                current_timestep_links[link] = [0, 0]
            current_timestep_links[link][0] += i[1]
            current_timestep_links[link][1] = max(current_timestep_links[link][1], i[2])  
            
    timesteps.append(current_timestep_links)
    
    max_count = 0
    max_time = 0
    for t, tstep in enumerate(timesteps):
        linkids = []
        counts = []
        times = []
        for linkid in tstep:
            count, time = tstep[linkid]
            if count > max_count: max_count = count
            if time > max_time: max_time = time
            linkids.append(linkid)
            counts.append(count)
            times.append(time)
        timesteps[t] = {'linkids': linkids, 'counts': counts, 'times': times}
        
    result = {'timesteps': timesteps, 'attributes': {'counts' : [0, max_count], 'times': [0, max_time]}}

    r = {'status': 'OK', 'name': dataset, 'data': result}
    rjson = simplejson.dumps(r)
    return HttpResponse(rjson, mimetype='application/json')

    
def load_path_data(request, network, dataset):
    user, network = tuple(network.split('_', 1))
    if os.path.exists('/var/opt/vtg/vista/%s/%s/%s' % (user, network, dataset)):
        return HttpResponse(simplejson.dumps({'status': 'OK', 'dataset': dataset}), mimetype='application/json')
    else:
        return HttpResponse(simplejson.dumps({'status': 'No such dataset as %s in %s' %  (dataset, network)}), mimetype='application/json')
 
def load_link_data(request, database, dataset):
    
    network = Network.objects.get(database=database)
    
    variable_name = dataset.rsplit('.', 1)[0]
    directory_name = '/var/opt/vtg/vista/%s/%s' % tuple(network.database.split('_', 1))                                                    
    fullname = directory_name + '/' + dataset

    try:
        tdd = TDD.load(fullname, directory_name + '/LinkIndex')
    except:
        return HttpResponse(simplejson.dumps({'status': 'No such dataset: %s' % fullname}), mimetype='application/json')

    data = {variable_name: {'timesteps': tdd.timesteps, 'ids': tdd.ids, 'data': tdd.data.tolist()}}
    r = {'status': 'OK', 'linkdata': data}
    rjson = simplejson.dumps(r)

    return HttpResponse(rjson, mimetype='application/json')


def load_network(request, database):
    
    try:
        network = Network.objects.get(database=database)
    except:
        return HttpResponseRedirect('error/Unable to identify network: %s' % database) 
    else:
        if network == None:
            return HttpResponseRedirect('error/Unable to identify network: %s' % database) 
        
    try:
        network.load()
    except:
        return HttpResponseRedirect('error/Unable to load network: %s' % database)
          
    nodelist = []
    for n in network.nodes:
        nodelist.append([n.nid, n.ntype, n.point, n.attributes])
  
    idlist  = []
    linklist    = []    
    linkattrvalues  = []
    for i in network.linkattrs:
        linkattrvalues.append([])

    for l in network.links:
        idlist.append(l.lid)
        linklist.append([l.lid, l.ltype, l.src, l.dst, l.path])
        for i,a in enumerate(linkattrvalues):
            a.append(l.attributes[i])

    linkattributes = {}
    for i,attrname in enumerate(network.linkattrs):
        if attrname == 'length':
            attrname = 'len'
        linkattributes[attrname] = {'timesteps': [0], 'ids': idlist, 'data': [linkattrvalues[i]]}

    busroutes = {}
    for bid in network.busroutes:
        br = network.busroutes[bid].split(',')
        busroutes[bid] = [int(a) for a in br]
    
    result = {
        'nodes': nodelist, 'nodeTypes': network.nodetypes.split(','), 'nodeAttributes': {}, 
        'links': linklist, 'linkTypes': network.linktypes.split(','), 'linkAttributes': linkattributes, 
        'busroutes': busroutes
    }
              
    s = simplejson.dumps(result)

    return HttpResponse(s, mimetype='application/json')

def visualize(request, database):

    try:
        network = Network.objects.get(database=database)
    except:
        return HttpResponseRedirect('error/Unable to identify network: %s' % database) 
    else:
        if network == None:
            return HttpResponseRedirect('error/Unable to identify network: %s' % database) 
    
    return render(request, 'visualize.html', {'database': database})

def network_error(request, errormsg):    
    return render(request, 'database_open_error.html', {"errormsg": errormsg})

def network_ok(request):
    return render(request, 'database_open_ok.html')

def new_network(request):
    if request.method == 'POST':
        form = NewNetworkForm(request.POST)
        if form.is_valid():
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
                network = Network.objects.get(database=database)
                network.host = host
                network.user = user
                network.password = password
                network.database = database
            except:
                network = Network.objects.create_network(host, user, password, database)
            network.save()
            return HttpResponseRedirect('ok')
    else:
        form = NewNetworkForm()

    return render(request, 'new_network.html', { 'form': form, })
