from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
import sys
class axisWidget(QtWidgets.QWidget):
    """
    an axis controller widget
    """

    def __init__(self,*args,**kwargs):
        super(axisWidget,self).__init__(*args,**kwargs)
        layout = QtWidgets.QHBoxLayout()
        
        self.setLayout(layout)



if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    axis = axisWidget()
    axis.show()
    app.exec()