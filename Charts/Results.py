#--------------------
# /results/Results.py
# Carlos I. Balderas
# +
# Aaron E. Balderas
#--------------------
import psycopg2
#from TDD import *
import time
DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)

def login(h, u, p, d):
    """Logs into database and returns a cursor"""
    a = psycopg2.connect(host=h, user=u, password=p, database=d)
    c = a.cursor()
    assert str(type(c)) == "<type 'psycopg2._psycopg.cursor'>"
    return c

def getNetworks(c):
    """Returns table of networks(databases) avalilible"""
    query = "SELECT datname FROM pg_database;"
    c.execute(query)
    networks = []
    assert c is not None
    for row in c:
        networks.append(row)
    return networks

def getReqs(cur, tname, rtype):
    c = cur
    query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE\
             table_name='%s'); " % (tname)
    c.execute(query)
    try:
        assert c.fetchone()[0] is True
    except:
        raise RuntimeError("table %s is not in the database") % (tname)

    query = "SELECT count(*) FROM %s" % (tname)
    c.execute(query)
    try:
        assert c.fetchone()[0] != 0
    except:
        raise RuntimeError("table %s is empty") % (tname)

    query = ("SELECT exists (SELECT 1 FROM pg_type WHERE typname = '%s');" %
             (rtype))
    c.execute(query)
    try:
        assert c.fetchone()[0] is True
    except:
        raise RuntimeError("type %s does not exist in the database") % (rtype)

def getODTimes(cur, n, origins, destinations):
    c = cur
    query = "Select origin,dest,avg(sim_exittime-sim_departure)/60 from\
             vehicle_path_time a, vehicle_path b where b.id=a.sim_path and\
             sim_departure>3600 and sim_departure<=8100 group by origin, dest;"
    c.execute(query)
    try:
        origins = [int(item) for item in (origins.split(','))]
        destinations = [int(item) for item in (destinations.split(','))]
        odPairs = zip(origins, destinations)
    except:
        pass # user put in a single route?
    times = []
    queryData = {}
    for triple in c:
        for i in xrange(len(origins)):
            if (triple[0] == odPairs[i][0]) and (triple[1] == odPairs[i][1]):
                queryData[str(odPairs[i])] = triple[2]
    try:
        assert(c.fetchone is not None and len(queryData) > 0)
    except:
        raise RuntimeError("This query did not work")
    return {'data': queryData, 'networkName': n}

def getDistance(cur, n, routes):
    """
    Will get results in tuple form: (ID, distance).
    Function returns distance.
    """
    c = cur
    # what are 7200 and 8100 for? currently hard-coded? --> str mod
    query = "select distinct (route), sum(length/5280*(c.flow-d.flow))\
             from bus_route_link a, linkdetails b,links_flow_out (8100) c,\
             links_flow_out(7200) d where c.linkid=d.linkid and c.linkid=b.id\
             and b.id=a.link group by route;"
    c.execute(query)
    routes = str(routes) # refactor --> faster way to do this
    try:
        routes = [int(item) for item in (routes.split(','))]
    except:
        pass # user put in a single route?
    print 'routes: ', routes
    print
    #queryData = [tup for tup in c if (tup[0] in routes) or (tup[0] == routes)]
    # try to refactor into dict comprehension below
    queryData = {}
    for tup in c:
        if tup[0] in routes or tup[0] == routes:
            queryData['%i'%(tup[0])] = tup[1]
    print 'queryData: ', queryData
    print
    # modify the following test case, might split into two different tests
    try:
        assert(c.fetchone is not None and len(queryData) > 0)
    except:
        raise RuntimeError("This query did not work")
    return {'data': queryData, 'networkName': n}

def getCorridorTimes(cur, n, s, e):
    """
    Will store results in type { id: [name, field_tt, model_time, err_min,\
    err_perc, starttime, endtime] }
    """
    c = cur
    query = "SELECT * FROM compare_t_times(%i, %i);" % (s, e)
    c.execute(query)
    try:
        assert c.fetchone is not None
    except:
        raise RuntimeError("This query did not work")
    results = {}
    names = ["id", "name", "field_time", "model_time",
             "error_minutes", "error_percentage", "start", "end"]
    for row in c:
        temp = {}
        i = 0
        for item in row:
            temp[names[i]] = item
            i += 1
        results[temp['id']] = temp
    return {'data': results, 'networkName': n}

def mapLinkSubset(link_map, links):
    mapped_links = []
    for link in links:
        mapped_links.append(operator.indexOf(link_map, link))
    return mapped_links

def unmap(link_map, link):
    return link_map[link]

def getVolumeData(links, tddld, tddDataList):
    data = {}
    for link in links:
        temp = {}
        count = 0
        for subset in tddDataList:
            temp[count] = subset[link]
            count += 1

        data[unmap(tddld, link)] = temp
    return data

def getFlow(cur, l, s, e):
    c = cur
    query = ("SELECT flow FROM link_flow_out(%i) WHERE timestep IN (%i, %i);" %
             (l, s, e))
    c.execute(query)
    results = c.fetchall()
    return results[1][0] - results[0][0]

def compVolume(cur, cb, n, s, e, links):
    c = cur
    query = "SELECT * FROM link_volume_data WHERE from_sec = %i AND\
             to_sec = %i;" % (s, e)
    c.execute(query)
    try:
        assert c.fetchone is not None
    except:
        raise RuntimeError("Query did not work")
    results = {}
    names = ["id", "from", "to", "count", "flow"]
    for row in c:
        if row[0] not in links:
            continue
        flow = getFlow(cb, row[0], s, e)
        temp = {}
        i = 0
        for item in row:
            temp[names[i]] = item
            i += 1
        temp[names[i]] = flow
        results[temp['id']] = temp
    return {'data': results, 'networkName': n}