from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from scene import Scene
from view import View

class PyPoly2D(QtWidgets.QMainWindow):
    """
    Core class with main UI components, view and a scene
    """

    def __init__(self):
        super(PyPoly2D, self).__init__()

        self.setupUI()

    def setupUI(self):
 
        #qmainwindow settings
        self.setMinimumSize(900,800)
        self.setObjectName("idPyPoly2D")
        self.setWindowTitle("PyPoly2D")

        #central widget
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        #central layout
        self.centralLayout = QtWidgets.QHBoxLayout()
        self.centralLayout.setContentsMargins(0,0,0,0)
        self.centralWidget.setLayout(self.centralLayout)

        #scene and view
        self.scene = Scene()
        self.view = View()
        self.view.setScene(self.scene) 
        self.centralLayout.addWidget(self.view)

        #scene options
        self.centralLayout.addWidget(self.rightPanelUI())

    def rightPanelUI(self):
        """Right panel with options"""
        self.slider_jitter = None

        mainWidget = QtWidgets.QWidget()
        mainWidget.setMinimumWidth(200)
        mainLayout = QtWidgets.QVBoxLayout() 
        mainLayout.setSpacing(20)
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainWidget.setLayout(mainLayout)

        cleanUpButton = QtWidgets.QPushButton("New Scene")
        cleanUpButton.clicked.connect(self.newScene)
        mainLayout.addWidget(cleanUpButton)

        # add segments num
        mainLayout.addLayout(self.addSegmentsNumControl())

        # add segments length
        mainLayout.addLayout(self.addSegmentsLengthControl())

        # add jitter
        mainLayout.addLayout(self.addJitterControl())

        #add visibility control
        mainLayout.addLayout(self.addVisibilityControl())

        return mainWidget

    def newScene(self):
        self.scene.cleanUp()
        if self.slider_jitter:
            self.slider_jitter.setValue(0)

    def addJitterControl(self):

        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Jitter effect")

        self.slider_jitter = QtWidgets.QSlider()
        self.slider_jitter.setMinimum(0)
        self.slider_jitter.setMaximum(50)
        self.slider_jitter.setValue(0)
        self.slider_jitter.setOrientation(QtCore.Qt.Horizontal)
        self.slider_jitter.valueChanged.connect(self.scene.gridJitter)

        layout.addWidget(label)
        layout.addWidget(self.slider_jitter)

        return layout

    def addSegmentsNumControl(self):

        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Segments Count")

        slider_num = QtWidgets.QSlider()
        slider_num.setMinimum(1)
        slider_num.setMaximum(10)
        slider_num.setValue(1)
        slider_num.setOrientation(QtCore.Qt.Horizontal)
        slider_num.valueChanged.connect(self.scene.setSegmentsNum)

        layout.addWidget(label)
        layout.addWidget(slider_num)

        return layout

    def addSegmentsLengthControl(self):

        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Segments length")

        slider_length = QtWidgets.QSlider()
        slider_length.setMinimum(2)
        slider_length.setMaximum(20)
        slider_length.setValue(2)
        slider_length.setOrientation(QtCore.Qt.Horizontal)
        slider_length.valueChanged.connect(self.scene.setSegmentsLength)

        layout.addWidget(label)
        layout.addWidget(slider_length)

        return layout

    def addVisibilityControl(self):

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(2)

        chbx_bezierCurve = QtWidgets.QCheckBox("Bezier Curve")
        chbx_bezierCurve.setChecked(1)
        chbx_bezierCurve.toggled.connect(self.scene.toggleBezierCurve)

        chbx_bezierHull = QtWidgets.QCheckBox("Bezier Hull")
        chbx_bezierHull.setChecked(0)
        chbx_bezierHull.toggled.connect(self.scene.toggleBezierHull)

        chbx_beizerSegments = QtWidgets.QCheckBox("Bezier Perp Segments")
        chbx_beizerSegments.setChecked(0)
        chbx_beizerSegments.toggled.connect(self.scene.togglePerpSegments)

        chbx_beizerPoints = QtWidgets.QCheckBox("Bezier Curve Points")
        chbx_beizerPoints.setChecked(0)
        chbx_beizerPoints.toggled.connect(self.scene.toggleBezierCurvePoints)

        chbx_delaunayTri = QtWidgets.QCheckBox("Delaunay Triangles")
        chbx_delaunayTri.setChecked(0)
        chbx_delaunayTri.toggled.connect(self.scene.toggleDelaunayTri)

        chbx_delaunayPolygons = QtWidgets.QCheckBox("Delaunay Polygons")
        chbx_delaunayPolygons.setChecked(0)
        chbx_delaunayPolygons.toggled.connect(self.scene.toggleDelaunayPolygons)

        chbx_shadow = QtWidgets.QCheckBox("Shadow")
        chbx_shadow.setChecked(0)
        chbx_shadow.toggled.connect(self.scene.toggleShadow)

        layout.addWidget(chbx_bezierCurve)
        layout.addWidget(chbx_beizerPoints)
        layout.addWidget(chbx_bezierHull)
        layout.addWidget(chbx_beizerSegments)
        layout.addWidget(chbx_delaunayTri)
        layout.addWidget(chbx_delaunayPolygons)
        layout.addWidget(chbx_shadow)

        return layout




def Main(*args, **kwargs):
    """entry point"""
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("appPyPoly2D")
    window = PyPoly2D()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    Main()