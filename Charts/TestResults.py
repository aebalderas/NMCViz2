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
        
    def testTurns(self):
        self.simvat = '../NMCharts/sim.vat'
        self.movemapTwo = movemap()
        network = 'coacongress_current_apr2013_am'
        c = login('nmc-compute1.ctr.utexas.edu', 'coacongress', 'coacongress00', network)
        self.movemapTwo = loadfile(self.simvat, self.movemapTwo)
        moves = self.movemapTwo.movesFromLink(6275)
        setDirection(moves[0], c)
        setDirection(moves[1], c)
        #self.assertEquals("through", moves[0].direction)
        self.assertEquals("left", moves[1].direction)
        moves = self.movemapTwo.movesFromLink(105239)
        for x in moves:
            setDirection(x, c)
        self.assertEquals("left", moves[0].direction)
        self.assertEquals("right", moves[1].direction)
        c.close()
     
       
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
    def test_compareCorridorTimes(self):
        c = login('nmc-compute2.ctr.utexas.edu', 'vista', 'vista00', 'vista_calibration_tuneup')
        times = getCorridorTimes(c,'vista_calibration_tuneup', 0, 900)
        c.close()
        self.assert_(times != None)
        
        
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
    def test_compVolume(self):
        c = login('nmc-compute1.ctr.utexas.edu', 'coacongress', 'coacongress00', 'coacongress_current_apr2013_am')
        cb = login('nmc-compute1.ctr.utexas.edu', 'coacongress', 'coacongress00', 'coacongress_current_apr2013_am')
        results = compVolume(c,cb,  'coacongress_current_apr2013_am', 5400, 6300, [105220, 18184, 105210, 105173])
        c.close()
        cb.close()
        self.assert_(results == {'data': {18184: {'count': 163.0, 'to': 6300, 'flow': 192, 'from': 5400, 'id': 18184},              
                                          105210: {'count': 159.0, 'to': 6300, 'flow': 131, 'from': 5400, 'id':105210}, 
                                          105220: {'count': 66.0, 'to': 6300, 'flow': 160, 'from': 5400, 'id': 105220}, 
                                          105173: {'count': 278.0, 'to': 6300, 'flow': 76, 'from': 5400, 'id': 105173}}, 
                                 'networkName' : 'coacongress_current_apr2013_am'})


     
print "TestResults.py"
unittest.main()
print "Done."