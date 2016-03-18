# -*- coding:utf-8 -*- 
import sys
import os

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import doUI
from qsphere_tools import *
from qsphere_objmaker import MyAction
from ui_editorXML import xmlEditor
import webbrowser

class MainPlugin(object):
  
  def __init__(self, iface):
    self.name = "qsphere"
    self._objectName = "qsphere"
    self.iface = iface
    self.MainPlugin = self

    overrideLocale = QSettings().value("locale/overrideFlag", False)
    localeFullName = QLocale.system().name() if not overrideLocale else QSettings().value("locale/userLocale", "")
    self.langueTR = localeFullName[0:2]
    self.localePath = "%s/i18n/qsphere_%s.qm" % (os.path.dirname(__file__), self.langueTR)
    self.localeFullName = localeFullName

    reload(sys)
    sys.setdefaultencoding('iso-8859-1') 

    self.languesDico = getisocodes_dict('ISO-639-2_utf-8.txt')
    self.langue, self.languageIndex = getUILangIndex(self)
    self.suffixeQSP = "qsp"
    self.suffixeXML = ("xml", "meta.xml") 

    self.dicoLangs = ("fr", "en", "it", "de", "es", "fi")
    self.indexLang = self.dicoLangs.index(self.langueTR) if self.langueTR in self.dicoLangs else 0
    self.toolBar = None
    self.translator = QTranslator()
    self.changeLang(False)

  def objectName(self): return self._objectName
  def changeLang(self, toReload):
        overrideLocale = QSettings().value("locale/overrideFlag", False)
        localeFullName = QLocale.system().name() if not overrideLocale else QSettings().value("locale/userLocale", "")
        self.localePath = "%s/i18n/qsphere_%s.qm" % (os.path.dirname(__file__), self.dicoLangs[self.indexLang])

        self.ListOfRules, self.DicoListOfRules = LoadData(self, "file:/ressources/roles_%s.csv" % (self.dicoLangs[self.indexLang]), "roles")

        if QFileInfo(self.localePath).exists():
             self.translator.load(self.localePath)
             QCoreApplication.installTranslator(self.translator)

        if toReload :
           self.toolBar.clear()
           self.iface.legendInterface().removeLegendLayerAction(self.metadataCtxtQSP)
           self.iface.legendInterface().removeLegendLayerAction(self.metadataCtxtXML)
           self.iface.legendInterface().removeLegendLayerAction(self.navigatorCtxt)
           self.initGui()


  def initGui(self):
    self.menu=QMenu("QSphere")
    self.menu.setObjectName("mQsphereMenu")

    self.barInfo = self.iface.messageBar()
    self.barInfo.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )
    self.barInfo.setGeometry(0, 0, self.iface.mapCanvas().width()-10, 60)
    

    try: self.QgisVersion =  QGis.QGIS_VERSION_INT 
    except: self.QgisVersion = QGis.qgisVersion[0]

    if self.toolBar == None :
      if self.QgisVersion < 20400 :
         self.toolBar = self.iface.addToolBar("QSphere")
      else :
         self.toolBar = QToolBar("QSphere")
         self.iface.addToolBar(self.toolBar)
      self.toolBar.setObjectName("mQsphereToolBar")   

    menuIcon = getThemeIcon("qsp.png")
    self.metadata = MyAction("mActionMetadata", QApplication.translate("QSphere","Create metadata ...", None, QApplication.UnicodeUTF8), menuIcon, self.iface.mainWindow())
    self.metadata.setShortcut(QKeySequence("Ctrl+M"))
    self.metadataCtxtQSP = MyAction("mActionMetadataCtxtQSP", QApplication.translate("QSphere","Edit QSphere project", None, QApplication.UnicodeUTF8), menuIcon, self.iface.mainWindow())
    self.metadataCtxtXML = MyAction("mActionMetadataCtxtXML", QApplication.translate("QSphere","Edit XML ISO Metadata", None, QApplication.UnicodeUTF8), menuIcon, self.iface.mainWindow())
    menuIcon = getThemeIcon("viewhtml.png")
    self.navigatorCtxt = MyAction("mActionNavigatorCtxt", QApplication.translate("QSphere","View metadata in HTML", None, QApplication.UnicodeUTF8), menuIcon, self.iface.mainWindow())

    self.navigator = MyAction("mActionNavigator", QApplication.translate("QSphere","Web navigator ...", None, QApplication.UnicodeUTF8), getThemeIcon("navigatorweb.png"), self.iface.mainWindow())
    self.navigator.setShortcut(QKeySequence("Ctrl+W"))
    self.contacts = MyAction("mActionContacts", QApplication.translate("QSphere","Contacts manager ...", None, QApplication.UnicodeUTF8), getThemeIcon("contact.png"), self.iface.mainWindow())
    self.contacts.setShortcut(QKeySequence("Ctrl+G"))
    self.xmleditor = MyAction("mActionXMLEditor", "%s ..." % QApplication.translate("QSphere", "Edit XML", None, QApplication.UnicodeUTF8), getThemeIcon("editxml.png"), self.iface.mainWindow())
    self.xmleditor.setShortcut(QKeySequence("Ctrl+E"))
   
    self.options = MyAction("mActionOptions", QApplication.translate("QSphere","Call the options GUI ...", None, QApplication.UnicodeUTF8), getThemeIcon("qsphereoptions.png"), self.iface.mainWindow())
    self.help = MyAction("mActionHelp", QApplication.translate("QSphere","Call the help page", None, QApplication.UnicodeUTF8), getThemeIcon("help.png"), self.iface.mainWindow())
    self.about = MyAction("mActionAbout", QApplication.translate("QSphere","About ...", None, QApplication.UnicodeUTF8), getThemeIcon("about.png"), self.iface.mainWindow())

    self.menu.addAction(self.metadata)
    self.menu.addAction(self.navigator)
    self.menu.addAction(self.xmleditor)
    self.menu.addAction(self.contacts)
    self.menu.addSeparator()
    self.menu.addAction(self.options)
    self.menu.addSeparator()
    self.menu.addAction(self.help)
    self.menu.addAction(self.about)

    menuBar = self.iface.mainWindow().menuBar()
    zMenu = menuBar
    for child in menuBar.children():
        if child.objectName()== "mPluginMenu" :
           zMenu =  child
           break
    zMenu.addMenu(self.menu)

    self.toolBar.addAction(self.metadata)
    self.toolBar.addAction(self.navigator)
    self.toolBar.addAction(self.xmleditor)
    self.toolBar.addAction(self.contacts)
    self.toolBar.addSeparator()
    self.toolBar.addAction(self.options)
    self.toolBar.addSeparator()
    self.toolBar.addAction(self.help)    
    self.toolBar.addAction(self.about)

    self.metadata.triggered.connect(self.clickMetaData)
    self.navigator.triggered.connect(self.clickNavigator)
    self.contacts.triggered.connect(self.clickContacts)
    self.xmleditor.triggered.connect(self.clickXMLEditor)
    self.options.triggered.connect(self.clickOptions)
    self.help.triggered.connect(self.clickHelp)
    self.about.triggered.connect(self.clickAbout)

    self.metadataCtxtQSP.triggered.connect(self.clickMetaData)
    self.metadataCtxtXML.triggered.connect(self.clickMetaData)
    self.navigatorCtxt.triggered.connect(self.clickNavigator)
    self.iface.mapCanvas().layersChanged.connect(self.MajDispoCommandQSP)

    self.iface.currentLayerChanged.connect(self.MajDispoCommandQSP)
    
    self.iface.legendInterface().addLegendLayerAction(self.metadataCtxtQSP, "", "idvect1",QgsMapLayer.VectorLayer, True)
    self.iface.legendInterface().addLegendLayerAction(self.metadataCtxtXML, "", "idvect2",QgsMapLayer.VectorLayer, True)
    self.iface.legendInterface().addLegendLayerAction(self.navigatorCtxt, "", "idvect3",QgsMapLayer.VectorLayer, True)

    self.iface.legendInterface().addLegendLayerAction(self.metadataCtxtQSP, "", "idrast1",QgsMapLayer.RasterLayer, True)
    self.iface.legendInterface().addLegendLayerAction(self.metadataCtxtXML, "", "idrast2",QgsMapLayer.RasterLayer, True)
    self.iface.legendInterface().addLegendLayerAction(self.navigatorCtxt, "", "idrast3",QgsMapLayer.RasterLayer, True)

    self.formats = MakeListFormats(self)
    self.langs = MakeListLangs(self)
    self.listCodecs = MakeListEncoders(self)
    self.listTemporalSystem = MakeListTemporalSystem(self)
    self.listTypeRessources = MakeListTypeRessources(self)
    self.listCountries, self.indexCountry, self.listCountriesCode = MakeListCountries(self)


  def MajDispoCommandQSP(self):
      layer = self.iface.activeLayer()
      if layer != None :
         self.metadataCtxtQSP.setEnabled(True) if self.getLayerXMLorQSP("", self.suffixeQSP)!= "#blank" else self.metadataCtxtQSP.setEnabled(False)
         self.metadataCtxtXML.setEnabled(True) if self.getLayerXMLorQSP("", self.suffixeXML)!= "#blank" else self.metadataCtxtXML.setEnabled(False)
         self.navigatorCtxt.setEnabled(True) if self.getLayerXMLorQSP("filexml:", self.suffixeXML)!= "#blank" else self.navigatorCtxt.setEnabled(False)
    
  def clickXMLEditor(self):
      d = xmlEditor(None, "" )
      icon = getThemeIcon("editxml.png")
      MakeWindowIcon(d, icon)
      MakePropertiesForWindow(d, self)
      d.setWindowTitle("%s : %s" % (d.racTitle, ""))
      d.LoadFile()
      d.exec_()
    
  def clickContacts(self):
        d = doUI.DialogContacts(self, False)
        d.exec_()
    
  def clickOptions(self):
       d = doUI.DialogOptions(self)
       d.exec_()
    
  def clickNavigator(self):
       zUrl = "" if self.iface.sender().objectName() == "mActionNavigator" else self.getLayerXMLorQSP("filexml:", self.suffixeXML)
       self.dnavigator = doUI.LoadDialogViewer(self, self.iface, zUrl, False, [], self.langueTR, self, None, "navigatorweb.png", False)

  def getLayerXMLorQSP(self, WithPrefix, WithSuffix):
      xmlFile = "#blank" 
      layer = self.iface.activeLayer()
      if layer != None :
          fileName = layer.source()
          fileDir = CorrigePath(os.path.dirname(fileName))
          fileOnlyName = os.path.basename(fileName)
          textension = os.path.splitext(fileName)
          extension = textension[len(textension)-1].lower()

          if type(WithSuffix)== str:
             baseName = "%s.%s" % (textension[0], WithSuffix)
             if os.path.exists(baseName):
                  xmlFile = "%s%s" % (WithPrefix, baseName)
          elif type(WithSuffix)== tuple:
             FileNameWithoutExt = os.path.splitext(fileOnlyName)[0]
             for suffix in WithSuffix :
                 basenames = ("%s.%s" % (textension[0], suffix), \
                              "%smd_%s.%s" % (fileDir, FileNameWithoutExt, suffix), \
                              "%s%s.qsp.%s" % (fileDir, FileNameWithoutExt, suffix), \
                              "%smd_%s.qsp.%s" % (fileDir, FileNameWithoutExt, suffix))
  
                 for elt in basenames :
                     if os.path.exists(elt): return "%s%s" % (WithPrefix, elt)
      return xmlFile
       
  def clickHelp(self): makeHelp(self)

  def clickAbout(self):
    zTest, zFileHTML = fileRessourceExist(self, "ressources/html/about_%s.html" % self.dicoLangs[self.indexLang]) #(self.langueTR))
    self.dabout = doUI.LoadDialogViewer(self, self.iface, zFileHTML, False, [], self.langueTR, self, None, "about.png", False) 

  def clickMetaData(self):
    self.dmetadata = doUI.DialogMetadata(self.iface, self.langue, self.languageIndex, self.langs, self.languesDico, \
                            self.langueTR, self.formats, self.listCodecs, self.listTemporalSystem, \
                            self.listTypeRessources, self.listCountries, self.indexCountry, self.listCountriesCode, self.localeFullName, self)
    self.dmetadata.show()

    dicoActions = {"mActionMetadataCtxtQSP": (self.suffixeQSP, self.dmetadata.GetDataFromQSP), "mActionMetadataCtxtXML": (self.suffixeXML, self.dmetadata.GetDataFromXML)}
    zkey = self.iface.sender().objectName()

    if DicoHasKey(dicoActions, zkey) : 
       fileName = self.getLayerXMLorQSP("", dicoActions[zkey][0])
       if fileName != "#blank" :
          if os.path.exists(fileName):
              dicoActions[zkey][1](fileName)
              IndexLayer = GetLayerCombo(self, self.dmetadata.ComboLayers, "%s" % (self.iface.activeLayer().id()))
              self.dmetadata.ComboLayers.setCurrentIndex(IndexLayer)
              if zkey == "mActionMetadataCtxtQSP" : self.dmetadata.IsVisibleRestoreDico(True)
              self.dmetadata.GetMetaData()
    self.dmetadata.exec_()
      
  def unload(self): pass


