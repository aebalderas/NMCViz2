#--------------------
# /results/Results.py
# Carlos I. Balderas
#--------------------
import psycopg2
#from TDD import *

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
    query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='%s'); " % (tname)
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
     
    query = "SELECT exists (SELECT 1 FROM pg_type WHERE typname = '%s');" % (rtype)
    c.execute(query)
    try:
        assert c.fetchone()[0] is True
    except:
        raise RuntimeError("type %s does not exist in the database") % (rtype)

def getCorridorTimes(cur, n, s, e):
    "will store results in type { id: [name, field_tt, model_time, err_min, err_perc, starttime, endtime] }"
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
    query = "SELECT flow FROM link_flow_out(%i) WHERE timestep IN (%i, %i);" % (l, s, e)
    c.execute(query)
    results = c.fetchall()
    return results[1][0] - results[0][0]

def compVolume(cur, cb, n, s, e, links):
    c = cur
    query = "SELECT * FROM link_volume_data WHERE from_sec = %i AND to_sec = %i;" % (s, e)
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
