# -*- coding:utf-8 -*- 
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_navigator import Ui_Dialog
from ui_catalogue import Ui_Dialog_Metadata
from ui_contacts import Ui_Dialog_Contact
from ui_options import Ui_Dialog_Options
from qsphere_tools import *
import os
import time


class MovieSplashScreen(QSplashScreen):
     def __init__(self, movie, parent = None):
         movie.jumpToFrame(0)
         pixmap = QPixmap(movie.frameRect().size())
        
         QSplashScreen.__init__(self, pixmap)
         self.movie = movie
         self.movie.frameChanged.connect(self.repaint)
     
     def showEvent(self, event): self.movie.start()
     def hideEvent(self, event): self.movie.stop()
     def sizeHint(self): return self.movie.scaledSize()
     
     def paintEvent(self, event):
         painter = QPainter(self)
         pixmap = self.movie.currentPixmap()
         self.setMask(pixmap.mask())
         painter.drawPixmap(0, 0, pixmap)
     
class DialogOptions(QDialog, Ui_Dialog_Options):
        def __init__(self, parent):
             QDialog.__init__(self)
             self.setObjectName("DialogOptions")
             self.setAccessibleName("DialogOptions")             
             
             icon = getThemeIcon("qsphereoptions.png")
             self.parent = parent
             MakeWindowIcon(self, icon)
             MakePropertiesForWindow(self, self.parent)
            
             self.setupUi()

class DialogContacts(QDialog, Ui_Dialog_Contact):
        def __init__(self, parent, IsNotSoloMode):
             QDialog.__init__(self)
             self.setObjectName("DialogContacts")
             self.setAccessibleName("DialogContacts")

             icon = getThemeIcon("contact.png")
             MakeWindowIcon(self, icon)
             MakePropertiesForWindow(self, parent)
             
             self.parent = parent
             self.notSoloMode = IsNotSoloMode
             self.setupUi()
             self.installEventFilter(self)

        def eventFilter(self, obj, event):
             if not event : return False
             if event == None : return False
             if event.type() == QEvent.WindowActivate : makeGetOptions(self)
             return QtGui.QDialog.eventFilter(self, obj, event)
          

def LoadDialogViewer(self, iface, zUrl, zCond, zEmprise, langueTR, parent, senderBut, icon, isModal):
    d = DialogViewer(iface, zUrl, zCond, zEmprise, self.langueTR, parent, senderBut, isModal)
    MakePropertiesForWindow(d, d.parent) #self avant!
    MakeWindowIcon(d, icon) 
    if not isModal :
        d.setModal(False)
        d.show()
        return d
    else : d.exec_()

class DialogViewer(QDialog, Ui_Dialog):
	def __init__(self, iface, zUrl, isXML, zEmprise, langueTR, parent, senderBut, isModal):
		QDialog.__init__(self)
		self.setObjectName("DialogViewer")
                self.setAccessibleName("DialogViewer")
		self.iface = iface
		self.langueTR = langueTR if langueTR in ("fr", "it", "fi", "es", "de") else "en"
		self.homeurl = zUrl                
		self.isXML = isXML
		self.emprise = zEmprise
		self.parent = parent
		self.senderBut = senderBut
		self.isModal = isModal
		self.setupUi()
		self.installEventFilter(self)


        def eventFilter(self, obj, event):
             if not event : return False
             if event == None : return False
             if event.type() == QEvent.WindowActivate : makeGetOptions(self)
             return QtGui.QDialog.eventFilter(self, obj, event)    
		
		
class DialogMetadata(QDialog, Ui_Dialog_Metadata):
	def __init__(self, iface, langue, languageIndex, langs, langsDico, langueTR, formats, listCodecs, \
                     listTemporalSystem, listTypeRessources, listCountries, indexCountry, listCountriesCode, \
                     localeFullName, parent):
                zMovie = getThemeIcon("animation.gif")
                zCond = os.path.exists(zMovie)
                if zCond :
                        movie = QMovie(zMovie)
                        splash = MovieSplashScreen(movie)
                        splash.show()
                        start = time.time()
                        while movie.state() == QMovie.Running and time.time() < start + 1: QApplication.processEvents()
                
                QDialog.__init__(self)
                self.setObjectName("DialogMetadata")
                self.setAccessibleName("DialogMetadata")
                MakePropertiesForWindow(self, parent)
                self.parent = parent
                self.isFromDownload = None
                self.indexLang = self.MainPlugin.indexLang
                self.setupUi()
                self.installEventFilter(self)

                if zCond : splash.finish(self)

             
        def eventFilter(self, obj, event):
             if not event : return False
             if event == None : return False
             if event.type() == QEvent.WindowActivate :
                 makeGetOptions(self)
                 if self.indexLang != self.MainPlugin.indexLang :
                    self.indexLang == self.MainPlugin.indexLang  
                    self.changeLang()
                 self.initBDownloadButton()

             if (event.type() == QEvent.KeyPress) :
                  if (event.key() == Qt.Key_F11) or (event.key() == Qt.Key_F12) :
                       if self.focusWidget().metaObject().className() in ("QTableWidget", "MyTableWidget"):
                          zRacAction = "Ajouter" if (event.key() == Qt.Key_F11) else "Effacer"     
                          zCommand = self.findChild(QAction,"%s_6_%s" % (zRacAction, self.focusWidget().objectName()))
                          if zCommand != None : zCommand.triggered.emit(True)
                 
             return QtGui.QDialog.eventFilter(self, obj, event)  
               
