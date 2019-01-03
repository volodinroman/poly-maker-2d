from PyQt5 import QtWidgets, QtGui, QtCore
from graphicsItems.bezierCP import BezierCP
from graphicsItems.bezierCurve import BezierCurve
from graphicsItems.bezierHull import BezierHull
from graphicsItems.bezierGrid import BezierGrid
from graphicsItems.delaunayTriangles import DelaunayTriangles
from graphicsItems.bezierPoints import BezierPoints
from graphicsItems.shadow import Shadow

import math2d
import random
import os
import copy
from matplotlib.tri import Triangulation

ROOT  = str(os.path.dirname(__file__))

class Scene(QtWidgets.QGraphicsScene):

    def __init__(self, parent = None):
        super(Scene, self).__init__()

        #bools 
        self._createItem = True
        self._showBezierCurve = True         #bezier curve
        self._showBezierHull = False         #bezier curve Hull
        self._showPerpSegments = False       #perpendicular lines segments
        self._showDelaunayTri = False        #Delaunay triangles
        self._showDelaunayPolygons = False   #Delauney colored polygons
        self._showBezierCurvePoints = False  #Bezier Curve points
        self._showShadow = False             #bottom shadow

        self._perpSegmentsNum = 1
        self._perpSegmentsLenght = 2

        #coords
        self._bezierCurveCoords = []        #the actual curve coordinates
        self._gridCoords = []               #perpendicular lines points coordinates
        self._gridLinesCoords = []          #perpendicular lines 
        self._gridJitter = []               #grid points jitter vectors

        #items
        self._bezierCurve = None            #the actual bezier curve
        self._bezierCPs = []                #bezier control points coordinates
        self._bezierHull = None             #bezier curve hull (a line that connects Control Points)
        self._bezierGrid= None              #Perpendicular dots (to which the jitter effect is applied)
        self._delaunayTriangles = None      #Delaunay triangles lines and polygons
        self._bezierCurvePoints = None      #the actual bezier curve points
        self._shadow = None                 #shadow under the LowPoly item (Y postion is always fixed)
         
        #options
        self.setSceneRect(0, 0, 1000, 800)


    def toggleShadow(self, vis = True):
        self._showShadow = vis
        self.buildPoly2d()

    def toggleBezierCurve(self, vis = True):
        self._showBezierCurve = vis
        self.buildPoly2d()

    def toggleBezierCP(self, vis = True):
        for i in self._bezierCPs:
            i.setVisible(vis)

        self.buildPoly2d()

    def toggleBezierHull(self, vis = True):
        self._showBezierHull = vis
        self.buildPoly2d()

    def togglePerpSegments(self, vis = True):
        self._showPerpSegments = vis
        self.buildPoly2d()

    def toggleDelaunayTri(self, vis = True):
        self._showDelaunayTri = vis
        self.buildPoly2d()

    def toggleDelaunayPolygons(self, vis = True):
        self._showDelaunayPolygons = vis
        self.buildPoly2d()

    def toggleBezierCurvePoints(self, vis = True):
        self._showBezierCurvePoints = vis
        self.buildPoly2d()

    def setSegmentsNum(self, num = 1):
        self._perpSegmentsNum = num
        self._gridJitter = []
        self.buildPoly2d()

    def setSegmentsLength(self, length = 5):
        self._perpSegmentsLenght = length
        self.buildPoly2d()

    def mouseReleaseEvent(self,event):
        """When we release mouse button over the scene canvas"""

        #if we have released left mouse button
        if event.button() == QtCore.Qt.LeftButton:

            if self._createItem:
   
                x = event.scenePos().x()
                y = event.scenePos().y()

                #create Bezier Control Point
                item  = BezierCP()
                self.addItem(item)

                #add Control Point to the list
                self._bezierCPs.append(item) 

                #move item to the mouse release position
                item.setPos(x,y)

                # create bezier curve and a grid when we get 4 CPs
                if len(self._bezierCPs) >= 4:
                    self.buildPoly2d()


        self.update()

        super(Scene, self).mouseReleaseEvent(event)

    def mousePressEvent(self,event):
        """When we press mouse button on the scene canvas"""

        if event.button() == QtCore.Qt.LeftButton:
            self._createItem = True

            if self.itemAt(event.scenePos(), QtGui.QTransform()):
                #if we pressed over an item
                self._createItem = False

            elif self.selectedItems():
                #if we already have items selected - then deselect
                self._createItem = False

        self.update()
        super(Scene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """when we move control points - recreate the curve and the grid"""

        if self.selectedItems():
            self.buildPoly2d()

        self.update()
        super(Scene,self).mouseMoveEvent(event)

    def buildPoly2d(self):
        """Build all graphics items step by step"""
        self.createHull()
        self.createBezier()
        self.createGrid()
        self.createDelaunayTri()
        self.drawShadow()
        self.update()

    def createHull(self):
        """Create/Update bezier curve hull"""

        CPCoords = []
        if self._bezierCPs:
            for i in self._bezierCPs:
                CPCoords.append([i.pos().x(), i.pos().y()]) 

        if not self._bezierHull:
            self._bezierHull = BezierHull(CPs = CPCoords, vis = self._showBezierHull)
            self.addItem(self._bezierHull)
        else:
            self._bezierHull.updateHull(CPs = CPCoords, vis = self._showBezierHull)

    def createBezier(self):
        """Calculate bezier curve segments and create the curve """
    
        if not self._bezierCPs:
            return 

        self._bezierCurveCoords = []

        # bezier Control Points coordinates
        CPCoords = [] #[ [x,y], [x,y], [x,y]]

        # get Control Points coordinates
        for i in self._bezierCPs:
            CPCoords.append([i.pos().x(), i.pos().y()]) 

        # get Curve Points coordinates
        for p in math2d.bezierCurve(20, CPCoords):
            self._bezierCurveCoords.append([p[0], p[1]])


        if not self._bezierCurvePoints:
            self._bezierCurvePoints = BezierPoints(points = self._bezierCurveCoords, vis = self._showBezierCurvePoints)
            self.addItem(self._bezierCurvePoints)
        else:
            self._bezierCurvePoints.updateCurve(points = self._bezierCurveCoords, vis = self._showBezierCurvePoints)
            

        # create Bezier Item and add it to the Scene
        if not self._bezierCurve:
            self._bezierCurve = BezierCurve(bezierCoords = self._bezierCurveCoords, vis = self._showBezierCurve)
            self.addItem(self._bezierCurve)
        else:
            self._bezierCurve.updateCurve(coords = self._bezierCurveCoords, vis = self._showBezierCurve)

    def gridJitter(self, offset = 0):
        """Calculate jitter effect for existing grid points"""
        
        self._gridJitter = []

        if self._gridCoords:
            for i in range(0, len(self._gridCoords)): #[x, y]

                if offset > 0:
                    randomVector = [random.uniform(-1 * offset, offset), random.uniform(-1 * offset, offset), 0]

                    unitVector = math2d.vectorNormalized(vector = randomVector)

                    offsetVector = [unitVector[0] * random.randint(0, offset), unitVector[1] * random.randint(0, offset)]

                    self._gridJitter.append(offsetVector)
                else:
                    self._gridJitter.append([0,0])

        self.buildPoly2d()

    def drawShadow(self):
        """Draws shadow item under the LowPoly Item. Shadow Y pos is fixed"""

        #image load
        imagePath = os.path.join(ROOT, "res", "shadow.png")
        pixmap = QtGui.QPixmap(imagePath)

        if not self._gridCoords:
            return

        #Delaunay triangles
        _x = []
        _y = []

        for i in self._gridCoords:
            _x.append(i[0])
            _y.append(i[1])

        xmin = min(_x)
        xmax = max(_x)
        ymin = min(_y)
        ymax = max(_y)
        width = int(xmax - xmin)
        height = int(ymax - ymin)
        
        pixmap = pixmap.scaled(width + 200, 20, QtCore.Qt.IgnoreAspectRatio)
        
        if not self._shadow:
            self._shadow = Shadow(pixmap = pixmap, vis = self._showShadow)
            self.addItem(self._shadow)
            self._shadow.setPos(xmin - 100, 300)
        else:
            self._shadow.updateShadow(pixmap = pixmap, vis = self._showShadow)
            self._shadow.setPos(xmin - 100, 300)

    def createGrid(self, segments = 10, length = 7):
        """Calculate perpendicular lines per each bazier curve point"""

        #if we still don't have Bezier curve coordinates calculated
        if not self._bezierCurveCoords:
            return

        self._gridCoords = []               #perpendicular lines points coordinates
        self._gridLinesCoords = []          #perpendicular lines 

        _bezierPointsNum = len(self._bezierCurveCoords)

        self._gridCoords.extend(self._bezierCurveCoords.copy()) #add all bezier curve coords

        self._gridCoords = copy.deepcopy(self._bezierCurveCoords)

        for direct in [-1,1]:

            prevCoord = self._bezierCurveCoords[0]

            for i in range(1, len(self._bezierCurveCoords) - 1): # for all bezier points between 0 and N

                currentCoord = self._bezierCurveCoords[i]

                vectorA = [currentCoord[0] - prevCoord[0], currentCoord[1] - prevCoord[1], 0] #Bezier curve segment vector
                vectorZ = [0,0,direct] # Depth vector

                #get vector cross product
                vectorCross = math2d.cross3D(a = vectorA, b = vectorZ)

                #normalize vector
                vectorUnit = math2d.vectorNormalized(vector = vectorCross)

                #for each chunk segment calculate coord
                chunkStart = [currentCoord[0], currentCoord[1]] #where we start

                for j in range(0, self._perpSegmentsNum):

                    #line end coord
                    #applies extra offdes depending on how close the line to the mid of the bezier curve
                    offset = _bezierPointsNum/2 - abs(_bezierPointsNum/2 - i)
                    # offset = 1
                    endCoordIncremented = j+1
                    # jitter_x = random.randint(0,30)
                    # jitter_y = random.randint(0,30)
                    chunkEnd = [currentCoord[0] + vectorUnit[0] * self._perpSegmentsLenght * endCoordIncremented * offset, 
                                currentCoord[1] + vectorUnit[1] * self._perpSegmentsLenght * endCoordIncremented * offset]

                    self._gridCoords.append([chunkEnd[0], chunkEnd[1]])

                    #update chunk start
                    chunkStart = [chunkEnd[0], chunkEnd[1]]

                prevCoord = currentCoord

        # generate jitter effect just once
        if not self._gridJitter:
            self.gridJitter()
            
        for i in range(0, len(self._gridCoords)):
            self._gridCoords[i][0] += self._gridJitter[i][0]
            self._gridCoords[i][1] += self._gridJitter[i][1]

        #generate grid points items
        if not self._bezierGrid:
            self._bezierGrid = BezierGrid(points = self._gridCoords, vis = self._showPerpSegments)
            self.addItem(self._bezierGrid)
        else:
            self._bezierGrid.updateGrid(points = self._gridCoords, vis = self._showPerpSegments)

    def createDelaunayTri(self):
        """Do Delauney triangulation for the grid points"""

        #image load
        imagePath = os.path.join(ROOT, "res", "color_01.jpg")
        pixmap = QtGui.QPixmap(imagePath)

        if not self._gridCoords:
            return

        #Delaunay triangles
        _x = []
        _y = []

        for i in self._gridCoords:
            _x.append(i[0])
            _y.append(i[1])

        xmin = min(_x)
        xmax = max(_x)
        ymin = min(_y)
        ymax = max(_y)
        width = int(xmax - xmin)
        height = int(ymax - ymin)
        
        pixmap = pixmap.scaled(width, height, QtCore.Qt.IgnoreAspectRatio)
        
        image = pixmap.toImage()

        tri = Triangulation(_x, _y)

        if not self._delaunayTriangles:
            self._delaunayTriangles = DelaunayTriangles(points = self._gridCoords, triangles = tri.triangles, image = image, sizes = [xmin, xmax, ymin, ymax], drawLines=self._showDelaunayTri, drawPoly=self._showDelaunayPolygons)
            self.addItem(self._delaunayTriangles)
        else:
            self._delaunayTriangles.updateTriangles(points = self._gridCoords, triangles = tri.triangles, image = image, sizes = [xmin, xmax, ymin, ymax], drawLines=self._showDelaunayTri, drawPoly=self._showDelaunayPolygons)
             
    def cleanUp(self):
        """ cleanUp the scene """

        self.clear()

        #coords
        self._bezierCurveCoords = []        #the actual curve coordinates
        self._gridCoords = []               #perpendicular lines points coordinates
        self._gridLinesCoords = []          #perpendicular lines 
        self._gridJitter = []                #grid points jitter vectors

        #items
        self._bezierCurve = None
        self._bezierCPs = []                #bezier control points coordinates
        self._bezierHull = None
        self._bezierGrid= None
        self._delaunayTriangles = None
        self._bezierCurvePoints = None
        self._shadow = None

        self.update()


        


