"""
To test the program:
    python TestResults.py >& TestResults.py.out
"""
import unittest
from Results import *
from TurnMove import *
import profile

class TestResults (unittest.TestCase):
    #def setUp(self):
    #    self.moveone = movement('123', '456')
    #    self.movetwo = movement('134', '467')
    #    self.movethree = movement('220', '060')
    #    self.movemapOne = movemap()
    #    self.movemapTwo = movemap()
    #    self.simvat = '../NMCharts/sim.vat'
    #
    #def testCounts(self):
    #    pass
    #
    #def testLinks(self):
    #    self.assertEquals(['123','456'], self.moveone.getLinks())
    #    self.assertEquals(['134','467'], self.movetwo.getLinks())
    #
    #def testIds(self):
    #    self.assertEquals(123456, self.moveone.mID)
    #    self.assertEquals(134467, self.movetwo.mID)
    #    self.assertEquals(220060, self.movethree.mID)
    #
    #def testMoveMap(self):
    #    self.assertEquals(False, self.movemapOne.hasMovement(134467))
    #    self.movemapOne.add(self.movetwo)
    #    self.assertEquals(True, self.movemapOne.hasMovement(134467))
    #    self.assertEquals(1, self.movetwo.getCount())
    #    self.movemapOne.add(self.movetwo)
    #    self.assertEquals(2, self.movetwo.getCount())

    #def testLoadfile(self):
    #    self.movemapTwo = movemap()
    #    self.movemapTwo = loadfile(self.simvat, self.movemapTwo)
    #    self.assertEquals(True, self.movemapTwo.hasMovement(4250176275))
    #    self.assertEquals(True, self.movemapTwo.hasMovement(627518421))
    #    self.assertEquals(True, self.movemapTwo.hasMovement(590218538))
    #    self.assertEquals(1857, self.movemapTwo.movements[590218538].getCount())
    #    self.assertEquals(2404, self.movemapTwo.movements[4250176275].getCount())
    #    self.assertEquals(2070, self.movemapTwo.movements[627518421].getCount())

    #def testTurns(self):
    #    self.simvat = '../Charts/sim.vat' # currently local?
    #    self.movemapTwo = movemap()
    #    network = 'coacongress_current_apr2013_am'
    #    c = login('nmc-compute1.ctr.utexas.edu', 'coacongress',
    #              'coacongress00', network)
    #    self.movemapTwo = loadfile(self.simvat, self.movemapTwo)
    #    # TEST 1
    #    moves = self.movemapTwo.movesFromLink(6275)
    #    print "Moves from link 6275: ", moves
    #    setDirection(moves[0], c)
    #    setDirection(moves[1], c)
    #    self.assertEquals("through", moves[0].direction)
    #    self.assertEquals("left", moves[1].direction)
    #
    #    # TEST 2
    #    moves = self.movemapTwo.movesFromLink(105239)
    #    print "Moves from link 105239: ", moves
    #    for x in moves:
    #        setDirection(x, c)
    #    self.assertEquals("left", moves[0].direction)
    #    self.assertEquals("right", moves[1].direction)
    #
    #    # TEST 3
    #    moves = self.movemapTwo.movesFromLink(6233)
    #    print "Moves from link 6233: ", moves
    #    for x in moves:
    #        setDirection(x, c)
    #    # id.6233: should have 3 movements: left, through, right
    #    self.assertEquals("left", moves[0].direction) # left onto id.106214
    #    self.assertEquals("through", moves[1].direction) # through onto id.6211
    #    self.assertEquals("right", moves[2].direction) # right onto id.6212
    #
    #    # TEST 4
    #    moves = self.movemapTwo.movesFromLink(5312)
    #    print "Moves from link 5312: ", moves
    #    for x in moves:
    #        setDirection(x, c)
    #    # id.5312 should have 2 movements: through, right
    #    self.assertEquals("through", moves[0].direction) # through onto id.5311
    #    self.assertEquals("right", moves[1].direction) # right onto id.114713
    #
    #    # TEST 5
    #    moves = self.movemapTwo.movesFromLink(104888)
    #    print "Moves from link 104888: ", moves
    #    for x in moves:
    #        setDirection(x, c)
    #    # id.104888 should have 2 movements: right, through
    #    self.assertEquals("right", moves[0].direction) # through onto id.4787
    #    self.assertEquals("through", moves[1].direction) # right onto id.104607
    #    c.close()


    #def test_login1(self):
    #    c = login('nmc-compute2.ctr.utexas.edu', 'vista', 'vista00', 'vista_calibration_tuneup')
    #    c.close()
    #
    #def test_login2(self):
    #    c = login('nmc-compute1.ctr.utexas.edu', 'vista', 'vista00', 'vista_austinsub_v3')
    #    c.close()
    #
    #def test_getNetwork(self):
    #    c = login('nmc-compute2.ctr.utexas.edu', 'vista', 'vista00', 'vista_calibration_tuneup')
    #    networks = getNetworks(c)
    #    self.assert_(networks != None)
    #    c.close()
    #
    #def test_getCountReqs(self):
    #    raised = False
    #    c = login('nmc-compute2.ctr.utexas.edu', 'vista', 'vista00', 'vista_calibration_tuneup')
    #    try:
    #        getReqs(c)
    #    except:
    #        raised = True
    #    c.close()
    #    self.assertFalse(raised, "Requirements not met")
    #
    #def test_getCountReqs(self):
    #    """vista_austinmopac does not have a count_data table currently, will raise error."""
    #
    #    raised = True
    #    c = login('nmc-compute2.ctr.utexas.edu', 'vista', 'vista00', 'vista_austinmopac')
    #    try:
    #        getReqs(c)
    #    except:
    #        raised = False
    #    c.close()
    #    self.assertFalse(raised, 'Requirements not met')
    #
    #def test_getReqs(self):
    #    raised = False
    #    c = login('nmc-compute2.ctr.utexas.edu', 'vista', 'vista00', 'vista_calibration_tuneup')
    #    try:
    #        getReqs(c, 'count_data', 'traveltime_return')
    #    except:
    #        raised = True
    #        c.close()
    #        self.assertFalse(raised, "Requirements not met")
    #
    #def testTravelDistances(self):
    #    epsilon = 0.00000001
    #    c = login('nmc-compute2.ctr.utexas.edu', 'sh45', 'sh4500', 'sh45_calibration_tuneup')
    #    # TEST 1
    #    distances = getDistance(c, 'sh45_calibration_tuneup', '9015,9016,9167,109146')
    #    self.assert_(distances != None and type(distances) == dict)
    #    self.assert_(abs(distances['data']['9015'] - 1613.23985783) < epsilon)
    #    print "Distance of ID.9015: ", distances['data']['9015']
    #    self.assert_(abs(distances['data']['9016'] - 758.784548193) < epsilon)
    #    print "Distance of ID.9016: ", distances['data']['9016']
    #    self.assert_(abs(distances['data']['109146'] - 648.53999298) < epsilon)
    #    print "Distance of ID.109146: ", distances['data']['109146']
    #    self.assert_(abs(distances['data']['9167'] - 467.530004351) < epsilon)
    #    print "Distance of ID.9167: ", distances['data']['9167']
    #    print "****************************************************************"
    #    # TEST 2
    #    distances = getDistance(c, 'sh45_calibration_tuneup', '9016')
    #    self.assert_(distances != None and type(distances) == dict)
    #    self.assert_(abs(distances['data']['9016'] - 758.784548193) < epsilon)
    #    print "Distance of ID.9016: ", distances['data']['9016']
    #    print "****************************************************************"
    #    # TEST 3
    #    distances = getDistance(c, 'sh45_calibration_tuneup', '9105,109146')
    #    self.assert_(distances != None and type(distances) == dict)
    #    self.assert_(abs(distances['data']['9105'] - 2070.36412406) < epsilon)
    #    print "Distance of ID.9105: ", distances['data']['9105']
    #    self.assert_(abs(distances['data']['109146'] - 648.53999298) < epsilon)
    #    print "Distance of ID.109146: ", distances['data']['109146']

    def testODTimes(self):
        #print 'TESTING getODTimes() IN Results.py...'
        epsilon = 0.00000001
        c = login('nmc-compute2.ctr.utexas.edu',
                  'sh45', 'sh4500', 'sh45_calibration_tuneup')
        # TEST 1
        #print "TEST 1..."
        timeData = getODTimes(c, 'sh45_calibration_tuneup',
                                 '124618,124618,100542',
                                 '200084,200085,201087')
        self.assert_(timeData != None and type(timeData) == dict)
        self.assert_(timeData['networkName'] == 'sh45_calibration_tuneup')
        self.assert_(abs(timeData['data']['(124618,200085)'] -
                         9.64649122807) < epsilon)
        self.assert_(abs(timeData['data']['(124618,200084)'] - 7.8) < epsilon)
        self.assert_(abs(timeData['data']['(100542,201087)'] - 9.85) < epsilon)
        #print "...TEST 1 PASSED."
        ## TEST 2
        #print "TEST 2..."
        timeData = getODTimes(c, 'sh45_calibration_tuneup',
                                 '124618,124618,100057,124618,100057,100063',
                                 '200074,200077,200099,200088,200101,200099')
        self.assert_(timeData != None and type(timeData) == dict)
        self.assert_(timeData['networkName'] == 'sh45_calibration_tuneup')
        self.assert_(abs(timeData['data']['(124618,200074)'] -
                                           11.162745098) < epsilon)
        self.assert_(abs(timeData['data']['(124618,200077)'] - 11.05) < epsilon)
        self.assert_(abs(timeData['data']['(100057,200099)'] -
                                           12.403333333) < epsilon)
        self.assert_(abs(timeData['data']['(124618,200088)'] -
                                           9.5111111111) < epsilon)
        self.assert_(abs(timeData['data']['(100057,200101)'] -
                                           16.233333333) < epsilon)
        self.assert_(abs(timeData['data']['(100063,200099)'] -
                                           14.583333333) < epsilon)
        #print "...TEST 2 PASSED."
        ## TEST 3
        #print "TEST 3..."
        timeData = getODTimes(c, 'sh45_calibration_tuneup', '124618', '200077')
        self.assert_(timeData != None and type(timeData) == dict)
        self.assert_(timeData['networkName'] == 'sh45_calibration_tuneup')
        self.assert_(abs(timeData['data'][(124618,200077)] - 11.05) < epsilon)
        #print "...TEST 3 PASSED."
        #print '\ngetODTimes() PASSED ALL TESTS.'


    #def test_compareCorridorTimes(self):
    #    c = login('nmc-compute2.ctr.utexas.edu', 'vista', 'vista00', 'vista_calibration_tuneup')
    #    times = getCorridorTimes(c,'vista_calibration_tuneup', 0, 900)
    #    c.close()
    #    self.assert_(times != None)


    #def test_mapLinkSubset(self):
    #    datadir = '/Users/Carlos/CTR/nmc_results_module/NMCharts/NMCharts/data/'
    #    tdd = TDD.load(datadir + 'Volume.tdd', datadir + 'LinkIndex')
    #    testlinks = [114693, 18560, 118289, 12086]
    #    links = mapLinkSubset(tdd.linkids, testlinks)
    #    self.assert_(links == [947,646,1109,254])
    #
    #def test_mapLinkSubset2(self):
    #    datadir = '/Users/Carlos/CTR/nmc_results_module/NMCharts/NMCharts/data/'
    #    tdd = TDD.load(datadir + "V_Over_C.tdd", datadir + "LinkIndex")
    #    testlinks = [1356,15776,205222]
    #    links = mapLinkSubset(tdd.linkids, testlinks)
    #    self.assert_(links == [0, 313, 1260])
    #
    #def test_getVolumeData(self):
    #    datadir = '/Users/Carlos/CTR/nmc_results_module/NMCharts/NMCharts/data/'
    #    tdd = TDD.load(datadir + 'Volume.tdd', datadir + 'LinkIndex')
    #    testlinks = [12086]
    #    links = mapLinkSubset(tdd.linkids, testlinks)
    #    data = getVolumeData(links, tdd.linkids, tdd.data.tolist())
    #    test = {12086: {0: 28, 1: 64, 2: 69, 3: 55, 4: 32, 5: 45, 6: 34, 7: 36, 8: 37,
    #                  9: 8, 10: 3, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0}}
    #    self.assert_(data == test)
    #
    #def test_getVolumeData2(self):
    #    datadir = '/Users/Carlos/CTR/nmc_results_module/NMCharts/NMCharts/data/'
    #    tdd = TDD.load(datadir + 'Volume.tdd', datadir + 'LinkIndex')
    #    testlinks = [1356]
    #    links = mapLinkSubset(tdd.linkids, testlinks)
    #    data = getVolumeData(links, tdd.linkids, tdd.data.tolist())
    #    #print data
    #    test = {1356: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
    #                   11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0}}
    #    pass
    #
    #def test_unmap(self):
    #    datadir = '/Users/Carlos/CTR/nmc_results_module/NMCharts/NMCharts/data/'
    #    tdd = TDD.load(datadir + 'Volume.tdd', datadir + 'LinkIndex')
    #    testlinks = [947, 646, 1109, 254]
    #    links = unmap(tdd.linkids, 947)
    #    self.assert_(links == 114693)
    #
    #def test_getFlow(self):
    #    c = login('nmc-compute1.ctr.utexas.edu', 'coacongress', 'coacongress00', 'coacongress_current_apr2013_am')
    #    flow = getFlow(c, 114516, 5400, 6300)
    #    c.close()
    #    self.assert_(flow == 84)
    #
    #def test_getFlow2(self):
    #    c = login('nmc-compute1.ctr.utexas.edu', 'coacongress', 'coacongress00', 'coacongress_current_apr2013_am')
    #    flow = getFlow(c, 104906, 1800, 6300)
    #    c.close()
    #    self.assert_(flow == 699)
    #

    # this test runs REALLY slowly --> check compVolume() in Results.py
    #def test_compVolume(self):
    #    print "starting test_compVolume(). Computing..."
    #    c = login('nmc-compute1.ctr.utexas.edu', 'coacongress', 'coacongress00', 'coacongress_current_apr2013_am')
    #    cb = login('nmc-compute1.ctr.utexas.edu', 'coacongress', 'coacongress00', 'coacongress_current_apr2013_am')
    #    results = compVolume(c,cb,  'coacongress_current_apr2013_am', 5400, 6300, [105220, 18184, 105210, 105173])
    #    c.close()
    #    cb.close()
    #    print "...information accessed!"
    #    self.assert_(results == {'data': {18184: {'count': 163.0, 'to': 6300, 'flow': 192, 'from': 5400, 'id': 18184},
    #                                      105210: {'count': 159.0, 'to': 6300, 'flow': 131, 'from': 5400, 'id':105210},
    #                                      105220: {'count': 66.0, 'to': 6300, 'flow': 160, 'from': 5400, 'id': 105220},
    #                                      105173: {'count': 278.0, 'to': 6300, 'flow': 76, 'from': 5400, 'id': 105173}},
    #                             'networkName' : 'coacongress_current_apr2013_am'})
    #    print "complete!"

print "Running TestResults.py..."
print ""
print "************************************************************************"
print "************************************************************************"
print "************************************************************************"
print ""
unittest.main()
print "Done. Passed all Tests."