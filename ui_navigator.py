# -*- coding:utf-8 -*-
from PyQt4 import QtCore, QtGui ,QtWebKit
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4 import QtXmlPatterns
from PyQt4.QtNetwork import *
from qsphere_tools import *
from qsphere_objmaker import *
import os.path
import os
import codecs
import sys
import xml.etree.ElementTree as ET
from cStringIO import StringIO
from xmlISOparser import *

from PyQt4.QtXml import *
from PyQt4.QtXmlPatterns  import *
from ui_editorXML import xmlEditor
import textwrap
import webbrowser

from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest, QNetworkCookieJar

import httplib
import urlparse
import urllib
import urllib2
import datetime


class Ui_Dialog(object):
    def setupUi(self):
        self._W, self._H, self.minwidth, self.minheight = 900, 800, 500, 90
        self.setMinimumSize(self.minwidth, 90)
        self.resize(QSize(QRect(0,0,self._W,self._H).size()).expandedTo(self.minimumSizeHint()))
        self.setWindowFlags(Qt.WindowMaximizeButtonHint)

        self.ListOfqueryURL = LoadSimpleData(self, "file:/ressources/query_url.csv")
        if self.ListOfqueryURL == [] : self.ListOfqueryURL = ["xml_iso19139?uuid", "iso19139.xml?id", "importerDonnees.do?importer", "xml.metadata.get?id", "xml.metadata.get?uuid"]
    
        self.initDir = ""
        self.initDirSearchFiles = ""
        self.oldurl = ""
        self.d = {}

        zSizeW = self.width()-20
        zSizeH = self.height()-50
        self.fileExtension = ".html"

        makeGetOptions(self)
        
        self.Listfiltres = ("All (*.htm*)", "HTML (*.html)", "HTM (*.htm)")
        self.HTML = ""
        self.countfiles, self.countdirs = 0, 0
               
        self.labeleURL = QLabel(self)
        self.labeleURL.setGeometry(QRect(10, 15,  50, 25))
        self.labeleURL.setText("URL : ")
        self.labeleURL.setAlignment(Qt.AlignRight)

        self.eURL = MyWebComboBox(self) 
        self.eURL.setEditable(True)
        self.eURL.textChanged.connect(self.eURL.VerifExpReg)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setStyleSheet(
            """QTabBar::tab:selected {color: black; background-color: rgb(255,255,255); font: 75 12pt "Arial Rounded MT Bold"; border: 1px solid black; text-decoration: underline;}"""
            """QTabBar::tab:!selected {color: rgb(255,255,255); background-color: #5D5D5D;border-bottom-color: #5D5D5D;}"""
            """QTabWidget:pane {margin: 1px,1px,1px,1px;background-color: rgb(255,255,255);}"""
            """QTabBar::tab {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #cccccc, stop: 1 #5D5D5D);  border-width: 2px; border-radius: 10px; border-color: black; height: 36px;width: 180px;}"""
            """QTabWidget{background-color: rgb(0, 0, 0); font: 75 10pt "Arial Rounded MT Bold";}"""
            """QTabWidget::tab-bar {left: 5px; bottom: 0px;background-color: rgb(255,255,255);} """
            """QTabBar::scroller {width: 0px;}"""
        )
        self.tabWidget.setTabPosition(QTabWidget.South) 
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setUsesScrollButtons(True)
        
        zTitle = ("Page", \
                  QApplication.translate("QSphere", "Analyzer", None, QApplication.UnicodeUTF8))
        zToolTip = (QApplication.translate("QSphere", "HTML page for help", None, QApplication.UnicodeUTF8), \
                    QApplication.translate("QSphere", "HTML page analyzer", None, QApplication.UnicodeUTF8))
        zIcons = ("pageweb.png", "pageanalyse.png")
        self.myPathIconvRightArrow, self.myPathIconvLeftArrow = "rightarrow.png", "leftarrow.png"
        self.myPathHome, self. myPathGoURL = "home.png", "gourl.png"
        self.myPathLoadXML, self.myPathLoadHTML = "loadxml.png", "loadxml.png"
        self.myPathPrint, self.myPathLoadFiles, self.myPathSave = "print.png", "open.png", "save.png"
        self.myReloadPage, self.myFilesNavigator, self.mySearchMenu = "reloadpage.png", "filesnavigator_true.png", "searchmenu.png"
        self.myPathEdit, self.myWaitingGIF = "editxml.png", "sablier.gif"


        self.tabWidget.setIconSize(QSize(64, 32))

        for i in range(1,len(zTitle)+1):
            zTab = QWidget(self)
            zTab.setObjectName("tab%s" % (i))
            zTab.setAccessibleName(zTitle[i-1])
            self.tabWidget.addTab(zTab, QIcon(getThemeIcon(zIcons[i-1])), zTitle[i-1])
            self.tabWidget.setTabToolTip(i-1, zToolTip[i-1])

            if i == 1:
                viewHTML = WebView(zTab)
                viewHTML.initWebView(self, self.parent, self.duration_info, self.duration_warning)
                viewHTML.setGeometry(QRect(0, 0, zSizeW-25, zSizeH-85))
                viewHTML.setObjectName("viewHTML")
                viewHTML.setAccessibleName("viewHTML")
                viewHTML.settings().setAttribute(QWebSettings.JavaEnabled, True)
                viewHTML.settings().setAttribute(QWebSettings.PluginsEnabled, True)
                viewHTML.settings().setAttribute(QWebSettings.AutoLoadImages, True)
                viewHTML.settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
                viewHTML.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
                viewHTML.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
                viewHTML.settings().setAttribute(QWebSettings.LinksIncludedInFocusChain, True)
                viewHTML.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
                viewHTML.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
                viewHTML.page().setForwardUnsupportedContent(True)
                self.viewHTML = viewHTML

                self.manager = QNetworkAccessManager()
                self.jar = QNetworkCookieJar()
                self.manager.setCookieJar(self.jar)
                
            elif i == 2:
                inspector = QtWebKit.QWebInspector(zTab)
                inspector.setGeometry(QRect(0, 0, zSizeW-25, zSizeH-85))
                inspector.setPage(self.viewHTML.page())
                inspector.show()
                inspector.setVisible(True)
                self.inspector = inspector
               

        self.BackButton = MyPushButton(self)
        self.BackButton.initPushButton(24, 24, 5, 5, "BackButton", "", QApplication.translate("QSphere", "Previous page", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathIconvLeftArrow), 24, 24, True)
        self.BackButton.setShortcut(QKeySequence("F2"))

        self.FowardButton = MyPushButton(self)
        self.FowardButton.initPushButton(24, 24, 5, 5, "FowardButton", "", QApplication.translate("QSphere", "Next page", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathIconvRightArrow), 24, 24, True)
        self.FowardButton.setShortcut(QKeySequence("F3"))

        self.goURL = MyPushButton(self)
        self.goURL.initPushButton(24, 24, 5, 5, "goURL", "", QApplication.translate("QSphere", "Go url", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathGoURL), 24, 24, True)

        self.AccueilButton = MyPushButton(self)
        self.AccueilButton.initPushButton(24, 24, 5, 5, "AccueilButton", "", QApplication.translate("QSphere", "Home page", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathHome), 24, 24, True)
        self.AccueilButton.setShortcut(QKeySequence("Ctrl+H"))

        self.ReloadButton = MyPushButton(self)
        self.ReloadButton.initPushButton(24, 24, 5, 5, "ReloadButton", "", QApplication.translate("QSphere", "Reload page", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myReloadPage), 24, 24, True)
        self.ReloadButton.setShortcut(QKeySequence("F5"))

        self.LoadButton = MyPushButton(self)
        self.LoadButton.initPushButton(24, 24, 5, 5, "LoadButton", "", QApplication.translate("QSphere", "Open Files", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathLoadFiles), 24, 24, True)
        self.LoadButton.setShortcut(QKeySequence("Ctrl+O"))
        
        self.FilesNavigatorButton = MyPushButton(self)
        self.FilesNavigatorButton.initPushButton(24, 24, 5, 5, "FilesNavigatorButton", "", QApplication.translate("QSphere","View files navigator", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myFilesNavigator), 24, 24, True)

        self.PrintButton = MyPushButton(self)
        self.PrintButton.initPushButton(24, 24, 5, 5, "PrintButton", "", QApplication.translate("QSphere", "Print", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathPrint), 24, 24, True)
        self.PrintButton.setShortcut(QKeySequence("Ctrl+P"))
                
        self.SaveButton = MyPushButton(self)
        self.SaveButton.initPushButton(24, 24, 5, 5, "SaveButton", "", QApplication.translate("QSphere", "Save XML as HTML File", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathSave), 24, 24, True)
        self.SaveButton.setShortcut(QKeySequence("Ctrl+S"))

        self.BReduceWindow = MyPushButton(self)
        self.BReduceWindow.initPushButton(24, 24, 700, 50, "BReduceWindow", "", QApplication.translate("QSphere","Get min size for the window", None, QApplication.UnicodeUTF8), True, getThemeIcon("reduce.png"), 24, 24, True)

        self.BExpandWindow = MyPushButton(self)
        self.BExpandWindow.initPushButton(24, 24, 700, 75, "BExpandWindow", "", QApplication.translate("QSphere","Get recommanded size for the window", None, QApplication.UnicodeUTF8), True, getThemeIcon("expand.png"), 24, 24, True)
        
        self.CloseButton = QPushButton(self)
        self.CloseButton.setObjectName("CloseButton")
        self.CloseButton.setText(QApplication.translate("QSphere", "Close", None, QApplication.UnicodeUTF8))

        self.EditorXMLButton = MyPushButton(self)
        self.EditorXMLButton.initPushButton(24, 24, 5, 5, "EditorXMLButton", "", QApplication.translate("QSphere", "Edit XML", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathEdit), 24, 24, True)
        self.EditorXMLButton.setShortcut(QKeySequence("Ctrl+E"))

        zIcon = getThemeIcon("qspherehelp.png")
        self.HelpButton = MyPushButton(self) 
        self.HelpButton.initPushButton(48, 48, -50, -50, "HelpButton", "", "", True, zIcon, 48, 48, True)
        self.HelpButton.setShortcut(QKeySequence("F1")) 
       
        self.filter = "*.xml" 

        self.myDock = QDockWidget("navigator", self)
        self.myDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.myDock.racTitle = QApplication.translate("QSphere","Files navigator", None, QApplication.UnicodeUTF8)
        self.myDock.setWindowTitle(self.myDock.racTitle)
        self.myDock.setVisible(False)
        self.myDock.setFloating(True)
        self.myDock.minimumWidth, self.myDock.minimumHeight = 250, 300
        self.myDock.setMinimumSize(self.myDock.minimumWidth, self.myDock.minimumHeight)
        self.myDock.setMaximumSize(self.myDock.minimumWidth*3, QDesktopWidget().screenGeometry().height()-105)

        width, height = QDesktopWidget().screenGeometry().width(), QDesktopWidget().screenGeometry().height()
        self.myDock.lastPosX = int((width - self._W)/2)-self.myDock.width()-20
        self.myDock.lastPosY = int((height-self._H)/2)+20
        self.myDock.lastWidth = 250
        self.myDock.lastHeight = self._H-105
        
        try : self.myDock.setGeometry(self.myDock.lastPosX, self.myDock.lastPosY, self.myDock.lastWidth, self.myDock.lastHeight)
        except : pass
        
        self.myDock.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.myDock.setAllowedAreas(Qt.NoDockWidgetArea)
        self.myDock.setStyleSheet(
                    "QDockWidget { color:rgb(255,255,255); font-size:12px; font-weight: bold; border: 1px solid lightgray;}"
                    "QDockWidget::title {  text-align: center; background: #5D5D5D; padding-left: 5px;}")
        
        self.txtPath = QComboBox(self.myDock)
        self.txtPath.setGeometry(0, 25, 215, 25)
        self.txtPath.setEditable(False)
        self.txtPath.setEnabled(True)
        self.txtPath.setObjectName("txtPath")
        self.txtPath.setAccessibleName("txtPath")
        self.txtPath.setObjectName("mActionFixePathOptions")

        self.labelFilters = QLabel(self.myDock)
        self.labelFilters.setText(QApplication.translate("QSphere", "Filters : ", None, QApplication.UnicodeUTF8))
        self.labelFilters.setAlignment(Qt.AlignRight)
        self.labelFilters.setGeometry(0, 60, 45, 25)

        self.saveFilters = MyPushButton(self.myDock)
        self.saveFilters.initPushButton(24, 24, 50, 60, "saveFilters", "", QApplication.translate("QSphere", "Save filters", None, QApplication.UnicodeUTF8), True, getThemeIcon("fastsave.png"), 24, 24, True)

        self.Filters = QComboBox(self.myDock)
        self.listFiltersSearch = LoadSimpleData(self, "file:/ressources/filters_search.csv") 
        if self.listFiltersSearch == [] : self.listFiltersSearch = ["*.csv", "*.htm*", "*.odp", "*.pdf", "*.qsp", "*.qsr", "*.xml"]
        
        self.Filters.addItems(self.listFiltersSearch)
        self.Filters.setCurrentIndex(0)
        self.Filters.setEditable(True)
        self.Filters.setInsertPolicy(QComboBox.InsertAlphabetically)

        self.chkSensibleCase = QCheckBox(self.myDock)
        self.chkSensibleCase.setText("aaa = AAA")
        self.chkSensibleCase.setToolTip(QApplication.translate("QSphere", "Case sensitive", None, QApplication.UnicodeUTF8))

        self.LoadPath = MyPushButton(self.myDock)
        self.LoadPath.initPushButton(24, 24, 220, 27, "ChoosePath", "", QApplication.translate("QSphere", "Choose path ...", None, QApplication.UnicodeUTF8), True, getThemeIcon("folder.png"), 24, 24, True)

        self.SearchFiles = MyPushButton(self.myDock)
        self.SearchFiles.initPushButton(24, 24, 115, 55, "SearchFiles", "", QApplication.translate("QSphere", "Search files in the path ...", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.mySearchMenu), 24, 24, True)

        self.PrintSearchFiles = MyPushButton(self.myDock)
        self.PrintSearchFiles.initPushButton(24, 24, 150, 55, "PrintSearchFiles", "", QApplication.translate("QSphere", "Print search files results", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathPrint), 24, 24, True)

        self.SaveSearchFiles = MyPushButton(self.myDock)
        self.SaveSearchFiles.initPushButton(24, 24, 185, 55, "SaveSearchFiles", "", QApplication.translate("QSphere", "Save search files results", None, QApplication.UnicodeUTF8), True, getThemeIcon("save.png"), 24, 24, True)

        self.LoadSearchFiles = MyPushButton(self.myDock)
        self.LoadSearchFiles.initPushButton(24, 24, 220, 55, "LoadSearchFiles", "", QApplication.translate("QSphere", "Load search files results", None, QApplication.UnicodeUTF8), True, getThemeIcon("open.png"), 24, 24, True)

        self.ViewModeResults = MyPushButton(self.myDock)
        self.lblmodeResults  = QApplication.translate("QSphere", "Change mode for results\nactive mode", None, QApplication.UnicodeUTF8)
        self.lblmodeResults1 = QApplication.translate("QSphere", "TreeWiget", None, QApplication.UnicodeUTF8)
        self.lblmodeResults2 = QApplication.translate("QSphere", "ListWidget", None, QApplication.UnicodeUTF8)
        self.ViewModeResults.initPushButton(48, 24, 10, 110, "ViewModeResults", "", "%s : %s." % (self.lblmodeResults, self.lblmodeResults1), True, getThemeIcon("table.png"), 48, 24, True)

        self.treeWidgetExpand = MyPushButton(self.myDock)
        self.treeWidgetExpand.initPushButton(40, 24, 60, 110, "treeWidgetExpand", "", QApplication.translate("QSphere", "Expand all", None, QApplication.UnicodeUTF8), True, getThemeIcon("tree_expand.png"), 40, 24, True)
        
        self.treeWidgetReduce = MyPushButton(self.myDock)
        self.treeWidgetReduce.initPushButton(40, 24, 105, 110, "treeWidgetReduce", "", QApplication.translate("QSphere", "Reduce all", None, QApplication.UnicodeUTF8), True, getThemeIcon("tree_reduce.png"), 40, 24, True)

        self.labelSearchFILE = QLabel(self.myDock)
        self.labelSearchFILE.setAlignment(Qt.AlignCenter)
        self.labelSearchFILE.setObjectName("labelSearchFILE")
        self.labelSearchFILE.setAccessibleName("labelSearchFILE")
        self.labelSearchFILE.setText("")

        self.refreshCounter(self.countfiles, self.countdirs)
        self.FixeEnabled()
        
        self.listeXSLT = makeListXSLT(self)
        
        self.listFiles = QListWidget(self.myDock)
        self.listFiles.setStyleSheet("* { font-size:12px; background-color: #5D5D5D; padding: 4px ; color: rgb(255,255,255)}"
                                      "QListWidget::item:selected {background-color: rgb(255,255,255); color: black;}")
        
        self.treeFiles = QTreeWidget(self.myDock)
        self.treeFiles.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.treeFiles.setObjectName("treeFiles")
        self.treeFiles.headerItem().setText(0, "1")
        self.treeFiles.header().setVisible(False)
        self.treeFiles.header().setDefaultSectionSize(200)

        self.treeFiles.setStyleSheet("* { font-size:12px; background-color: rgb(255,255,255); padding: 4px ; color: black}"
                                     "QTreeWidget::item:selected {background-color: #5D5D5D; color: rgb(255,255,255); }")        

        self.initTreeFiles()
        self.listFiles.setVisible(False)
        self.treeFiles.setVisible(True)
        
        self.labelPrimaryXSLT = QLabel(self.myDock)
        self.labelPrimaryXSLT.setText(QApplication.translate("QSphere", "Primary XSLT : ", None, QApplication.UnicodeUTF8))
        self.PrimaryXSLT = QComboBox(self.myDock)
        self.PrimaryXSLT.addItems(self.listeXSLT)
        
        self.labelSecondaryXSLT = QLabel(self.myDock)
        self.labelSecondaryXSLT.setText(QApplication.translate("QSphere", "Secondary XSLT : ", None, QApplication.UnicodeUTF8))
        self.SecondaryXSLT = QComboBox(self.myDock)
        self.SecondaryXSLT.addItems(self.listeXSLT)
        
        self.movie = QMovie(getThemeIcon(self.myWaitingGIF))

        self.status_txt = QLabel(self.myDock)
        self.status_txt.setMovie(self.movie)
        self.status_txt.setGeometry(100, 60, 64, 64)
        self.status_txt.setLayout(QHBoxLayout())
        self.status_txt.layout().addWidget(QLabel(''))
        self.status_txt.setVisible(False)


        self.movie2 = QMovie(getThemeIcon("attente.gif"))
        self.status_txt2 = QLabel(self)
        self.status_txt2.setMovie(self.movie2)
        self.status_txt2.setLayout(QHBoxLayout())
        self.status_txt2.layout().addWidget(QLabel(''))
        self.status_txt2.setVisible(False)
        

        self.barInfo = QgsMessageBar(self)
        self.barInfo.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )

        zTest, zValue = fileRessourceExist(self, "xml/xsl/transformation_%s.xsl" % (self.langueTR))

        if self.parent != None :
            if self.parent.objectName()=="DialogContacts" :
                if self.homeurl != "" :
                    if self.homeurl.startswith("filexml:") :
                       zFile = self.homeurl.replace("filexml:", "")
                       if os.path.exists(zFile) :
                            myISO = xmlISOparser(zFile, None, 'MEDDE', self.langueTR)
                            zCond = myISO.getTagDictionnary()
                            if not zCond : zTest, zValue = fileRessourceExist(self, "xml/xsl/contacts_%s.xsl" % (self.langueTR))

        if zValue != "" : zValue = os.path.basename(zValue)
        zIndex = self.listeXSLT.index(zValue) if zValue in (self.listeXSLT) else 0
        self.PrimaryXSLT.setCurrentIndex(zIndex)

        zTest, zValue = fileRessourceExist(self, "xml/xsl/iso19115_%s.xsl" % (self.langueTR))
        if zValue != "" : zValue = os.path.basename(zValue)
        zIndex = self.listeXSLT.index(zValue) if zValue in (self.listeXSLT) else 0
        self.SecondaryXSLT.setCurrentIndex(zIndex)

        self.listFiles.itemDoubleClicked.connect(self.openXMLMDD)
        self.treeFiles.itemClicked.connect(self.loadFile)
        self.treeFiles.currentItemChanged.connect(self.loadFile)
        self.treeFiles.itemDoubleClicked.connect(self.openXMLMDD)
        self.ViewModeResults.clicked.connect(self.modeVisible)
        self.treeWidgetExpand.clicked.connect(self.expandTreeWidget)
        self.treeWidgetReduce.clicked.connect(self.expandTreeWidget)
        self.saveFilters.clicked.connect(self.saveCurrentFilters)
        self.LoadPath.clicked.connect(self.fixePath)
        self.SearchFiles.clicked.connect(self.makeListFiles)
        self.LoadButton.clicked.connect(self.loadTheFile)
        self.PrimaryXSLT.currentIndexChanged.connect(self.reloadPageURL)
        self.SecondaryXSLT.currentIndexChanged.connect(self.reloadPageURL)

        self.FilesNavigatorButton.clicked.connect(self.FilesNavigator)

        self.myDock.topLevelChanged.connect(self.FixeMyDock)
        self.myDock.visibilityChanged.connect(self.FixeMyDockVisibility)
        self.myDock.resizeEvent = self.FixeMyDockSize
        self.myDock.moveEvent = self.FixeMyDockSize

        
        self.PrintButton.clicked.connect(self.printhelp)
        self.PrintSearchFiles.clicked.connect(self.resultsSearchFiles)
        self.SaveSearchFiles.clicked.connect(self.resultsSaveSearchFiles)
        self.LoadSearchFiles.clicked.connect(self.resultsLoadSearchFiles)

        self.BackButton.clicked.connect(self.go_back)
        self.AccueilButton.clicked.connect(self.go_accueil)
        self.goURL.clicked.connect(self.go_url)
        self.ReloadButton.clicked.connect(self.reloadPageURL)
        self.FowardButton.clicked.connect(self.go_forward)

        self.viewHTML.urlChanged.connect(self.changePageURL)
        self.viewHTML.linkClicked.connect(self.changePageURL)

        self.SaveButton.clicked.connect(self.SaveHTML)
        self.HelpButton.clicked.connect(self.clickHelp)

        self.BReduceWindow.clicked.connect(self.ResizeWindow)
        self.BExpandWindow.clicked.connect(self.ResizeWindow)           
        self.EditorXMLButton.clicked.connect(self.LoadXMLEditor)
        self.CloseButton.clicked.connect(self.closeme)

        if self.homeurl == "" : self.eURL.currentIndexChanged.connect(self.go_url)

        self.eURL.addItems(self.serverNavigator)
        if self.homeurl != "" :
            if self.eURL.findText(self.homeurl)==-1 : self.eURL.addItem(self.homeurl)
            self.eURL.setCurrentIndex(self.eURL.findText(self.homeurl))
            self.go_url()
            self.eURL.currentIndexChanged.connect(self.go_url)    
        else : self.homeurl = self.eURL.currentText()   


    def saveCurrentFilters(self):
        fichier = os.path.join(os.path.dirname(__file__), "ressources/filters_search.csv") 
        with codecs.open(fichier,'w','utf8') as f:
             for index in range(self.Filters.model().rowCount()):
                 if self.Filters.itemText(index)!= "" : f.write( "\"%s\"\n" % (self.Filters.itemText(index)))
        if f!= None : f.close()
        
        zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
        zMsg = QApplication.translate("QSphere","The file ini was saved as", None, QApplication.UnicodeUTF8)
        SendMessage(self, zTitle , "%s :<br><u><i>%s</i></ul>" % (zMsg, fichier), QgsMessageBar.INFO, self.duration_info)

    def expandTreeWidget(self):
        if self.sender() == self.treeWidgetExpand : self.treeFiles.expandAll()
        else :
            self.treeFiles.collapseAll()
            self.treeFiles.expandItem(self.treeFiles.itemAt(0, 0))
        
    def modeVisible(self):
        self.listFiles.setVisible(not self.listFiles.isVisible())
        self.treeFiles.setVisible(not self.listFiles.isVisible())
        self.treeWidgetExpand.setEnabled(not self.listFiles.isVisible())
        self.treeWidgetReduce.setEnabled(not self.listFiles.isVisible())
        if self.listFiles.isVisible() :
            zToolTip = self.lblmodeResults2
            zIcon = QIcon(getThemeIcon("tree.png"))
            try :
                QObject.disconnect(self.treeFiles,SIGNAL("itemClicked(QTreeWidgetItem*)"), self.loadFile)
                QObject.disconnect(self.treeFiles,SIGNAL("currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)"), self.loadFile)
            except : pass
            self.listFiles.itemClicked.connect(self.loadFile)
            self.listFiles.currentItemChanged.connect(self.loadFile)
            self.listFiles.currentRowChanged.connect(self.loadFileByInt)            
        else :
            zToolTip = self.lblmodeResults1
            zIcon = QIcon(getThemeIcon("table.png"))
            try :
                QObject.disconnect(self.listFiles,SIGNAL("itemClicked(QListWidgetItem*)"), self.loadFile)
                QObject.disconnect(self.listFiles,SIGNAL("currentItemChanged(QListWidgetItem*,QListWidgetItem*)"), self.loadFile)
                QObject.disconnect(self.listFiles,SIGNAL("currentRowChanged(int)"), self.loadFileByInt)
            except : pass
            self.treeFiles.itemClicked.connect(self.loadFile)
            self.treeFiles.currentItemChanged.connect(self.loadFile)
        self.ViewModeResults.setToolTip("%s : %s." % (self.lblmodeResults, zToolTip))
        self.ViewModeResults.setIcon(zIcon)  
        

    def initTreeFiles(self):
        self.layers_item = None
        self.layers_item = QTreeWidgetItem()
        self.layers_item.setText(0, QApplication.translate("QSphere", "Results", None, QApplication.UnicodeUTF8))

        self.treeFiles.addTopLevelItem(self.layers_item)
        self.treeFiles.expandAll()
        self.treeFiles.resizeColumnToContents(0)
        self.treeFiles.resizeColumnToContents(1)

    def clickHelp(self): makeHelp(self)
    
    def startMovie(self):
        self.status_txt.setVisible(True)
        self.movie.start()
        self.status_txt.repaint()

    def stopMovie(self):
        self.movie.stop()
        self.status_txt.setVisible(False)

    def startMovie2(self):
        self.status_txt2.setVisible(True)
        self.movie2.start()
        self.status_txt2.repaint()

    def stopMovie2(self):
        self.movie2.stop()
        self.status_txt2.setVisible(False)


    def ResizeWindow(self):
        self.resize(self.minwidth, self.minheight) if (self.sender().accessibleName() == "BReduceWindow") else self.resize(self._W, self._H)

    def reject(self): self.killWindow()
    def closeme(self): self.killWindow()
    def killWindow(self):
        if self.parent != None  and not self.isModal :
           if self.senderBut != None :
              if self.senderBut.objectName().startswith("help_") : ChangeButtonIcon(self.parent, self.senderBut,"info.png", 24, 24)
           try :   
               if (self) in self.parent.childswindows :
                   self.parent.childswindows.remove(self)
                   self.parent.nb_window_childs.setText("%s" % (len(self.parent.childswindows)))
           except: pass        
        self.myDock.close()
        self.d = {}
        self.reject()
        
    def printhelp(self):
        printer = QPrinter() 
        printer.setPageSize(QPrinter.A4)
        printer.setOrientation(QPrinter.Portrait) if self.isXML else printer.setOrientation(QPrinter.Landscape)
        printer.setPageMargins(5, 10, 5, 10, QPrinter.Millimeter) if self.fileExtension == ".xml" else printer.setPageMargins(10, 10, 10, 10, QPrinter.Millimeter)
        printer.setOutputFormat(QPrinter.NativeFormat)
        printDialog = QPrintPreviewDialog(printer)
        MakeWindowIcon(printDialog, self.myPathPrint)
        printDialog.setWindowTitle(QApplication.translate("QSphere", "Print current page", None, QApplication.UnicodeUTF8))
        printDialog.setWindowFlags(Qt.WindowMaximizeButtonHint)
        printDialog.paintRequested.connect(self.viewHTML.print_)
        printDialog.exec_()     

    def resultsSearchFiles(self):
        printer = QPrinter()
        printer.setPageSize(QPrinter.A4)
        printer.setOrientation(QPrinter.Landscape) 
        printer.setPageMargins(5, 10, 5, 10, QPrinter.Millimeter) 
        printer.setOutputFormat(QPrinter.NativeFormat)

        myicon = getThemeIcon("open.png")
        editor = QTextEdit()
        editor.setAcceptRichText(True) 
        ztxtListWidget = "<h1>%s</h1>" %  (QApplication.translate("QSphere", "Results for a search files", None, QApplication.UnicodeUTF8))
        ztxtListWidget+= "path=%s<br><hr><br>" % (self.txtPath.currentText())
        ztxtListWidget+= "%s" % (self.labelSearchFILE.text())
        ztxtListWidget+= "<table width='100%'>"
        for i in range(self.listFiles.count()):
            if self.listFiles.item(i).type()==0 : ztxtListWidget+= "<tr><td><b>%s</b></td><td>[uri : <i>%s</i>]</td></tr>" % (self.listFiles.item(i).text(), self.listFiles.item(i).toolTip())
            elif self.listFiles.item(i).type()==1 :  ztxtListWidget+= "<tr bgcolor=#90b4d6 valign='middle'><td colspan='2'><table cellspacing=10><tr><td><img src='%s'></td><td><h3>%s</h3></td></tr></table></td></tr>" % (myicon,self.listFiles.item(i).text())
        ztxtListWidget+= "</table>"
        editor.setText(ztxtListWidget)
        
        printDialog = QPrintPreviewDialog(printer)
        MakeWindowIcon(printDialog, "print.png")
        printDialog.setWindowTitle(QApplication.translate("QSphere", "Print search files results", None, QApplication.UnicodeUTF8))
        printDialog.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint)

        printDialog.paintRequested.connect(editor.print_)
        printDialog.exec_()

    def resultsSaveSearchFiles(self):
        InitDir = os.path.dirname(__file__) if self.initDirSearchFiles == "" else self.initDirSearchFiles
        InitDir = CorrigePath(InitDir)
        zTitle = QApplication.translate("QSphere","Save search files results", None, QApplication.UnicodeUTF8)
        MyFileDialog = QFileDialog(self, zTitle)
        zElt0 = QApplication.translate("QSphere","files", None, QApplication.UnicodeUTF8).title()
        MyFileDialog.setNameFilters(("%s QSphere (*.qsr)" % (zElt0),)) 
        MyFileDialog.setDefaultSuffix("qsr")
        MyFileDialog.setViewMode(QFileDialog.Detail)
        MyFileDialog.setAcceptMode(QFileDialog.AcceptSave)

        FixeLabelsFileDialog(self, MyFileDialog, 1, True)
        zFileUrl = urllib.unquote(self.eURL.currentText())
        if os.path.exists(zFileUrl):
           zFile = QFileInfo(zFileUrl)
           if zFile.suffix().lower() == "qsr" :
              InitName = os.path.basename(zFileUrl).split(".")[0]
              InitDir = os.path.dirname(zFileUrl)
              MyFileDialog.selectFile(InitName)
              
        MyFileDialog.setDirectory(InitDir)
        
        if MyFileDialog.exec_():
            fileName = FileNameWithExtension(self, MyFileDialog.selectedFiles()[0], MyFileDialog.selectedNameFilter())
            self.initDirSearchFiles = os.path.dirname(fileName)
            
            zLOG = open(fileName, "w")
            Config = ConfigParser.ConfigParser()
            NameSection = "QSphere Search Results"
            Config.add_section(NameSection)
            Config.set(NameSection,'date', datetime.datetime.now().strftime("%d/%m/%Y %Hh%Mm%Ss"))
            Config.set(NameSection,'mandatoryPlugin',"QSphere")
            Config.set(NameSection,'version',"2.14.0")

            NameSection = "Root"
            Config.add_section(NameSection)
            Config.set(NameSection, 'Path', self.txtPath.currentText())
            Config.set(NameSection, 'filtre', self.Filters.currentText())
            Config.set(NameSection, 'files', self.countfiles)
            counter=0
            for i in range(self.listFiles.count()):
                if self.listFiles.item(i).type()==0 :
                    Config.set(NameSection,'File_%s' % (counter),self.listFiles.item(i).toolTip().replace("\\","/").encode("cp1252"))
                    counter+= 1                                 
                elif self.listFiles.item(i).type()==1 :
                    NameSection = self.listFiles.item(i).toolTip().encode("cp1252")
                    Config.add_section(NameSection)
        
            Config.write(zLOG)
            if zLOG != None : zLOG.close()

            zTitle = QApplication.translate("QSphere","Save as a file", None, QApplication.UnicodeUTF8) 
            zMsg = QApplication.translate("QSphere","The metadata record was saved as", None, QApplication.UnicodeUTF8)
            SendMessage(self, zTitle , "%s :<br><u><i>%s</i></ul>" % (zMsg, fileName), QgsMessageBar.INFO, self.duration_info)

            if fileName == zFileUrl : self.reloadPageURL()

    def resultsLoadSearchFiles(self):
        zTitle = QApplication.translate("QSphere","Load search files results", None, QApplication.UnicodeUTF8)
        InitDir = os.path.dirname(__file__) if self.initDirSearchFiles == "" else self.initDirSearchFiles
        MyFileDialog = QFileDialog(self, zTitle)
        zElt0 = QApplication.translate("QSphere","files", None, QApplication.UnicodeUTF8).title()        
        MyFileDialog.setNameFilters(("%s QSphere (*.qsr)" % (zElt0),)) 
        MyFileDialog.setViewMode(QFileDialog.Detail)
        MyFileDialog.setDirectory(InitDir)
        MyFileDialog.setFileMode(QFileDialog.ExistingFile) 
        MyFileDialog.setAcceptMode(QFileDialog.AcceptOpen)

        FixeLabelsFileDialog(self, MyFileDialog, 0, True)
        
        if MyFileDialog.exec_():
            fileName = "%s" % (MyFileDialog.selectedFiles()[0])
            if fileName!="" :
               self.initDirSearchFiles = os.path.dirname(fileName)
               self.myDock.setWindowTitle("%s :%s" % (self.myDock.racTitle, fileName))
               
               config = ConfigParser.ConfigParser()
               config.read(fileName)
               zSections = config.sections()

               fontDirs = QtGui.QFont()
               fontDirs.setPointSize(8) 
               fontDirs.setWeight(10) 
               fontDirs.setBold(True)

               self.countfiles, self.countdirs = 0, 1

               self.listFiles.clear()
               self.listFiles.update()

               self.treeFiles.clear()
               self.initTreeFiles()
               
               menuIcon = getThemeIcon("xml.png")
               icondir = getThemeIcon("open.png")
               pos, countfiles, countdirs, oldirs = 0, 0, 1, []

               for section in zSections :
                   if section == "Root" :
                       zPath = config.get(section,'path')
                       if self.txtPath.findText(zPath) == -1: self.txtPath.addItem(zPath)
                       else : self.txtPath.setCurrentIndex(self.txtPath.findText(zPath))

                       self.listdirectories = {}
                       self.listdirectories["%s" % (zPath)]= (self.layers_item, [])
                       groupItems = self.layers_item
                       refpath = zPath
                       
                       zFiltre = config.get(section,'filtre')

                       if zFiltre not in self.listFiltersSearch :
                           self.listFiltersSearch.append(zFiltre)
                           self.Filters.addItem(zFiltre)
                           
                       index = self.Filters.findText(zFiltre)
                       
                       if index < 0 : index = 0
                       menuIcon = getThemeIcon("%s.png" % (zFiltre.replace("*","").replace(".","")))
                       self.Filters.setCurrentIndex(index)
                       self.countfiles = int(config.get(section,'files'))

                   if not section in ("QSphere Search Results", "Root") :
                        self.countdirs+= 1
                        if os.path.exists("%s%s/" % (zPath,section)):
                            zItem = QListWidgetItem(QIcon(icondir), "%s" % (textwrap.fill(section, 50)), None, 1)
                            zItem.setFont(fontDirs)
                            zItem.setBackground(QBrush(QColor(200,200,200,125),Qt.SolidPattern))
                            zItem.setFlags(Qt.ItemIsEnabled)
                            zItem.setToolTip(section)
                            self.listFiles.addItem(zItem)
                            countdirs+= 1

                            groupItems = self.layers_item
                            abspath = os.path.dirname("%s%s/" % (zPath, section))
                            tpath = abspath.split("/")
                            dirname = "%s/" % (abspath.replace(zPath, ""))
                            tdirname = dirname.split("/")
                            compath = ""

                            for  i in range(len(tdirname)):
                                if tdirname[i]!= "" :
                                    compath+=  tdirname[i]+"/"
                                    zkey = ("%s%s" % (refpath, compath))
                                   
                                    if not DicoHasKey(self.listdirectories, zkey) :
                                        groupItemsSub = QTreeWidgetItem()
                                        groupItemsSub.setIcon(0, QIcon(icondir))
                                        groupItemsSub.setText(0, "%s" % (tdirname[i]))
                                        groupItemsSub.setToolTip(0, "")
                                        groupItems.addChild(groupItemsSub)
                                        self.listdirectories[zkey] = (groupItemsSub, [])
                                        groupItems = groupItemsSub
                                    else:
                                        groupItems = self.listdirectories[zkey][0]
                            
                        else : oldirs.append("%s%s/" % (zPath,section))
                            
                            
                   if section != "QSphere Search Results" :
                       for i in range(pos, self.countfiles, 1):
                           try : zFile = config.get(section,'file_%s' % (i))
                           except : break

                           if os.path.exists(zFile):
                               zItem = QListWidgetItem(QIcon(menuIcon), "%s" % (os.path.basename(zFile)), None, 0)
                               zItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                               zItem.setToolTip("%s" % (zFile.decode('cp1252', 'ignore')))
                               self.listFiles.addItem(zItem)
                               countfiles+= 1

                               if groupItems!= None :
                                  FileItem = QTreeWidgetItem()
                                  FileItem.setIcon(0, QIcon(menuIcon))
                                  FileItem.setText(0, "%s" % (os.path.basename(zFile)))
                                  FileItem.setToolTip(0, zFile)
                                  groupItems.addChild(FileItem)  
                               
                           pos+= 1
                   self.refreshCounter(self.countfiles, self.countdirs)

               if (self.countfiles != countfiles) or (self.countdirs != countdirs) :    
                   zTitle = QApplication.translate("QSphere","Warning", None, QApplication.UnicodeUTF8)
                   zEltFiles = QApplication.translate("QSphere","files", None, QApplication.UnicodeUTF8).title()
                   zEltIn = QApplication.translate("QSphere","in", None, QApplication.UnicodeUTF8).title()
                   zEltFolders = QApplication.translate("QSphere","folders", None, QApplication.UnicodeUTF8).title()
                   zEltReload = QApplication.translate("QSphere","Read from download stream ", None, QApplication.UnicodeUTF8)
                   zEltFile = QApplication.translate("QSphere","File", None, QApplication.UnicodeUTF8)
                   
                   SendMessage(self, zTitle , "%s ... : %s %s %s %s %s<br>%s : %s %s %s %s %s<br>%s" % (zEltFile, self.countfiles, zEltFiles, zEltIn, self.countdirs, zEltFolders, zEltReload, countfiles, zEltFiles, zEltIn, countdirs, zEltFolders, oldirs), QgsMessageBar.WARNING, self.duration_warning)    

               self.countfiles, self.countdirs = countfiles, countdirs
               
               self.refreshCounter(countfiles, countdirs)
               self.FixeEnabled()

               if self.listFiles.count()> 0 :
                  self.listFiles.setCurrentRow(0)
                  self.loadFile(self.listFiles.currentItem())
                
    def resizeEvent(self,ev):
        zSize = ev.size()
        
        self.BackButton.setGeometry(65, 10, 25, 25)
        self.eURL.setGeometry(95, 10,  zSize.width()-380, 25)
        self.FowardButton.setGeometry(zSize.width()-270, 10, 60, 25)
        self.goURL.setGeometry(zSize.width()-240, 10, 60, 25)
        self.AccueilButton.setGeometry(zSize.width()-210, 10, 60, 25)
        self.ReloadButton.setGeometry(zSize.width()-180, 10, 60, 25)
        self.LoadButton.setGeometry(zSize.width()-150, 10, 60, 25)
        self.FilesNavigatorButton.setGeometry(zSize.width()-120, 10, 60, 25)
        self.PrintButton.setGeometry(zSize.width()-90, 10, 60, 25)
        self.EditorXMLButton.setGeometry(zSize.width()-60, 10, 60, 25)
        self.status_txt2.setGeometry(int(zSize.width()/2)-64, int(zSize.height()/2)-64, 64, 64)
        
        self.SaveButton.setGeometry(zSize.width()-30, 10, 60, 25)

        if not self.myDock.isVisible(): self.tabWidget.setGeometry(10, 40,  zSize.width()-20, zSize.height()-90)
        else : self.FixeMyDock()
            
        self.viewHTML.setGeometry(0, 0,  zSize.width()-25, zSize.height()-105)
        self.inspector.setGeometry(0, 0,  zSize.width()-25, zSize.height()-105)
        
        self.barInfo.setGeometry(0, 40, zSize.width(), 90)    
        self.CloseButton.setGeometry(zSize.width()-120, zSize.height()-30, 100, 25)

        self.BReduceWindow.setGeometry(zSize.width()-180, zSize.height()-55, 100, 25)
        self.BExpandWindow.setGeometry(zSize.width()-180, zSize.height()-30, 100, 25)
        self.BReduceWindow.setEnabled(False) if ((self.height() == self.minheight) and (self.width()== self.minwidth)) else self.BReduceWindow.setEnabled(True)
        self.BExpandWindow.setEnabled(False) if ((self.height() == self._H) and (self.width()== self._W)) else self.BExpandWindow.setEnabled(True)        
        
    def reloadPageURL(self):
        self.viewHTML.pageAction(QtWebKit.QWebPage.Reload)
        self.go_url()
        
    def go_back(self):
        self.viewHTML.history().back()
        zUrl = "%s" % (unicode(self.viewHTML.history().currentItem().url().toString()))
        if self.eURL.findText(zUrl)==-1 : self.eURL.addItem(zUrl)
        self.eURL.setCurrentIndex(self.eURL.findText(zUrl))
        FixeEnabledHistory(self, self.viewHTML)
        
    def go_forward(self):
        self.viewHTML.history().forward()
        zUrl = "%s" % (unicode(self.viewHTML.history().currentItem().url().toString()))
        if self.eURL.findText(zUrl)==-1 : self.eURL.addItem(zUrl)
        self.eURL.setCurrentIndex(self.eURL.findText(zUrl))        
        FixeEnabledHistory(self, self.viewHTML)

    def SaveHTML(self):
        if self.HTML.find('javascript') != -1 :
            zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
            zMsg1 = QApplication.translate("QSphere","Javascript detected ! Risk of trouble with the HTML save ...", None, QApplication.UnicodeUTF8)
            zMsg2 = QApplication.translate("QSphere","Choose another XSLT for saving in HTML format.", None, QApplication.UnicodeUTF8)
            SendMessage(self, zTitle , "%s<br>%s" % (zMsg1, zMsg2), QgsMessageBar.WARNING, self.duration_warning)
            return
        zUrl = self.eURL.currentText() 
        InitDir = os.path.dirname(zUrl) if self.initDir == "" else self.initDir
        InitDir = CorrigePath(InitDir)
        fileName, fileExtension = os.path.splitext(zUrl)
        NameFile = os.path.basename(zUrl).split(".")[0]
        InitDir = "%s%s%s" % (InitDir,NameFile.rsplit(".",1)[0], ".html")

        zTitle = QApplication.translate("QSphere","Save as a HTML file", None, QApplication.UnicodeUTF8)
        MyFileDialog = QFileDialog(self, zTitle)
        MyFileDialog.setNameFilters(self.Listfiltres)
        MyFileDialog.setDefaultSuffix("html")
        MyFileDialog.setViewMode(QFileDialog.Detail)
        MyFileDialog.setDirectory(InitDir)
        MyFileDialog.selectFile(NameFile)
        MyFileDialog.setAcceptMode(QFileDialog.AcceptSave)
        
        FixeLabelsFileDialog(self, MyFileDialog, 1, True)
        
        if MyFileDialog.exec_():
            fileName = FileNameWithExtension(self, MyFileDialog.selectedFiles()[0], MyFileDialog.selectedNameFilter())
            zHTML = self.HTML.encode(encoding='cp1252',errors='strict') 
            zLOG = open(fileName, "w")
            try :
                zLOG.write(urllib.unquote_plus(zHTML))
                zTitleMsg = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
                zSuccess = QApplication.translate("QSphere","Successfull !", None, QApplication.UnicodeUTF8)
                SendMessage(self, zTitleMsg , "%s :<br>%s<br>%s" % (zTitle, fileName, zSuccess) , QgsMessageBar.INFO, self.duration_info)                
            except :
                try :
                    zLOG.write("%s" % (zHTML))
                    zTitleMsg = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
                    zSuccess = QApplication.translate("QSphere","Successfull !", None, QApplication.UnicodeUTF8)
                    SendMessage(self, zTitleMsg , "%s :<br>%s<br>%s" % (zTitle, fileName, zSuccess) , QgsMessageBar.INFO, self.duration_info)
                except :
                    zLOG.write("<html><style>h1 {	font-size: 1.5em;}</style><h1>error</h1></html>")
                    zTitleMsg = QApplication.translate("QSphere","Warning", None, QApplication.UnicodeUTF8)
                    zSuccess = QApplication.translate("QSphere","Error", None, QApplication.UnicodeUTF8)
                    SendMessage(self, zTitleMsg , "%s :<br>%s<br>%s" % (zTitle, fileName, zSuccess) , QgsMessageBar.WARNING, self.duration_warning)
                                                      
            if zLOG != None : zLOG.close()
            
      
    def go_url(self):
        
        zUrl = self.eURL.currentText() 
        if not zUrl.startswith("file:") and zUrl.startswith("filexml:") and zUrl.startswith("fileHTML:") and zUrl.startswith("about:") :    
            if (zUrl[0:7] != "http://" and zUrl[0:6] != "ftp://" and zUrl[0:8] != "https://") and not(os.path.exists(zUrl.split("#")[0])) :
                zUrl = "http://%s" % (zUrl) if zUrl != "" else zUrl
                if self.eURL.findText(zUrl)==-1 : self.eURL.addItem(zUrl)
                self.eURL.setCurrentIndex(self.eURL.findText(zUrl))
            if self.eURL.styleSheet() == "background-color:red;" and not os.path.exists(zUrl.split("#")[0]) :
               zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8) 
               zMsg = QApplication.translate("QSphere","Invalid URL ! Use open function if necessary for local ressources ...", None, QApplication.UnicodeUTF8)
               SendMessage(self, zTitle , zMsg, QgsMessageBar.WARNING, self.duration_warning)
               return
        else :
                ActiveLink(self, zUrl, False, self.viewHTML)
                self.setWindowTitle(zUrl)

                if self.listFiles.count()> 0 :
                    for i in range(self.listFiles.count()) :
                        if self.listFiles.item(i).type()==0:
                           if self.listFiles.item(i).toolTip()== zUrl :
                              self.listFiles.setCurrentRow(i)
                              break
                return
            
        if self.eURL.currentText() != "" and self.eURL.styleSheet()!="background-color:red;" :
            ActiveLink(self, self.eURL.currentText(), False, self.viewHTML)
        else :
            if self.eURL.currentText() != "" :
                zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
                zMsg = QApplication.translate("QSphere","URL not natively supported ! Use open function if necessary for local ressources ...", None, QApplication.UnicodeUTF8)
                SendMessage(self, zTitle , zMsg, QgsMessageBar.WARNING, self.duration_warning)


    def FilesNavigator(self):
        self.myDock.setVisible(not self.myDock.isVisible())
        self.FixeMyDockVisibility()
        self.FixeMyDock()

    def FixeMyDockVisibility(self):
        zcond = "%s" % (not self.myDock.isVisible())
        self.FilesNavigatorButton.setToolTip(QApplication.translate("QSphere","Mask files navigator", None, QApplication.UnicodeUTF8)) if self.myDock.isVisible() else self.FilesNavigatorButton.setToolTip(QApplication.translate("QSphere","View files navigator", None, QApplication.UnicodeUTF8))
        if not self.myDock.isVisible(): self.tabWidget.setGeometry(10, 40,  self.width()-20, self.height()-90)
        else : self.FixeMyDock()        
        ChangeButtonIcon(self, self.FilesNavigatorButton,"filesnavigator_%s.png" % (zcond.lower()), 24, 24)

    def FixeMyDockSize(self, obj):
        if self.myDock.isFloating() :
            self.myDock.lastPosX = self.myDock.x()
            self.myDock.lastPosY = self.myDock.y()
            self.myDock.lastWidth = self.myDock.width()
            self.myDock.lastHeight = self.myDock.height()

        width, height = self.myDock.width(), self.myDock.height()
        self.txtPath.setGeometry(0, 25, width-35, 25)
        self.LoadPath.setGeometry(self.txtPath.width()+5, 27, 24, 24)

        self.saveFilters.setGeometry(50, 57, 25, 25)
        self.Filters.setGeometry(75, 55, width-195, 25)
        self.chkSensibleCase.setGeometry(width-115, 55, width-115, 25)
        self.SearchFiles.setGeometry(self.chkSensibleCase.width()+85, 55, 24, 24)

        self.labelSearchFILE.setGeometry(5, 80, width-5, 25)
        
        self.listFiles.setGeometry(0, 140, width-5, height-210)
        self.treeFiles.setGeometry(0, 140, width-5, height-210)
        
        self.LoadSearchFiles.setGeometry(self.Filters.width()+15, 110, 24, 24)
        self.PrintSearchFiles.setGeometry(self.Filters.width()+50, 110, 24, 24)
        self.SaveSearchFiles.setGeometry(self.Filters.width()+85, 110, 24, 24)

        self.labelPrimaryXSLT.setGeometry(10, height-60,  90, 25)
        self.PrimaryXSLT.setGeometry(100, height-60,  150, 25)
        self.labelSecondaryXSLT.setGeometry(10, height-30,  90, 25)
        self.SecondaryXSLT.setGeometry(100, height-30,  150, 25)        
        
    def FixeMyDock(self):
        if not self.myDock.isFloating() :
            self.myDock.setGeometry(10, 40, 250, self.height()-105)
            self.tabWidget.setGeometry(260, 40,  self.width()-20, self.height()-90)
        else :
            self.tabWidget.setGeometry(10, 40,  self.width()-20, self.height()-90)

    def fixePath(self):
          InitDir = os.path.dirname(__file__) if self.txtPath.currentText()=="" else os.path.dirname("%s" % (self.txtPath.currentText()))
          zTitle = QApplication.translate("QSphere", "Select the folder to search files", None, QApplication.UnicodeUTF8)
          MyFileDialog = QFileDialog(self, zTitle)
          MyFileDialog.setDirectory(InitDir)
          MyFileDialog.setFileMode(QFileDialog.DirectoryOnly)

          FixeLabelsFileDialog(self, MyFileDialog, 0, False)          
          
          if MyFileDialog.exec_():
             inputDir = MyFileDialog.selectedFiles()[0] 
             zCible = "%s/" % (inputDir.replace("\\","/"))
             if self.txtPath.findText(zCible)==-1 : self.txtPath.addItem("%s" % (zCible))
             self.txtPath.setCurrentIndex(self.txtPath.model().rowCount()-1)
             self.initDir = inputDir
          self.FixeEnabled()
      
    def FixeEnabled(self):
        self.txtPath.setEnabled(False) if self.txtPath.count()<=0 else self.txtPath.setEnabled(True)
        self.SearchFiles.setEnabled(False) if self.txtPath.currentText()=="" else self.SearchFiles.setEnabled(True)
        self.SaveSearchFiles.setEnabled(False) if self.txtPath.currentText()=="" else self.SaveSearchFiles.setEnabled(True)

    def makeListFiles(self):
        if not os.path.exists(self.txtPath.currentText()) :
            zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
            zMsg = QApplication.translate("QSphere","Error", None, QApplication.UnicodeUTF8)
            zMsg1 = QApplication.translate("QSphere","folder", None, QApplication.UnicodeUTF8)
            SendMessage(self, zTitle , "%s %s :<br>%s" % (zMsg, zMsg1, self.txtPath.currentText()), QgsMessageBar.WARNING, self.duration_warning)
            self.txtPath.removeItem(self.txtPath.currentIndex())
            self.countfiles, self.countdirs = 0, 0
            self.refreshCounter(self.countfiles, self.countdirs)        
            try : self.txtPath.setCurrentIndex(0)
            except : pass
            self.FixeEnabled()
            return 

        self.treeFiles.clear()
        self.initTreeFiles()
        self.myDock.setWindowTitle(self.myDock.racTitle)
        
        self.countfiles, self.countdirs = 0, 1
        self.refreshCounter(self.countfiles, self.countdirs)        
        self.filter = QRegExp("%s" % (self.Filters.currentText()))
        self.filter.setCaseSensitivity(Qt.CaseInsensitive) if self.chkSensibleCase.isChecked() else self.filter.setCaseSensitivity(Qt.CaseSensitive)
        self.filter.setPatternSyntax(QRegExp.Wildcard)
        self.listFiles.clear()
        self.listFiles.update()
        self.EditorXMLButton.setEnabled(False)
        self.listFiles.setEnabled(False)
        self.startMovie()
        self.countfiles, self.countdirs = listdirectoryWeb(self, self.txtPath.currentText(), self.listFiles, self.movie.frameCount())
        self.stopMovie()
        if self.listFiles.count()> 0 :
           self.listFiles.setCurrentRow(0)
           self.loadFile(self.listFiles.currentItem())
        self.refreshCounter(self.countfiles, self.countdirs)
        self.movie.stop()   
        self.listFiles.update()
        self.listFiles.setEnabled(True)

    def refreshCounter(self, countfiles, countdirs):
        sFile = QApplication.translate("QSphere", "files", None, QApplication.UnicodeUTF8) if self.countfiles > 1 else QApplication.translate("QSphere", "file", None, QApplication.UnicodeUTF8) 
        sFolder = QApplication.translate("QSphere", "folders", None, QApplication.UnicodeUTF8) if self.countdirs > 1 else QApplication.translate("QSphere", "folder", None, QApplication.UnicodeUTF8)
        self.labelSearchFILE.setText("%s %s %s %s %s." % (countfiles, sFile, \
                                                      QApplication.translate("QSphere", "in", None, QApplication.UnicodeUTF8), \
                                                      countdirs, sFolder))        


    def openXMLMDD(self, Item):
        fileName = ""
        if self.sender() == self.listFiles :
            if self.listFiles.count()==0 : return
            if Item == None : return
            if Item.type()==1 : return
            if not Item : return
            fileName = Item.toolTip()
        elif self.sender() == self.treeFiles :
            if Item == None : return
            if Item.toolTip(0)=="": return
            fileName = Item.toolTip(0)
        if fileName == "": return

        if os.path.exists(fileName) :
            zFile = QFileInfo(fileName)
            extension = zFile.suffix().lower()

            if extension in ("xml", "qsp") : 
                from doUI import DialogMetadata
                self.dmetadata = DialogMetadata(self.iface, self.langue, self.languageIndex, self.langs, self.languesDico, \
                                        self.langueTR, self.formats, self.listCodecs, self.listTemporalSystem, \
                                        self.listTypeRessources, self.listCountries, self.indexCountry, self.listCountriesCode, self.localeFullName, self)
                self.dmetadata.show()
                self.dmetadata.GetDataFromQSP(fileName) if (extension == "qsp") else self.dmetadata.GetDataFromXML(fileName)
                self.dmetadata.exec_()        
            else :
                self.viewHTML.ToOpenURL = fileName
                self.viewHTML.MakeOpenURL()  


    def loadFileByInt(self, index): self.loadFile(self.listFiles.currentItem())
    
    def loadFile(self, Item):
        fileName = ""
        if self.sender() == self.listFiles :
            if self.listFiles.count()==0 : return
            if Item == None : return
            if Item.type()==1 : return
            if not Item : return
            fileName = Item.toolTip()
        elif self.sender() == self.treeFiles :
            if Item == None : return
            if Item.toolTip(0)=="": return
            fileName = Item.toolTip(0)

        if fileName == "": return
        self.selfActiveLink(fileName)
        self.eURL.setStyleSheet("""QComboBox {background-color:#AEEE00;}"""
                          """QComboBox QAbstractItemView {background-color:#AEEE00; min-width:%spx;}""" % (self.minwidth)
                          )
        self.synchronise(self.sender())


    def synchronise(self, zSender):
        if zSender  == self.treeFiles :
            zItems = self.listFiles.findItems(zSender.currentItem().text(0), Qt.MatchExactly)
            if zItems != [] :
               for item in zItems :
                   if item.toolTip() ==  zSender.currentItem().toolTip(0) :
                      self.listFiles.setCurrentItem(item)
                      break
           
        elif zSender == self.listFiles :
            zItems = self.treeFiles.findItems(zSender.currentItem().text(), Qt.MatchExactly | Qt.MatchRecursive, 0)
            if zItems != [] :
               for item in zItems :
                   if item.toolTip(0) ==  zSender.currentItem().toolTip() :
                      self.treeFiles.setCurrentItem(item)
                      break
        else : return

    def selfActiveLink(self, fileName):
        if os.path.exists(fileName) :
            zFile = QFileInfo(fileName)
            zRac = "filexml:" if zFile.suffix().lower() == "xml" else ""
            self.homeurl = "%s%s" % (zRac, fileName.replace("\\", "/"))
    
            FixeEnabledHistory(self, self.viewHTML)
            zIndex = self.eURL.findText(self.homeurl)
            if zIndex == -1 :
                self.eURL.addItem(self.homeurl)
                zIndex = self.eURL.findText(self.homeurl)
            self.eURL.setCurrentIndex(zIndex)
    
    def loadTheFile(self):
        zTitle = QApplication.translate("QSphere","View a file (XML ISO 19139, HTML ...)", None, QApplication.UnicodeUTF8)
        InitDir = os.path.dirname(__file__) if self.initDir == "" else self.initDir
        MyFileDialog = QFileDialog(self, zTitle)
        zElt0 = QApplication.translate("QSphere","files", None, QApplication.UnicodeUTF8).title()
        zElt1 = QApplication.translate("QSphere","project", None, QApplication.UnicodeUTF8).title()
        MyFileDialog.setNameFilters(("%s Web (*.htm* *.xml)" % (zElt0), "%s HTML (*.htm*)" % (zElt0), "%s eXtensible Markup Language (*.xml *.XML)" % (zElt0), "%s QSphere (*.qsp)" % (zElt1), \
                                     "%s QSphere (*.qsr)" % (zElt0), "%s CSV (*.csv)" % (zElt0), "%s PDF (*.pdf)" % (zElt0))) 
        MyFileDialog.setViewMode(QFileDialog.Detail)
        MyFileDialog.setDirectory(InitDir)
        MyFileDialog.setFileMode(QFileDialog.ExistingFile) 
        MyFileDialog.setAcceptMode(QFileDialog.AcceptOpen)

        FixeLabelsFileDialog(self, MyFileDialog, 0, True)
        
        if MyFileDialog.exec_():
            fileName = "%s" % (MyFileDialog.selectedFiles()[0])
            if fileName!="" :
               zSuffix = QFileInfo(fileName).suffix().lower()
               if zSuffix == "pdf" :
                  self.viewHTML.ToOpenURL = fileName
                  self.viewHTML.MakeOpenURL()  
               else : self.selfActiveLink(fileName)
               self.initDir = os.path.dirname(fileName)


    def go_accueil(self):
        FixeEnabledHistory(self, self.viewHTML)
        ActiveLink(self, self.homeurl, False, self.viewHTML)

    def changePageURL(self):
        zPage = self.viewHTML.page()
        linkact = zPage.action(QWebPage.OpenLink)

    def LoadXMLEditor(self):
        zUrl = self.eURL.currentText() 
        if zUrl.find("filexml:")!=-1 :
            zUrl = zUrl.replace("filexml:","")
            zUrl = urllib.unquote(zUrl)

            editor = xmlEditor(self, zUrl )
            editor.setWindowTitle("%s : %s" % (editor.racTitle, zUrl))
            MakeWindowIcon(editor, "editxml.png")
            editor.show()
            editor.LoadFile()


            
