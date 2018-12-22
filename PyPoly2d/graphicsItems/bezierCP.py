from PyQt5 import QtWidgets, QtGui, QtCore

class BezierCP(QtWidgets.QGraphicsItem):
    """Bezier curve Control Points"""

    def __init__(self):
        super(BezierCP, self).__init__()

        self.pen = QtGui.QPen(QtGui.QColor(10, 10, 10, 0), 2, QtCore.Qt.SolidLine)
        self.brush = QtGui.QBrush(QtGui.QColor(200, 10, 200, 255)) 
        self.brushSelected = QtGui.QBrush(QtGui.QColor(250, 250, 10, 255)) 

        self.setFlags(QtWidgets.QGraphicsItemGroup.ItemIsMovable | QtWidgets.QGraphicsItemGroup.ItemIsSelectable)
        self.setCacheMode(QtWidgets.QGraphicsItem.DeviceCoordinateCache)

        self.setZValue(20)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):

        painter.setPen(self.pen)

        if self.isSelected():
            painter.setBrush(self.brushSelected)
        else:
            painter.setBrush(self.brush)

        painter.drawRect(-4,-4,8,8)

    def boundingRect(self):
        return QtCore.QRectF(-4,-4,8,8)

    