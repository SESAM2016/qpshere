import codecs, os.path
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from qsphere_tools import *
import doUI
import os
import ConfigParser
import datetime

from cswt_connector import *
import xml.etree.ElementTree as etree

class Ui_Dialog_Options(object):
  def setupUi(self):

    self._W, self._H = 835, 500
    self.setMinimumSize(QSize(self._W,self._H))
    self.setMaximumSize(QSize(self._W*1.5,self._H))
    self.setObjectName("DialogOptions")
    self.setAccessibleName("DialogOptions")
    self.resize(QSize(QRect(0,0,self._W,self._H).size()).expandedTo(self.minimumSizeHint()))
    self.setModal(True)
    self.setWindowFlags(Qt.WindowMaximizeButtonHint)
    self.setWindowTitle("%s" % (QApplication.translate("QSphere", "QSphere options", None, QApplication.UnicodeUTF8)))
    self.msgItem = QApplication.translate("QSphere","Item", None, QApplication.UnicodeUTF8)

    self.tabWidget = QTabWidget(self)
    self.tabWidget.setObjectName("tabWidget")
    self.tabWidget.setGeometry(QRect(205, 10, 615, 460))
    self.labelXMLFiles = "eXtensible Markup Language (*.xml *.XML)"
    self.InitDir = ""

    myPathIconvRightArrow = getThemeIcon("rightarrow.png")
    myPathIconvLeftArrow = getThemeIcon("leftarrow.png")
    self.tabWidget.setStyleSheet(
        """QTabBar::tab:selected {color: #5D5D5D;background-color: rgb(255,255,255);}"""
        """QTabBar::tab:!selected {color: rgb(255,255,255);background-color: #5D5D5D;border-bottom-color: #5D5D5D;}"""
        """QTabWidget:pane {margin: 1px,1px,1px,1px;background-color: rgb(255,255,255);}"""
        """QTabBar::tab {border: 0px solid rgb(0,149,48);border-bottom-color: rgb(255,255,255);border-top-left-radius: 0px;border-top-right-radius: 0px;height: 0px;width: 170px;background-color: rgb(255,255,255);}"""
        """QTabWidget{background-color: rgb(255,255,255);font: 75 10pt "Arial Rounded MT Bold";}"""
        """QTabWidget::tab-bar {left: 5px; bottom: -1px;background-color: rgb(0,0,0); } """
        """QTabBar::scroller {width: 0px;}"""
    )
    self.tabWidget.setTabPosition(QTabWidget.South) 
    self.tabWidget.setTabShape(QTabWidget.Rounded)
    self.tabWidget.setUsesScrollButtons(True)

    zTitle = (QApplication.translate("QSphere","Servers", None, QApplication.UnicodeUTF8), \
               QApplication.translate("QSphere","Time and Folders", None, QApplication.UnicodeUTF8), \
               QApplication.translate("QSphere","Parser and Editor", None, QApplication.UnicodeUTF8), \
               "CSW-T"
              )

    zIcons = ("servers.png", "timeandfolders.png", "editxml.png", "cswt.png") 

    zToolTipList = (QApplication.translate("QSphere","Server parameters : ", None, QApplication.UnicodeUTF8), \
               QApplication.translate("QSphere","Fix duration for process (Web queries, QgsMessageBox)", None, QApplication.UnicodeUTF8), \
               QApplication.translate("QSphere","Parser autocorrection parameters", None, QApplication.UnicodeUTF8), \
               QApplication.translate("QSphere","CSW-T parameters", None, QApplication.UnicodeUTF8)
              )

    self.listWidget = QListWidget(self)
    self.listWidget.setGeometry(QRect(10, 10, 200, 460))
    self.listWidget.setObjectName("listWidget")
    self.listWidget.setStyleSheet("* { font-size:12px; background-color:#5D5D5D; padding: 4px ; color:rgb(255,255,255)}"
                                  "QListWidget::item:selected {color: #5D5D5D;background-color: rgb(255,255,255);  padding: 12px;}")
    self.listWidget.setIconSize(QSize(42, 42))

    for i in range(1,len(zTitle)+1):
        zIcon = getThemeIcon(zIcons[i-1])
        zItem =  QListWidgetItem(QIcon(zIcon),zTitle[i-1],self.listWidget)
        zItem.setToolTip(zToolTipList[i-1])

        zTab = QWidget(self)
        zTab.setObjectName("tab%s" % (i))
        zTab.setAccessibleName(zTitle[i-1])
        
        self.tabWidget.addTab(zTab, zTitle[i-1])
        self.tabWidget.setTabToolTip(i-1, zToolTipList[i-1])


        if (i-1) == 0 :
          self.tab1 = zTab
          #Group Informations Server
          self.groupBoxServer = QGroupBox(zTab)
          self.groupBoxServer.setObjectName("groupBoxServer")
          self.groupBoxServer.setTitle(QApplication.translate("QSphere","Server parameters : ", None, QApplication.UnicodeUTF8))
          
          #Metadata
          zText = "%s" % (QApplication.translate("QSphere","Url Server for metadata : ", None, QApplication.UnicodeUTF8))
          self.labelServerMetadata = QLabel(self.groupBoxServer)
          self.labelServerMetadata.setText(zText)
          self.labelServerMetadata.setAccessibleDescription(zText)
          self.labelServerMetadata.setObjectName("LblserverMetadata")
          self.labelServerMetadata.setAccessibleName("LblserverMetadata")
          self.labelServerMetadata.setAlignment(Qt.AlignLeft)    

          self.serverMetadata = MyWebComboBox(self.groupBoxServer)
          self.serverMetadata.setEditable(True)
          self.serverMetadata.setObjectName("serverMetadata")
          self.serverMetadata.setAccessibleName("serverMetadata")
          self.serverMetadata.textChanged.connect(self.serverMetadata.VerifExpReg)

          zIcon = getThemeIcon("actions.png")
          zToolTip = QApplication.translate("QSphere","Actions ...", None, QApplication.UnicodeUTF8)
          self.ButServerMetadata = MyPushButton(self.groupBoxServer) 
          self.ButServerMetadata.initPushButton(40, 24,  0, 20, "ButServerMetadata", "", zToolTip, True, zIcon, 40, 24, True)

          self.contextMnuActions("ServerMetadata", self.ButServerMetadata)

          #keywords
          self.labelServerKeywords = QLabel(self.groupBoxServer)
          zText = "%s" % (QApplication.translate("QSphere","Url Server for keywords : ", None, QApplication.UnicodeUTF8))
          self.labelServerKeywords.setText(zText)
          self.labelServerKeywords.setAccessibleDescription(zText)          
          self.labelServerKeywords.setObjectName("LblserverKeywords")
          self.labelServerKeywords.setAccessibleName("LblserverKeywords")
          self.labelServerKeywords.setAlignment(Qt.AlignLeft)

          self.serverKeywords = MyWebComboBox(self.groupBoxServer)
          self.serverKeywords.setEditable(True)
          self.serverKeywords.setObjectName("serverKeywords")
          self.serverKeywords.setAccessibleName("serverKeywords")
          self.serverKeywords.textChanged.connect(self.serverKeywords.VerifExpReg)

          zIcon = getThemeIcon("actions.png")
          zToolTip = QApplication.translate("QSphere","Actions ...", None, QApplication.UnicodeUTF8)
          self.ButServerKeywords = MyPushButton(self.groupBoxServer) 
          self.ButServerKeywords.initPushButton(40, 24,  0, 20, "ButServerKeywords", "", zToolTip, True, zIcon, 40, 24, True)

          self.contextMnuActions("ServerKeywords", self.ButServerKeywords)
          
          #URL navigator
          self.labelServerNavigator = QLabel(self.groupBoxServer)
          zText = "%s" % (QApplication.translate("QSphere","Url for navigator : ", None, QApplication.UnicodeUTF8))
          self.labelServerNavigator.setText(zText)
          self.labelServerNavigator.setAccessibleDescription(zText)
          self.labelServerNavigator.setObjectName("LblserverNavigator")
          self.labelServerNavigator.setAccessibleName("LblserverNavigator")
          self.labelServerNavigator.setAlignment(Qt.AlignLeft)

          self.serverNavigator = MyWebComboBox(self.groupBoxServer)
          self.serverNavigator.setObjectName("serverNavigator")
          self.serverNavigator.setAccessibleName("serverNavigator")
          self.serverNavigator.setEditable(True)
          self.serverNavigator.textChanged.connect(self.serverNavigator.VerifExpReg)

          zIcon = getThemeIcon("actions.png")
          zToolTip = QApplication.translate("QSphere","Actions ...", None, QApplication.UnicodeUTF8)
          self.ButServerNavigator = MyPushButton(self.groupBoxServer) 
          self.ButServerNavigator.initPushButton(40, 24,  0, 20, "ButServerNavigator", "", zToolTip, True, zIcon, 40, 24, True)

          self.contextMnuActions("ServerNavigator", self.ButServerNavigator)

        elif (i-1) == 1 :
          self.tab2 = zTab
          #Group Informations InitDir
          self.groupBoxDir = QGroupBox(zTab)
          self.groupBoxDir.setObjectName("groupBoxDir")
          self.groupBoxDir.setTitle(QApplication.translate("QSphere","Init Directory (open, save files) : ", None, QApplication.UnicodeUTF8))

          self.labelRep = QLabel(self.groupBoxDir)
          self.labelRep.setText(QApplication.translate("QSphere","Folder : ", None, QApplication.UnicodeUTF8))
          self.labelRep.setObjectName("labelRep")
          self.labelRep.setAlignment(Qt.AlignLeft)    

          self.txtRep = MyTextEdit(self.groupBoxDir)
          self.txtRep.initTextEdit(self._W-310, 25, 10, 50, "txtRep", True, False, True, False, True)
          self.txtRep.setStyleSheet("color: black; background-color: #C0C0C0")

          self.BDefineRep = MyPushButton(self.groupBoxDir)
          self.BDefineRep.initPushButton(24, 24, 660, 32 , "BDefineRep", "", QApplication.translate("QSphere","Select a Folder", None, QApplication.UnicodeUTF8), True, getThemeIcon("folder.png"), 24, 24, True)


          #Group Informations Duration
          self.groupBoxDuration = QGroupBox(zTab)
          self.groupBoxDuration.setObjectName("groupBoxDuration")
          self.groupBoxDuration.setTitle(QApplication.translate("QSphere","Fix duration for process (Web queries, QgsMessageBox)", None, QApplication.UnicodeUTF8))

          zToolTip = ""
          
          self.labelSliderINFO = QLabel(self.groupBoxDuration)
          self.labelSliderINFO.setObjectName("labelSliderINFO")
          self.labelSliderINFO.setAlignment(Qt.AlignRight)
          self.labelSliderINFO.setGeometry(10, 40, 300, 25)
          self.labelSliderINFO.setText(QApplication.translate("QSphere","Duration for information message : ", None, QApplication.UnicodeUTF8))

          self.SliderINFO = MySlider(self.groupBoxDuration)
          self.SliderINFO.initSlider(200, 20, 320, 40, "SliderINFO", zToolTip, True, False, Qt.Horizontal, 1, 10, 1)

          self.txtSliderINFO = QLabel(self.groupBoxDuration)
          self.txtSliderINFO.setGeometry(540, 40, 25, 25) 
          self.txtSliderINFO.setStyleSheet("color: black; background-color: #C0C0C0")
          self.txtSliderINFO.setAlignment(Qt.AlignCenter)

          self.labelSliderWARNING = QLabel(self.groupBoxDuration)
          self.labelSliderWARNING.setObjectName("labelSliderWARNING")
          self.labelSliderWARNING.setAlignment(Qt.AlignRight)
          self.labelSliderWARNING.setGeometry(10, 80, 300, 25)
          self.labelSliderWARNING.setText(QApplication.translate("QSphere","Duration for warning message : ", None, QApplication.UnicodeUTF8))

          self.SliderWARNING = MySlider(self.groupBoxDuration)
          self.SliderWARNING.initSlider(200, 20, 320, 80, "SliderWARNING", zToolTip, True, False, Qt.Horizontal, 1, 10, 1)

          self.txtSliderWARNING = QLabel(self.groupBoxDuration)
          self.txtSliderWARNING.setGeometry(540, 80, 25, 25) 
          self.txtSliderWARNING.setStyleSheet("color: black; background-color: #C0C0C0")
          self.txtSliderWARNING.setAlignment(Qt.AlignCenter)

          self.labelSliderTIMEOUT = QLabel(self.groupBoxDuration)
          self.labelSliderTIMEOUT.setObjectName("labelSliderTIMEOUT")
          self.labelSliderTIMEOUT.setAlignment(Qt.AlignRight)
          self.labelSliderTIMEOUT.setGeometry(10, 120, 300, 25)
          self.labelSliderTIMEOUT.setText(QApplication.translate("QSphere","TimeOut for testing URL : ", None, QApplication.UnicodeUTF8))

          self.SliderTIMEOUT = MySlider(self.groupBoxDuration)
          self.SliderTIMEOUT.initSlider(200, 20, 320, 120, "SliderTIMEOUT", zToolTip, True, False, Qt.Horizontal, 1, 10, 1)
          
          self.txtSliderTIMEOUT = QLabel(self.groupBoxDuration)
          self.txtSliderTIMEOUT.setGeometry(540, 120, 25, 25) 
          self.txtSliderTIMEOUT.setStyleSheet("color: black; background-color: #C0C0C0")
          self.txtSliderTIMEOUT.setAlignment(Qt.AlignCenter)

        elif (i-1) == 2 :
          self.tab3 = zTab
          #Group Parser Informations
          self.groupParserInfo = QGroupBox(zTab)
          self.groupParserInfo.setObjectName("groupParserInfo")
          self.groupParserInfo.setTitle("%s : " % (QApplication.translate("QSphere","XML Parser parameters", None, QApplication.UnicodeUTF8)))

          self.checkAutoCorrect = QCheckBox(self.groupParserInfo)
          self.checkAutoCorrect.setObjectName("checkAutoCorrect")
          self.checkAutoCorrect.setAccessibleName("checkAutoCorrect")
          zText = QApplication.translate("QSphere","Auto-correction mode", None, QApplication.UnicodeUTF8)
          self.checkAutoCorrect.setText(zText)
          self.checkAutoCorrect.setToolTip(zText)


          self.radioStream = QRadioButton(self.groupParserInfo)
          self.radioStream.setObjectName("radioStream")
          self.radioStream.setAccessibleName("radioStream")
          zText = QApplication.translate("QSphere","working with stream", None, QApplication.UnicodeUTF8)
          self.radioStream.setText(zText)
          self.radioStream.setToolTip(zText)

          self.radioFile = QRadioButton(self.groupParserInfo)
          self.radioFile.setObjectName("radioFile")
          self.radioFile.setAccessibleName("radioFile")
          zText = QApplication.translate("QSphere","working with file", None, QApplication.UnicodeUTF8)
          self.radioFile.setText(zText)
          self.radioFile.setToolTip(zText)

          self.labelRepXML = QLabel(self.groupParserInfo)
          self.labelRepXML.setText("%s : " % (QApplication.translate("QSphere","Folder", None, QApplication.UnicodeUTF8)))
          self.labelRepXML.setObjectName("labelRepXML")
          self.labelRepXML.setAlignment(Qt.AlignLeft)    

          self.txtRepXML = MyTextEdit(self.groupParserInfo)
          self.txtRepXML.initTextEdit(self._W-310, 25, 10, 50, "txtRepXML", True, False, True, False, True)
          self.txtRepXML.setStyleSheet("color: black; background-color: #C0C0C0")

          self.BDefineRepXML = MyPushButton(self.groupParserInfo)
          self.BDefineRepXML.initPushButton(24, 24, 660, 32 , "BDefineRepXML", "", QApplication.translate("QSphere","Select a Folder", None, QApplication.UnicodeUTF8), True, getThemeIcon("folder.png"), 24, 24, True)

          self.groupEditorInfo = QGroupBox(zTab)
          self.groupEditorInfo.setObjectName("groupEditorInfo")
          self.groupEditorInfo.setTitle("%s : " % (QApplication.translate("QSphere","Editor parameters", None, QApplication.UnicodeUTF8)))

          self.checkSilentMode = QCheckBox(self.groupEditorInfo)
          self.checkSilentMode.setObjectName("checkSilentMode")
          self.checkSilentMode.setAccessibleName("checkSilentMode")
          zText = QApplication.translate("QSphere","Silent mode (unrespected metadata iso XML standard)", None, QApplication.UnicodeUTF8)
          self.checkSilentMode.setText(zText)
          self.checkSilentMode.setToolTip(zText)
          
          self.checkReportingCSWT = QCheckBox(self.groupEditorInfo)
          self.checkReportingCSWT.setObjectName("checkReportingCSWT")
          self.checkReportingCSWT.setAccessibleName("checkReportingCSWT")
          zText = QApplication.translate("QSphere","Opening report for CSW-T transactions", None, QApplication.UnicodeUTF8)
          self.checkReportingCSWT.setText(zText)
          self.checkReportingCSWT.setToolTip(zText)

        elif (i-1) == 3 :
          self.tab4 = zTab
          #Group CSW-T Informations
          self.groupCSWTInfo = QGroupBox(zTab)
          self.groupCSWTInfo.setObjectName("groupCSWTInfo")
          self.groupCSWTInfo.setTitle("%s : " % (QApplication.translate("QSphere","Service CSW-T parameters", None, QApplication.UnicodeUTF8)))

          self.labelListConnexionCSWT = QLabel(self.groupCSWTInfo)
          zText = "%s : " % (QApplication.translate("QSphere","List of connections", None, QApplication.UnicodeUTF8))
          self.labelListConnexionCSWT.setText(zText)
          self.labelListConnexionCSWT.setAccessibleDescription(zText)
          self.labelListConnexionCSWT.setObjectName("LblListConnexionCSWT")
          self.labelListConnexionCSWT.setAccessibleName("LblListConnexionCSWT")
          self.labelListConnexionCSWT.setAlignment(Qt.AlignRight)


          zIcon = getThemeIcon("actionsleft.png")
          zToolTip = "%s ..." % (QApplication.translate("QSphere","Actions", None, QApplication.UnicodeUTF8))
          self.ButListConnexionCSWT = MyPushButton(self.groupCSWTInfo) 
          self.ButListConnexionCSWT.initPushButton(40, 24,  0, 20, "ButListConnexionCSWT", "", zToolTip, True, zIcon, 40, 24, True)

          self.contextMnuActionsConnexions("ListConnexionCSWT", self.ButListConnexionCSWT)
          
          self.ListConnexionCSWT = QComboBox(self.groupCSWTInfo)
          self.ListConnexionCSWT.setEditable(False)
          self.ListConnexionCSWT.setObjectName("ListConnexionCSWT")
          self.ListConnexionCSWT.setAccessibleName("ListConnexionCSWT")

          self.ListConnexionCSWT.currentIndexChanged.connect(self.loadConnexion)
          
          self.butDefaultConnexionCSWT = MyPushButton(self.groupCSWTInfo)
          zIcon = getThemeIcon("defaulttrue.png")
          zToolTip = QApplication.translate("QSphere","Select this connection as active connection", None, QApplication.UnicodeUTF8)
          self.butDefaultConnexionCSWT.initPushButton(24, 24,  0, 20, "butDefaultConnexionCSWT", "", zToolTip, True, zIcon, 24, 24, True)
          self.butDefaultConnexionCSWT.clicked.connect(self.selConnexion)

          zIcon = getThemeIcon("new.png")
          zToolTip = QApplication.translate("QSphere","New connection", None, QApplication.UnicodeUTF8)
          self.ButNewConnexionCSWT = MyPushButton(self.groupCSWTInfo) 
          self.ButNewConnexionCSWT.initPushButton(24, 24,  0, 20, "ButNewConnexionCSWT", "", zToolTip, True, zIcon, 24, 24, True)
          self.ButNewConnexionCSWT.clicked.connect(self.newConnexion)

          zIcon = getThemeIcon("edit.png")
          zToolTip = QApplication.translate("QSphere","Edit the connection", None, QApplication.UnicodeUTF8)
          self.butEditConnexionCSWT = MyPushButton(self.groupCSWTInfo) 
          self.butEditConnexionCSWT.initPushButton(24, 24,  0, 20, "butEditConnexionCSWT", "", zToolTip, True, zIcon, 24, 24, True)
          self.butEditConnexionCSWT.clicked.connect(self.loadConnexion)

          zIcon = getThemeIcon("del.png")
          zToolTip = QApplication.translate("QSphere","Delete the connection", None, QApplication.UnicodeUTF8)
          self.butDelConnexionCSWT = MyPushButton(self.groupCSWTInfo) 
          self.butDelConnexionCSWT.initPushButton(24, 24,  0, 20, "butDelConnexionCSWT", "", zToolTip, True, zIcon, 24, 24, True)
          self.butDelConnexionCSWT.clicked.connect(self.delConnexion)


          self.groupConnexionInfo = QGroupBox(self.groupCSWTInfo)

          #CSW-T Service
          self.labelNameConnexionCSWT = QLabel(self.groupConnexionInfo)
          self.labelNameConnexionCSWT.setText("%s : " % (QApplication.translate("QSphere","Name for connection to CSW-T server", None, QApplication.UnicodeUTF8)))
          self.labelNameConnexionCSWT.setObjectName("labelNameConnexionCSWT")
          self.labelNameConnexionCSWT.setAlignment(Qt.AlignLeft)

          self.nameConnexionCSWT = MyWidgetLineEdit(self.groupConnexionInfo)
          self.nameConnexionCSWT.initType(6)
          self.nameConnexionCSWT.setObjectName("nameConnexionCSWT")
          self.nameConnexionCSWT.setAccessibleName("nameConnexionCSWT")
          self.nameConnexionCSWT.textChanged.connect(self.nameConnexionCSWT.VerifExpReg)

          zIcon = getThemeIcon("saveactions.png")
          zToolTip = QApplication.translate("QSphere","Add or update the connection", None, QApplication.UnicodeUTF8)
          self.ButAddConnexionCSWT = MyPushButton(self.groupConnexionInfo) 
          self.ButAddConnexionCSWT.initPushButton(40, 40,  0, 20, "ButAddConnexionCSWT", "", zToolTip, True, zIcon, 40, 40, True)
          self.ButAddConnexionCSWT.clicked.connect(self.saveConnexion)

          self.labelServerCSWT = QLabel(self.groupConnexionInfo)
          self.labelServerCSWT.setText("%s : " % (QApplication.translate("QSphere","Url Server for CSW-T", None, QApplication.UnicodeUTF8)))
          self.labelServerCSWT.setObjectName("labelServerCSWT")
          self.labelServerCSWT.setAlignment(Qt.AlignLeft)    

          self.serverCSWT = MyWidgetLineEdit(self.groupConnexionInfo)
          self.serverCSWT.initType(40)
          self.serverCSWT.setObjectName("serverCSWT")
          self.serverCSWT.setAccessibleName("serverCSWT")
          self.serverCSWT.textChanged.connect(self.serverCSWT.VerifExpReg)

          #BUTTON GETCAPABILITIES
          zIcon = getThemeIcon("cswtgetcapabilities.png")
          zToolTip = QApplication.translate("QSphere","Get capabilities for the server", None, QApplication.UnicodeUTF8)
          self.ButGetCapabilitiesServerCSWT = MyPushButton(self.groupConnexionInfo) 
          self.ButGetCapabilitiesServerCSWT.initPushButton(40, 40,  0, 20, "ButGetCapabilitiesServerCSWT", "", "%s %s" % (zToolTip, "CSW-T"), True, zIcon, 40, 40, True)
          self.ButGetCapabilitiesServerCSWT.clicked.connect(self.getCapabilitiesCSWT)

          self.labelAuthServerCSWT = QLabel(self.groupConnexionInfo)
          self.labelAuthServerCSWT.setText("%s : " % (QApplication.translate("QSphere","Url Server for CSW-T Authentification", None, QApplication.UnicodeUTF8)))
          self.labelAuthServerCSWT.setObjectName("labelAuthServerCSWT")
          self.labelAuthServerCSWT.setAlignment(Qt.AlignLeft)    

          self.authServerCSWT = MyWidgetLineEdit(self.groupConnexionInfo)
          self.authServerCSWT.initType(41)
          self.authServerCSWT.setObjectName("authServerCSWT")
          self.authServerCSWT.setAccessibleName("authServerCSWT")
          self.authServerCSWT.textChanged.connect(self.authServerCSWT.VerifExpReg)

          zIcon = getThemeIcon("cswtusersrights.png")
          zToolTip = QApplication.translate("QSphere","Test URL for authentification to the server CSW-T", None, QApplication.UnicodeUTF8)
          self.ButGetAuthentificationServerCSWT = MyPushButton(self.groupConnexionInfo) 
          self.ButGetAuthentificationServerCSWT.initPushButton(40, 40,  0, 20, "ButGetAuthentificationServerCSWT", "", zToolTip, True, zIcon, 40, 40, True)
          self.ButGetAuthentificationServerCSWT.clicked.connect(self.goURL) #testURL

          #User CSW-T Service
          self.labelUserServerCSWT = QLabel(self.groupConnexionInfo)
          self.labelUserServerCSWT.setText("%s : " % (QApplication.translate("QSphere","User for CSW-T", None, QApplication.UnicodeUTF8)))
          self.labelUserServerCSWT.setObjectName("labelUserServerCSWT")
          self.labelUserServerCSWT.setAlignment(Qt.AlignLeft)    

          self.UserCSWT = MyWidgetLineEdit(self.groupConnexionInfo)
          self.UserCSWT.initType(6)
          self.UserCSWT.setObjectName("UserCSWT")
          self.UserCSWT.setAccessibleName("UserCSWT")
          self.UserCSWT.textChanged.connect(self.UserCSWT.VerifExpReg)

          self.labelPwdUserServerCSWT = QLabel(self.groupConnexionInfo)
          self.labelPwdUserServerCSWT.setText("%s : " % (QApplication.translate("QSphere","Password for the connection", None, QApplication.UnicodeUTF8)))
          self.labelPwdUserServerCSWT.setObjectName("labelPwdUserServerCSWT")
          self.labelPwdUserServerCSWT.setAlignment(Qt.AlignLeft)  

          self.pwdUserCSWT = MyWidgetLineEdit(self.groupConnexionInfo)
          self.pwdUserCSWT.initType(9)
          self.pwdUserCSWT.setObjectName("pwdUserCSWT")
          self.pwdUserCSWT.setAccessibleName("pwdUserCSWT")
          self.pwdUserCSWT.textChanged.connect(self.pwdUserCSWT.VerifExpReg)

          self.checkViewPwdUserCSWT = QCheckBox(self.groupConnexionInfo)
          self.checkViewPwdUserCSWT.setObjectName("checkViewPwdUserCSWT")
          self.checkViewPwdUserCSWT.setAccessibleName("checkViewPwdUserCSWT")
          zText = QApplication.translate("QSphere","View the password", None, QApplication.UnicodeUTF8)
          self.checkViewPwdUserCSWT.setText(zText)
          self.checkViewPwdUserCSWT.setToolTip(zText)

        
        else : pass  


    self.myPathPrint, self.myPathSave = "print.png", "save.png"
    self.myPathSizeUp, self.myPathSizeDown = "sizeup.png", "sizedown.png"
    
    self.PrintButton = MyPushButton(self)
    self.PrintButton.initPushButton(24, 24, 5, 5, "PrintButton", "", QApplication.translate("QSphere", "Print", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathPrint), 24, 24, True)
    self.PrintButton.setShortcut(QKeySequence("Ctrl+P"))

    self.SaveButton = MyPushButton(self)
    self.SaveButton.initPushButton(24, 24, 5, 5, "SaveButton", "", QApplication.translate("QSphere", "Save", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathSave), 24, 24, True)
    self.SaveButton.setShortcut(QKeySequence("Ctrl+S"))

    zIcon = getThemeIcon("qspherehelp.png")
    self.HelpButton = MyPushButton(self) 
    self.HelpButton.initPushButton(48, 48, -50, -50, "HelpButton", "", "", True, zIcon, 48, 48, True)
    self.HelpButton.setShortcut(QKeySequence("F1")) 

    self.barInfo = QgsMessageBar(self)
    self.barInfo.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )

    self.status_txt = QLabel(self)
    self.movie = QMovie(getThemeIcon("sablier.gif"))
    self.status_txt.setMovie(self.movie)
    self.status_txt.setLayout(QHBoxLayout())
    self.status_txt.layout().addWidget(QLabel(''))
    self.status_txt.setVisible(False)

    self.CloseButton = QPushButton(self)
    self.CloseButton.setObjectName("CloseButton")
    self.CloseButton.setText(QApplication.translate("QSphere", "Close", None, QApplication.UnicodeUTF8))

    self.listWidget.currentRowChanged.connect(self.fixeONGLETL)
    self.SliderINFO.valueChanged.connect(self.MakeVisibleValue)
    self.SliderWARNING.valueChanged.connect(self.MakeVisibleValue)
    self.SliderTIMEOUT.valueChanged.connect(self.MakeVisibleValue)

    self.SliderINFO.setValue(2)
    self.SliderWARNING.setValue(5)
    self.SliderTIMEOUT.setValue(5)

    self.checkAutoCorrect.clicked.connect(self.enabledCTRL)
    self.checkViewPwdUserCSWT.clicked.connect(self.enabledPWD)
    self.PrintButton.clicked.connect(self.printFile)
    self.BDefineRep.clicked.connect(self.FixeREPSearchFILE)
    self.BDefineRepXML.clicked.connect(self.FixeREPSearchFILE)
    self.SaveButton.clicked.connect(self.saveOptions)
    self.CloseButton.clicked.connect(self.close)
    self.ListConnexionCSWT.currentIndexChanged.connect(self.setImageDefault)
    self.HelpButton.clicked.connect(self.clickHelp)

    self.loadOptions()
    self.enabledCTRL()
    self.enabledPWD()

    key = getSelConnexion(self) 
    self.FixeCurrentConnexion(key)
    self.listWidget.setCurrentRow(0)    

  def clickHelp(self): makeHelp(self)

  def enabledCTRL(self):
      zCond = self.checkAutoCorrect.isChecked()
      self.radioStream.setEnabled(zCond)
      self.radioFile.setEnabled(zCond)
      self.BDefineRepXML.setEnabled(zCond)
      
  def enabledPWD(self):
      zCond = self.checkViewPwdUserCSWT.isChecked()
      self.pwdUserCSWT.setEchoMode(QLineEdit.Normal) if zCond else self.pwdUserCSWT.setEchoMode(QLineEdit.Password)

  def setImageDefault(self):
      zCond  = (getSelConnexion(self)==self.ListConnexionCSWT.currentText())
      sIcon = "default%s.png" % (zCond)
      sIcon = getThemeIcon(sIcon.lower())
      myIcon = QIcon(sIcon)
      self.butDefaultConnexionCSWT.setIcon(myIcon) 

  def fixeONGLETL(self): self.tabWidget.setCurrentIndex(self.listWidget.currentRow())

  def contextMnuActionsConnexions(self, nameObj, zButtonAction):
      contextMnu_Actions = QMenu()

      menuIcon = getThemeIcon("importmetasearch.png")
      zToolTip = "%s ..." % (QApplication.translate("QSphere","Import from MetaSearch", None, QApplication.UnicodeUTF8))
      self.importFromMetaSearch = QAction(QIcon(menuIcon), zToolTip, self)
      self.importFromMetaSearch.setObjectName("import%s" % (nameObj))
      contextMnu_Actions.addAction(self.importFromMetaSearch)
      self.importFromMetaSearch.triggered.connect(self.selImportConnexion)
      
      menuIcon = getThemeIcon("open.png")
      zToolTip = "%s ..." % (QApplication.translate("QSphere","Load from XML File", None, QApplication.UnicodeUTF8))
      self.loadFromXMLFile = QAction(QIcon(menuIcon), zToolTip, self)
      self.loadFromXMLFile.setObjectName("load%s" % (nameObj))
      contextMnu_Actions.addAction(self.loadFromXMLFile)
      self.loadFromXMLFile.triggered.connect(self.getConnexionsFromXMLFile)

      contextMnu_Actions.addSeparator()

      menuIcon = getThemeIcon("save.png")
      zToolTip = "%s ..." % (QApplication.translate("QSphere","Save to XML File", None, QApplication.UnicodeUTF8))
      self.saveToXMLFile = QAction(QIcon(menuIcon), zToolTip, self)
      self.saveToXMLFile.setObjectName("save%s" % (nameObj))
      contextMnu_Actions.addAction(self.saveToXMLFile)
      self.saveToXMLFile.triggered.connect(self.saveConnexionsInXMLFile)

      contextMnu_Actions.addSeparator()
      
      menuIcon = getThemeIcon("deleteall.png")
      zToolTip = "%s ..." % (QApplication.translate("QSphere","Delete all entries", None, QApplication.UnicodeUTF8))
      self.deleteAllItems = QAction(QIcon(menuIcon), zToolTip, self)
      self.deleteAllItems.setObjectName("deleteallitems%s" % (nameObj))
      contextMnu_Actions.addAction(self.deleteAllItems)
      self.deleteAllItems.triggered.connect(self.deleteAll)      

      zButtonAction.setMenu(contextMnu_Actions)


  def contextMnuActions(self, nameObj, zButtonAction):
      contextMnu_Actions = QMenu()

      menuIcon = getThemeIcon("add.png")
      zAction = QAction(QIcon(menuIcon), QApplication.translate("QSphere","Add the server", None, QApplication.UnicodeUTF8), self)
      zAction.setObjectName("add%s" % (nameObj))
      contextMnu_Actions.addAction(zAction)
      zAction.triggered.connect(self.addItem)

      menuIcon = getThemeIcon("del.png")
      zAction = QAction(QIcon(menuIcon), QApplication.translate("QSphere","Delete the server", None, QApplication.UnicodeUTF8), self)
      zAction.setObjectName("del%s" % (nameObj))
      contextMnu_Actions.addAction(zAction)
      zAction.triggered.connect(self.delItem)

      contextMnu_Actions.addSeparator()

      menuIcon = getThemeIcon("moveup.png")
      zAction = QAction(QIcon(menuIcon), QApplication.translate("QSphere","Move the line up", None, QApplication.UnicodeUTF8), self)
      zAction.setObjectName("moveup%s" % (nameObj))
      contextMnu_Actions.addAction(zAction)
      zAction.triggered.connect(self.moveItemUp)

      menuIcon = getThemeIcon("movedown.png")
      zAction = QAction(QIcon(menuIcon), QApplication.translate("QSphere","Move the line down", None, QApplication.UnicodeUTF8), self)
      zAction.setObjectName("movedown%s" % (nameObj))
      contextMnu_Actions.addAction(zAction)
      zAction.triggered.connect(self.moveItemDown)


      contextMnu_Actions.addSeparator()

      menuIcon = getThemeIcon("urlvalid.png")
      zAction = QAction(QIcon(menuIcon), QApplication.translate("QSphere","Test the URL", None, QApplication.UnicodeUTF8), self)
      zAction.setObjectName("testor%s" % (nameObj))
      contextMnu_Actions.addAction(zAction)
      zAction.triggered.connect(self.testURL)

      menuIcon = getThemeIcon("urllocalisator.png")
      zAction = QAction(QIcon(menuIcon), QApplication.translate("QSphere","Go to the URL", None, QApplication.UnicodeUTF8), self)
      zAction.setObjectName("open%s" % (nameObj))
      contextMnu_Actions.addAction(zAction)
      zAction.triggered.connect(self.goURL)
         
      zButtonAction.setMenu(contextMnu_Actions)
     

  def deleteAll(self):
      zTitle = QApplication.translate("QSphere","Warning", None, QApplication.UnicodeUTF8)
      zMsg = QApplication.translate("QSphere","Delete all the connections ?", None, QApplication.UnicodeUTF8)
      if QMessageBox.question(None, zTitle, zMsg, QApplication.translate("QSphere","Validate", None, QApplication.UnicodeUTF8), QApplication.translate("QSphere","Cancel", None, QApplication.UnicodeUTF8)) ==  0 : 
          mySettings = QSettings()
          mySettings.beginGroup("/qsphere/connections/")
          keys = mySettings.childGroups()
          if keys != []:
             mySettings.setValue("/qsphere/connections/selected", "")
             for key in keys :
                 mySettings = QSettings()
                 mySettings.remove("/qsphere/connections/%s" % (key))
             self.ListConnexionCSWT.clear()
             countItems(self, self.ListConnexionCSWT.accessibleName(), self.ListConnexionCSWT)
          
          
  def MakeVisibleValue(self):
      zValue = "%s" % (self.sender().value())
      self.sender().setToolTip(zValue)
      if self.sender() == self.SliderINFO : self.txtSliderINFO.setText(zValue)
      elif self.sender() == self.SliderWARNING : self.txtSliderWARNING.setText(zValue)
      elif self.sender() == self.SliderTIMEOUT : self.txtSliderTIMEOUT.setText(zValue)
      else : pass
     
  def loadOptions(self):
      savefile = os.path.join(os.path.dirname(__file__),"ressources/options.ini")
      if os.path.exists(savefile):

         config = ConfigParser.ConfigParser()
         config.read(savefile)
         zSections = config.sections()

         for section in zSections :
             try : zObj = getWidget(self, section)
             except : zObj = None
             
             if zObj !=None :
                if type(zObj) in (MyWebComboBox, MyUserComboBox) :
                    zInfos = config.get(section,'Index')
                    zIndexObj = int(zInfos.rstrip())
                    zInfosItem = config.get(section,'Items')
                    zItemCount = int(zInfosItem.rstrip())
                    zObj.clear()
                    for k in range(zItemCount): zObj.addItem(config.get(section,'Item_%s' % (k)))
                    zObj.setCurrentIndex(zIndexObj)
                    countItems(self, zObj.accessibleName(), zObj)

                elif type(zObj) == MySlider :
                    zInfos = config.get(section,'value')
                    zObj.setValue(int(zInfos))

                elif type(zObj) in (QRadioButton, QCheckBox) :
                     zInfos = config.get(section,'state').lower().strip()
                     zObj.setChecked(zInfos=='true')

                elif type(zObj) == MyTextEdit :
                    InitDir = config.get(section,'InitDir')
                    zObj.setPlainText(os.path.dirname(__file__)) if InitDir=="" or not (os.path.exists(InitDir)) else zObj.setPlainText(InitDir)

  def newConnexion(self):
      self.nameConnexionCSWT.setText("")
      self.serverCSWT.setText("")
      self.authServerCSWT.setText("")
      self.UserCSWT.setText("")
      self.pwdUserCSWT.setText("")

  def selImportConnexion(self):
      try :
        metaSearchSettings = QSettings()
        metaSearchSettings.beginGroup('/MetaSearch/')
        keys = metaSearchSettings.childGroups()
        addkeys = []
        if keys != []:
           for key in keys :
               if self.ListConnexionCSWT.findText("%s" % (key),  Qt.MatchFixedString) == -1 : 
                  self.newConnexion()
                  self.nameConnexionCSWT.setText(key)
                  self.serverCSWT.setText(metaSearchSettings.value('%s/url' % key))
                  self.saveConnexion(True)
                  addkeys.append(key)

           zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
           zMsg = QApplication.translate("QSphere","Added URL", None, QApplication.UnicodeUTF8)
           SendMessage(self, "%s :" % (zTitle), "%s (%s)<br>%s" % (zMsg, len(addkeys), addkeys), QgsMessageBar.INFO, self.SliderINFO.value())
      except :
           zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
           zMsg = QApplication.translate("QSphere","Import stopped.", None, QApplication.UnicodeUTF8)
           SendMessage(self, "%s :" % (zTitle), "<h1>%s</h1>" % (zMsg), QgsMessageBar.INFO, self.SliderINFO.value())
      
  def saveConnexion(self, *args):
      if self.nameConnexionCSWT.text() == "" :
          zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
          zMsg = QApplication.translate("QSphere","The connection must have a name !", None, QApplication.UnicodeUTF8)
          SendMessage(self, zTitle , "<b>%s</b>" % (zMsg), QgsMessageBar.INFO, self.SliderINFO.value())
          return

      mySettings = QSettings()
      key = self.nameConnexionCSWT.text()        
      index, newItem = self.findkey(key)

      zMsg1 =  QApplication.translate("QSphere","Add the connection", None, QApplication.UnicodeUTF8) if newItem else QApplication.translate("QSphere","Update the connection", None, QApplication.UnicodeUTF8)
   
      mySettings.setValue("/qsphere/connections/", key) 
      mySettings.setValue("/qsphere/connections/%s/host" % (key), self.serverCSWT.text())
      mySettings.setValue("/qsphere/connections/%s/authhost" % (key), self.authServerCSWT.text())
      mySettings.setValue("/qsphere/connections/%s/username" % (key), self.UserCSWT.text())
      mySettings.setValue("/qsphere/connections/%s/password" % (key),  self.pwdUserCSWT.text())

      if args[0] == False :
        zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
        zMsg2 = QApplication.translate("QSphere","Successfull !", None, QApplication.UnicodeUTF8)
        SendMessage(self, "%s :" % (zTitle), "%s<br>%s<br>%s" % (zMsg1, key, zMsg2), QgsMessageBar.INFO, self.SliderINFO.value())

      self.FixeCurrentConnexion(key)
      countItems(self, self.ListConnexionCSWT.accessibleName(), self.ListConnexionCSWT)
      if newItem : self.ListConnexionCSWT.setCurrentIndex(self.ListConnexionCSWT.count()-1)

  def FixeCurrentConnexion(self, key):
      self.loadConnexions()
      try : index = self.ListConnexionCSWT.findText(key)
      except : index = self.ListConnexionCSWT.currentIndex()
      try : self.ListConnexionCSWT.setCurrentIndex(index)
      except : pass

  def loadConnexions(self):
      self.ListConnexionCSWT.clear()
      mySettings = QSettings()
      try : 
          mySettings.beginGroup("/qsphere/connections/")
          keys = mySettings.childGroups()
          if keys != []:
             for key in keys : self.ListConnexionCSWT.addItem(key)
          countItems(self, self.ListConnexionCSWT.accessibleName(), self.ListConnexionCSWT)   
      except : pass

  def loadConnexion(self):
      if self.ListConnexionCSWT.currentIndex()==-1: return
      mySettings = QSettings()
      key = self.ListConnexionCSWT.currentText()
      self.nameConnexionCSWT.setText(key)
      self.serverCSWT.setText(mySettings.value("/qsphere/connections/%s/host" % (key)))
      self.authServerCSWT.setText(mySettings.value("/qsphere/connections/%s/authhost" % (key)))
      self.UserCSWT.setText(mySettings.value("/qsphere/connections/%s/username" % (key)))
      self.pwdUserCSWT.setText(mySettings.value("/qsphere/connections/%s/password" % (key)))

  def getCapabilitiesCSWT(self):
      myConnexion = cswtConnection(self, self.nameConnexionCSWT.text(), self.serverCSWT.text(), self.authServerCSWT.text())
      try :
        responseCSWT = myConnexion.getCapabilities()

        if responseCSWT != None and self.checkReportingCSWT.isChecked() :
            from ui_editorXML import xmlEditor
            d = xmlEditor(self, "")
            MakeWindowIcon(d, "editxml.png")
            d.setWindowTitle("%s : %s" % (d.racTitle, ""))
            d.show()
            d.move(self.x()+100, self.y()+100)

            try : charset = (responseCSWT.headers["Content-Type"].split("=")[1].strip())
            except : charset = "utf-8"  
            
            d.editor.setText("%sDATA RESPONSE :\n%s" % (myConnexion.reporting(), responseCSWT.text)) 
            d.checkProperties()
            d.BadMyISO()
      except :
                zTitle = QApplication.translate("QSphere","Warning", None, QApplication.UnicodeUTF8)
                zMsg1 = QApplication.translate("QSphere","Unable to establish connection to", None, QApplication.UnicodeUTF8)
                zMsg2 = QApplication.translate("QSphere","HTTP error", None, QApplication.UnicodeUTF8)
                msg = "%s :<br>%s [%s] " % (zMsg1, self.serverCSWT.text(), zMsg2)
                SendMessage(self, zTitle , msg, QgsMessageBar.WARNING, self.SliderWARNING.value())

  def selConnexion(self):
      if self.ListConnexionCSWT.currentText()=="" : return
      if getSelConnexion(self)==self.ListConnexionCSWT.currentText() : return
      mySettings = QSettings()
      mySettings.setValue("/qsphere/connections/selected", self.ListConnexionCSWT.currentText())
      self.setImageDefault()
      if self.parent != None :
          try :
            if self.parent.objectName() == "DialogMetaData" :
                  self.parent.disconnectCSWT()
          except : pass

  def delConnexion(self):
      oldkey = self.ListConnexionCSWT.currentText()
      zTitle = QApplication.translate("QSphere","Warning", None, QApplication.UnicodeUTF8)
      zMsg = QApplication.translate("QSphere","Delete the current connection ?", None, QApplication.UnicodeUTF8)
      if QMessageBox.question(None, zTitle, "%s :\n%s" % (zMsg, oldkey), QApplication.translate("QSphere","Validate", None, QApplication.UnicodeUTF8), QApplication.translate("QSphere","Cancel", None, QApplication.UnicodeUTF8)) ==  0 : 
          mySettings = QSettings()
          mySettings.remove("/qsphere/connections/%s" % (oldkey))
          newsel = (getSelConnexion(self)==oldkey)
          zIndex = self.ListConnexionCSWT.currentIndex()-1 if self.ListConnexionCSWT.currentIndex()>0 else 0
          self.loadConnexions()
          if newsel : mySettings.setValue("/qsphere/connections/selected", self.ListConnexionCSWT.currentText())
          countItems(self, self.ListConnexionCSWT.accessibleName(), self.ListConnexionCSWT)
          self.ListConnexionCSWT.setCurrentIndex(zIndex)
          

  def saveConnexionsInXMLFile(self):

      zTitle = QApplication.translate("QSphere","Save to XML File", None, QApplication.UnicodeUTF8)
      self.InitDir = os.path.dirname(__file__) if self.InitDir == "" else self.InitDir
      
      MyFileDialog = QFileDialog(self, zTitle)
      MyFileDialog.setDefaultSuffix("xml")
      MyFileDialog.setNameFilters((self.labelXMLFiles,))
      MyFileDialog.selectNameFilter(self.labelXMLFiles)
      MyFileDialog.setViewMode(QFileDialog.Detail)
      MyFileDialog.setDirectory(self.InitDir)
      MyFileDialog.setAcceptMode(QFileDialog.AcceptSave)

      FixeLabelsFileDialog(self, MyFileDialog, 1, True)
      
      if MyFileDialog.exec_():
          fileName = FileNameWithExtension(self, MyFileDialog.selectedFiles()[0], MyFileDialog.selectedNameFilter())
          self.initDir = os.path.dirname(fileName)

          doc = etree.Element('qgsCSWConnections')
          doc.attrib['version'] = '1.0'

          mySettings = QSettings()
          mySettings.beginGroup("/qsphere/connections/")
          keys = mySettings.childGroups()
          if keys != []:
             for key in keys :
                url = mySettings.value("%s/host" % (key))
                
                if url is not None :
                   connection = etree.SubElement(doc, 'csw')
                   connection.attrib['name'] = key
                   connection.attrib['url'] = url
                   connection.attrib['authurl'] = mySettings.value("%s/authhost" % (key))

          with open(fileName, 'w') as fileobj: fileobj.write(prettify_xml(etree.tostring(doc)))
          
          zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
          zMsg = QApplication.translate("QSphere","The file xml was saved as", None, QApplication.UnicodeUTF8)
          SendMessage(self, zTitle , "%s :<br>%s" % (zMsg, fileName), QgsMessageBar.INFO, self.SliderINFO.value())          

  def getConnexionsFromXMLFile(self):
        zTitle = QApplication.translate("QSphere", "Load from XML File", None, QApplication.UnicodeUTF8)
        self.InitDir = os.path.dirname(__file__) if self.InitDir == "" else self.InitDir
        
        MyFileDialog = QFileDialog(self, zTitle)
        MyFileDialog.setNameFilters((self.labelXMLFiles,))  
        MyFileDialog.setViewMode(QFileDialog.Detail)
        MyFileDialog.setDirectory(self.InitDir)
        MyFileDialog.setFileMode(QFileDialog.ExistingFile) 
        MyFileDialog.setAcceptMode(QFileDialog.AcceptOpen)

        FixeLabelsFileDialog(self, MyFileDialog, 0, True)        
        
        if MyFileDialog.exec_():
           fileName = "%s" % (MyFileDialog.selectedFiles()[0])
           error = 0
           try:
               doc = etree.parse(fileName).getroot()
               if doc.tag != 'qgsCSWConnections':
                  error = 1
                  zMsg = QApplication.translate("QSphere", "Invalid CSW connections XML", None, QApplication.UnicodeUTF8)
                  err = QApplication.translate("QSphere","Root qgsCSWConnections not found", None, QApplication.UnicodeUTF8)
           except etree.ParseError, err:
               error = 1
               zMsg = QApplication.translate("QSphere", "Cannot parse XML file", None, QApplication.UnicodeUTF8) 
           except IOError, err:
               error = 1
               zMsg = QApplication.translate("QSphere", "Cannot open file", None, QApplication.UnicodeUTF8) 

           if error == 1:
               zTitle = QApplication.translate("QSphere","Warning", None, QApplication.UnicodeUTF8)
               SendMessage(self, "%s :" % (zTitle), "%s :<br>%s." % (zMsg, err), QgsMessageBar.WARNING, self.SliderWARNING.value())
               return

           addkeys = []
           for csw in doc.findall('csw'):
               key = csw.attrib.get('name')
               if self.ListConnexionCSWT.findText("%s" % (key),  Qt.MatchFixedString) == -1 : 
                  self.newConnexion()
                  self.nameConnexionCSWT.setText(key)
                  try : self.serverCSWT.setText(csw.attrib.get('url'))
                  except : self.serverCSWT.setText("")
                  try : self.authServerCSWT.setText(csw.attrib.get('authurl'))
                  except : self.authServerCSWT.setText("")
                  self.saveConnexion(True)
                  addkeys.append(key)
           if len(addkeys) > 0 :     
               zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
               zMsg = QApplication.translate("QSphere","Added URL", None, QApplication.UnicodeUTF8)
               SendMessage(self, "%s :" % (zTitle), "%s (%s)<br>%s" % (zMsg, len(addkeys), addkeys), QgsMessageBar.INFO, self.SliderINFO.value())
          
         
  def findkey(self, targetKey):
      mySettings = QSettings()
      mySettings.beginGroup("/qsphere/connections")
      keys = mySettings.childGroups()
      i, newitem = 0, True
      if keys != []:
         for key in keys :
             if targetKey == key :
                newitem = False
                break
             i+= 1 
      return i, newitem

  def saveOptions(self):
      savefile = os.path.join(os.path.dirname(__file__),"ressources/options.ini")
      zLOG = open(savefile, "w")
      Config = ConfigParser.ConfigParser()
      Config.add_section("Options")
      Config.set("Options",'date', datetime.datetime.now().strftime("%d/%m/%Y %Hh%Mm%Ss"))
      Config.set("Options",'mandatoryPlugin',"QSphere")
      Config.set("Options",'version',"2.14.2")
      zIndex = self.tabWidget.currentIndex()

      zTabs = self.tabWidget.count()
      for i in range(zTabs):
          self.tabWidget.setCurrentIndex(i)
          zTab = self.tabWidget.currentWidget()

          for child in zTab.children() :
              if type(child) == QGroupBox :
                
                 for subchild in child.children() :
                     if  type(subchild) in (MyWebComboBox, MyUserComboBox, MyTextEdit, MySlider, QRadioButton, QCheckBox) :
                         
                         zNameObj = subchild.objectName()
                         Config.add_section(zNameObj)
                         zClassObjName = "%s" % (subchild.metaObject().className())
                         Config.set(zNameObj, 'Type', zClassObjName)

                         if type(subchild) in (MyWebComboBox, MyUserComboBox) :
                             Config.set(zNameObj,'Items',subchild.count())
                             Config.set(zNameObj,'Index',subchild.currentIndex())
                             for k in range(subchild.count()): Config.set(zNameObj,'Item_%s' % (k), "%s" % (subchild.itemText(k)))
                             
                         elif type(subchild) == MySlider : Config.set(zNameObj,'value',subchild.value())

                         elif type(subchild) in (QRadioButton, QCheckBox) : Config.set(zNameObj, "state","%s" % (subchild.isChecked()))

                         elif type(subchild) == MyTextEdit :
                              Config.set(zNameObj,'InitDir',subchild.toPlainText())

      Config.write(zLOG)
      if zLOG != None : zLOG.close()

      zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
      zMsg = QApplication.translate("QSphere","The file ini was saved as", None, QApplication.UnicodeUTF8)
      SendMessage(self, zTitle , "%s :<br>%s" % (zMsg, savefile), QgsMessageBar.INFO, self.SliderINFO.value())

      self.tabWidget.setCurrentIndex(zIndex)



  def FixeREPSearchFILE(self):
      if self.sender() == None : return
      if self.sender()== self.BDefineRep : zObj = self.txtRep
      elif self.sender()== self.BDefineRepXML : zObj = self.txtRepXML
      else : return
      
      InitDir = os.path.dirname(__file__) if zObj.toPlainText()=="" else os.path.dirname(zObj.toPlainText())
      zTitle = QApplication.translate("QSphere", "Select the folder", None, QApplication.UnicodeUTF8)
      
      MyFileDialog = QFileDialog(self, zTitle)
      MyFileDialog.setDirectory(InitDir)
      MyFileDialog.setFileMode(QFileDialog.DirectoryOnly)

      FixeLabelsFileDialog(self, MyFileDialog, 0, False)      

      if MyFileDialog.exec_():
         inputDir = MyFileDialog.selectedFiles()[0] 
         zObj.setPlainText(CorrigePath(inputDir.replace("\\","/")))

  def fixeItem(self, TextProperty):
      if not TextProperty :
         if self.sender().objectName().find("ServerMetadata")!=-1 : zCombo = self.serverMetadata
         elif self.sender().objectName().find("ServerKeywords")!=-1 : zCombo = self.serverKeywords
         elif self.sender().objectName().find("ServerNavigator")!=-1 : zCombo = self.serverNavigator
         else : zCombo == None
         return zCombo
      else:
         if self.sender().objectName().find("ServerMetadata")!=-1 : zUrl = self.serverMetadata.currentText()
         elif self.sender().objectName().find("ServerKeywords")!=-1 : zUrl = self.serverKeywords.currentText()
         elif self.sender().objectName().find("ServerNavigator")!=-1 : zUrl = self.serverNavigator.currentText()
         elif self.sender().objectName().find("GetAuthentificationServerCSWT")!=-1 : zUrl = self.authServerCSWT.text()
         elif self.sender().objectName().find("GetCapabilitiesCSWT")!=-1 : zUrl = self.serverCSWT.currentText()
         else : zUrl = "#blank"
         return zUrl

  def addItem(self):
      zCombo = self.fixeItem(False)
      if zCombo == None : return
      if zCombo.findText(zCombo.currentText()) == -1:
          zCombo.addItem(zCombo.currentText())
          zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
          zMsg = QApplication.translate("QSphere","added to the list !", None, QApplication.UnicodeUTF8)
          SendMessage(self, zTitle , "%s :<br><u><i>%s</i></u><br>%s" % (self.msgItem, zCombo.currentText(), zMsg), QgsMessageBar.INFO, self.SliderINFO.value())
          countItems(self, zCombo.accessibleName(), zCombo)
          zCombo.setCurrentIndex(zCombo.count()-1)
      else :
          zTitle = QApplication.translate("QSphere","Warning", None, QApplication.UnicodeUTF8)
          zMsg = QApplication.translate("QSphere","already found in the list !", None, QApplication.UnicodeUTF8)
          SendMessage(self, zTitle , "%s :<br><u><i>%s</i></u><br>%s" % (self.msgItem, zCombo.currentText(), zMsg), QgsMessageBar.WARNING, self.SliderWARNING.value())

  def delItem(self):
      zCombo = self.fixeItem(False)
      if zCombo == None : return
      if zCombo.currentIndex()!=-1 :
         zItem = zCombo.currentText()
         zIndex = zCombo.currentIndex()-1 if zCombo.currentIndex()>0 else 0
         zCombo.removeItem(zCombo.currentIndex())   
         zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
         zMsg = QApplication.translate("QSphere","removed the list !", None, QApplication.UnicodeUTF8)
         SendMessage(self, zTitle , "%s :<br><u><i>%s</i></u><br>%s" % (self.msgItem, zItem, zMsg), QgsMessageBar.INFO, self.SliderINFO.value())
         countItems(self, zCombo.accessibleName(), zCombo)
         zCombo.setCurrentIndex(zIndex)

  def moveItemDown(self):
      zCombo = self.fixeItem(False)
      if zCombo == None : return
      index = zCombo.currentIndex()
      if index <= zCombo.count()-1:
         zText = zCombo.itemText(index)
         zCombo.insertItem(index+2, zText)
         zCombo.removeItem(index)
         index = zCombo.findText(zText)
         zCombo.setCurrentIndex(index)
         zCombo.showPopup()

  def moveItemUp(self):
      zCombo = self.fixeItem(False)
      if zCombo == None : return
      index = zCombo.currentIndex()
      if index >= 1 :
         zText = zCombo.itemText(index)
         zCombo.insertItem(index-1, zText)
         zCombo.removeItem(index+1)
         index = zCombo.findText(zText)
         zCombo.setCurrentIndex(index)
         zCombo.showPopup()

  def goURL(self):
      zURL = self.fixeItem(True)
      self.dnavigator = doUI.LoadDialogViewer(self, self.iface, zURL, False, [], self.langueTR, self.parent, None, "navigatorweb.png", True) 

  def startMovie(self):
      self.status_txt.setVisible(True)
      self.movie.start()
      self.status_txt.repaint()

  def stopMovie(self):
      self.movie.stop()
      self.status_txt.setVisible(False)
      
  def testURL(self):
      self.startMovie()
      zURL = self.fixeItem(True)
      sites = [('%s' % (zURL), 'GET', {'Content-Type': 'application/html'}, 'None')] 
      try : isValidURL = multi_get(self.movie, self.status_txt, sites, self.SliderTIMEOUT.value())[0][1]
      except : isValidURL = None

      if isValidURL != None :
         zTitle = QApplication.translate("QSphere", "Information" , None, QApplication.UnicodeUTF8) 
         zTextIsValid = QApplication.translate("QSphere", "Valid", None, QApplication.UnicodeUTF8)
         zPicto = QgsMessageBar.INFO
         zDuration = self.SliderINFO.value()
      else :
         zTitle = QApplication.translate("QSphere", "Warning" , None, QApplication.UnicodeUTF8) 
         zTextIsValid = QApplication.translate("QSphere", "Not valid", None, QApplication.UnicodeUTF8)
         zPicto = QgsMessageBar.WARNING
         zDuration = self.SliderWARNING.value()
      zMsg = "%s :<br><u><i>%s</i></u><br>%s." % (QApplication.translate("QSphere", "Current URL", None, QApplication.UnicodeUTF8), \
                                zURL, zTextIsValid)
      SendMessage(self, zTitle, zMsg, zPicto, zDuration)
      self.stopMovie()

      return isValidURL

    
  def resizeEvent(self,ev):
     zSize = ev.size()
     self.PrintButton.setGeometry(zSize.width()-240, zSize.height()-30, 25, 25) 
     self.SaveButton.setGeometry(zSize.width()-190, zSize.height()-30, 25, 25)
     self.CloseButton.setGeometry(zSize.width()-120, zSize.height()-30, 100, 25)

     self.tabWidget.setGeometry(QRect(205, 10, zSize.width()-225, 460))
     
     self.groupBoxServer.setGeometry(10, 10, zSize.width()-240, zSize.height()-240)
     
     self.labelServerMetadata.setGeometry(10, 25, zSize.width()-165, 25)
     self.serverMetadata.setGeometry(10, 50, zSize.width()-310, 25)
     self.ButServerMetadata.setGeometry(zSize.width()-295, 50, 40, 24)

     self.labelServerKeywords.setGeometry(10, 100, zSize.width()-165, 25)
     self.serverKeywords.setGeometry(10, 125, zSize.width()-310, 25)
     self.ButServerKeywords.setGeometry(zSize.width()-295, 125, 25, 25)

     self.labelServerNavigator.setGeometry(10, 175, zSize.width()-165, 25)
     self.serverNavigator.setGeometry(10, 200, zSize.width()-310, 25)
     self.ButServerNavigator.setGeometry(zSize.width()-295, 200, 25, 25)

     self.groupBoxDir.setGeometry(10, 10, zSize.width()-240, 80)

     self.labelRep.setGeometry(10, 25, zSize.width()-165, 25)
     self.txtRep.setGeometry(10, 50, zSize.width()-310, 25)
     self.BDefineRep.setGeometry(zSize.width()-295, 50, 25, 25)

     self.groupBoxDuration.setGeometry(10, 100, zSize.width()-240, 180)

     self.groupParserInfo.setGeometry(10, 10, zSize.width()-240, zSize.height()-320)
     self.checkAutoCorrect.setGeometry(10, 15, zSize.width()-165, 25)
     self.radioStream.setGeometry(30, 45, zSize.width()-165, 25)
     self.radioFile.setGeometry(30, 75, zSize.width()-165, 25)

     self.labelRepXML.setGeometry(10, 110, zSize.width()-165, 25)
     self.txtRepXML.setGeometry(10, 135, zSize.width()-310, 25)
     self.BDefineRepXML.setGeometry(zSize.width()-295, 135, 25, 25)

     self.groupEditorInfo.setGeometry(10, zSize.height()-300, zSize.width()-240, 90)
     self.checkSilentMode.setGeometry(10, 20, zSize.width()-165, 25)
     self.checkReportingCSWT.setGeometry(10, 50, zSize.width()-165, 25)
     
     self.groupCSWTInfo.setGeometry(10, 10, zSize.width()-240, zSize.height()-60)

     self.labelListConnexionCSWT.setGeometry(10, 30, 140, 20)

     self.ButListConnexionCSWT.setGeometry(20, 55, 25, 25)
     self.ListConnexionCSWT.setGeometry(65, 55, zSize.width()-435, 25)
     self.butDefaultConnexionCSWT.setGeometry(zSize.width()-365, 55, 25, 25)
     self.ButNewConnexionCSWT.setGeometry(zSize.width()-335, 55, 25, 25)
     self.butEditConnexionCSWT.setGeometry(zSize.width()-310, 55, 25, 25)
     self.butDelConnexionCSWT.setGeometry(zSize.width()-285, 55, 25, 25)
     
     self.groupConnexionInfo.setGeometry(20, 100, zSize.width()-280, zSize.height()-170)

     self.labelNameConnexionCSWT.setGeometry(10, 15, 250, 20)
     self.nameConnexionCSWT.setGeometry(10, 35, 300, 25)
     self.ButAddConnexionCSWT.setGeometry(315, 28, 48, 48)

     self.labelServerCSWT.setGeometry(10, 70, 250, 20)
     self.serverCSWT.setGeometry(10, 90, zSize.width()-350, 25)
     self.ButGetCapabilitiesServerCSWT.setGeometry(zSize.width()-330, 80, 25, 25)

     self.labelAuthServerCSWT.setGeometry(10, 145, 250, 20)
     self.authServerCSWT.setGeometry(10, 165, zSize.width()-350, 25)
     self.ButGetAuthentificationServerCSWT.setGeometry(zSize.width()-330, 155, 25, 25)

     self.labelUserServerCSWT.setGeometry(10, 200, zSize.width()-165, 20)
     self.UserCSWT.setGeometry(10, 220, zSize.width()-610, 25)
     
     self.labelPwdUserServerCSWT.setGeometry(10, 250, 250, 20)
     self.pwdUserCSWT.setGeometry(10, 270, zSize.width()-610 , 25)
    
     self.checkViewPwdUserCSWT.setGeometry(20, 300, 200, 20)

     self.status_txt.setGeometry(int(zSize.width()/2)-64, int(zSize.height()/2)-64, 64, 64)
     self.barInfo.setGeometry(0, 0, zSize.width(), 90)
     

  def close(self): self.reject()

  def printFile(self):
      savefile = os.path.join(os.path.dirname(__file__),"ressources/options.ini")
      if os.path.exists(savefile):

          myfile = open(savefile, 'r')
          myfileText = myfile.readlines()
          myfile.close()
          lineText = ""
          for k in range(len(myfileText)): lineText+= "%s" % (MarkerText(self, myfileText[k]))

          printer = QPrinter()
          printer.setPageSize(QPrinter.A4)
          printer.setOrientation(QPrinter.Landscape) 
          printer.setPageMargins(5, 10, 5, 10, QPrinter.Millimeter) 
          printer.setOutputFormat(QPrinter.NativeFormat)

          editor = QWebView()
          editor.setHtml(lineText)
          
          printDialog = QPrintPreviewDialog(printer)
          MakeWindowIcon(printDialog, "print.png")
          printDialog.setWindowTitle(QApplication.translate("QSphere", "Print ini file", None, QApplication.UnicodeUTF8))
          printDialog.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint)

          printDialog.paintRequested.connect(editor.print_)
          printDialog.exec_() 