class MyWebPage(QWebPage):
    formSubmitted = pyqtSignal(QUrl)
    
    def __init__(self, parent=None): super(MyWebPage, self).__init__(parent)

    def acceptNavigationRequest(self, frame, req, nav_type):
        zElts, zQueryURL, zTestQUERY = req.url().toString().split("/"), [], False
        zQueryURL = zElts[-1].split("=")
        if zQueryURL != [] :
           if zQueryURL[0] in self.parent.Dialog.ListOfqueryURL : zTestQUERY = True
           if zTestQUERY :
              self.parent.Dialog.viewHTML.telech = Telecharge(req.url(), self.parent.Dialog, None, "*.xml", self.parent.Dialog.duration_info, self.parent.Dialog.duration_warning, False)
              self.parent.Dialog.viewHTML.telech.fintelecharge.connect(self.parent.Dialog.viewHTML.telecharge_ok)
              if  self.parent.objectName() == "tempoViewer" : self.parent.close()
              return super(MyWebPage, self).acceptNavigationRequest(frame, req, nav_type)
        
        if nav_type == QWebPage.NavigationTypeFormSubmitted:
            self.properties = {}
            for header in req.rawHeaderList(): self.properties["%s" % (header)] = "%s" % (req.rawHeader(header))
            self.formSubmitted.emit(req.url())
        return super(MyWebPage, self).acceptNavigationRequest(frame, req, nav_type)

    
