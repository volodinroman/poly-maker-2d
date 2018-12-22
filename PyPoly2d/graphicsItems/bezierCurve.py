from PyQt5 import QtWidgets, QtGui, QtCore

class BezierCurve(QtWidgets.QGraphicsLineItem):

    def __init__(self, bezierCoords = [], vis = True):
        super(BezierCurve, self).__init__()

        self._bezierCoords = bezierCoords # [ [a,b], [b,c], [c,d] ... etc]

        self.pen_color = QtGui.QPen((QtGui.QColor(100, 100, 100, 255)), 2, QtCore.Qt.DashLine)
        self.setZValue(10)
        self.setVisible(vis)

    def updateCurve(self, coords = [], vis = True):
        """Update """
        self._bezierCoords = coords
        self.setVisible(vis)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):

        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        painter.setPen(self.pen_color)

        #start path with initial point
        self.path = QtGui.QPainterPath(QtCore.QPointF(self._bezierCoords[0][0], self._bezierCoords[0][1]))

        #add more points to the path
        for i in range(1, len(self._bezierCoords)):
            self.path.lineTo(self._bezierCoords[i][0], self._bezierCoords[i][1])

        painter.drawPath(self.path)