 
from PyQt5 import QtWidgets, QtGui, QtCore

class Shadow(QtWidgets.QGraphicsPixmapItem):
    """Shadow Item"""

    def __init__(self, pixmap = None, vis = True):
        super(Shadow, self).__init__()

        self.pen_color = QtGui.QPen((QtGui.QColor(100, 100, 100, 150)), 1, QtCore.Qt.DashLine)
        self.setZValue(18)
        self.setVisible(vis)

        self._pixmap = pixmap
        if self._pixmap:
            self.setPixmap(self._pixmap)

    def updateShadow(self, pixmap = None, vis = True):

        self._pixmap = pixmap
        if self._pixmap:
            self.setPixmap(self._pixmap)

        self.setVisible(vis)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):

        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        painter.setPen(self.pen_color)

        painter.drawPixmap(QtCore.QPointF(0, 0), self._pixmap)

