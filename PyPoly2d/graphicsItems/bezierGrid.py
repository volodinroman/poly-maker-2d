from PyQt5 import QtWidgets, QtGui, QtCore

class BezierGrid(QtWidgets.QGraphicsLineItem):

    def __init__(self, points = [], vis = True):
        super(BezierGrid, self).__init__()

        self._points = points
        self.setVisible(vis)
        self.setZValue(10)

        

    def updateGrid(self, points = [], vis = True):

        self._points = points
        self.setVisible(vis)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):

        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0, 100)) #, QtCore.Qt.BrushStyle.SolidPattern)
        pen = QtGui.QPen((QtGui.QColor(255, 0, 0, 100)), 1, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(brush)

        for i in self._points:
            painter.drawEllipse(QtCore.QPointF(i[0], i[1]), 2, 2)

