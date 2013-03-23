import sys, psycopg2, pickle

a = psycopg2.connect(host='nmc-compute1.ctr.utexas.edu', user='vista', password='vista00', database='tacc_downtown_pm')
c = a.cursor()

nodes = []
c.execute("select id, type, x, y from nodes;")
for i in c:
  print "insert into network_nodes (nodeid, type, point) values (%d, %d, ST_GeomFromText('POINT(%f %f)', 4326));" % (i[0], i[1], i[2], i[3])

c.execute('select d.id, d.lanes, d.destination, d.source, d.type, d.capacity, d.speed, d.length, l.points from linkdetails d join links l on d.id = l.id;')
for i in c:
  j = eval(i[8])
  gstr = "ST_GeomFromText('LINESTRING(" + ','.join(["%f %f" % k for k in j]) + ")', 4326)"
  print "insert into network_links (linkid, lanes, source_id, destination_id, type, length, speed, capacity, path) values (%d, %d, %d, %d, %d, %f, %f, %f, %s);" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], gstr)