class WebView(QWebView):
    def __init__(self, parent=None):
        QWebView.__init__(self, parent)
        self.ToCopy = ""
        self.current_url = QUrl("")
        self.fileName = self.TypeMime = None
        self.parent = parent
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu_requested)

        self.setPage(MyWebPage())

        self.setPage(MyWebPage())
        self.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.page().parent = self
        self.page().unsupportedContent.connect(self.unsupportedContent)
        self.page().linkClicked.connect(self.GoLink) 
        self.page().formSubmitted.connect(self.handleFormSubmitted)


    def createWindow(self, windowType):
        if windowType == QtWebKit.QWebPage.WebBrowserWindow:
            self.webView = WebView()
            self.webView.setObjectName("tempoViewer")
            self.webView.Dialog = self.Dialog 
            self.webView.Metadata = self.Metadata 
            self.webView.duration_info = self.duration_info
            self.webView.duration_warning = self.duration_warning 
            self.webView.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            return self.webView
        return super(WebView, self).createWindow(windowType)
        
        

    def handleFormSubmitted(self, url):
        path = url.path()
        if path.lower().find("search") == -1 :
            zDoc = self.page().mainFrame()
            inputs = zDoc.findAllElements("input")
            data, fileName = {}, ""
            for item in  inputs :
                data[item.attribute("name")] = item.attribute("value")
                if item.attribute("name") == "nom" : fileName = item.attribute("value")

            if data != {} : data = urllib.urlencode(data)
            headers = {"Content-Type" : "application/x-www-form-urlencoded"}
            performUrl = url.toString()+"?"+data
            data = None
            self.telech = Telecharge(QUrl(performUrl), self.Dialog, fileName, "*.zip", self.duration_info, self.duration_warning, False)
            self.telech.fintelecharge.connect(self.Dialog.viewHTML.telecharge_ok)
        

    def initWebView(self, zDialog, metadata, duration_info, duration_warning):
        self.Dialog = zDialog
        self.Metadata = metadata
        self.duration_info = duration_info
        self.duration_warning = duration_warning
        
    def context_menu_requested(self, point):
        self.imageurl = None
        context_menu = QMenu()
        page = self.page()
        frame = page.currentFrame()
        if unicode(self.selectedText()):
            menuIcon = getThemeIcon("copier.png")
            zText = (QApplication.translate("QSphere", "Copy", None, QApplication.UnicodeUTF8))
            self.copy = context_menu.addAction(QIcon(menuIcon), zText)
            self.ToCopy = unicode(self.selectedText())
            self.copy.triggered.connect(self.MakeToCopy)

            zTableWidget = ("tablelocalisator", "tableformats", "tablemotsclefsf","tableemprises","tablespecifications")
            zNameTableWidget = ("Identificator", "Format", "Mot clef", "Emprise", "Specification")
            zTableWidgetCols = ((0,1), (0,2), (0,2), (0,1,2,3), (0,2))

            Subsend_menu = menuTableWidget = []
            counterMenu = 0
            
            if self.Metadata != None and self.Metadata.objectName() == "DialogMetaData" : 
                zText = QApplication.translate("QSphere", "Send to", None, QApplication.UnicodeUTF8)
       
                send_menu = QMenu(zText)
                menuIcon = getThemeIcon("sendtometadata.png")
                self.ToSendto = unicode(self.selectedText())

                zTextComp = QApplication.translate("QSphere", "Add an extent", None, QApplication.UnicodeUTF8)
                self.sendto_newE = context_menu.addAction(QIcon(menuIcon), "%s" % (zTextComp))
                self.sendto_newE.setObjectName("Ajouter_6_tableemprises")
                self.sendto_newE.triggered.connect(self.SendToNewParentWidget)

                zIndex = self.Metadata.tabWidget.currentIndex()
                for i in range(len(zTableWidget)):
                    zObj = getWidget(self.Metadata, zTableWidget[i])
                    if zObj :
                       if zNameTableWidget[i] == "Emprise" :
                          if zObj.rowCount()==1 :
                              zAction = send_menu.addAction(QIcon(menuIcon), "%s %s" % (zNameTableWidget[i], 0))
                              zAction.setObjectName("%s %s %s" % (zTableWidget[i], 0, 0))
                              zAction.triggered.connect(self.SendToParentWidget)
                          else : Subsend_menu.append(QMenu("%s" % (zNameTableWidget[i])))
                              
                          
                       for line in range(zObj.rowCount()):
                           if zNameTableWidget[i] != "Emprise" :
                               Subsend_menu.append(QMenu("%s %s" % (zNameTableWidget[i], line)) )
                               for col in range(len(zTableWidgetCols[i])):
                                   zTextComp = zObj.horizontalHeaderItem(zTableWidgetCols[i][col]).text() 
                                   zAction = Subsend_menu[counterMenu].addAction(QIcon(menuIcon), "%s" % (zTextComp))
                                   zAction.setObjectName("%s %s %s" % (zTableWidget[i], line, zTableWidgetCols[i][col]))
                                   zAction.triggered.connect(self.SendToParentWidget)
                               send_menu.addMenu(Subsend_menu[counterMenu])
                               counterMenu+= 1
                           else :
                               if zObj.rowCount()> 1 :     
                                  zAction = Subsend_menu[counterMenu].addAction(QIcon(menuIcon), "%s %s" % (zNameTableWidget[i], line))
                                  zAction.setObjectName("%s %s %s" % (zTableWidget[i], line, 0))
                                  zAction.triggered.connect(self.SendToParentWidget)

                       if zNameTableWidget[i] == "Emprise" and zObj.rowCount()> 1 :
                           send_menu.addMenu(Subsend_menu[counterMenu])
                           counterMenu+= 1                            

                context_menu.addMenu(send_menu)
                self.Metadata.tabWidget.setCurrentIndex(zIndex) #self.Metadata.listeOnglets.setCurrentIndex(zIndex)
                
            elif self.Metadata != None and self.Metadata.objectName() =="ViewerTableWidget" :

                 zText = QApplication.translate("QSphere", "Send to", None, QApplication.UnicodeUTF8)
       
                 send_menu = QMenu(zText)
                 menuIcon = getThemeIcon("sendtometadata.png")
                 self.ToSendto = unicode(self.selectedText())
                 
                 zActionRac = QApplication.translate("QSphere", "Add a ", None, QApplication.UnicodeUTF8)
                 zTextComp = "Item"
                 if self.Metadata.tableWidget.objectName() in zTableWidget :
                    i = zTableWidget.index(self.Metadata.tableWidget.objectName())
                    zTextComp = zNameTableWidget[i]
                    
                    self.sendto_newF = context_menu.addAction(QIcon(menuIcon), "%s %s" % (zActionRac, zTextComp))
                    self.sendto_newF.setObjectName("Ajouter_6_%s" % self.Metadata.tableWidget.objectName())
                    self.sendto_newF.triggered.connect(self.SendToNewParentWidget)

                 zObj = getWidget(self.Metadata, self.Metadata.tableWidget.objectName())
                 if zObj :
                       if self.Metadata.tableWidget.objectName() in zTableWidget :
                           i = zTableWidget.index(self.Metadata.tableWidget.objectName())
                           for line in range(zObj.rowCount()):
                               if self.Metadata.tableWidget.objectName() != "tableemprises" :
                                   Subsend_menu.append(QMenu("%s %s" % (zNameTableWidget[i], line)) )
                                   for col in range(len(zTableWidgetCols[i])):
                                       zTextComp = zObj.horizontalHeaderItem(zTableWidgetCols[i][col]).text() 
                                       zAction = send_menu.addAction(QIcon(menuIcon), "%s %s" % (zTextComp, line))
                                       zAction.setObjectName("%s %s %s" % (zTableWidget[i], line, zTableWidgetCols[i][col]))
                                       zAction.triggered.connect(self.SendToParentWidget)
                                   counterMenu+= 1
                               else :
                                   if zObj.rowCount()>= 1 :     
                                      zAction = send_menu.addAction(QIcon(menuIcon), "%s %s" % (zNameTableWidget[i], line))
                                      zAction.setObjectName("%s %s %s" % (zTableWidget[i], line, 0))
                                      zAction.triggered.connect(self.SendToParentWidget)

                 context_menu.addMenu(send_menu)

        hit_test = frame.hitTestContent(point)
        
        if unicode(hit_test.linkUrl().toString()):
            menuIcon = getThemeIcon("copierlink.png")
            zText = (QApplication.translate("QSphere", "Copy link", None, QApplication.UnicodeUTF8))
            self.copyURL = context_menu.addAction(QIcon(menuIcon), zText)
            self.ToCopyURL = unicode(hit_test.linkUrl().toString())
            self.copyURL.triggered.connect(self.MakeToCopyURL)

            
            zText = QApplication.translate("QSphere", "Force open link", None, QApplication.UnicodeUTF8)
            self.openLink = context_menu.addAction(QIcon(menuIcon), zText)
            self.ToOpenLink = unicode(hit_test.linkUrl().toString())
            self.openLink.triggered.connect(self.MakeOpenLink)


            zText = QApplication.translate("QSphere", "Open link in my default navigator", None, QApplication.UnicodeUTF8)
            self.openURL = context_menu.addAction(QIcon(menuIcon), zText)
            self.ToOpenURL = unicode(hit_test.linkUrl().toString())
            self.openURL.triggered.connect(self.MakeOpenURL)
            
        context_menu.addSeparator()

           
        menuIcon = getThemeIcon("selectall.png")
        zText = (QApplication.translate("QSphere", "Select all", None, QApplication.UnicodeUTF8))
        self.selall = QAction(QIcon(menuIcon), zText, self)
        context_menu.addAction(self.selall)
        self.selall.triggered.connect(self.SelectAll)
        
        context_menu.addSeparator()
        
        menuIcon = getThemeIcon("coller.png")
        zText = (QApplication.translate("QSphere", "Paste", None, QApplication.UnicodeUTF8))
        self.paste = QAction(QIcon(menuIcon), zText, self)
        context_menu.addAction(self.paste)
        self.paste.triggered.connect(self.MakeToPaste)
        
        if unicode(page.mainFrame().hitTestContent(point).element().tagName()).lower()== "img":
            self.imageurl =  page.mainFrame().hitTestContent(point).imageUrl()
            tempoSRC = page.mainFrame().hitTestContent(point).element().attribute("src")
            tempoSRC = tempoSRC.replace("\\","/")

            if tempoSRC!="" :
               self.fileName = tempoSRC.rsplit("/",1)[1]
               self.TypeMime = "*.%s" % (self.fileName.rsplit(".",1)[1])
            
            context_menu.addSeparator()

            menuIcon = getThemeIcon("saveas.png")
            zText = (QApplication.translate("QSphere", "Save image as ...", None, QApplication.UnicodeUTF8))
            self.downloadimg = QAction(QIcon(menuIcon), zText, self)
            context_menu.addAction(self.downloadimg)
            self.downloadimg.triggered.connect(self.DownloadImg)

            self.paste.setEnabled(False)
   
        context_menu.exec_(self.mapToGlobal(point))


    def DownloadImg(self):
        self.telech = Telecharge(self.imageurl, self.Dialog, self.fileName, self.TypeMime, self.duration_info, self.duration_warning, True)
        self.telech.fintelecharge.connect(self.telecharge_ok)


    def unsupportedContent(self, reply, outfd=None):

        if not reply.error():
            url = self.current_url.toString()    
            try : 
                zElts = urlparse.urlparse(url)
                zFile = zElts.path.split("/")[-1]
                zExtension = zFile.split(".")[-1]
            except : zFile, zExtension = "", "*"    
           
            self.telech = Telecharge(reply.url(), self.Dialog, zFile, "*.%s" % (zExtension), self.duration_info, self.duration_warning, False)
            self.telech.fintelecharge.connect(self.telecharge_ok)
        else :
            zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
            zMsg = QApplication.translate("QSphere","Error on unsupported content :", None, QApplication.UnicodeUTF8)
            SendMessage(self.Dialog, zTitle , "%s %s" % (zMsg, reply.errorString()), QgsMessageBar.WARNING, self.duration_warning)


    def telecharge_ok(self, ok):
        if ok:
            zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
            zMsg = QApplication.translate("QSphere","Donwload success ! File save as :", None, QApplication.UnicodeUTF8)
            SendMessage(self.Dialog, zTitle , "%s %s" % (zMsg, self.fileName), QgsMessageBar.INFO, self.duration_info)
        else:
            zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
            zMsg = QApplication.translate("QSphere","Donwload error ! File not save ...", None, QApplication.UnicodeUTF8)
            SendMessage(self.Dialog, zTitle , zMsg, QgsMessageBar.WARNING, self.duration_warning)


    def SendToNewParentWidget(self):
        zActionName = self.sender().objectName()
        zButWidget = getWidget(self.Metadata, zActionName)
        
        if zButWidget or not zButWidget :
           zActionName = zActionName.split("_")[2]
           zWidget = getWidget(self.Metadata, zActionName)
           if zWidget :
              if zActionName == "tableemprises":
                 zEmprise = self.ToSendto.split(",")
                 if len(zEmprise)!= 4 : return
                 else :
                    self.Metadata.AddLine()
                    zLine = zWidget.rowCount()-1
                    self.FixeValuesForEmprise(zWidget, zLine, zEmprise)
              else :
                 self.Metadata.AddLine()
                 zLine = zWidget.rowCount()-1
                 zWidget.cellWidget(zLine, 0).setText(self.ToSendto)
                  

    def SendToParentWidget(self):
        zActionName = self.sender().objectName()
        if zActionName.find(" ") :
           zInfos = zActionName.split(" ") 
           zActionName = zInfos[0]
        zWidget = getWidget(self.Metadata, zActionName)
        if zWidget :
           if type(zWidget)==QLineEdit: zWidget.setText(self.ToSendto)
           elif type(zWidget)in (QTextEdit, MyTextEdit) : zWidget.setPlainText(self.ToSendto)
           elif type(zWidget) in (QTableWidget, MyTableWidget) :
               if len(zInfos)== 3 : zCol = int(zInfos[2])
               zLine = int(zInfos[1])
               if zActionName == "tableemprises" :
                  zEmprise = self.ToSendto.split(",")
                  if len(zEmprise)!= 4 : return
                  else :  self.FixeValuesForEmprise(zWidget, zLine, zEmprise)
               else :
                  zWidget.cellWidget(zLine, zCol).setText(self.ToSendto)

    def FixeValuesForEmprise(self, zWidget, zLine, zEmprise):
        if convertSTR(zEmprise[0], "float") and convertSTR(zEmprise[1], "float") and convertSTR(zEmprise[2], "float") and convertSTR(zEmprise[3], "float") : 
           zWidget.cellWidget(zLine, 0).setValue(float(zEmprise[3]))
           zWidget.cellWidget(zLine, 1).setValue(float(zEmprise[1]))
           zWidget.cellWidget(zLine, 2).setValue(float(zEmprise[0]))
           zWidget.cellWidget(zLine, 3).setValue(float(zEmprise[2])) 

    def MakeOpenLink(self):
        zUrl = self.ToOpenLink
        reLinked = False
        if self.Dialog.eURL.findText(zUrl)==-1 : self.Dialog.eURL.addItem(zUrl)
        else : reLinked = True
        self.Dialog.eURL.setCurrentIndex(self.Dialog.eURL.findText(zUrl))
        self.current_url = QUrl(zUrl)
        if reLinked : ActiveLink(self.Dialog, self.current_url, True, self)
        
    def MakeOpenURL(self):
        try : webbrowser.open(self.ToOpenURL)
        except :
            zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
            zMsg = QApplication.translate("QSphere","Try to open Web navigator for https protocol ...", None, QApplication.UnicodeUTF8)
            SendMessage(self.Dialog, zTitle , zMsg, QgsMessageBar.WARNING, 3)
        
    def MakeToCopy(self): QApplication.clipboard().setText(self.ToCopy)
    def MakeToCopyURL(self): QApplication.clipboard().setText(self.ToCopyURL)
    def MakeToPaste(self): self.page().triggerAction(QWebPage.Paste)
    def SelectAll(self): self.page().triggerAction(QWebPage.SelectAll)
    
    def GoLink(self, url):
        reLinked = False
        zUrl = url.toString()
        if self.Dialog.eURL.findText(zUrl)==-1 : self.Dialog.eURL.addItem(zUrl)
        else : reLinked = True
        self.Dialog.eURL.setCurrentIndex(self.Dialog.eURL.findText(zUrl))
        self.current_url = url
        if reLinked : ActiveLink(self.Dialog, self.current_url, True, self)


