from PyQt5 import QtWidgets, QtGui, QtCore

class BezierPoints(QtWidgets.QGraphicsLineItem):

    def __init__(self, points = [], vis = True):
        super(BezierPoints, self).__init__()

        self._points = points

        self.setVisible(vis)

        self.setZValue(19)

    def updateCurve(self, points = [], vis = True):

        self._points = points
        self.setVisible(vis)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):

        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0, 255)) #, QtCore.Qt.BrushStyle.SolidPattern)
        pen = QtGui.QPen((QtGui.QColor(255, 0, 0, 50)), 1, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(brush)

        for i in self._points:
            painter.drawEllipse(QtCore.QPointF(i[0], i[1]), 4, 4)