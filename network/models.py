#for pydoc
import sys
sys.path.append('/Users/Carlos')
sys.path.append('/Users/Carlos/nmc/')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nmc.settings")

from django.db import models
import sys, psycopg2

#what are these for? necessary?
#Nodes = {}
#Links = []

class Node():
    """
    class pydoc test
    """
    def __init__(self, nid, ntype, point, attrs):
        """
        nid  : unique node identifier
        ntype: specifies node or centroid
        point:
        attrs:
        """
        self.nid        = nid
        self.ntype      = ntype
        self.point      = point
        self.attributes = attrs
        
class Link():
    def __init__(self, lid, ltype, src, dst, path, attrs):
        """
        lid  : unique link identifier
        ltype: specifies link or centroid connector
        src  :
        dst  :
        path :
        attrs:
        """
        self.lid        = lid
        self.src        = src
        self.dst        = dst
        self.ltype      = ltype
        self.path       = eval(path)
        self.attributes = attrs
      
class NetworkManager(models.Manager):
    def create_network(self, name, host, user, password, database):
        """
        
        """
        n = self.create(name=name, host=host, user=user, password=password, database=database)
        return n
class Network(models.Model): #original
#class Network(): #pydoc
    """
    name, host, user, password, database
    """
    name = models.CharField(max_length = 64)
    host = models.CharField(max_length = 64)
    user = models.CharField(max_length = 64)
    password = models.CharField(max_length = 64)
    database = models.CharField(max_length = 64) 
        
    objects = NetworkManager()   
    nodemap = {}
    nodes = []
    linkmap = {}
    links = []
    busroutes = []
    loaded = False
    linktypes = ""
    nodetypes = ""
    busroutes = ""
        
    def __unicode__(self):
        """
        network unicode respresentation, returns network name
        """
        return self.name
    
    def load(self):
        """
        cursor is the cursor() do the nmc database
        
        loads nodes: 
          nodes is a list containing instances of class Nodes
          nodemap is a dictionary
            key : node id
            value : index of node id within nodes 
          types is a list containing type numbers of nodes; node or centroid
          nodetypes is a string, comma delimited listing of types
          
        loads links:
          links is a list containing instances of class Link
          linkmap is a dictonary
            key: link id
            value: index of link id within links
          attrs is a dictionary containing link attributes
          types is replaced wiht a list containing type numbers of links: link or centroid connector
          linktypes is a string, comma delimited listing of types
          
        load busroutes:
          busroutes is a dictionary
            key: route id
            value: list of all links in the bus route
        """
        if self.loaded == False:
            self.loaded = True
            
            dbc = psycopg2.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = dbc.cursor()
            
        cursor.execute('select id, type, x, y from nodes;')
            
        for node in cursor:
            self.nodemap[node[0]] = len(self.nodes)
            self.nodes.append(Node(node[0], node[1], [node[2], node[3]], {}))
            
        cursor.execute('select distinct(type) from nodes;')
        types = []
        for t in cursor:
            types.append(str(t[0]))
            
        self.nodetypes = ','.join(types)
          
        cursor.execute('select d.id, d.lanes, d.destination, d.source, d.type, d.capacity, d.speed, d.length, l.points from linkdetails d join links l on d.id = l.id;')
            
        for link in cursor:
            self.linkmap[link[0]] = len(self.links)
            attrs = {}
            attrs['lanes']    = link[1]
            attrs['capacity'] = link[5]
            attrs['speed']    = link[6]
            attrs['length']   = link[7]
            self.links.append(Link(link[0], link[4], self.nodemap[link[3]], self.nodemap[link[2]], link[8], attrs))
        
        cursor.execute('select distinct(d.type) from linkdetails d join links l on d.id = l.id;')
        types = []
        for t in cursor:
            types.append(str(t[0]))
            
        self.linktypes = ','.join(types)
        
        cursor.execute('select b.route, l.id from links l join bus_route_link b on l.id = b.link;')
        
        self.busroutes={}
        for r in cursor:
            if not self.busroutes.has_key(r[0]):
                self.busroutes[r[0]] = []
            self.busroutes[r[0]].append(r[1])
        
        for r in self.busroutes:
            self.busroutes[r] = ','.join([str(l) for l in self.busroutes[r]])
            
        return

          