def FixeEnabledHistory(zDialog, MyWebView):
    zDialog.BackButton.setEnabled(True) if MyWebView.history().backItems(100) else zDialog.BackButton.setEnabled(False)
    zDialog.FowardButton.setEnabled(True) if MyWebView.history().forwardItems(100)  else zDialog.FowardButton.setEnabled(False)

def CheckingListeXSLT(self, url):
    if self.listeXSLT == [] and url.startswith("filexml:"): url = url.replace("filexml:", "")
    return url   
    
def ActiveLink(zDialog, zUrl, isUnicode, MyWebView) :
        zPath = getThemeIcon(os.path.dirname(__file__))
        zAnchor = zDialog.HTML = ""
        isXML = False

        zUrl = CheckingListeXSLT(zDialog, zUrl)
        try :
            if isUnicode : zUrl = "%s" % (unicode(zUrl.toString()))
        except : return
        
        if zDialog.eURL.findText(zUrl)==-1 : zDialog.eURL.addItem(zUrl)
        
        if zUrl.find("xml:")!=-1 or zUrl.find("file:")!=-1 :
           zDialog.eURL.setStyleSheet("""QComboBox {background-color:#AEEE00;}"""
                                      """QComboBox QAbstractItemView {background-color:#AEEE00; min-width:%spx;}""" % (zDialog.minwidth)
                                      )
        zDialog.fileExtension, zDialog.isXML, zDialog.iconName = ".html", False, "navigatorweb.png"
    
        if zUrl.find("file:")!=-1 or zUrl.find("fileHTML:")!=-1 :
           zDialog.iconName = "info.png" 
           zUrl = zUrl.replace("file:///","")
           if zUrl.find("file:")!=-1 : zUrl = zUrl.replace("file:","")
           if zUrl.find("fileHTML:")!=-1 : zUrl = zUrl.replace("fileHTML:","")
           if zUrl.find(".html#")!= -1 :
              zTemp = zUrl.split("#")
              zUrl = zTemp[0]
              zAnchor = zTemp[1]
           MyWebView.setStyleSheet("background-color:rgb(255,255,255); padding: 7px ; color:rgb(255,255,255)")

           zTest, zFileHelp = fileRessourceExist(None, zUrl)
           if zFileHelp == "" :
               zFileHelp = "/ressources/html/%s" % (zUrl)
               zTest, zFileHelp = fileRessourceExist(None, zFileHelp)
           if zFileHelp!= "" :
               if zDialog.eURL.findText(zFileHelp)==-1 : zDialog.eURL.addItem(zFileHelp)
               zDialog.eURL.setCurrentIndex(zDialog.eURL.findText(zFileHelp))
               zDialog.eURL.setStyleSheet("""QComboBox {background-color:#AEEE00;}"""
                                      """QComboBox QAbstractItemView {background-color:#AEEE00; min-width:%spx;}""" % (zDialog.minwidth)
                                      )               
               zText = ""

               if zDialog.emprise!=[]: sEmprise = "<script>var bounds = new OpenLayers.Bounds(%s, %s, %s, %s);</script>" % (zDialog.emprise[2], zDialog.emprise[1], zDialog.emprise[3], zDialog.emprise[0])
               else : sEmprise = "<script>var bounds = new OpenLayers.Bounds(-9.6199999999999992, 41.18, 10.300000000000001, 51.539999999999999);</script>"

               f = codecs.open(zFileHelp, encoding='cp1252') if zUrl.find("fileHTML:")==-1 else  codecs.open(zFileHelp) #test utf_8, utf_32
               try :
                   for line in f: zText+= line
               except : pass

               if zText.find("%SCRIPT_EMPRISE%")!= -1: zText = zText.replace("%SCRIPT_EMPRISE%", sEmprise)
               if zText.find("%LOADER(IMAGES)%")!= - 1:
                  zList = ""
                  zList = listdirectory(MyWebView.parent(), "%s/icons/" % (zPath))
                  zText = zText.replace("%LOADER(IMAGES)%",zList)

               baseUrl = QUrl.fromLocalFile(zFileHelp) 
               MyWebView.setHtml(zText, baseUrl)
               f.close()
               if zAnchor != "" :
                  zTest = MyWebView.findText(zAnchor)
                  if not zTest : MyWebView.page().mainFrame().scrollToAnchor(zAnchor) 
               
           else : MyWebView.setHtml(QApplication.translate("QSphere", "Resource file missing !", None, QApplication.UnicodeUTF8))
           
        elif zUrl.find("filexml:")!=-1 :
            zDialog.isXML = True
            zDialog.iconName = "viewhtml.png"
            zUrl = zUrl.replace("filexml:","")
            zUrl = urllib.unquote(zUrl)

            zDialog.initDir = CorrigePath(os.path.dirname(zUrl))
            fileName, zDialog.fileExtension = os.path.splitext(zUrl)

            if zDialog.fileExtension.lower() == ".xml" :
                #Primary XSLT
                baseUrl = ""
                qry = QXmlQuery(QXmlQuery.XSLT20)
                zTest, XSL = fileRessourceExist(zDialog, "xml/xsl/%s" % (zDialog.PrimaryXSLT.currentText()))
                if XSL!= "" : baseUrl = QUrl.fromLocalFile(XSL)
                qry.setFocus(QUrl.fromLocalFile(zUrl)) 
                qry.setQuery(QUrl.fromLocalFile(XSL)) 
                HTML = qry.evaluateToString()

                if HTML is None:
                   #Secondary XSLT 
                   zTest, XSL = fileRessourceExist(zDialog, "xml/xsl/%s" % (zDialog.SecondaryXSLT.currentText()))
                   if XSL!= "" : baseUrl = QUrl.fromLocalFile(XSL)
                   qry.setFocus(QUrl.fromLocalFile(zUrl))
                   qry.setQuery(QUrl.fromLocalFile(XSL)) 
                   HTML = qry.evaluateToString()
                   if HTML is None :
                      HTML = QApplication.translate("QSphere", "File parsing XSLT error !<br>Invalid XSLT or XML file !", None, QApplication.UnicodeUTF8)
                      HTML = "<div align='center'><img src='%s'><br><br>%s</div>" % (getThemeIcon("parsing_error.png"), HTML)
                      zDialog.PrimaryXSLT.setStyleSheet("""QComboBox {background: red;}""")
                      zDialog.SecondaryXSLT.setStyleSheet("""QComboBox {background: red;}""")
                   else :
                      HTML = NetHTML(HTML)
                      zDialog.PrimaryXSLT.setStyleSheet("""QComboBox {background: red;}""")
                      zDialog.SecondaryXSLT.setStyleSheet("""QComboBox {background: green;}""")
                      
                else:
                    HTML = NetHTML(HTML)
                    zDialog.PrimaryXSLT.setStyleSheet("QComboBox {background: green;}")
                    zDialog.SecondaryXSLT.setStyleSheet("QComboBox {background: white;}")

                isXML = True
                MyWebView.setHtml(HTML, baseUrl)
                zDialog.HTML = HTML
                zDialog.oldurl = CorrigePath(os.path.dirname(baseUrl.toString()))


        elif zUrl == "#blank" :
            baseUrl = QUrl.fromLocalFile(os.path.dirname(__file__))
            MyWebView.setHtml("", baseUrl)
            zDialog.eURL.setStyleSheet("QComboBox {background-color:#AEEE00;}"
                          "QComboBox QAbstractItemView {background-color:#AEEE00; min-width:%spx;}" % (zDialog.minwidth)
                          )
               
        else :

            if QUrl(zUrl).isValid() :
               zFile = None
               zFileUrl = urllib.unquote(zUrl)
               zTestQUERY = False
               if os.path.exists(zFileUrl) :
                   zFile = QFileInfo(zFileUrl)
                   zSuffixe = zFile.suffix().lower()
                   zTest = FileIsRaster(zFileUrl)
                   if (zSuffixe not in ("html", "htm", "qsp", "qsr", "csv") and not zTest) or (zSuffixe in ("ecw", "jp2", "view") and zTest): 
                       baseUrl = QUrl.fromLocalFile(zFileUrl)
                       HTML = MakeFileInfosToHTML(zDialog, zFile, zSuffixe) 
                       MyWebView.setHtml(HTML, baseUrl)
                       zDialog.viewHTML.ToOpenURL = zFileUrl
                       return
               else : 
                   zElts, zQueryURL, zTestQUERY = zUrl.split("/"), [], False
                   zQueryURL = zElts[-1].split("=")
                   if zQueryURL != [] : 
                      if zQueryURL[0] in zDialog.ListOfqueryURL : zTestQUERY = True
                   
               if zTestQUERY :                   
                   zDialog.viewHTML.telech = Telecharge(QUrl(zUrl), zDialog, None, "*.xml", zDialog.duration_info, zDialog.duration_warning, False)
                   zDialog.viewHTML.telech.fintelecharge.connect(zDialog.viewHTML.telecharge_ok)
               else :
                       zDialog.eURL.setStyleSheet("QComboBox {background-color:#AEEE00;}"
                                  "QComboBox QAbstractItemView {background-color:#AEEE00; min-width:%spx;}" % (zDialog.minwidth)
                                  )

                       if zFile != None :
                           if zSuffixe in ("qsp", "qsr") :
                              baseUrl = QUrl.fromLocalFile(zUrl)
                              myfile = open(zFileUrl, 'r')
                              myfileText = myfile.readlines()
                              myfile.close()
                              HTML = ""
                              for k in range(len(myfileText)): HTML+= "%s" % (MarkerText(zDialog, myfileText[k]))
                              MyWebView.setHtml(HTML, baseUrl)
                           else :
                              MyWebView.load(QUrl(zUrl))
                       else :

                           try : MyWebView.load(QUrl(zUrl))
                           except : pass
                           
            else :
               zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
               zMsg = QApplication.translate("QSphere","Invalid URL ! Use open function if necessary for local ressources ...", None, QApplication.UnicodeUTF8)
               SendMessage(zDialog, zTitle , zMsg, QgsMessageBar.WARNING, zDialog.duration_warning)

        zCond = (zDialog.HTML!="") 
        zDialog.SaveButton.setEnabled(zCond)
        zDialog.EditorXMLButton.setEnabled(zCond)

        if not isXML : zDialog.oldurl = ""
        FixeEnabledHistory(zDialog, MyWebView)    
        page = MyWebView.page()
        page.setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        MakeWindowIcon(zDialog, zDialog.iconName)

