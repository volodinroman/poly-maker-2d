from PyQt5 import QtWidgets, QtGui, QtCore

class BezierHull(QtWidgets.QGraphicsLineItem):

    def __init__(self, CPs = [], vis = True):
        super(BezierHull, self).__init__()

        self._CPs = CPs # [ [a,b], [b,c], [c,d] ... etc]

        self.pen_color = QtGui.QPen((QtGui.QColor(100, 100, 100, 150)), 1, QtCore.Qt.DashLine)
        self.setZValue(18)
        self.setVisible(vis)

    def updateHull(self, CPs = [], vis = True):
        self._CPs = CPs
        self.setVisible(vis)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):

        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        painter.setPen(self.pen_color)

        #start path with initial point
        self.path = QtGui.QPainterPath(QtCore.QPointF(self._CPs[0][0], self._CPs[0][1]))

        #add more points to the path
        for i in range(1, len(self._CPs)):
            self.path.lineTo(self._CPs[i][0], self._CPs[i][1])

        painter.drawPath(self.path)