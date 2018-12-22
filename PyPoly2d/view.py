from PyQt5 import QtWidgets, QtGui, QtCore


class View(QtWidgets.QGraphicsView):
    
    def __init__(self):
        super(View, self).__init__()

        self.setObjectName("atom_graphicsView")

        #set the actual view size that we can scroll
        self.setSceneRect(-5000, -5000, 10000, 10000)

        #hide scrollbars
        self.setHorizontalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )
        self.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )

        #defines what will happen when we click-move Mouse Left Button
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag) #ScrollHandDrag

        #defines when items get selected when we drun our cursor over
        # IntersectsItemShape - if we touch the shape of the item with a RubberBand
        self.setRubberBandSelectionMode(QtCore.Qt.IntersectsItemShape)
        
        # set view's render options
        self.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.TextAntialiasing)
        
        self.setStyleSheet("border: no-focus;")
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(220, 220, 220, 255), QtCore.Qt.SolidPattern))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(sizePolicy)

    def mouseMoveEvent(self,event):

        # don't create any item (do RubberBand or Item Move)
        self.scene()._createItem = False # do rubberBand, don't create item 
        self.scene().update()
        super(View, self).mouseMoveEvent(event)

    # def wheelEvent(self,event):

    #     if event.delta() > 0: #PyQt4 specific thing. PyQt5 -> angleDelta()
    #         self.scale(1.1, 1.1)
    #     else:
    #         self.scale(0.90, 0.90)

