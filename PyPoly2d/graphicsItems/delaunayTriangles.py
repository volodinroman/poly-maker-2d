from PyQt5 import QtWidgets, QtGui, QtCore
import math2d

class DelaunayTriangles(QtWidgets.QGraphicsLineItem):

    def __init__(self, points = [], triangles = [], image = None, sizes = [],  drawLines = True, drawPoly = True):
        super(DelaunayTriangles, self).__init__()

        self._points = points
        self._triangles = triangles
        self._img = image
        self._sizes = sizes # xmin xmax ymin ymax
        self._drawLines = drawLines
        self._drawPoly = drawPoly
  
        self.setZValue(9)

    def updateTriangles(self, points = [], triangles = [], image = None, sizes = [],  drawLines = True, drawPoly = True):
        self._points = points
        self._triangles = triangles
        self._img = image
        self._sizes = sizes # xmin xmax ymin ymax
        self._drawLines = drawLines
        self._drawPoly = drawPoly




    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):

        for i in self._triangles:
            p0 = self._points[i[0]]
            p1 = self._points[i[1]]
            p2 = self._points[i[2]]

            d_p0p1 = math2d.vectorMagnitude([p1[0] - p0[0], p1[1] - p0[1], 0])
            d_p1p2 = math2d.vectorMagnitude([p2[0] - p1[0], p2[1] - p1[1], 0])
            d_p0p2 = math2d.vectorMagnitude([p2[0] - p0[0], p2[1] - p0[1], 0])

            maxDistance = max([d_p0p1, d_p1p2, d_p0p2])
            if maxDistance > 200:
                continue

            
            
            if self._drawLines:
                pen = QtGui.QPen((QtGui.QColor(0, 0, 0, 50)), 1, QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(QtCore.QLineF(p0[0], p0[1], p1[0], p1[1]))
                painter.drawLine(QtCore.QLineF(p1[0], p1[1], p2[0], p2[1]))
                painter.drawLine(QtCore.QLineF(p0[0], p0[1], p2[0], p2[1]))

            if self._drawPoly:
                centerx = (p0[0] + p1[0] + p2[0])/3
                centery = (p0[1] + p1[1] + p2[1])/3

                pixX = centerx - self._sizes[0]
                pixY = centery - self._sizes[2] 

                pixelColor = self._img.pixelColor(QtCore.QPoint(int(pixX), int(pixY)))

                brush = QtGui.QBrush(QtGui.QColor(pixelColor.red(), pixelColor.green(),pixelColor.blue(), 255)) 
                pen = QtGui.QPen((QtGui.QColor(pixelColor.red(), pixelColor.green(),pixelColor.blue(), 150)), 1, QtCore.Qt.SolidLine)
                painter.setBrush(brush)
                painter.setPen(pen)

                polygon = QtGui.QPolygon()
                QtPoint_1 = QtCore.QPoint(int(p0[0]), int(p0[1]))
                QtPoint_2 = QtCore.QPoint(int(p1[0]), int(p1[1]))
                QtPoint_3 = QtCore.QPoint(int(p2[0]), int(p2[1]))
                polygon.append(QtPoint_1)
                polygon.append(QtPoint_2)
                polygon.append(QtPoint_3)
                painter.drawPolygon(polygon)
