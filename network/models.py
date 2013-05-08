from django.db import models
import sys, psycopg2

Nodes = {}
Links = []

class Node():
    def __init__(self, nid, ntype, point, attrs):
        self.nid        = nid
        self.ntype      = ntype
        self.point      = point
        self.attributes = attrs
        
class Link():
    def __init__(self, lid, ltype, src, dst, path, attrs):
        self.lid        = lid
        self.src        = src
        self.dst        = dst
        self.ltype      = ltype
        self.path       = eval(path)
        self.attributes = attrs
        
class NetworkManager(models.Manager):
    def create_network(self,  host, user, password, database):
        n = self.create(host=host, user=user, password=password, database=database)
        return n

class Network(models.Model):
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
    linkattrs = ['lanes', 'capacity', 'speed', 'length']
    nodeattrs = []
    
    def __unicode__(self):
        return self.database
    
    def load(self):
        if self.loaded == False:
            self.loaded = True
            
            self.nodemap = {}
            self.nodes = []
            self.linkmap = {}
            self.links = []
            self.busroutes = []
            self.linktypes = ""
            self.nodetypes = ""
            self.busroutes = ""
            self. nodeattrs = []
            
            dbc = psycopg2.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = dbc.cursor()
            
            sql = 'select id, type, x, y'
            
            for n in self.nodeattrs:
                sql += (', %s' % n)
            
            sql += ' from nodes;'
            
            cursor.execute(sql)
            for node in cursor:
                self.nodemap[node[0]] = len(self.nodes)
                self.nodes.append(Node(node[0], node[1], [node[2], node[3]], node[4:]))
    
            cursor.execute('select distinct(type) from nodes;')
            types = []
            for t in cursor:
                types.append(str(t[0]))
                
            self.nodetypes = ','.join(types)
              
            sql = 'select d.id, d.type, d.source, d.destination, l.points'
            
            for l in self.linkattrs:
                sql += (', d.%s' % l)
                
            sql += ' from linkdetails d join links l on d.id = l.id;'
                    
            cursor.execute(sql)
            for link in cursor:
                self.linkmap[link[0]] = len(self.links)
                self.links.append(Link(link[0], link[1], self.nodemap[link[2]], self.nodemap[link[3]], link[4], link[5:]))
            
            cursor.execute('select distinct(d.type) from linkdetails d join links l on d.id = l.id;')
            types = []
            for t in cursor:
                types.append(str(t[0]))
                
            self.linktypes = ','.join(types)
            
            cursor.execute('select route, link from bus_route_link;')
            
            self.busroutes={}
            for r in cursor:
                if not self.busroutes.has_key(r[0]):
                    self.busroutes[r[0]] = []
                self.busroutes[r[0]].append(r[1])
            
            for r in self.busroutes:
                self.busroutes[r] = ','.join([str(l) for l in self.busroutes[r]])
                
        return

          
