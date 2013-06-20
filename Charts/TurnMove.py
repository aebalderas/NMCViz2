#--------------------
# /results/TurnMove.py
# Carlos I. Balderas
#--------------------
import psycopg2

DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)

class movement:
    def __init__(self, fromlink, tolink):
        self.fromlink = fromlink
        self.tolink = tolink
        self.count = 1
        self.mID = int(str(fromlink) + str(tolink))
        self.direction = None
        
    def __repr__(self):
        return str(self.mID)
       
    def addCount(self):
        self.count += 1
        
    def getCount(self):
        return self.count
        
    def getLinks(self):
        return [str(self.fromlink), str(self.tolink)]
        
    def getInfo(self):
        return {"id": self.mID, "from": self.fromlink, "to": self.tolink, "count": self.count, "direction": self.direction}
              
class movemap:
    def __init__(self):
        self.movements = {}
      
    def hasMovement(self, mID):
        if mID in self.movements:
            return True      
        return False
        
    def add(self, move):
        '''movements is a list of movement instances'''    
        try:
            self.movements[move.mID].count += 1
        except KeyError:
            self.movements[move.mID] = move
            
    def movesFromLink(self, fromlink):        
        moves = [self.movements[move] for move in self.movements if self.movements[move].fromlink == str(fromlink)]
        return moves
         
def formatPath(lpath):
    return [float(x.strip('[]()')) for x in lpath.split(',')]
     
def setDirection(movement, c):
    direction = None
    turn = None
    query = "SELECT points FROM links WHERE id = %s ;" % (movement.fromlink)
    c.execute(query)
    frompoints = str(c.fetchone()[0])
    query = "SELECT points FROM links WHERE id = %s ;" % (movement.tolink)
    c.execute(query)
    topoints = str(c.fetchone()[0])
    frompoints, topoints = formatPath(frompoints), formatPath(topoints)
    dx, dy = frompoints[2] - frompoints[0], frompoints[3] - frompoints[1]
    dx2, dy2 = topoints[2] - topoints[0], topoints[3] - topoints[1]
    if abs(dx) < abs(dy): 
        if dy < 0:
            direction = "south"
        else:
            direction = "north"
    elif dx < 0:
        direction = "west"
    else: 
        direction = "east"
        
    if abs(dx2) > abs(dy2) and direction == "north" or direction == "south":
        if direction == "north" and dx2 > 0:
            turn = "right"
        elif direction == "south" and dx2 < 0:
            turn = "right"
        else:
            turn = "left"
            
    elif abs(dx2) < abs(dy2) and direction == "east" or direction == "west":
        if direction == "west" and dy2 < 0:
            turn = "right"
        elif direction == "east" and dy2 > 0:
            turn = "right"
        else:
            turn = "left"
    else:
        turn = "through"
    movement.direction = turn 
                 
def loadfile(simvat, mmap):
    mmap = movemap() 
    with open(simvat, 'r') as f:
        while True:
            s = f.readline()
            t = f.readline()
            if not t:
                break
            l = s.split()
            m = t.split()   
            links = int(m[0]) - 1 
          
            for i in range(1, links*2, 2):
                mmap.add(movement(m[i], m[i+2]))
    return mmap


    
    

    



    