"""
def NetHTML(HTML):
    #QXmlPattern not support CDATA section
    HTML = HTML.replace('&amp;', '&')
    HTML = HTML.replace('&gt;', '>')
    HTML = HTML.replace('&lt;', '<')
    return HTML
"""
class Telecharge(QNetworkAccessManager):
    fintelecharge = pyqtSignal(bool)
    def __init__(self, url, dialog, fileName, typeMime, duration_info, duration_warning, silentmode) : 
        QNetworkAccessManager.__init__(self)
        self.initDir = CorrigePath(os.path.dirname(__file__))
        self.Dialog = dialog
        self.messageBuffer = QByteArray()
        self.fileName, self.typeMime = fileName, typeMime
        self.duration_info = duration_info
        self.duration_warning = duration_warning
        self.silentmode = silentmode
        self.reply = self.get(QNetworkRequest(url))
        self.reply.readyRead.connect(self.readData)
        self.reply.finished.connect(self.finished)
        self.url = url
        self.Dialog.startMovie2()

    @pyqtSlot()
    def readData(self):
        self.messageBuffer+= self.reply.readAll()
        if not self.silentmode :
            zMsg = "%s (%s) %s" % (QApplication.translate("QSphere","Read from download stream ", None, QApplication.UnicodeUTF8), convertSize(len(self.messageBuffer)), self.reply.url() )
            zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8) 
            SendMessage(self.Dialog, zTitle , zMsg, QgsMessageBar.INFO, 1)

 
    @pyqtSlot()
    def finished(self):
        self.Dialog.barInfo.clearWidgets()
        self.Dialog.barInfo.setVisible(False)
        self.Dialog.stopMovie2()
        
        filtermime = "*.*" if self.typeMime == None else self.typeMime
        initDir = self.initDir if self.fileName == None else "%s%s" % (self.initDir, self.fileName)


        if not filtermime in ("*.htm", "*.xml", "*.html") :
           if filtermime == "*.*" :
               typemime, filtermime = "%s" % (self.reply.header(0)), "*.*"
               if typemime.find(";")!=-1 :
                   typemime = typemime.rsplit(";",1)[0]
                   if typemime.find("/")!=-1 :
                      filtermime = "*.%s" % (typemime.rsplit("/",1)[1].lower()) 
           self.saveFile(filtermime)
           return


        #For XML
        if filtermime == "*.*" :
           typemime, filtermime = "%s" % (self.reply.header(0)), "*.*"
           if typemime.find(";")!=-1 :
               typemime = typemime.rsplit(";",1)[0]
               if typemime.find("/")!=-1 :
                  filtermime = "*.%s" % (typemime.rsplit("/",1)[1].lower())


        if filtermime == "*.xml" :
            dataXML = StringIO(self.messageBuffer)
            try :
                tree = ET.parse(dataXML)
                root = tree.getroot()
            except : tree, root = None, None

            if root == None :
                zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
                zMsg = QApplication.translate("QSphere","Error on download stream ", None, QApplication.UnicodeUTF8) 
                SendMessage(self.Dialog, zTitle , "%s :\n%s" % (zMsg, self.messageBuffer), QgsMessageBar.INFO, self.duration_info)                
                return

            self.fileName = ""

            if root.tag == '{http://www.isotc211.org/2005/gmd}MD_Metadata':
                   myISO = xmlISOparser(None, StringIO(self.messageBuffer) , 'MEDDE', 'fr') 
                   myISO.createISOdataStructure(True)

                   if myISO.getTagDictionnary() :
                               try :
                                   zCond = True if (self.Dialog.parent)!= None and self.Dialog.parent.objectName()=="DialogMetaData" else False
                               except : zCond = False 
                               
                               zTitle = QApplication.translate("QSphere","Request for confirmation", None, QApplication.UnicodeUTF8)
                               zMsg = QApplication.translate("QSphere","Directly Load Data in Main Window ?", None, QApplication.UnicodeUTF8)
                               zYes = QApplication.translate("QSphere","Yes", None, QApplication.UnicodeUTF8)
                               zNo = QApplication.translate("QSphere","No", None, QApplication.UnicodeUTF8)

                               MyMsgBoxDialog = QMessageBox(self.Dialog)

                               MyMsgBoxDialog.setWindowTitle(zTitle)
                               MyMsgBoxDialog.setIcon(QMessageBox.Question)

                               groupBox1 = QGroupBox(MyMsgBoxDialog)
                               groupBox1.setFixedSize(420, 130)
                               groupBox1.setObjectName("groupBox1")

                               zRadioButton1 = QRadioButton(groupBox1)
                               zRadioButton1.setObjectName("zRadioButton1")
                               zRadioButton1.setAccessibleName("zRadioButton1")
                               zRadioButton1.setFixedSize(420, 25)
                               zRadioButton1.setGeometry(5, 5, 420, 25)
                               zRadioButton1.setText("%s" % (QApplication.translate("QSphere","Directly Load Data in Main Window ?", None, QApplication.UnicodeUTF8)))
                               zRadioButton1.setChecked(True) if zCond else zRadioButton1.setChecked(False)
                               if not zCond : zRadioButton1.setEnabled(False)

                               zRadioButton2 = QRadioButton(groupBox1)
                               zRadioButton2.setObjectName("zRadioButton2")
                               zRadioButton2.setAccessibleName("zRadioButton2")
                               zRadioButton2.setFixedSize(420, 25)
                               zRadioButton2.setGeometry(5, 40, 420, 25)
                               zRadioButton2.setText("%s" % (QApplication.translate("QSphere","Open a new Main Window ?", None, QApplication.UnicodeUTF8)))
                               if not zCond : zRadioButton2.setChecked(True)

                               zRadioButton3 = QRadioButton(groupBox1)
                               zRadioButton3.setObjectName("zRadioButton3")
                               zRadioButton3.setAccessibleName("zRadioButton3")
                               zRadioButton3.setFixedSize(420, 25)
                               zRadioButton3.setGeometry(5, 70, 420, 25)
                               zRadioButton3.setText("%s" % (QApplication.translate("QSphere","Save file as ...", None, QApplication.UnicodeUTF8))) 

                               zRadioButton4 = QRadioButton(groupBox1)
                               zRadioButton4.setObjectName("zRadioButton4")
                               zRadioButton4.setAccessibleName("zRadioButton4")
                               zRadioButton4.setFixedSize(420, 25)
                               zRadioButton4.setGeometry(5, 100, 420, 25)
                               zRadioButton4.setText("%s" % (QApplication.translate("QSphere", "Open link in my default navigator", None, QApplication.UnicodeUTF8))) 
    
                               zButtonAccept = QPushButton(MyMsgBoxDialog)
                               zButtonAccept.setObjectName("SaveButton")
                               zButtonAccept.setText(QApplication.translate("QSphere", "Apply", None, QApplication.UnicodeUTF8))
                               zButtonAccept.setFixedSize(100, 25)

                               zButtonReject = QPushButton(MyMsgBoxDialog)
                               zButtonReject.setObjectName("CloseButton")
                               zButtonReject.setText(QApplication.translate("QSphere", "Close", None, QApplication.UnicodeUTF8))
                               zButtonReject.setFixedSize(100, 25)

                               zButtonAccept.clicked.connect(MyMsgBoxDialog.accept)
                               zButtonReject.clicked.connect(MyMsgBoxDialog.reject)
                               

                               MyMsgBoxDialog.layout().addWidget(groupBox1,0,1,1,2)
                               MyMsgBoxDialog.layout().addWidget(zButtonAccept,4,1,1,1)
                               MyMsgBoxDialog.layout().addWidget(zButtonReject,4,2,1,1)

                               MyMsgBoxDialog.setStandardButtons(MyMsgBoxDialog.NoButton)

                               #ONE INSTANCE OR PERSISTENT ?
                               #ret = MyMsgBoxDialog.exec_()
                               i = len(self.Dialog.d)
                               
                               result = False
                               while True :
                                   ret = MyMsgBoxDialog.exec_()
                                   if ret == 1 : 
                                      if zRadioButton1.isChecked() : 
                                           zIndex = self.Dialog.parent.tabWidget.currentIndex()
                                           self.Dialog.parent.listImportCategories = []
                                           result = self.Dialog.parent.ReloadDataFromXML(myISO, None, zIndex)
                                      elif zRadioButton2.isChecked() :
                                           from doUI import DialogMetadata
                                           zObjRef = self.Dialog.MainPlugin if self.Dialog.parent == None else self.Dialog.parent
                                           try : zParent = zObjRef.parent
                                           except : zParent = zObjRef
                                           
                                           self.Dialog.d[i] = DialogMetadata(zObjRef.iface, zObjRef.langue, zObjRef.languageIndex, zObjRef.langs, zObjRef.languesDico, \
                                                              zObjRef.langueTR, zObjRef.formats, zObjRef.listCodecs, zObjRef.listTemporalSystem, \
                                                              zObjRef.listTypeRessources, zObjRef.listCountries, zObjRef.indexCountry, zObjRef.listCountriesCode, zObjRef.localeFullName, zParent)
                                           self.Dialog.d[i].show()
                                           self.Dialog.d[i].isFromDownload = self.Dialog
                                           zIndex = self.Dialog.d[i].tabWidget.currentIndex()
                                           self.Dialog.d[i].listImportCategories = []
                                           result = self.Dialog.d[i].ReloadDataFromXML(myISO, None, zIndex)
                                           zRadioButton1.setEnabled(True)
                                           i = len(self.Dialog.d)
                                           
                                      elif zRadioButton4.isChecked() :
                                           self.Dialog.viewHTML.ToOpenURL = self.reply.url().toString()
                                           self.Dialog.viewHTML.MakeOpenURL()
                                           
                                      elif zRadioButton3.isChecked() :
                                           zCond, self.fileName = False, "*.xml"
                                           try :
                                               self.fileName = "%s.xml" % (myISO.UUID[0][0]) if myISO.UUID[0][0]!="" else "*.xml"
                                           except :
                                               #zCond, self.fileName = False, "*.xml"
                                               for child in root :
                                                   if "fileIdentifier" in child.tag :
                                                       for elVal in child:
                                                           self.fileName = "%s.xml" % (elVal.text)
                                                           zCond = True
                                                   if zCond : break
                                           finally : pass

                                           self.saveFile(filtermime)

                                   else : return   


    def saveFile(self, filtermime):

       if len(self.messageBuffer) > 0 :

          zTitle = QApplication.translate("QSphere","Save file as ...", None, QApplication.UnicodeUTF8)
          MyFileDialog = QFileDialog(self.Dialog, zTitle)

          if filtermime!= "*.*" : MyFileDialog.setDefaultSuffix(filtermime.split(".")[1])
          MyFileDialog.setNameFilters((filtermime,))
          MyFileDialog.selectNameFilter(filtermime)
          MyFileDialog.selectFile(self.fileName.replace(":", "-"))
          MyFileDialog.setViewMode(QFileDialog.Detail)
          MyFileDialog.setDirectory(self.initDir)
          MyFileDialog.setAcceptMode(QFileDialog.AcceptSave)

          FixeLabelsFileDialog(self, MyFileDialog, 1, True)
          
          if MyFileDialog.exec_():
                fileName = FileNameWithExtension(self, MyFileDialog.selectedFiles()[0], MyFileDialog.selectedNameFilter())          
                self.initDir = os.path.dirname(fileName)
                saveFile = QFile(fileName)
                zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
                if (saveFile.open(QIODevice.WriteOnly)):
                    saveFile.write(self.messageBuffer)
                    saveFile.close()
                    self.Dialog.viewHTML.fileName = fileName
                    self.fintelecharge.emit(True)
                else:
                    self.fintelecharge.emit(False)

       elif len(self.messageBuffer) == 0 :       

            zTitle = QApplication.translate("QSphere","Warning", None, QApplication.UnicodeUTF8)
            zMsg = QApplication.translate("QSphere","Some troubleshooting to download the file ", None, QApplication.UnicodeUTF8)
            zMsg1 = QApplication.translate("QSphere", "Open link in my default navigator", None, QApplication.UnicodeUTF8)

            if QMessageBox.question(None, zTitle, "%s :\n%s\n%s ?" % (zMsg, self.url.toString(), zMsg1),
               QApplication.translate("QSphere","Validate", None, QApplication.UnicodeUTF8),
               QApplication.translate("QSphere","Cancel", None, QApplication.UnicodeUTF8)) ==  0 : 

               webbrowser.open(unicode(self.url.toString()))
