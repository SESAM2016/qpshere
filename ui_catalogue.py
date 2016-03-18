# -*- coding:utf-8 -*-

import ConfigParser
import os.path
import doUI 
from qsphere_tools import *
from qsphere_objmaker import *
from importexport import *
from ui_editorXML import xmlEditor

from datetime import date
import datetime
from PyQt4 import QtCore, QtGui
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from PyQt4 import Qsci
from PyQt4.Qsci import QsciScintilla, QsciScintillaBase, QsciLexerXML
from PyQt4.QtWebKit import *
from PyQt4 import QtWebKit
from qgis.core import *
from qgis.gui import *

import urllib, webbrowser
import xml.etree.ElementTree as ET
from cswt_connector import *


class Ui_Dialog_Metadata(object):
    def __init__(self, iface):
        self.iface = iface
    
    def setupUi(self):
        self.setObjectName("DialogMetaData")
        self.setAccessibleName("DialogMetaData")
        MakeWindowIcon(self, "qsp.png")
        sizeW, sizeH, self.minwidth, self.minheight = 1100, 680, 290, 680
        self._W, self._H = sizeW, sizeH

        self.libelles = {
                         0:  ("tab1", QWidget, "Identification", "Identification data (title, abstract,\ntype, encoding ...)", "identification.png", ""), \
                         1:  ("titletab1", QLabel, "Data identification : ","Data identification ", None, ""), \
                         2:  ("intitule", QLineEdit, "Title : ", "Title of spatial data sets and services ", None, "file:intitule_%s.html"), \
                         3:  ("resume", MyTextEdit, "Abstract : ", "Abstract of the dataset describing the resource ", None, "file:resume_%s.html"), \
                         4:  ("typedata", QComboBox, "Resource type : ", "Resource type ", None, "file:type_ressource_%s.html"), \
                         5:  ("tablelocalisator", MyTableWidget, "Locator (s) for the resource : ", "Link(s) for the resource ", None, "file:localisateur_%s.html"), \
                         6:  ("tablelocalisator_c0", None, "URL", "", None, ""), \
                         7:  ("tablelocalisator_c1", None, "Name", "", None, ""), \
                         8:  ("identificator", QLineEdit, "Resource Identifier : ", "Identifier for the resource ", None, "file:identificateur_%s.html"), \
                         9:  ("tablelangues", QTableView, "Language(s) for the resource : ", "List of language(s) for the resource : ", None, "file:langue_%s.html"), \
                         10: ("tableformats", MyTableWidget, "Format(s) : ", "Different formats of spatial data sets and services ", None, "file:format_fichier_%s.html"), \
                         11: ("tableformats_c0", None, "Format", "", None, ""), \
                         12: ("tableformats_c1", None, "", "", None, ""), \
                         13: ("tableformats_c2", None, "Version", "", None, ""), \
                         14: ("tablecarac", QComboBox, "Encoding : ", "Character encoding of spatial data sets and services ", None, "file:encodage_%s.html"), \
                         15: ("tab2", QWidget, "Classification & Keywords","Classification & Keywords", "classification.png", ""), \
                         16: ("titletab2_1", QLabel, "Classification of spatial data and services : ", "Data classification and mapping services ", None, ""), \
                         17: ("tablecategories", QTableView, "Thematic categories : ", "Thematic categories\n(INSPIRE Annexes - INSPIRE Themes - ISO classes ) ", None, "file:categorie_thematique_%s.html"), \
                         18: ("titletab2_2", QLabel, "Keywords : ", "Keywords ", None, ""), \
                         19: ("tablemotsclefso", MyTableWidget, "Keywords from INSPIRE<br>Data themes & repositories : ", "List of keywords required (INSPIRE Themes) ", None, "file:mots_clefs_%s.html"), \
                         20: ("tablemotsclefso_c0", None, "Thematic", "", None, ""), \
                         21: ("tablemotsclefso_c1", None, "Keyword", "", None, ""), \
                         22: ("tablemotsclefsf", MyTableWidget, "<i>Free</i> keywords : ", "List of optional keywords (INSPIRE Themes) ", None, "file:mots_clefs_%s.html"), \
                         23: ("tablemotsclefsf_c0", None, "Keyword", "", None, ""), \
                         24: ("tablemotsclefsf_c1", None, "", "", None, ""), \
                         25: ("tablemotsclefsf_c2", None, "Controlled vocabulary ", "", None, ""), \
                         26: ("tablemotsclefsf_c3", None, "Date", "", None, ""), \
                         27: ("tablemotsclefsf_c4", None, "Date type", "", None, ""), \
                         28: ("tab3", QWidget, "Geographic", "Geographical location", "location.png", None, ""), \
                         29: ("titletab3_1", QLabel, "Location : ", "Information for the location (data required) ", None, ""), \
                         30: ("subtitletab3_1", QLabel, "Bouding box : ", "Information for the location (Bouding box) ", None, ""), \
                         31: ("tableemprises", MyTableWidget, "", "List of the extents of spatial data sets and services ", None, "file:emprise_%s.html"), \
                         32: ("tableemprises_c0", None, "North lat.", "", None, ""), \
                         33: ("tableemprises_c1", None, "South lat.", "", None, ""), \
                         34: ("tableemprises_c2", None, "West long.", "", None, ""), \
                         35: ("tableemprises_c3", None, "East long.", "", None, ""), \
                         36: ("tableemprises_c4", None, "Extent", "", None, ""), \
                         37: ("subtitletab3_2", QLabel, "Coordinate reference system(s) : ", "Information about coordinate reference system(s) (data required) ", None, ""), \
                         38: ("tablescr", MyTableWidget, "SRS : " ,"List of reference system(s) of spatial data sets and services ", None, "file:systeme_de_reference_%s.html"), \
                         39: ("tablescr_c0", None, "Selected CRS", "", None, ""), \
                         40: ("tablescr_c1", None, "", "", None, ""), \
                         41: ("tab4", QWidget, "Temporal", "Dates temporal referencing", "temporality.png", ""), \
                         42: ("titletab4_1", QLabel, "Temporal informations : ", "Temporal informations ", None, ""), \
                         43: ("tableetenduetemporelle", MyTableWidget, "Temporal extent : ", "Information about temporal extent (optional data)", None, "file:etendue_temporelle_%s.html"), \
                         44: ("tableetenduetemporelle_c0", None, " Start <-> End ", "", None, ""), \
                         45: ("tableetenduetemporelle_c1", None, "", "", None, ""), \
                         46: ("tabledatepubdata", MyTableWidget, "Date of publication : ", "Date of publication of spatial data sets and services ", None, "file:dates_reference_%s.html"), \
                         47: ("tabledatepubdata_c0", None, "Date", "", None, ""), \
                         48: ("tabledatepubdata_c1", None, "", "", None, ""), \
                         49: ("datecredata", QCalendarWidget, "Date of creation : ", "Date of creation of spatial data sets and services ", None, "file:dates_reference_%s.html"), \
                         50: ("daterevdata", QCalendarWidget, "Date of the last revision : ", "Date of the last revision of spatial data sets and services ", None, "file:dates_reference_%s.html"), \
                         51: ("sysreftemp", QComboBox, "Temporal reference system : ", "Temporal reference system ", None, "file:systeme_de_reference_temporel_%s.html"), \
                         52: ("tab5", QWidget, "Quality, Validity and Conformity", "Quality, Validity and Conformity", "quality.png", ""), \
                         53: ("titletab5_1", QLabel, "Quality & validity : ", "Quality & validity", None, ""), \
                         54: ("subtitletab5_1", QLabel, "Lineage : ", "Lineage of spatial data sets and services ", None, ""), \
                         55: ("genealogie", MyTextEdit, "Lineage for the data : ", "Lineage of spatial data sets and services ", None, "file:genealogie_%s.html"), \
                         56: ("subtitletab5_2", QLabel, "Spatial resolution : ", "Spatial resolution of spatial data sets and services ", None, ""), \
                         57: ("grouperesolutionscale", QGroupBox, "Equivalent scale : ", "Equivalent scale of spatial data sets and services ", None, "file:resolution_spatiale_%s.html"), \
                         58: ("coherence", MyTextEdit, "Topological consistency : ", "Topological consistency of spatial data sets and services (data not required) ", None, "file:coherence_topologique_%s.html"), \
                         59: ("subtitletab5_3", QLabel, "Compliance : ", "Compliance of spatial data sets and services ", None, ""), \
                         60: ("tablespecifications", MyTableWidget, "Compliance specifications : ", "List of compliance specifications of spatial data sets and services ", None, "file:conformite_specifications_%s.html"), \
                         61: ("tablespecifications_c0", None, "Specification", "", None, ""), \
                         62: ("tablespecifications_c1", None, "Date", "", None, ""), \
                         63: ("tablespecifications_c2", None, "Date type", "", None, ""), \
                         64: ("tablespecifications_c3", None, "Class", "", None, ""), \
                         65: ("tab6", QWidget, "Constraints", "Access and uses", "rights_and_uses.png", ""), \
                         66: ("titletab6_1", QLabel, "Constraint related to access and use : ", "Constraint related to access and use ", None, ""), \
                         67: ("groupedroits", QGroupBox, "Conditions applying...\nto access and use : ", "Conditions applying to access and use ", None, "file:contraintes_%s.html"), \
                         68: ("licence", MyTextEdit, "Conditions licensing applying...\nto access and use : ", "Licensing conditions applying to access and use ", None, "file:licence_%s.html"), \
                         69: ("tab7", QWidget, "Responsible party", "Responsible party", "responsible.png", ""), \
                         70: ("titletab7_1", QLabel, "Responsible party : ", "Organisations reponsible for the etablishment, management, maintenance and distribution of spatial data sets and services ", None, ""), \
                         71: ("tableroles", MyTableWidget, "", "Responsible party role ", None, "file:organisme_responsable_%s.html"), \
                         72: ("tableroles_c0", None, "Role", "", None, ""), \
                         73: ("tableroles_c1", None, "Organization name", "", None, ""), \
                         74: ("tableroles_c2", None, "Address", "", None, ""), \
                         75: ("tableroles_c3", None, "Country", "", None, ""), \
                         76: ("tableroles_c4", None, "Zip code", "", None, ""), \
                         77: ("tableroles_c5", None, "City", "", None, ""), \
                         78: ("tableroles_c6", None, "E-mail", "", None, ""), \
                         79:("tableroles_c7", None, "Phone", "", None, ""), \
                         80:("tableroles_c8", None, "URL", "", None, ""), \
                         81: ("tab8", QWidget, "Metadata", "Metadata", "metadata.png", ""), \
                         82: ("titletab8_1", QLabel, "Informations about Metadata : ", "Informations about Metadata ", None, ""), \
                         83: ("datemetada", QCalendarWidget, "Metadata date : ", "Metadata date ", None, "file:date_metadonnee_%s.html"), \
                         84: ("langmetada", QComboBox, "Metadata language : ", "Metadata language ", None, "file:langue_metadonnee_%s.html"), \
                         85: ("tab9", QWidget, "QGIS metadata", "Metadata by QGIS", "qgis.png", ""), \
                         86: ("titletab9_1", QLabel, "Additional Information QGIS QSPHERE : ", "Additional Information QGIS QSPHERE : ", None, ""), \
                         87: ("namelayer", QLineEdit, "Name layer : ", "Name Layer ", None, "file:catalogue_attributaire_%s.html"), \
                         88: ("typelayer", QLineEdit, "Type layer : ", "Type Layer ", None, "file:catalogue_attributaire_%s.html"), \
                         89: ("metadata", MyTextEdit, "", "Generic metadata QGIS for geographical layer (vector or raster) ", None, "file:catalogue_attributaire_%s.html"), \
                         90: ("tabledico", MyTableWidget, "", "Fields for the query layer (vector) ", None, "file:catalogue_attributaire_%s.html") , \
                         91: ("tabledico_c0", None, "Id", "", None, ""), \
                         92: ("tabledico_c1", None, "Name", "", None, ""), \
                         93: ("tabledico_c2", None, "Type", "", None, ""), \
                         94: ("tabledico_c3", None, "Length", "", None, ""), \
                         95: ("tabledico_c4", None, "Precision", "", None, ""), \
                         96: ("tabledico_c5", None, "Comment", "", None, ""), \
                         100:("helptopic", MyPushButton, "", "Get informations for this topic", "info.png", ""), \
                         101:("actionsmetadata", MyPushButton, "", "Actions for the metadata...", "actions.png", ""), \
                         102:("callwizard", MyPushButton, "", "Call the wizards ...", "wizards.png", ""), \
                         103:("calllustre", MyPushButton, "", "Call the LusTRE wizard ...", "lustre_wizard.png", "")
                         }

        self.Tableaux, self.comboLayersCurrentLayerId = {}, 0
        self.ParamsLineWidget = { "tablescr" : [(0, 3, "4258"), (1, -1, "")], \
                                  "tableformats" : [(0, 6, ""), ( 1, -1, ""), (-1, 0, "")], \
                                  "tableroles" : [(2, 0, 6),(-1, 0, ""), (-1, 0, ""), (2, 5, self.indexCountry), (0, 2, ""), (-1, 0, ""), (0, 0, ""), (-1, 0, ""), (0, 4, "")], \
                                  "tablelocalisator" : [(0, 4, ""), (-1, 0, "")], \
                                  "tableemprises" : [(3, 0, -1), (3, 0, -1), (3, 0, -1), (3, 0, -1), (5, 0, "")], \
                                  "tableetenduetemporelle" :[(0, 1, "")], \
                                  "tabledatepubdata": [(0, 5, "")], \
                                  "tablemotsclefso" : [(2, 1, 0), (2, -1, (0,0))], \
                                  "tablemotsclefsf" : [(-1, 0, ""), (6, 0, 0), (-1, 0, ""), (0, 5, ""), (2, 2, 0)], \
                                  "tablespecifications" : [(-1, 0, ""), (0, 5, ""), (2, 2, 0), (2, 3, 0)], \
                                  "tableechelles" : [(4, 0, -1)]
                                  }
        
        self.ShowWarning = True
        self.translatezTablesWidget()
        makeGetOptions(self)
        
        self.InitName = ""
        self.TypeData = ("dataset", "series", "service")
        self.ListUnitsMesure = ["m", "km", "foot", "inch", "mile", "yard"]
        self.restore_tabledico = None

        self._connexionCSWT = None
        self.ToolTipLangue = ""

        self.setMinimumSize(QSize(self.minwidth, self.minheight))
        self.setMaximumSize(QSize(sizeW-30, sizeH))
        self.resize(QSize(QRect(0,0,sizeW-30,sizeH).size()).expandedTo(self.minimumSizeHint()))
        
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setGeometry(280, 10, 780, 620)
        
        self.editor = QsciScintilla(self)
        self.editor.findDialog = FindDialog(self)
       
        self.editor.setObjectName("xmlWidget")
        self.editor.setReadOnly(True)
        self.editor.setGeometry(280, 10, 780, 615)

        self.editor.find_text = ""
        self.editor.find_forward = True
        self.ARROW_MARKER_NUM = 8

        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.editor.setFont(font)
        self.editor.setMarginsFont(font)

        fontmetrics = QFontMetrics(font)
        self.editor.setMarginsFont(font)
        self.editor.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.editor.setMarginLineNumbers(1, True)
        self.editor.setMarginsBackgroundColor(QColor("#cccccc"))

        self.editor.setMarginSensitivity(1, True)
        self.editor.marginClicked.connect(self.on_margin_clicked)
        
        self.editor.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        self.editor.setMarkerBackgroundColor(QColor("#ee1111"), self.ARROW_MARKER_NUM)
        self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor("#ffffcc"))
        self.editor.setUtf8(True)

        lexer = QsciLexerXML(self) 
        api = Qsci.QsciAPIs(lexer)
        api.prepare()
        self.editor.setAutoCompletionSource(QsciScintilla.AcsDocument)
        self.editor.setAutoCompletionFillupsEnabled(True)
        self.editor.setAutoCompletionThreshold(2)
        self.editor.setLexer(lexer)
        
        font = QFont() 
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.editor.setFont(font)
        
        font.setFamily('Courier')
        font.setPointSize(8)
        self.editor.setMarginsFont(font)
        large = '9999'
        self.editor.setMarginWidth(0, large) 
        self.editor.setMarginLineNumbers(0, True)
        self.editor.setMarginWidth(1,1) 
        
        self.editor.setMarginsBackgroundColor(QColor("#cccccc"))
        self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor("#ffe4e4"))
        
        self.editor.setTabWidth(5) 
        self.editor.setIndentationsUseTabs(True) 
        self.editor.setIndentationWidth(5) 
        self.editor.setTabIndents(True) 
        self.editor.setBackspaceUnindents(True) 
        self.editor.setAutoIndent( True )
        self.editor.setIndentationGuides( True )
        self.editor.setFolding(QsciScintilla.CircledTreeFoldStyle) 
        self.editor.setFoldMarginColors(QColor("#99CC66"), QColor("#AAAAAA"))
        self.editor.setMarginsBackgroundColor(QColor("#00b4FF"))
        self.editor.setMarginsForegroundColor(QColor("#FFFFFF"))
        
        self.editor.setWrapMode( QsciScintilla.WrapWord )
        self.editor.setWrapIndentMode( QsciScintilla.WrapIndentSame )        
        
        self.webWidget = QWebView(self)
        self.webWidget.setGeometry(280, 10, 780, 615)
        self.webWidget.setObjectName("viewHTML")
        self.webWidget.setAccessibleName("viewHTML")
        self.webWidget.settings().setAttribute(QWebSettings.JavaEnabled, True)
        self.webWidget.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        self.webWidget.settings().setAttribute(QWebSettings.AutoLoadImages, True)
        self.webWidget.settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
        self.webWidget.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
        self.webWidget.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        self.webWidget.settings().setAttribute(QWebSettings.LinksIncludedInFocusChain, True)
        self.webWidget.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.webWidget.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.webWidget.page().setForwardUnsupportedContent(True)

        self.webWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.webWidget.customContextMenuRequested.connect(self.context_menu_requested)

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

        SizeLabelW, SizeLabelH = 60, 25
        self.SizeWW, self.SizeWH = 200, 25
        self.EmpriseLat, self.EmpriseLong = 180, 360

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(QRect(10, 10, 280, 620))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet("* { font-size:12px; background-color:#5D5D5D; padding: 4px ; color:rgb(255,255,255)}"
                                      "QListWidget::item:selected {color: #5D5D5D;background-color: rgb(255,255,255);  padding: 12px;}")
        self.listWidget.setIconSize(QSize(42, 42))
        
        zScroll, i = {}, 1
        for key in (self.libelles.keys()):
            if self.libelles[key][1]== QWidget :
                zIcon = getThemeIcon(self.libelles[key][4])
                zNameTab = self.libelles[key][0]

                zText    = QApplication.translate("QSphere", self.libelles[key][2], None, QApplication.UnicodeUTF8)
                zToolTip = QApplication.translate("QSphere", self.libelles[key][3], None, QApplication.UnicodeUTF8)
                zItem =  QListWidgetItem(QIcon(zIcon), zText, self.listWidget)
                zItem.setToolTip(zToolTip)

                zTab = QWidget(self)
                zTab.setObjectName(zNameTab) 
                zTab.setAccessibleName(zNameTab) 
                
                self.tabWidget.addTab(zTab, zText) 
                self.tabWidget.setTabToolTip(i-1, zToolTip) 
                makeTABWidgets(self, zTab, i, SizeLabelW, SizeLabelH, self.SizeWW, self.SizeWH)
                i+= 1

        self.barInfo = QgsMessageBar(self)
        self.barInfo.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )
        self.barInfo.setGeometry(QRect(0, 0, sizeW-10, 90))

        self.backgroundMode = QLabel(self)
        self.backgroundMode.setGeometry(QRect(11, 480, 278, 15))
        myDefPathIcon = getThemeIcon("base.png")
        carIcon = QImage(myDefPathIcon) 
        self.backgroundMode.setPixmap(QPixmap.fromImage(carIcon))
        
        self.changeMode = QButtonGroup(self)

        styleSheetPushButton = "QPushButton {icon-size: 48px, 48px; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #cccccc, stop: 1 #5D5D5D);  border-width: 2px; border-radius: 10px; border-color: beige;}"
        styleSheetPushButton+= "QPushButton::checked {icon-size: 48px, 48px;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E0E0E0, stop: 1 #FFFFFF); border-width: 2px; border-radius: 10px; border-color: white;}"
        
        self.formMode = MyPushButton(self)
        self.formMode.initPushButton(48, 48, 60, 460, "formMode", "", "", True, getThemeIcon("n_project.png"), 48, 48, True)
        self.formMode.setCheckable(True)
        self.formMode.setChecked(True)
        self.formMode.setStyleSheet(styleSheetPushButton)

        self.xmlMode = MyPushButton(self)
        self.xmlMode.initPushButton(48, 48, 120, 460, "xmlMode", "", "", True, getThemeIcon("n_xml.png"), 48, 48, True)
        self.xmlMode.setCheckable(True)
        self.xmlMode.setStyleSheet(styleSheetPushButton)

        self.htmlMode = MyPushButton(self)
        self.htmlMode.initPushButton(48, 48, 180, 460, "htmlMode", "", "", True, getThemeIcon("n_html.png"), 48, 48, True)
        self.htmlMode.setCheckable(True)
        self.htmlMode.setStyleSheet(styleSheetPushButton)

        self.changeMode.addButton(self.formMode, 0)
        self.changeMode.addButton(self.xmlMode, 1)
        self.changeMode.addButton(self.htmlMode, 2)

        self.childswindows = []

        self.window_childs = QLabel(self)
        self.window_childs.setGeometry(QRect(120, 550, 48, 48))
        myDefPathIcon = getThemeIcon("mdi.png")
        carIcon = QImage(myDefPathIcon) 
        self.window_childs.setPixmap(QPixmap.fromImage(carIcon))

        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(12)
        font.setBold(True)

        self.nb_window_childs = QLabel(self.window_childs)
        self.nb_window_childs.setGeometry(15, 25, 20, 20)
        self.nb_window_childs.setText("0")
        self.nb_window_childs.setFont(font)

        self.mode_project = QLabel(self)
        self.mode_project.setGeometry(QRect(210, 560, 80, 40))
        myDefPathIcon = getThemeIcon("modenone.png")
        carIcon = QImage(myDefPathIcon) 
        self.mode_project.setPixmap(QPixmap.fromImage(carIcon))

        self.langs_gui_base = QLabel(self)
        self.langs_gui_base.setGeometry(QRect(11, 600, 278, 15))
        myDefPathIcon = getThemeIcon("langs_gui.png")
        carIcon = QImage(myDefPathIcon) 
        self.langs_gui_base.setPixmap(QPixmap.fromImage(carIcon))

        self.langs_gui = MyPushButtonMappable(self)
        myDefPathIcon = getThemeIcon("langs_gui_%s.png" % (self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]))
        self.langs_gui.initPushButton(278, 15, 11, 600, "langs_gui", "", "", True, myDefPathIcon, 278, 15, True)
        self.langs_gui.isMappable = True
        self.langs_gui.MainPlugin = self.MainPlugin

        self.BReduceWindow = MyPushButton(self)
        self.BReduceWindow.initPushButton(24, 24, 10, 575, "BReduceWindow", "", "", True, getThemeIcon("hreduce.png"), 24, 24, True)

        self.BExpandWindow = MyPushButton(self)
        self.BExpandWindow.initPushButton(24, 24, 35, 575, "BExpandWindow", "", "", True, getThemeIcon("hexpand.png"), 24, 24, True)

        self.progressBar = QProgressBar(self)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet(
             """QProgressBar {border: 2px solid grey; border-radius: 5px; text-align: center;}"""
             """QProgressBar::chunk {background-color: #6C96C6; width: 20px;}"""
        )
        self.progressBar.setVisible(False)
        self.progressBar.setGeometry(20, 520, 260, 15)
        self.progressBar.setValue(0)

        self.ToolBarActionsTools = QToolBar(self)
	self.ToolBarActionsTools.setObjectName("ToolBarActionsTools")
	self.ToolBarActionsTools.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
	self.ToolBarActionsTools.setGeometry(10, sizeH-50, 280, 50)
	
        self.ToolBarActions = QToolBar(self)
	self.ToolBarActions.setObjectName("ToolBarActions")
	self.ToolBarActions.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
	self.ToolBarActions.setGeometry(285, sizeH-50, sizeW-420, 50)
        
        zIcon = getThemeIcon("servers.png")
        self.navigatorWeb = MyPushButton() 
        self.navigatorWeb.initPushButton(48, 32, 30, 570, "navigatorWeb", "", "", True, zIcon, 48, 32, True)
        
        zIcon = getThemeIcon("editxml.png")
        self.editXMLButton = MyPushButton() 
        self.editXMLButton.initPushButton(48, 32, 80, 570, "editXMLButton", "", "", True, zIcon, 48, 32, True)
        
        zIcon = getThemeIcon("contact.png")
        self.loadContacts = MyPushButton() 
        self.loadContacts.initPushButton(48, 32, 130, 570, "loadContacts", "", "", True, zIcon, 48, 32, True)

        zIcon = getThemeIcon("qsphereoptions.png")
        self.OptionsButton = MyPushButton() 
        self.OptionsButton.initPushButton(64, 32, 180, 570, "OptionsButton", "", "", True, zIcon, 64, 32, True)        

        zIcon = getThemeIcon("help.png") 
        self.HelpButton = MyPushButton() 
        self.HelpButton.initPushButton(48, 32, 230, 570, "HelpButton", "", "", True, zIcon, 48, 32, True)
        self.HelpButton.setShortcut(QKeySequence("F1"))
	
        zIcon = getThemeIcon("new.png")
        self.NewButton = MyPushButton() 
        self.NewButton.initPushButton(48, 48, 690, sizeH-30, "NewButton", "", "", True, zIcon, 48, 48, True)
        self.NewButton.setShortcut(QKeySequence("Ctrl+N"))

        zIcon = getThemeIcon("open.png")
        self.LoadButton = MyPushButton() 
        self.LoadButton.initPushButton(48, 48, 720, sizeH-30, "LoadButton", "", "", True, zIcon, 48, 48, True)
        self.LoadButton.setShortcut(QKeySequence("Ctrl+O"))

        zIcon = getThemeIcon("reload.png")
        self.ReLoadButton = MyPushButton() 
        self.ReLoadButton.initPushButton(48, 48, 760, sizeH-30, "ReLoadButton", "", "", True, zIcon, 48, 48, True)
        self.ReLoadButton.setShortcut(QKeySequence("F5"))

        zIcon = getThemeIcon("print.png")
        self.PrintButton = MyPushButton() 
        self.PrintButton.initPushButton(48, 48, 800, sizeH-30, "PrintButton", "", "", True, zIcon, 48, 48, True)
        self.PrintButton.setShortcut(QKeySequence("Ctrl+P"))

        zIcon = getThemeIcon("save.png")
        self.SaveButton = MyPushButton() 
        self.SaveButton.initPushButton(48, 48, 800, sizeH-30, "SaveButton", "", "", True, zIcon, 48, 48, True)
        self.SaveButton.setShortcut(QKeySequence("Ctrl+S"))

        zIcon = getThemeIcon("saveactions.png")
        self.ActionsSaveButton = MyPushButton() 
        self.ActionsSaveButton.initPushButton(64, 48, 830, sizeH-30, "ActionsSaveButton", "", "", True, zIcon, 64, 48, True)

        zIcon = getThemeIcon("cswtactions.png")
        self.ActionsCSWTButton = MyPushButton() 
        self.ActionsCSWTButton.initPushButton(64, 48, 890, sizeH-30, "ActionsCSWTButton", "", "", True, zIcon, 64, 48, True)
        self.ActionsCSWTButton.setShortcut(QKeySequence("Ctrl+T"))


        self.LblComboLayers = QLabel()
        self.LblComboLayers.setGeometry(10, 10, 150, SizeLabelH)
        self.LblComboLayers.setAlignment(Qt.AlignRight)
        self.LblComboLayers.setObjectName("LblComboLayers")
        

        self.model = QStandardItemModel()
        self.view = QTableView()
        self.view.setModel( self.model )
        self.view.horizontalHeader().setVisible(False)
        self.view.verticalHeader().setVisible(False)
        self.view.setColumnHidden(1, True)
        self.view.verticalHeader().setDefaultSectionSize(20)
        self.view.setStyleSheet("QTableView {min-width: 400px; max-width: 500px; selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5, stop: 0 #FFFFFF, stop: 1 #000000);}")
        self.view.setShowGrid(False)

        self.ComboLayers = QComboBox()
        self.ComboLayers.setGeometry(170, sizeH-30, 150, SizeLabelH)
        self.ComboLayers.setMinimumSize(150, SizeLabelH)
        self.ComboLayers.setMaximumSize(150, SizeLabelH)
        self.ComboLayers.setObjectName("ComboLayers")
        self.ComboLayers.setAccessibleName("ComboLayers")
        self.ComboLayers.setModel(self.model)
        self.ComboLayers.setView(self.view)

       
        self.listeXSLT = makeListXSLT(self)
        self.LblPrimaryXSLT = QLabel()
        self.PrimaryXSLT = QComboBox()
        self.PrimaryXSLT.addItems(self.listeXSLT)
        
        zTest, zValue = fileRessourceExist(self, "xml/xsl/transformation_%s.xsl" % (self.langueTR))

        if zValue != "" : zValue = os.path.basename(zValue)
        zIndex = self.listeXSLT.index(zValue) if zValue in (self.listeXSLT) else 0
        self.PrimaryXSLT.setCurrentIndex(zIndex)

        self.findprevious = MyPushButton()
        self.findprevious.initPushButton(48, 24, 5, 5, "findprevious", "", QApplication.translate("QSphere", "Find previous", None, QApplication.UnicodeUTF8), True, getThemeIcon("leftarrow.png"), 48, 24, True)
        self.findprevious.setShortcut(QKeySequence("F2"))

        self.searchbutton = MyPushButton()
        self.searchbutton.initPushButton(24, 24, 5, 5, "searchbutton", "", QApplication.translate("QSphere", "Search word", None, QApplication.UnicodeUTF8), True, getThemeIcon("find.png"), 24, 24, True)
        self.searchbutton.setShortcut(QKeySequence("Ctrl+F"))

        self.findnext = MyPushButton()
        self.findnext.initPushButton(48, 24, 5, 5, "findnext", "", QApplication.translate("QSphere", "Find next", None, QApplication.UnicodeUTF8), True, getThemeIcon("rightarrow.png"), 48, 24, True)
        self.findnext.setShortcut(QKeySequence("F3"))

        self.ToolBarActionsTools.addWidget(self.navigatorWeb)
        self.ToolBarActionsTools.addWidget(self.editXMLButton)
        self.ToolBarActionsTools.addWidget(self.loadContacts)
        self.ToolBarActionsTools.addWidget(self.OptionsButton)
        self.ToolBarActionsTools.addWidget(self.HelpButton)

        self.ToolBarActions.addSeparator()
        self.ToolBarActions.addWidget(self.NewButton)
        self.ToolBarActions.addWidget(self.LoadButton)
        self.ToolBarActions.addWidget(self.ReLoadButton)
        self.ToolBarActions.addSeparator()
        self.ToolBarActions.addWidget(self.PrintButton)
        self.ToolBarActions.addSeparator()
        self.ToolBarActions.addWidget(self.SaveButton)
        self.ToolBarActions.addWidget(self.ActionsSaveButton)
        self.ToolBarActions.addWidget(self.ActionsCSWTButton)
        self.ToolBarActions.addSeparator()
        self.actionLblComboLayers = self.ToolBarActions.addWidget(self.LblComboLayers)
        self.actionComboLayers = self.ToolBarActions.addWidget(self.ComboLayers)
        self.actionLblPrimaryXSLT = self.ToolBarActions.addWidget(self.LblPrimaryXSLT)
        self.actionPrimaryXSLT = self.ToolBarActions.addWidget(self.PrimaryXSLT)
        self.actionfindprevious = self.ToolBarActions.addWidget(self.findprevious)
        self.actionsearchbutton = self.ToolBarActions.addWidget(self.searchbutton)
        self.actionfindnext = self.ToolBarActions.addWidget(self.findnext)


        self.doChangeMode(0)

        self.status_txt = QLabel(self)
        self.movie = QMovie(getThemeIcon("sablier.gif"))
        self.status_txt.setMovie(self.movie)
        self.status_txt.setLayout(QHBoxLayout())
        self.status_txt.layout().addWidget(QLabel(''))
        self.status_txt.setVisible(False)
        self.status_txt.setGeometry(int(sizeW/2)-64, int(sizeH/2)-64, 64, 64)

        self.CloseButton = MyButton(self)
        self.CloseButton.initButton(100, SizeLabelH, 960, sizeH-40, "CloseButton", "", "" , True, True) 


        self.langs_gui.clicked.connect(self.changeLang)
        self.BReduceWindow.clicked.connect(self.ResizeWindow)
        self.BExpandWindow.clicked.connect(self.ResizeWindow)
        self.editXMLButton.clicked.connect(self.LoadXMLEditor)
        self.OptionsButton.clicked.connect(self.clickOptions)
        self.loadContacts.clicked.connect(self.ChooseContact)
        self.HelpButton.clicked.connect(self.clickHelp)        
        self.NewButton.clicked.connect(self.NewSheet)
        self.LoadButton.clicked.connect(self.loadMetadata)
        self.SaveButton.clicked.connect(self.SaveData)
        self.ReLoadButton.clicked.connect(self.ReLoadMetadata)
        self.changeMode.buttonClicked[int].connect(self.doChangeMode)
        self.PrintButton.clicked.connect(self.PrintMetadata)
        self.PrimaryXSLT.currentIndexChanged.connect(self.passChangeMode)
        self.findprevious.clicked.connect(self.findPrevious)
        self.searchbutton.clicked.connect(self.findText)
        self.findnext.clicked.connect(self.findNext)
        self.actionfindprevious.setEnabled(False)
        self.actionfindnext.setEnabled(False)
        self.CloseButton.clicked.connect(self.closeme)

        self.iface.mapCanvas().layersChanged.connect(self.UpdateListComboLayers)
        try : self.iface.mapCanvas().currentLayerChanged.connect(self.UpdateListComboLayers)
        except : pass
        self.iface.newProjectCreated.connect(self.UpdateListComboLayers)        
        self.listWidget.currentRowChanged.connect(self.fixeONGLETL)
        
        QMetaObject.connectSlotsByName(self)

        self.translateFixedWidgets()
        self.UpdateListComboLayers()
        
        self.iface.newProjectCreated.connect(self.UpdateListComboLayers)
        self.iface.projectRead.connect(self.UpdateListComboLayers)

        self.DessCadre()
        self.tabWidget.setCurrentIndex(0)
        self.listWidget.setCurrentRow(0)
        self.fixeONGLET()
        self.CountLangues()
        self.IsVisibleViewXMLButton()



    def on_margin_clicked(self, nmargin, nline, modifiers):
        if self.editor.markersAtLine(nline) != 0: self.editor.markerDelete(nline, self.ARROW_MARKER_NUM)
        else: self.editor.markerAdd(nline, self.ARROW_MARKER_NUM)
    
    def isBfind(self, bfind):          
        if not bfind:
           zTitle = QApplication.translate("QSphere", "Information", None, QApplication.UnicodeUTF8)
           zMsg = QApplication.translate("QSphere","Not found", None, QApplication.UnicodeUTF8)
           SendMessage(self, zTitle , "%s :<br><u><i>%s</i></ul>" % (zMsg, self.editor.find_text), QgsMessageBar.INFO, self.duration_info)
         
    def enableFindPrevNextButton(self):
        self.findprevious.setEnabled(not self.editor.find_text=="")
        self.findnext.setEnabled(not self.editor.find_text=="")
    
    def findText(self):
        ret = self.editor.findDialog.exec_()
        self.editor.findDialog.lineEdit.setFocus()
        if self.editor.findDialog.ret > 0 :
          self.editor.find_text = self.editor.findDialog.getFindText()
          self.enableFindPrevNextButton()

    def findNext(self):
        line, index = self.editor.getCursorPosition()
        bfind = self.editor.findFirst(self.editor.find_text, True, self.editor.findDialog.isCaseSensitive(), self.editor.findDialog.isWholeWord(), True, True, line, index)
        self.isBfind(bfind)
        self.enableFindPrevNextButton()

    def findPrevious(self):
        line, index = self.editor.getCursorPosition()
        index -= len(self.editor.find_text)
        bfind = self.editor.findFirst(self.editor.find_text, True, self.editor.findDialog.isCaseSensitive(), self.editor.findDialog.isWholeWord(), True, False, line, index)
        self.isBfind(bfind)
        self.enableFindPrevNextButton()

    def PrintMetadata(self):
        idbutton = self.changeMode.id(self.changeMode.checkedButton())
       
        printer = QPrinter()
        printer.setPageSize(QPrinter.A4)
        printer.setOrientation(QPrinter.Landscape) if idbutton == 1 else  printer.setOrientation(QPrinter.Portrait)
        printer.setPageMargins(5, 10, 5, 10, QPrinter.Millimeter) 
        printer.setOutputFormat(QPrinter.NativeFormat)

        if idbutton in (0, 1) :
            if idbutton == 0 :
                editor = QWebView()
                editor.setHtml(SaveQSP(self, ""))
            else :     
                editor = QTextEdit()
                editor.setAcceptRichText(True)
                editor.setPlainText(self.editor.text())
        
        printDialog = QPrintPreviewDialog(printer)
        MakeWindowIcon(printDialog, "print.png")
        printDialog.setWindowTitle(QApplication.translate("QSphere", "Print current file", None, QApplication.UnicodeUTF8))
        printDialog.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint)

        if idbutton in (0, 1) : printDialog.paintRequested.connect(editor.print_)
        elif idbutton == 2 : printDialog.paintRequested.connect(self.webWidget.print_)
        else : return
        printDialog.exec_() 

        

    def context_menu_requested(self, point):
        self.imageurl = None
        context_menu = QMenu()
        page = self.webWidget.page()
        frame = page.currentFrame()
        if unicode(self.webWidget.selectedText()):
            menuIcon = getThemeIcon("copier.png")
            zText = (QApplication.translate("QSphere", "Copy", None, QApplication.UnicodeUTF8))
            self.copy = context_menu.addAction(QIcon(menuIcon), zText)
            self.ToCopy = unicode(self.webWidget.selectedText())
            self.copy.triggered.connect(self.MakeToCopy)

        hit_test = frame.hitTestContent(point)
        
        if unicode(hit_test.linkUrl().toString()):
            menuIcon = getThemeIcon("copierlink.png")
            zText = (QApplication.translate("QSphere", "Copy link", None, QApplication.UnicodeUTF8))
            self.copyURL = context_menu.addAction(QIcon(menuIcon), zText)
            self.ToCopyURL = unicode(hit_test.linkUrl().toString())
            self.copyURL.triggered.connect(self.MakeToCopyURL)

            context_menu.addSeparator()

            zText = QApplication.translate("QSphere", "Go url", None, QApplication.UnicodeUTF8)
            self.openURL = context_menu.addAction(QIcon(menuIcon), zText)
            self.ToOpenURL = unicode(hit_test.linkUrl().toString())
            self.openURL.triggered.connect(self.MakeOpenURL)

            zText = QApplication.translate("QSphere", "Open link in my default navigator", None, QApplication.UnicodeUTF8)
            self.openURLExt = context_menu.addAction(QIcon(menuIcon), zText)
            self.ToOpenURL = unicode(hit_test.linkUrl().toString())
            self.openURLExt.triggered.connect(self.MakeOpenURL)


        context_menu.addSeparator()
           
        menuIcon = getThemeIcon("selectall.png")
        zText = (QApplication.translate("QSphere", "Select all", None, QApplication.UnicodeUTF8))
        self.selall = QAction(QIcon(menuIcon), zText, self)
        context_menu.addAction(self.selall)
        self.selall.triggered.connect(self.SelectAll)

        context_menu.exec_(self.webWidget.mapToGlobal(point))     

    def MakeOpenURL(self):
        if self.sender()== self.openURLExt :
            try : webbrowser.open(self.ToOpenURL)
            except :
                zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
                zMsg = QApplication.translate("QSphere","Try to open Web navigator for https protocol ...", None, QApplication.UnicodeUTF8)
                SendMessage(self, zTitle , zMsg, QgsMessageBar.WARNING, 3)
        elif self.sender()== self.openURL :
            d = doUI.LoadDialogViewer(self, self.iface, self.ToOpenURL, False, [], self.langueTR, self, None, "navigatorweb.png", False)
            self.childswindows.append(d) 
            self.nb_window_childs.setText("%s" % (len(self.childswindows)))
   
    def MakeToCopy(self): QApplication.clipboard().setText(self.ToCopy)
    def MakeToCopyURL(self): QApplication.clipboard().setText(self.ToCopyURL)
    def MakeToPaste(self): self.webWidget.page().triggerAction(QWebPage.Paste)
    def SelectAll(self): self.webWidget.page().triggerAction(QWebPage.SelectAll)

    def passChangeMode(self):
        idbutton = self.changeMode.id(self.changeMode.checkedButton())
        self.doChangeMode(idbutton) 
            
    def doChangeMode(self, idbutton):
        container = (self.tabWidget, self.editor, self.webWidget)
        dims = len(container)

        self.actionLblComboLayers.setVisible(idbutton == 0)
        self.actionComboLayers.setVisible(idbutton == 0)
        self.actionfindprevious.setVisible(idbutton == 1)
        self.actionsearchbutton.setVisible(idbutton == 1)
        self.actionfindnext.setVisible(idbutton == 1)        
        self.actionLblPrimaryXSLT.setVisible(idbutton == 2)
        self.actionPrimaryXSLT.setVisible(idbutton == 2)
        
        for i in range(dims):
            if i == idbutton : container[i].setVisible(True)
            else : container[i].setVisible(False)

        if self.editor.isVisible() :
           dataxml = ExportToXML(self, None)
           self.editor.setText(dataxml.decode("utf-8"))

        if self.webWidget.isVisible() :
           dataxml = ExportToXML(self, None)
           fileName = os.path.join(os.path.dirname(__file__),"xml/tempo.xml")
           
           try :
               zLOG = open(fileName, "w")
               WriteInLOGWithoutEncoding(zLOG, dataxml) 
               CloseLOG(zLOG)
           except : return

           from PyQt4.QtXml import *
           from PyQt4.QtXmlPatterns  import *
           baseUrl = ""
           qry = QXmlQuery(QXmlQuery.XSLT20)
           zTest, XSL = fileRessourceExist(self, "xml/xsl/%s" % self.PrimaryXSLT.currentText() ) 
           if XSL!= "" : baseUrl = QUrl.fromLocalFile(XSL)
           qry.setFocus(QUrl.fromLocalFile(fileName)) 
           qry.setQuery(QUrl.fromLocalFile(XSL))

           HTML = qry.evaluateToString() 

           if HTML is None :
              HTML = QApplication.translate("QSphere", "File parsing XSLT error !<br>Invalid XSLT or XML file !", None, QApplication.UnicodeUTF8)
              HTML = "<div align='center'><img src='%s'><br><br>%s</div>" % (getThemeIcon("parsing_error.png"), HTML)
           else : HTML = NetHTML(HTML)
           self.webWidget.setHtml(HTML, baseUrl)
               

    def clickHelp(self): makeHelp(self)

    def translatezTablesWidget(self):
        self.ListOfConformities = LoadDefautValue(self, "file:/ressources/conformity_default_%s.csv"  % (self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]))
        self.ListOfRules, self.DicoListOfRules = LoadData(self, "file:/ressources/roles_%s.csv" % (self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]), "roles") 
        self.ListOfThesaurus , self.DateListOfThesaurus = LoadData(self, "file:/ressources/thesaurus_%s.csv" % (self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]), "thesaurus")
        
        self.ListTypeDates = [QApplication.translate("QSphere","Date of creation", None, QApplication.UnicodeUTF8), \
                              QApplication.translate("QSphere","Date of last revision", None, QApplication.UnicodeUTF8), \
                              QApplication.translate("QSphere","Date of publication", None, QApplication.UnicodeUTF8),]
        self.ListDegres = [QApplication.translate("QSphere","Conformant", None, QApplication.UnicodeUTF8), \
                           QApplication.translate("QSphere","Not conformant", None, QApplication.UnicodeUTF8), \
                           QApplication.translate("QSphere","Not evaluated", None, QApplication.UnicodeUTF8)]

        self.zTablesWidget = {"tablelocalisator" : ((190, 200), \
                                (QApplication.translate("QSphere", self.libelles[6][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[7][2], None, QApplication.UnicodeUTF8)) ), \
                             "tableformats" : ((80, 40, 80), \
                                (QApplication.translate("QSphere", self.libelles[11][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[12][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[13][2], None, QApplication.UnicodeUTF8)) ), \
                             "tableemprises" : ((140, 140, 140, 140, 80), \
                                (QApplication.translate("QSphere", self.libelles[32][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[33][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[34][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[35][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[36][2], None, QApplication.UnicodeUTF8)) ), \
                             "tablescr" : ((120, 40), \
                                (QApplication.translate("QSphere", self.libelles[39][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[40][2], None, QApplication.UnicodeUTF8)) ), \
                             "tableetenduetemporelle" : ((140), \
                                (QApplication.translate("QSphere", self.libelles[44][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[45][2], None, QApplication.UnicodeUTF8)) ), \
                             "tabledatepubdata" : ( (100), \
                                (QApplication.translate("QSphere", self.libelles[47][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[48][2], None, QApplication.UnicodeUTF8)) ), \
                              "tablemotsclefso" : ((200, 300), \
                                (QApplication.translate("QSphere", self.libelles[20][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[21][2], None, QApplication.UnicodeUTF8)) ), \
                             "tablemotsclefsf" : ((150, 25, 140, 80, 90), \
                                (QApplication.translate("QSphere", self.libelles[23][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[24][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[25][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[26][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[27][2], None, QApplication.UnicodeUTF8)) ), \
                              "tablespecifications" : ((240, 80, 100, 100),\
                                (QApplication.translate("QSphere", self.libelles[61][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[62][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[63][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[64][2], None, QApplication.UnicodeUTF8))), \
                             "tableroles" : ((100, 80, 80, 80, 60, 80, 80, 80, 80), \
                                (QApplication.translate("QSphere", self.libelles[72][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[73][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[74][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[75][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[76][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[77][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[78][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[79][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[80][2], None, QApplication.UnicodeUTF8)) ), \
                             "tabledico" : ((50, 150, 70, 60, 50, 150), \
                                (QApplication.translate("QSphere", self.libelles[91][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[92][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[93][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[94][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[95][2], None, QApplication.UnicodeUTF8), \
                                 QApplication.translate("QSphere", self.libelles[96][2], None, QApplication.UnicodeUTF8)) )}


    def translateFixedWidgets(self):

        try : 
            fileName = self.windowTitle().replace(self.racWindowTitle, "") if self.windowTitle() != self.racWindowTitle else ""
        except : fileName = ""
        
        zElt0 = QApplication.translate("QSphere","project", None, QApplication.UnicodeUTF8).title()
        zElt1 = QApplication.translate("QSphere","metadata", None, QApplication.UnicodeUTF8)
        self.racWindowTitle = "%s :" % (zElt1.title())

        self.setWindowTitle("%s%s" % (self.racWindowTitle, fileName))
        self.setToolTip("%s%s" % (self.racWindowTitle, fileName))
        
        self.Listfiltres = ("%s QSphere (*.qsp)" % (zElt0), "eXtensible Markup Language %s (*.xml)" % (zElt1), "eXtensible Markup Language %s (*.meta.xml)" % (zElt1))
        self.ListfiltresOut = ("%s QSphere (*.qsp)" % (zElt0), "eXtensible Markup Language %s (*.xml)" % (zElt1), "eXtensible Markup Language %s (*.meta.xml)" % (zElt1), "QSphere eXtensible Markup Language %s (*.xqsp)" % (zElt0))
        self.NamedFiltres = {"qsp": "%s QSphere (*.qsp)" % (zElt0), "xml" : "eXtensible Markup Language %s (*.xml)" %( zElt1), "xqsp" : "QSphere eXtensible Markup Language %s (*.xqsp)" % (zElt0)}
        
        self.window_childs.setToolTip(QApplication.translate("QSphere","Mainwindow's children", None, QApplication.UnicodeUTF8))
        self.mode_project.setToolTip(QApplication.translate("QSphere","Current saving mode for the project", None, QApplication.UnicodeUTF8))
        zToolTip = QApplication.translate("QSphere","Langs for the GUI", None, QApplication.UnicodeUTF8)
        self.langs_gui_base.setToolTip(zToolTip)
        self.langs_gui.setToolTip(zToolTip)

        self.formMode.setToolTip(QApplication.translate("QSphere","Form view", None, QApplication.UnicodeUTF8))
        self.xmlMode.setToolTip(QApplication.translate("QSphere","rendering XML", None, QApplication.UnicodeUTF8))
        self.htmlMode.setToolTip(QApplication.translate("QSphere","rendering HTML", None, QApplication.UnicodeUTF8))
        
        self.BReduceWindow.setToolTip(QApplication.translate("QSphere","Get min size for the window", None, QApplication.UnicodeUTF8))
        self.BExpandWindow.setToolTip(QApplication.translate("QSphere","Get recommanded size for the window", None, QApplication.UnicodeUTF8))
        self.navigatorWeb.setToolTip(QApplication.translate("QSphere", "Web navigator ...", None, QApplication.UnicodeUTF8))
        self.editXMLButton.setToolTip(QApplication.translate("QSphere", "Edit XML", None, QApplication.UnicodeUTF8))
        try :
            self.OpenNavigatorWeb.setText(QApplication.translate("QSphere","Web navigator ...", None, QApplication.UnicodeUTF8))
            self.contextMnu_serverMetadata.setTitle(QApplication.translate("QSphere","Url Server for metadata : ", None, QApplication.UnicodeUTF8))
            self.contextMnu_serverKeywords.setTitle(QApplication.translate("QSphere","Url Server for keywords : ", None, QApplication.UnicodeUTF8))
        except : pass
        
        self.loadContacts.setToolTip(QApplication.translate("QSphere","Choose a contact from a contacts list file", None, QtGui.QApplication.UnicodeUTF8))
        self.OptionsButton.setToolTip(QApplication.translate("QSphere","Fixe options for QSphere", None, QApplication.UnicodeUTF8))
        self.HelpButton.setToolTip(QApplication.translate("QSphere","Call the help page", None, QApplication.UnicodeUTF8))
        self.LblComboLayers.setText("\n %s" % QApplication.translate("QSphere","Query a layer : ", None, QApplication.UnicodeUTF8))
        self.LblComboLayers.setToolTip(QApplication.translate("QSphere","Query a layer : ", None, QApplication.UnicodeUTF8))
        self.ComboLayers.setToolTip(self.LblComboLayers.toolTip())
        self.LblPrimaryXSLT.setText(" %s" % QApplication.translate("QSphere", "Primary XSLT : ", None, QApplication.UnicodeUTF8))
        self.NewButton.setToolTip(QApplication.translate("QSphere","New sheet", None, QApplication.UnicodeUTF8))
        self.LoadButton.setToolTip("%s ..." % (QApplication.translate("QSphere","Load a metadata file", None, QApplication.UnicodeUTF8)))
        self.PrintButton.setToolTip(QApplication.translate("QSphere", "Print current page", None, QApplication.UnicodeUTF8))
        self.SaveButton.setToolTip(QApplication.translate("QSphere","Save the current sheet QSphere", None, QApplication.UnicodeUTF8))
        self.ActionsSaveButton.setToolTip(QApplication.translate("QSphere","Other saving actions ...", None, QApplication.UnicodeUTF8))
        self.ReLoadButton.setToolTip(QApplication.translate("QSphere","Reload the current metadata file", None, QApplication.UnicodeUTF8))
        self.ActionsCSWTButton.setToolTip(QApplication.translate("QSphere","CSW-T actions", None, QApplication.UnicodeUTF8))
        self.contextMnuSaveActions()
        self.contextMnuCSWTActions()
        
        self.CloseButton.setText(QApplication.translate("QSphere","Close", None, QApplication.UnicodeUTF8))
        self.CloseButton.setToolTip(QApplication.translate("QSphere","Close the dialog box", None, QApplication.UnicodeUTF8))

        self.ComboLayers.setItemText(0, QApplication.translate("QSphere","No layer", None, QApplication.UnicodeUTF8))
        
    def changeLang(self):

        zObj = self.findChild(MyTableWidget, "tablemotsclefso")
        if zObj != None :     
               data = {}
               for row in range(zObj.rowCount()):
                  datarow = [] 
                  for col in range(zObj.columnCount()):
                      ObjWidget = zObj.cellWidget(row, col)
                      datarow.append(ObjWidget.currentIndex())
                  data[row] = datarow


        self.MainPlugin.changeLang(True)
        self.langs_gui.setIcon(QIcon(getThemeIcon("langs_gui_%s.png" % (self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]))))
        MakePropertiesForWindow(self, self.parent)
        self.translatezTablesWidget()

        zIndex = self.tabWidget.currentIndex() 
        i, zBounds = 0, len(self.libelles.keys())
        self.progressBar.setValue(0)
        self.tabWidget.setVisible(False)
        self.progressBar.setVisible(True) 
        
        for key in self.libelles.keys() :
            i+= 1
            self.progressBar.setValue(int(100 * i/zBounds))

            nameObj, typeObj, textObj, toolTipObj = self.libelles[key][0], self.libelles[key][1], self.libelles[key][2], self.libelles[key][3]

            if typeObj != None :
                zObj = self.findChild(typeObj, nameObj)
                
                if zObj != None :
                   zText = QApplication.translate("QSphere", toolTipObj, None, QApplication.UnicodeUTF8)
                   if zText == "" : zText = toolTipObj 
                   try : zObj.setToolTip(zText)
                   except: pass

                   nameObjTable = "" 
                   if type(zObj) == MyTableWidget : 
                      isShowWarning = self.ShowWarning
                      self.ShowWarning = False 
                      zTrans, nameObjTable, zObjTarget = [], nameObj, zObj
                     
                      for col in range(zObj.columnCount()) :
                          cKey = key+(col+1)
                          if DicoHasKey(self.libelles, cKey) : zTrans.append(QApplication.translate("QSphere", self.libelles[cKey][2], None, QApplication.UnicodeUTF8))
                      if zTrans!= []: zObj.setHorizontalHeaderLabels(zTrans)

                      for row in range(zObj.rowCount()):
                         for col in range(zObj.columnCount()):
                             ObjWidget = zObj.cellWidget(row, col)
                          
                             if ObjWidget != None :
                                 
                               if type(ObjWidget) in (QPushButton, MyComboBox, MyCheckBox):
                                   indexWidget = 0 
                                   if type(ObjWidget) == MyComboBox : indexWidget = ObjWidget.currentIndex()

                                   if ObjWidget.objectName().startswith("tableroles_combobox") :
                                      zTest = False 
                                      if not ObjWidget.isEditable() :
                                         zTest = True
                                         ObjWidget.setEditable(True)                                       
                                      ObjWidget.clear()
                                      ObjWidget.addItems(self.ListOfRules)
                                      if zTest : ObjWidget.setEditable(False)

                                   elif ObjWidget.objectName().startswith("tablemotsclefsf_combobox") :
                                      zTest = False
                                      if not ObjWidget.isEditable() :
                                         zTest = True   
                                         ObjWidget.setEditable(True)
                                      ObjWidget.clear()
                                      ObjWidget.addItems(self.ListTypeDates)
                                      if zTest : ObjWidget.setEditable(False)
                                      

                                   elif ObjWidget.objectName().startswith("tablespecifications_combobox") :
                                        ObjWidget.clear()
                                        if ObjWidget.objectName().endswith("2") : ObjWidget.addItems(self.ListTypeDates)
                                        elif ObjWidget.objectName().endswith("3") : ObjWidget.addItems(self.ListDegres)
                                    
                                   if type(ObjWidget) == MyComboBox : ObjWidget.setCurrentIndex(indexWidget)

                                   elif ObjWidget.objectName().startswith("tablemotsclefsf_action") :   
                                      ObjWidget.setToolTip(QApplication.translate("QSphere", "From controlled Vocabulary ", None, QApplication.UnicodeUTF8))
                                      
                                   elif ObjWidget.objectName().startswith("tableformats_action") :
                                      ObjWidget.setToolTip(QApplication.translate("QSphere","Call the QSphere Formats Dialog box", None, QApplication.UnicodeUTF8))

                                   elif ObjWidget.objectName().startswith("tablescr_action") : 
                                      ObjWidget.setToolTip(QApplication.translate("QSphere","Call the SRS QGIS Dialog box", None, QApplication.UnicodeUTF8))

                                   elif ObjWidget.objectName().startswith("tableemprises_action") :   
                                      ObjWidget.setToolTip(QApplication.translate("QSphere","View with WMS service the current extent", None, QApplication.UnicodeUTF8))

                      self.ShowWarning = isShowWarning

                   if type(zObj) == QWidget :
                       index = int(nameObj.replace("tab",""))
                       zText = QApplication.translate("QSphere", textObj, None, QApplication.UnicodeUTF8)
                       zToolTip = QApplication.translate("QSphere", toolTipObj, None, QApplication.UnicodeUTF8)
                       self.listWidget.item(index-1).setText(zText)
                       self.listWidget.item(index-1).setToolTip(zToolTip)
                    
                   if type(zObj) == QGroupBox :
                      if nameObj == "grouperesolutionscale" :
                         zObj = self.findChild(MyPushButton, "ActionsButton_%s" % (nameObj))
                         zObjTarget = self.findChild(MyTableWidget, "tableechelles")
                         if zObj != None and zObjTarget!= None :
                            contextMnuMDDActions(self, self.listWidget, zObjTarget, "tableechelles", 6, zObj, "")

                      if nameObj == "groupedroits" :
                         valObj = ((QApplication.translate("QSphere","No restriction for public access in INSPIRE", None, QApplication.UnicodeUTF8),"norestriction_droits",25000.00), \
                                      (QApplication.translate("QSphere","With restriction for public access in INSPIRE (Directive 2007/2/CE)", None, QApplication.UnicodeUTF8),"restriction_droits",2.0)) 
                         for oi in range(len(valObj)):
                             zButton = self.findChild(QRadioButton, valObj[oi][1]) 
                             if zButton : zButton.setText(valObj[oi][0])
                         zObjTable = self.findChild(QTableView, "tablegroupedroits")
                         if zObjTable : CleanSheetTable(self, zObjTable, "file:280:contraintes_%s.csv:1:0" % (self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]), None)
                            

                   if type(zObj) == QComboBox and nameObj in ("typedata", "sysreftemp") :
                       indexWidget = zObj.currentIndex()
                       zObj.clear()
                       if nameObj == "typedata" :
                           self.listTypeRessources = MakeListTypeRessources(self)
                           zObj.addItems(self.listTypeRessources)
                       if nameObj == "sysreftemp" :
                           self.listTemporalSystem = MakeListTemporalSystem(self)
                           zObj.addItems(self.listTemporalSystem)
                       zObj.setCurrentIndex(indexWidget)

                   if type(zObj) == QTableView  :
                       if zObj.objectName() == "tablecategories" : CleanSheetTable(self, zObj, "file:300:categories_thematiques_%s.csv:1:0" % (self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]), "tablemotsclefso")
                
                zObj = self.findChild(QLabel, "Lbl%s" % (nameObj))
                if zObj != None :
                   try :
                       if textObj!= "" :
                          zText = QApplication.translate("QSphere", textObj, None, QApplication.UnicodeUTF8)
                          if zText == "" : zText = textObj
                          if nameObj.startswith("titletab") : zText = ">> %s" % (zText)
                          zObj.setText(zText)
                          zObj.setAccessibleDescription(zText)
                   except: pass
                   if nameObjTable != "" :
                      countItems(self, nameObjTable, zObjTarget)

                      zObj = self.findChild(MyPushButton, "ActionsButton_%s" % (nameObj))
                      if zObj != None :
                         zObj.setToolTip(QtGui.QApplication.translate("QSphere", self.libelles[101][3], None, QtGui.QApplication.UnicodeUTF8))
                         contextMnuMDDActions(self, self.listWidget, zObjTarget, nameObj, 6, zObj, "")

                      zObj = self.findChild(MyPushButton, "OpenWizard_%s_%s" % (6, nameObj))  
                      if zObj != None :
                         zObj.setToolTip(QtGui.QApplication.translate("QSphere", self.libelles[102][3], None, QtGui.QApplication.UnicodeUTF8))              
                         contextMnuMDDWizards(self, self.listWidget, zObjTarget, nameObj, 6, zObj, "")

                   
                zObj = self.findChild(MyPushButton, "help_%s" % (nameObj))
                if zObj != None : zObj.setToolTip(QtGui.QApplication.translate("QSphere", self.libelles[100][3], None, QtGui.QApplication.UnicodeUTF8))

                zObj = self.findChild(MyPushButton, "OpenLusTRE_%s_%s" % (6, nameObj))
                if zObj != None : zObj.setToolTip(QtGui.QApplication.translate("QSphere", self.libelles[103][3], None, QtGui.QApplication.UnicodeUTF8))


        zObj = self.findChild(QRadioButton, "resolution_scale")       
        if zObj != None : zObj.setText( QtGui.QApplication.translate("QSphere", self.libelles[57][2], None, QtGui.QApplication.UnicodeUTF8)+" 1/")
        zObj = self.findChild(QRadioButton, "resolution_pixel")
        if zObj != None : zObj.setText(QApplication.translate("QSphere","Equivalent scale in unit of measure ", None, QApplication.UnicodeUTF8))

        if data != {}:
           zObj = self.findChild(MyTableWidget, "tablemotsclefso")
           if zObj != None :
              zObj.clearContents()
              for j in range(zObj.rowCount()): zObj.removeRow(0)
              for row in data :
                  for col in range(len(data[row])):
                      if col == 0 : MakeLine(self, zObj, False, False, -1, True)
                      ObjWidget = zObj.cellWidget(row, col)
                      if ObjWidget != None :
                          ObjWidget.setCurrentIndex(data[row][col])
                          if data[row][0]== 0 : ObjWidget.setEnabled(False)
 
        self.translateFixedWidgets()
        self.setEnabledCSWTActions()

        idbutton = self.changeMode.id(self.changeMode.checkedButton())
        if idbutton == 2 : self.doChangeMode(idbutton)  
 
        self.progressBar.setValue(0)
        self.tabWidget.setVisible(True)
        self.progressBar.setVisible(False) 
        self.tabWidget.setCurrentIndex(zIndex) 

       
    def startMovie(self):
        self.status_txt.setVisible(True)
        self.movie.start()
        self.status_txt.repaint()

    def stopMovie(self):
        self.movie.stop()
        self.status_txt.setVisible(False)

    def reject(self): self.killWindows()
    def closeme(self): self.killWindows()
    def killWindows(self):
        try :
            for key, obj in self.isFromDownload.d.items() :
                if self == obj :
                   self.isFromDownload.d.pop(key)
                   if self.isFromDownload.d == {} : self.isFromDownload.parent = None
                   break
            if self.isFromDownload.d != {} :
                for key, obj in self.isFromDownload.d.items() :    
                    self.isFromDownload.parent = self.isFromDownload.d[key]
                    break
        except : pass    
        
        for zobject in self.childswindows :
            if zobject != None:
                try : zobject.reject()
                except : pass
        self.disconnectCSWT()        
        self.reject()

    def resizeEvent(self,ev):
        zSize = ev.size()
        self.BReduceWindow.setEnabled(False) if ((self.height() == self.minheight) and (self.width()== self.minwidth)) else self.BReduceWindow.setEnabled(True)
        self.BExpandWindow.setEnabled(False) if ((self.height() == self._H) and (self.width()== self._W-30)) else self.BExpandWindow.setEnabled(True)
       
    def ResizeWindow(self):
        self.resize(self.minwidth, self._H) if (self.sender().accessibleName() == "BReduceWindow") else self.resize(self._W, self._H)

    def UpdateListComboLayers(self):
        try : QObject.disconnect(self.ComboLayers,SIGNAL("currentIndexChanged(QString)"), self.GetMetaData)
        except : pass
        self.modelLayers = QStandardItemModel()
        if self.ComboLayers.model().item(self.ComboLayers.currentIndex(),1)!= None : self.comboLayersCurrentLayerId = self.ComboLayers.model().item(self.ComboLayers.currentIndex(),1).text() 
        maxdim = MakeListLayer(self, self.model, self.ComboLayers)
        IndexLayer = GetLayerCombo(self, self.ComboLayers, "%s" % (self.comboLayersCurrentLayerId))
        self.ComboLayers.setCurrentIndex(IndexLayer)
        self.GetMetaData()
        self.ComboLayers.currentIndexChanged.connect(self.GetMetaData)
        if self.iface.mapCanvas().currentLayer()!= None:
            self.iface.mapCanvas().currentLayer().layerNameChanged.connect(self.UpdateListComboLayers)
            self.iface.mapCanvas().currentLayer().legendChanged.connect(self.UpdateListComboLayers)

        self.view.horizontalHeader().setDefaultSectionSize(maxdim*8)
        self.view.setStyleSheet("QTableView {min-width: %spx; max-width: %spx; selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5, stop: 0 #FFFFFF, stop: 1 #000000);}" % (maxdim*8, (maxdim+1)*8))

        
    def initBDownloadButton(self):
        self.contextMnu_navigatorWeb = QMenu()

        menuIcon = getThemeIcon("navigatorweb.png")
        zText = QApplication.translate("QSphere","Web navigator ...", None, QApplication.UnicodeUTF8)
        self.OpenNavigatorWeb = QAction(QIcon(menuIcon), zText, self)
        self.OpenNavigatorWeb.setObjectName("mActionNavigator")
        self.OpenNavigatorWeb.setShortcut(QKeySequence("Ctrl+W"))
        self.contextMnu_navigatorWeb.addAction(self.OpenNavigatorWeb)
        self.OpenNavigatorWeb.triggered.connect(self.DownloadMetadata)

        self.contextMnu_navigatorWeb.addSeparator()

        menuIcon = getThemeIcon("dmetadata.png")
        zText = QApplication.translate("QSphere","Url Server for metadata : ", None, QApplication.UnicodeUTF8)
        self.contextMnu_serverMetadata = QMenu(zText)
        self.contextMnu_serverMetadata.setIcon(QIcon(menuIcon))
        i = 0
        for elt in self.serverMetadata :
            self.OpenServerMDD = QAction(QIcon(menuIcon), elt, self)
            self.OpenServerMDD.setObjectName("OpenServerMDD%s" % (i) )
            self.contextMnu_serverMetadata.addAction(self.OpenServerMDD)
            self.OpenServerMDD.triggered.connect(self.DownloadMetadata)
            i+= 1

        self.contextMnu_navigatorWeb.addMenu(self.contextMnu_serverMetadata)
        self.contextMnu_navigatorWeb.addSeparator()

        menuIcon = getThemeIcon("dkeywords.png")
        zText = QApplication.translate("QSphere","Url Server for keywords : ", None, QApplication.UnicodeUTF8)
        self.contextMnu_serverKeywords = QMenu(zText)
        self.contextMnu_serverKeywords.setIcon(QIcon(menuIcon))
        i = 0
        for elt in self.serverKeywords :
            self.OpenServerKW = QAction(QIcon(menuIcon), elt, self)
            self.OpenServerKW.setObjectName("OpenServerKW%s" % (i) )
            self.contextMnu_serverKeywords.addAction(self.OpenServerKW)
            self.OpenServerKW.triggered.connect(self.DownloadMetadata)
            i+= 1

        self.contextMnu_navigatorWeb.addMenu(self.contextMnu_serverKeywords)
        
        self.navigatorWeb.setMenu(self.contextMnu_navigatorWeb)


        
    def callInitSizeCols(self):
        zIndex = self.tabWidget.currentIndex() 
        callInitSizeCols(self)
        self.tabWidget.setCurrentIndex(zIndex) 
        
    def clickOptions(self):
           d = doUI.DialogOptions(self)
           d.exec_()

    def DownloadMetadata(self):
        zicon, zurl = "navigatorweb.png", "#blank"
        if self.sender() == self.HelpButton :
            zLang = "_%s" % (self.langueTR) if self.langueTR!= "en" else ""
            zicon, zurl = "help.png", getThemeIcon("ressources/html/help/index%s.html" % (zLang))
        else :
            if self.sender()!=self.OpenNavigatorWeb : zurl = self.sender().text()
            else : zUrl = ""
        d = doUI.LoadDialogViewer(self, self.iface, zurl, False, [], self.langueTR, self, None, zicon, False)
        self.childswindows.append(d) 
        self.nb_window_childs.setText("%s" % (len(self.childswindows)))
        
    def IsVisibleRestoreDico(self, zCond) : self.restore_tabledico.setEnabled(zCond)

    def IsVisibleViewXMLButton(self):
        if self.restore_tabledico != None : self.restore_tabledico.setEnabled(False)
        if self.windowTitle() != self.racWindowTitle :
            fileName = self.windowTitle().replace(self.racWindowTitle, "")
            extension = GetExtension(fileName)
            if extension == ".qsp" : self.IsVisibleRestoreDico(True)
            myDefPathIcon = getThemeIcon("mode%s.png" % (extension.replace(".","")))
            carIcon = QImage(myDefPathIcon) 
            self.mode_project.setPixmap(QPixmap.fromImage(carIcon))    


    def LoadXMLEditor(self):
        zTitle = QApplication.translate("QSphere", "Warning" , None, QApplication.UnicodeUTF8)
        if self.windowTitle() != self.racWindowTitle :
            fileName = self.windowTitle().replace(self.racWindowTitle, "")
            textension = os.path.splitext(fileName)
            extension = textension[len(textension)-1].lower()
            if extension == ".xml" :
               d = xmlEditor(self, fileName)
               MakeWindowIcon(d, "editxml.png")
               d.setWindowTitle("%s : %s" % (d.racTitle, fileName))
               d.show()
               d.LoadFile()                
            else :
               dataxml = ExportToXML(self, None)
               self.getReporting(dataxml.decode("utf-8"), False)
        else:
               dataxml = ExportToXML(self, None)
               self.getReporting(dataxml.decode("utf-8"), False)


    def LoadGeoLocalisator(self): LoadGeoLocalisator(self)

    #CSW-T BLOC FUNTIONS
    def setEnabledCSWTActions(self):
        zCond = True if (self._connexionCSWT != None and self._connexionCSWT.connected()) else False
        self.AuthCSWTButton.setEnabled(not zCond)
        self.CloseCSWTButton.setEnabled(zCond)
        self.RecordsCSWTButton.setEnabled(zCond)
        self.ReportingCSWTButton.setEnabled(zCond)
        self.AddCSWTButton.setEnabled(zCond)
        self.EditCSWTButton.setEnabled(zCond)
        self.DelCSWTButton.setEnabled(zCond)
        
    def getReporting(self, responseCSWT, isReporting):
        d = xmlEditor(self, "")
        MakeWindowIcon(d, "editxml.png")
        d.setWindowTitle("%s : %s" % (d.racTitle, ""))
        d.show()
        d.move(self.x()+100, self.y()+100)
    
        if isReporting :
            try : charset = (responseCSWT.headers["Content-Type"].split("=")[1].strip())
            except : charset = "utf-8"  
            try : d.editor.setText("%s%s" % (self._connexionCSWT.reporting(), responseCSWT.read().decode(charset)))
            except : d.editor.setText("%s%s" % (self._connexionCSWT.reporting(), responseCSWT))
        else :
            d.editor.setText(responseCSWT)
            
        d.checkProperties()
        d.BadMyISO()


    def disconnectCSWT(self):
        if self._connexionCSWT != None :
            if self._connexionCSWT.connected() :
               self._connexionCSWT.closeSession()
               self.setEnabledCSWTActions()

               if self.AuthCSWTButton.isEnabled():
                  zTitle = QApplication.translate("QSphere", "Information" , None, QApplication.UnicodeUTF8) 
                  zMsg = QApplication.translate("QSphere","Disconnected with the server", None, QApplication.UnicodeUTF8)
                  zPicto = QgsMessageBar.INFO
                  zDuration = self.duration_info
               else :
                  zTitle = QApplication.translate("QSphere", "Warning" , None, QApplication.UnicodeUTF8) 
                  zMsg = QApplication.translate("QSphere","Error", None, QApplication.UnicodeUTF8)
                  zPicto = QgsMessageBar.WARNING
                  zDuration = self.duration_warning
              
               SendMessage(self, zTitle, "%s" % (zMsg), zPicto, zDuration)      
            
        
    def authCSWT(self):
        nameCSWT = getSelConnexion(self)
        mySettings = QSettings()
        serverCSWT = (mySettings.value("/qsphere/connections/%s/host" % (nameCSWT)))
        authServerCSWT = (mySettings.value("/qsphere/connections/%s/authhost" % (nameCSWT)))
        UserCSWT = (mySettings.value("/qsphere/connections/%s/username" % (nameCSWT)))
        pwdUserCSWT = (mySettings.value("/qsphere/connections/%s/password" % (nameCSWT)))
       
        dialog = AuthCSWTDialog(UserCSWT, pwdUserCSWT,serverCSWT)
        MakeWindowIcon(dialog, "connect.png")
        if dialog.exec_():
           self.startMovie()
       
           self._connexionCSWT = cswtConnection(self, nameCSWT, serverCSWT, authServerCSWT)
           responseCSWT = self._connexionCSWT.initSession(dialog.authInfos()[0], dialog.authInfos()[1], True) 
           self.setEnabledCSWTActions()

           if not self.AuthCSWTButton.isEnabled():
              zTitle = QApplication.translate("QSphere", "Information" , None, QApplication.UnicodeUTF8) 
              zMsg = QApplication.translate("QSphere","Connected with the server", None, QApplication.UnicodeUTF8)
              zPicto = QgsMessageBar.INFO
              zDuration = self.duration_info
           else :
              zTitle = QApplication.translate("QSphere", "Warning" , None, QApplication.UnicodeUTF8) 
              zMsg = QApplication.translate("QSphere","Error", None, QApplication.UnicodeUTF8)
              zPicto = QgsMessageBar.WARNING
              zDuration = self.duration_warning
          
           SendMessage(self, zTitle, "%s" % (zMsg), zPicto, zDuration)
           if responseCSWT == None : self.getAllReporting()

           self.stopMovie()
           
    def getAllReporting(self):
        if self._connexionCSWT != None : self.getReporting(self._connexionCSWT.allreporting(), False)

    def recordsInCSWT(self): self.actionsInCSWT(6)                
    def insertInCSWT(self): self.actionsInCSWT(1)
    def updateInCSWT(self): self.actionsInCSWT(2)
    def deleteInCSWT(self): self.actionsInCSWT(-1)
        
    def actionsInCSWT(self, ucase):
        self.startMovie()
        
        if ucase in (1,2) :
            if self.windowTitle()!=self.racWindowTitle :
                self.SaveData()
                fileName = self.windowTitle().replace(self.racWindowTitle, "")
                extension = GetExtension(fileName)
                if extension == ".xml" :
                    f = open(fileName, "r")
                    dataxml = f.read()
                    f.close()
                elif extension == ".qsp" : dataxml = ExportToXML(self, None)
            else :
                dataxml = ExportToXML(self, None)
                
            pos = dataxml.find("<gmd:MD_Metadata")
            dataxml = dataxml[pos:]
            
        elif ucase == -1 :
            zObj = self.findChild(QLineEdit, "identificator")
            if zObj :
                dataxml = zObj.text()
            else : return
        elif ucase == 6: dataxml = None    
        else : return

        if self._connexionCSWT != None :
           responseCSWT = self._connexionCSWT.metadata_csw_publication(ucase, dataxml, True) 
           if ucase != 6 : self._connexionCSWT.analyseResponse(ucase, responseCSWT)
           if self.reportingCSWT : self.getReporting(responseCSWT, True)

        self.stopMovie()


    def contextMnuCSWTActions(self):
        self.contextMnu_CSWTActions = QMenu() 

        menuIcon = getThemeIcon("connect.png")
        zText = QApplication.translate("QSphere","Authentification for the CSW-T Server ...", None, QApplication.UnicodeUTF8)
        self.AuthCSWTButton = QAction(QIcon(menuIcon), zText, self)
        self.AuthCSWTButton.setObjectName("AddCSWTButton")
        self.contextMnu_CSWTActions.addAction(self.AuthCSWTButton)
        self.AuthCSWTButton.triggered.connect(self.authCSWT)

        menuIcon = getThemeIcon("disconnect.png")
        zText = QApplication.translate("QSphere","Close the CSWT session", None, QApplication.UnicodeUTF8)
        self.CloseCSWTButton = QAction(QIcon(menuIcon), zText, self)
        self.CloseCSWTButton.setObjectName("CloseCSWTButton")
        self.contextMnu_CSWTActions.addAction(self.CloseCSWTButton)
        self.CloseCSWTButton.triggered.connect(self.disconnectCSWT)
        self.CloseCSWTButton.setEnabled(False)

        self.contextMnu_CSWTActions.addSeparator()
        
        menuIcon = getThemeIcon("reporting.png")
        zText = QApplication.translate("QSphere","Get all reporting for CSWT session", None, QApplication.UnicodeUTF8)
        self.ReportingCSWTButton = QAction(QIcon(menuIcon), zText, self)
        self.ReportingCSWTButton.setObjectName("ReportingCSWTButton")
        self.contextMnu_CSWTActions.addAction(self.ReportingCSWTButton)
        self.ReportingCSWTButton.triggered.connect(self.getAllReporting)
        self.ReportingCSWTButton.setEnabled(False)


        menuIcon = getThemeIcon("records.png")
        zText = QApplication.translate("QSphere","Get records in CSWT server", None, QApplication.UnicodeUTF8)
        self.RecordsCSWTButton = QAction(QIcon(menuIcon), zText, self)
        self.RecordsCSWTButton.setObjectName("RecordsCSWTButton")
        self.contextMnu_CSWTActions.addAction(self.RecordsCSWTButton)
        self.RecordsCSWTButton.triggered.connect(self.recordsInCSWT)
        self.RecordsCSWTButton.setEnabled(False)
        
        self.contextMnu_CSWTActions.addSeparator()

        menuIcon = getThemeIcon("add.png")
        zText = QApplication.translate("QSphere","Add to the CSW-T Server", None, QApplication.UnicodeUTF8)
        self.AddCSWTButton = QAction(QIcon(menuIcon), zText, self)
        self.AddCSWTButton.setObjectName("AddCSWTButton")
        self.contextMnu_CSWTActions.addAction(self.AddCSWTButton)
        self.AddCSWTButton.triggered.connect(self.insertInCSWT)
        self.AddCSWTButton.setEnabled(False)

        menuIcon = getThemeIcon("copyinlist.png")
        zText = QApplication.translate("QSphere", "Update to the CSW-T Server", None, QApplication.UnicodeUTF8)
        self.EditCSWTButton = QAction(QIcon(menuIcon), zText, self)
        self.EditCSWTButton.setObjectName("EditCSWTButton")
        self.contextMnu_CSWTActions.addAction(self.EditCSWTButton)
        self.EditCSWTButton.triggered.connect(self.updateInCSWT)
        self.EditCSWTButton.setEnabled(False)

        menuIcon = getThemeIcon("del.png")
        zText = QApplication.translate("QSphere","Delete to the CSW-T Server", None, QApplication.UnicodeUTF8)
        self.DelCSWTButton = QAction(QIcon(menuIcon), zText, self)
        self.DelCSWTButton.setObjectName("DelCSWTButton")
        self.contextMnu_CSWTActions.addAction(self.DelCSWTButton)
        self.DelCSWTButton.triggered.connect(self.deleteInCSWT)
        self.DelCSWTButton.setEnabled(False)

        self.ActionsCSWTButton.setMenu(self.contextMnu_CSWTActions)

    #END BLOC CSWT


    def contextMnuSaveActions(self):
        contextMnu_SaveActions = QMenu()

        menuIcon = getThemeIcon("saveas.png")
        zText = QApplication.translate("QSphere","Save as ...", None, QApplication.UnicodeUTF8)
        self.SaveAsButton = QAction(QIcon(menuIcon), zText, self)
        self.SaveAsButton.setObjectName("SaveAsButton")
        self.SaveAsButton.setShortcut(QKeySequence("Ctrl+Shift+S"))
        contextMnu_SaveActions.addAction(self.SaveAsButton)
        self.SaveAsButton.triggered.connect(self.SaveDataAs)

        contextMnu_SaveActions.addSeparator()
        
        menuIcon = getThemeIcon("savecopy.png")
        zText = QApplication.translate("QSphere","Save as a copy ...", None, QApplication.UnicodeUTF8)
        self.SaveCopyAsButton = QAction(QIcon(menuIcon), zText, self)
        self.SaveCopyAsButton.setObjectName("SaveCopyAsButton")
        self.SaveCopyAsButton.setShortcut(QKeySequence("Ctrl+Shift+C"))
        contextMnu_SaveActions.addAction(self.SaveCopyAsButton)
        self.SaveCopyAsButton.triggered.connect(self.SaveDataAs)

        contextMnu_SaveActions.addSeparator()
        
        menuIcon = getThemeIcon("saveattribut.png")
        zText = QApplication.translate("QSphere","Save as the Fields Map ...", None, QApplication.UnicodeUTF8)
        self.SaveXmlCatButton = QAction(QIcon(menuIcon), zText, self)
        self.SaveXmlCatButton.setObjectName("SaveXmlCatButton")
        contextMnu_SaveActions.addAction(self.SaveXmlCatButton)
        self.SaveXmlCatButton.triggered.connect(self.SaveXmlCat)

        self.ActionsSaveButton.setMenu(contextMnu_SaveActions)

    def fixeONGLETL(self):
        self.tabWidget.setCurrentIndex(self.listWidget.currentRow())
        idbutton = self.changeMode.id(self.changeMode.checkedButton())
        if idbutton > 0 :
            self.formMode.setChecked(True)
            self.doChangeMode(0)
        
    def fixeONGLET(self): self.listWidget.setCurrentRow(self.tabWidget.currentIndex())

    def fixeTABPLUS(self):
        if self.tabWidget.currentIndex() < (self.tabWidget.count()-1) : self.tabWidget.setCurrentIndex(self.tabWidget.currentIndex()+1)

    def fixeTABMOINS(self):
        if self.tabWidget.currentIndex() > 0 : self.tabWidget.setCurrentIndex(self.tabWidget.currentIndex()-1)

    def RestoreComments(self): RestoreComments(self)

    def GetMetaData(self):
        if self.ComboLayers.currentIndex()==-1 : return
        
        zCRS, zLATN, zLATS, zLONO, zLONE = "EPSG:4326", 51.9, 41.36, -5.79, 9.56
        zCoherence = "{'TopologyLevelCode':'unknow', 'GeometricObjectTypeCode':'unknow'}"
        zIndex = self.tabWidget.currentIndex()

        zObjDico = self.findChild(MyTableWidget, "tabledico")
        if zObjDico == None : return
        zObjDico.clearContents()
        zOnlyEnabledColor = QBrush(QColor(240,240,240))
        while zObjDico.rowCount()> 0 : zObjDico.removeRow(0)

        SetTextWidget(self, "namelayer", "", False)
        SetTextWidget(self, "typelayer", "", False)
        SetTextWidget(self, "metadata", "", False)
        
        if self.ComboLayers.currentIndex() > 0 :
           zLayer = GetzLayerCombo(self, self.ComboLayers, True)
           self.comboLayersCurrentLayerId = self.ComboLayers.model().item(self.ComboLayers.currentIndex(),1).text()
           if not zLayer : return            

           sTypeLayer = FixeLayerType(self, zLayer.type()) 
           if sTypeLayer == "vector" :
               zTypoTopology = {QGis.Point: "{'TopologyLevelCode':'geometryOnly', 'GeometricObjectTypeCode':'point'}", QGis.Line : "{'TopologyLevelCode':'topology1D', 'GeometricObjectTypeCode':'curve'}", QGis.Polygon : "{'TopologyLevelCode':'abstract', 'GeometricObjectTypeCode':'surface'}"}
               zkey = zLayer.geometryType() 
               if DicoHasKey(zTypoTopology, zkey) : zCoherence = zTypoTopology[zkey]
           
           zExtent = zLayer.extent()
           zTransform = DefzTransform(zLayer, 4326)

           MyPoint = zTransform.transform(QgsPoint(zExtent.xMinimum(), zExtent.yMaximum()))
           zLONO, zLATN = MyPoint.x(), MyPoint.y()

           MyPoint = zTransform.transform(QgsPoint(zExtent.xMaximum(), zExtent.yMinimum()))                                          
           zLONE, zLATS = MyPoint.x(), MyPoint.y()

           if IsCorrectLayer(zLayer, True) and zObjDico :
               zProvider = zLayer.dataProvider()
               zFields = zProvider.fields()
               i = 0
               DicoModel = QStandardItemModel()
               for j in range(len(zFields)):
                   zItemId = QTableWidgetItem()
                   zItemName = QTableWidgetItem()
                   zItemTypeName = QTableWidgetItem()
                   zItemLength = QTableWidgetItem()
                   zItemPrecision = QTableWidgetItem()
                   zItemComment = QTableWidgetItem()
                                     
                   zObjDico.insertRow(i)
                   
                   zItemId.setText("%s" % (i))
                   zObjDico.setItem(i,0,zItemId)
                   zObjDico.item( i, 0 ).setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                   zObjDico.item( i, 0 ).setBackground(zOnlyEnabledColor)
                                      
                   zItemName.setText("%s" % (zFields[j].name()))
                   zObjDico.setItem(i,1,zItemName)
                   zObjDico.item( i, 1 ).setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                   zObjDico.item( i, 1 ).setBackground(zOnlyEnabledColor)
                   
                   zItemTypeName.setText("%s" %(zFields[j].typeName()))
                   zObjDico.setItem(i,2,zItemTypeName)
                   zObjDico.item( i, 2 ).setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                   zObjDico.item( i, 2 ).setBackground(zOnlyEnabledColor)
                   
                   zItemLength.setText("%s" %(zFields[j].length()))
                   zObjDico.setItem(i,3,zItemLength)
                   zObjDico.item( i, 3 ).setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                   zObjDico.item( i, 3 ).setBackground(zOnlyEnabledColor)
                   
                   zItemPrecision.setText("%s" %(zFields[j].precision()))
                   zObjDico.setItem(i,4,zItemPrecision)
                   zObjDico.item( i, 4 ).setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                   zObjDico.item( i, 4 ).setBackground(zOnlyEnabledColor)
                   
                   zItemComment.setText("%s" %(zFields[j].comment()))
                   zObjDico.setItem(i,5,zItemComment)
                   zObjDico.item( i, 5 ).setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled)

                   i+= 1


           zObj = self.findChild(MyTableWidget, "tableemprises")
           if zObj :
                zIndexEmp = GetIndex(zObj)
           
                zItem = zObj.cellWidget(zIndexEmp,2)
                if zItem == None : return
                zItem.setValue(zLONO)
                XposD = int(zItem.value())+180

                zItem = zObj.cellWidget(zIndexEmp,3)
                zItem.setValue(zLONE)
                XposF = int(zItem.value())+180
                   
                zItem = zObj.cellWidget(zIndexEmp,0)
                zItem.setValue(zLATN)
                YposD = 90-int(zItem.value())

                zItem = zObj.cellWidget(zIndexEmp,1)
                zItem.setValue(zLATS)
                YposF = 90-int(zItem.value())


           zObj = self.findChild(MyTableWidget, "tablescr")
           if zObj :
                zIndexEmp = GetIndex(zObj)
                zItem = zObj.cellWidget(zIndexEmp,0)
                if zItem == None : return
                zItem.setText(zLayer.crs().authid())
                
           SetTextWidget(self, "namelayer", zLayer.name(), False)
           SetTextWidget(self, "typelayer", sTypeLayer, False)
           SetTextWidget(self, "metadata", zLayer.metadata(), False)
           SetTextWidget(self, "scr", zLayer.crs().authid(), False)
           SetTextWidget(self, "coherence", zCoherence, False)

           if os.path.exists(zLayer.source()):
               self.InitDir = "%s" % (os.path.dirname(zLayer.source()))
               self.InitDir = CorrigePath(self.InitDir.replace("\\","/"))
               self.InitName = os.path.splitext(os.path.basename(zLayer.source()))[0]
           else :
               self.InitName = zLayer.name()
  
        self.tabWidget.setCurrentIndex(zIndex)
        return


    def OpenLusTRE(self):
        dialog = LusTREDialog(self, "http://linkeddata.ge.imati.cnr.it/", False)
        MakeWindowIcon(dialog, "lustre_wizard.png")
        self.childswindows.append(dialog) 
        self.nb_window_childs.setText("%s" % (len(self.childswindows)))
        dialog.show()

    def OpenViewerTable(self):
        zCible = self.sender().objectName().split("_")[1]
        zObj = self.findChild(MyTableWidget, zCible)
        if zObj == None : return
        if type(zObj ) != MyTableWidget : return

        dialog = TableWidgetDialog(zObj, self)
        if dialog.exec_():
           QMessageBox.information(None,"QSPHERE", "return !")

    def OpenFormTable(self):
        zCible = self.sender().objectName().split("_")[1]
        zObj = self.findChild(MyTableWidget, zCible)
        if zObj == None : return
        if type(zObj ) != MyTableWidget : return
        if zObj.rowCount()==0: return

        dialog = formWidgetDialog(zObj, self)
        if dialog.exec_():
           QMessageBox.information(None,"QSPHERE", "return !")
        
    def AddLine(self): AddLine(self)
    
    def CheckTable(self, zObj):
        for i in range(zObj.rowCount()):
            if i in (0, 1) :
                zObj.cellWidget(i,0).setEnabled(False)
                if i == 0 : zObj.cellWidget(i,0).setCurrentIndex(2)
                else : zObj.cellWidget(i,0).setCurrentIndex(6)
            else :
                zObj.cellWidget(i,0).setEnabled(True)
                if zObj.cellWidget(i,0).currentIndex() in (2,6) : zObj.cellWidget(i,0).setCurrentIndex(1)

        
    def MoveLineUp(self):
        zIndex = self.tabWidget.currentIndex() 
        zObject = "%s" % (self.sender().objectName()) 
        MoveLineUpProcess(self, zObject)
        self.tabWidget.setCurrentIndex(zIndex) 

    def MoveLineDown(self):
        zIndex = self.tabWidget.currentIndex() 
        zObject = "%s" % (self.sender().objectName()) 
        MoveLineDownProcess(self, zObject)
        self.tabWidget.setCurrentIndex(zIndex) 

    def DelLine(self):
        zIndex = self.tabWidget.currentIndex() 
        zObject = "%s" % (self.sender().objectName()) 
        DelLineProcess(self, zObject, True)
        self.tabWidget.setCurrentIndex(zIndex) 

    def DelCurrentLine(self):
        zIndex = self.tabWidget.currentIndex() 
        zObject = "%s" % (self.sender().objectName()) 
        DelLineProcess(self, zObject, False)
        self.tabWidget.setCurrentIndex(zIndex) 

    def reinitDateMDD(self, zObj):
        zDate = "%s" % (datetime.datetime.now())
        zDate = zDate.split(" ")[0]
        zEltsDate = zDate.split("-")
        zObj.setSelectedDate(QDate(int(zEltsDate[0]), int(zEltsDate[1]), int(zEltsDate[2])))

    def NewSheet(self):
        self.setWindowTitle(self.racWindowTitle)
        self.setToolTip(self.racWindowTitle)
        zIndex = self.tabWidget.currentIndex()
        zTabs = self.tabWidget.count()
        zObj = None

        mylang = QLocale.languageToString( self.langue )
        for key in self.languesDico.keys():
            if self.languesDico[key]['english'] == mylang :
               mycodelang = self.languesDico[key]['bibliographic']
               break

        viewProgressBar = True if self.sender()== self.NewButton else False
        if viewProgressBar :
            self.tabWidget.setVisible(False)
            self.progressBar.setVisible(True)
            zBounds, i = zTabs, 0
        
        for i in range(zTabs):
            self.tabWidget.setCurrentIndex(i)
            zTab = self.tabWidget.currentWidget()
            zObjs = zTab.children()
            for j in range(len(zObjs)):
                zObj = zObjs[j]
                zClassObjName = "%s" % (zObj.metaObject().className())

                if viewProgressBar : self.progressBar.setValue(int(100 * i/zBounds))

                if zClassObjName=="MyButton" : pass
                elif zClassObjName=="QCalendarWidget" : self.reinitDateMDD(zObj)

                elif zClassObjName in ("QTextEdit","MyTextEdit") :
                    if zObj.isEnabled(): zObj.setPlainText("")
                    else :
                        if zObj.accessibleName()== "coherence" : zObj.setPlainText("{'TopologyLevelCode':'unknow', 'GeometricObjectTypeCode':'unknow'}")
                    if zObj.accessibleName() == "licence" : zObj.setPlainText("%s" % (QApplication.translate("QSphere","Open Licence", None, QApplication.UnicodeUTF8)))
                elif zClassObjName in ("QLineEdit", "MySimpleWidgetLineEdit", "MyWidgetLineEdit") :
                    zObj.setText("") if zObj.accessibleName() != "identificator" else zObj.setText("%s-%s-%s" % (self.langueTR.upper(), datetime.datetime.now().year, getRandowId(self)))
                elif zClassObjName in ("QComboBox", "MyComboBox") :
                    iIndex = 0
                    zObj.clear()
                    if zObj.accessibleName() == "typedata" : zObj.insertItems(0, self.listTypeRessources)
                    elif zObj.accessibleName()== "sysreftemp" :
                       zObj.insertItems(0, self.listTemporalSystem)
                       iIndex = 1
                    elif zObj.accessibleName()== "tablecarac" :
                       zObj.insertItems(0, self.listCodecs)
                       iIndex = self.listCodecs.index("utf8")
                    elif zObj.accessibleName()== "langmetada" :
                       iIndex = MakeListLangues(self, zObj, mylang)
                    zObj.setCurrentIndex(iIndex)

                elif zClassObjName=="QGroupBox" :
                    zChildren = zObj.children()
                    zChildren[0].setChecked(True)
                    zTable = zChildren[2]
                    if zTable.metaObject().className() in ("QTableWidget", "MyTableWidget") :
                        zTable.clearContents()
                        for j in range(zTable.rowCount()): zTable.removeRow(0)
                        MakeLine(self, zTable, False, True, -1, True)
    
                    elif zTable.metaObject().className() == "QTableView" :
                        if zObj.objectName() == "tablegroupedroits" : CleanSheetTable(self, zObj, "file:280:contraintes_%s.csv:1:0" % (self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]), None)
                            

                    if len(zChildren) > 3 :    
                        zCombo = zChildren[3]
                        zCombo.setCurrentIndex(0)
    
                elif zClassObjName=="QTableView" :
                     if zObj.objectName() == "tablelangues" :
                            for i in range(len(self.langs)):
                                zItem = zObj.model().item(i, 0)
                                language = self.langs[i]
                   
                     for k in range(zObj.model().rowCount()):
                         zItem = zObj.model().item(k, 0)
                         zItem.setCheckState(Qt.Unchecked)
                         if zObj.objectName() == "tablelangues" and zItem.text().startswith(self.langueTR): zItem.setCheckState(Qt.Checked)

                elif zClassObjName in ("QTableWidget", "MyTableWidget") :
                    zObj.clearContents()
                    for j in range(zObj.rowCount()): zObj.removeRow(0)
                    MakeLine(self, zObj, False, True,-1, True)
                    if zObj.objectName() == "tableemprises" : self.DessCadre()
                    
        self.CountLangues()
        self.tabWidget.setCurrentIndex(zIndex) #self.listeOnglets.setCurrentIndex(zIndex)
        self.IsVisibleViewXMLButton()
        myDefPathIcon = getThemeIcon("modenone.png")
        carIcon = QImage(myDefPathIcon) 
        self.mode_project.setPixmap(QPixmap.fromImage(carIcon))

        if viewProgressBar :
            self.tabWidget.setVisible(True)
            self.progressBar.setVisible(False)

        idbutton = self.changeMode.id(self.changeMode.checkedButton())
        self.doChangeMode(idbutton)    

    def SaveData(self):
        if self.windowTitle() != self.racWindowTitle :
            fileName = self.windowTitle().replace(self.racWindowTitle, "")
            zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
            if fileName!="": self.MakeSave(fileName, True, zTitle)
            else : self.SaveDataAs()
        else : self.SaveDataAs()

    def SaveDataAs(self):
        extension = "qsp"
        if self.windowTitle()!= self.racWindowTitle:
            fileName = self.windowTitle().replace(self.racWindowTitle, "")
            self.InitName = os.path.basename(fileName) 
            extension = GetExtension(fileName)
            extension = extension.replace(".","")

        if self.sender()==self.SaveAsButton : zTitle, zActiveProject = QApplication.translate("QSphere","Save as a file", None, QApplication.UnicodeUTF8), True
        elif self.sender()==self.SaveCopyAsButton : zTitle, zActiveProject = QApplication.translate("QSphere","Save as a copy ...", None, QApplication.UnicodeUTF8), False
        else : zTitle, zActiveProject = QApplication.translate("QSphere","Save as a file", None, QApplication.UnicodeUTF8), True

        MyFileDialog = QFileDialog(self, zTitle)
        MyFileDialog.setNameFilters(self.Listfiltres)
        MyFileDialog.selectNameFilter(self.NamedFiltres[extension])
        MyFileDialog.setViewMode(QFileDialog.Detail)
        MyFileDialog.setDirectory(self.InitDir)
        MyFileDialog.setAcceptMode(QFileDialog.AcceptSave)

        FixeLabelsFileDialog(self, MyFileDialog, 1, True)
        
        MyFileDialog.selectFile(self.InitName)
        if MyFileDialog.exec_():
            fileName = FileNameWithExtension(self, MyFileDialog.selectedFiles()[0], MyFileDialog.selectedNameFilter())
            self.MakeSave(fileName, zActiveProject, zTitle)

        
    def MakeSave(self, fileName, zActiveProject, zTitle):
        extension = GetExtension(fileName)
        if extension == ".qsp" : SaveQSP(self, fileName)
        elif extension == ".xqsp" : SaveXQSP(self, fileName)
        elif extension == ".xml" : ExportToXML(self, fileName)
        zMsg = QApplication.translate("QSphere","The metadata record was saved as", None, QApplication.UnicodeUTF8)
        SendMessage(self, zTitle , "%s :<br><u><i>%s</i></ul>" % (zMsg, fileName), QgsMessageBar.INFO, self.duration_info)
        if zActiveProject :
           if extension != ".xqsp" :
               zFileName = "%s%s" % (self.racWindowTitle, fileName)
               self.setWindowTitle(zFileName)
               self.setToolTip(zFileName)
           self.IsVisibleViewXMLButton()
           try : self.parent.MajDispoCommandQSP()
           except : pass

           if type(self.parent)== doUI.DialogViewer :
               try : self.parent.reloadPageURL()
               except : pass

    def getDialogViewerFromAnother(self, zUrl):
        d = doUI.LoadDialogViewer(self, self.iface,  zUrl, False, [], self.langueTR, self, None, "info.png", False)
        self.childswindows.append(d)
        self.nb_window_childs.setText("%s" % (len(self.childswindows)))
           
                       
    def SaveXmlCat(self):
        zObj = self.findChild(MyTableWidget, "tabledico")
        zTitle = QApplication.translate("QSphere","Warning", None, QApplication.UnicodeUTF8)
        if zObj.rowCount()==0 :
            zMsg =  QApplication.translate("QSphere","No information for fields map.", None, QApplication.UnicodeUTF8)
            zObj.setFocus()
            SendMessage(self, zTitle , "%s" % (zMsg), QgsMessageBar.WARNING, self.duration_warning)
            return

        zTitle = QApplication.translate("QSphere","Export Fields Map from QSphere record in XML", None, QApplication.UnicodeUTF8)
        MyFileDialog = QFileDialog(self, zTitle)
        MyFileDialog.setDefaultSuffix("xml")
        MyFileDialog.setNameFilters((self.Listfiltres[1],))
        MyFileDialog.selectNameFilter(self.NamedFiltres["xml"])
        zObjNameLayer = self.findChild(QLineEdit, "namelayer")
        zObjNameLayer = zObjNameLayer.text() if zObjNameLayer else ""
        MyFileDialog.selectFile("cat_%s.xml" % (zObjNameLayer))
        MyFileDialog.setViewMode(QFileDialog.Detail)
        MyFileDialog.setDirectory(self.InitDir)
        MyFileDialog.setAcceptMode(QFileDialog.AcceptSave)

        FixeLabelsFileDialog(self, MyFileDialog, 1, True)        
        
        if MyFileDialog.exec_():
           fileName = FileNameWithExtension(self, MyFileDialog.selectedFiles()[0], MyFileDialog.selectedNameFilter())
           ExportCatToXML(self, fileName)
           zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
           zMsg =  QApplication.translate("QSphere","The Field Map was exported as :\n", None, QApplication.UnicodeUTF8) 
           SendMessage(self, zTitle , "%s<u><i>%s</i></ul>" % (zMsg, fileName), QgsMessageBar.INFO, self.duration_info)    


    def ReinitIHM(self, fileName, zIndex):
        if fileName != None :
            self.InitDir = os.path.dirname(fileName)
            zFileName = "%s%s" % (self.racWindowTitle, fileName)
            self.setWindowTitle(zFileName)
            self.setToolTip(zFileName)            
        self.CountLangues()
        self.tabWidget.setCurrentIndex(zIndex) 
        self.progressBar.setValue(0)
        self.tabWidget.setVisible(True)
        self.progressBar.setVisible(False)
        self.IsVisibleViewXMLButton()

        idbutton = self.changeMode.id(self.changeMode.checkedButton())
        self.doChangeMode(idbutton)

    def ReLoadMetadata(self):
        if self.windowTitle()!= self.racWindowTitle:
            fileName = self.windowTitle().replace(self.racWindowTitle, "")
            extension = GetExtension(fileName)
            if extension == ".qsp" : self.GetDataFromQSP(fileName)
            elif extension == ".xml" : self.GetDataFromXML(fileName)

    def loadMetadata(self):
        extension = "qsp"
        if self.windowTitle()!= self.racWindowTitle:
            fileName = self.windowTitle().replace(self.racWindowTitle, "")
            extension = GetExtension(fileName)
            extension = extension.replace(".","")
           
        zTitle = QApplication.translate("QSphere","Load a metadata file", None, QApplication.UnicodeUTF8)
        MyFileDialog = QFileDialog(self, zTitle)
        MyFileDialog.setNameFilters(self.Listfiltres)  
        MyFileDialog.selectNameFilter(self.NamedFiltres[extension])
        MyFileDialog.setDefaultSuffix(extension)
        MyFileDialog.setViewMode(QFileDialog.Detail)
        MyFileDialog.setDirectory(self.InitDir)
        MyFileDialog.setFileMode(QFileDialog.ExistingFile) 
        MyFileDialog.setAcceptMode(QFileDialog.AcceptOpen)

        FixeLabelsFileDialog(self, MyFileDialog, 0, True)
        
        if MyFileDialog.exec_():
            fileName = MyFileDialog.selectedFiles()[0]
            if fileName!="" :
                extension = GetExtension(fileName)
                if extension == ".qsp" : self.GetDataFromQSP(fileName)
                elif extension == ".xml" : self.GetDataFromXML(fileName)
                

    def GetDataFromQSP(self, fileName):
        zIndex = self.tabWidget.currentIndex()
        self.NewSheet()
        LoadQSP(self, fileName)
        self.checkSelectKeyWords()
        self.ReinitIHM(fileName, zIndex)
        
    def GetDataFromXML(self, fileName):
        zIndex = self.tabWidget.currentIndex()
        try : tree = ET.parse(fileName)
        except :
           self.BadMyISO()
           return
        root = tree.getroot()
        if root.tag != '{http://www.isotc211.org/2005/gmd}MD_Metadata':
           zMsg = QApplication.translate("QSphere","XML document does not appear to be ISO (not gmd:MD_Metadata found) !", None, QApplication.UnicodeUTF8)
           SendMessage(self, "information" , zMsg, QgsMessageBar.WARNING, self.duration_warning) 
           return

        if self.autoCorrect == True : 
            f = open(fileName, "r")
            bufferXML = f.read()#.decode('utf8')
            f.close()

            from cStringIO import StringIO

            if bufferXML.find("<fra:FRA_DataIdentification gco:isoType=\"gmd:MD_DataIdentification\">")!=-1:
               bufferXML = bufferXML.replace("xsi:schemaLocation=\"http://www.cnig.gouv.fr/2005/fra http://eden.ign.fr/xsd/fra/20060106/fra/fra.xsd\"", "xsi:schemaLocation=\"http://www.isotc211.org/2005/gmx http://schemas.opengis.net/iso/19139/20070417/gmx/gmx.xsd\"")
               bufferXML = bufferXML.replace("<fra:FRA_DataIdentification gco:isoType=\"gmd:MD_DataIdentification\">", "<gmd:MD_DataIdentification>")
               bufferXML = bufferXML.replace("</fra:FRA_DataIdentification>", "</gmd:MD_DataIdentification>")
               bufferXML = bufferXML.replace("<gco:CharacterString/>", "<gco:CharacterString> </gco:CharacterString>")

               if self.byStream == True :
                   from xmlISOparser import *
                   self.listImportCategories = []
                   myISO = xmlISOparser(None, StringIO(bufferXML) , 'MEDDE', self.langueTR)
                   if myISO == None :
                       self.BadMyISO()
                       return               
                   myISO.createISOdataStructure(True)

                   if myISO.getTagDictionnary() : self.ReloadDataFromXML(myISO, None, zIndex)
                   return

               elif self.byFile == True :
                   baseName = os.path.splitext(os.path.basename(fileName))[0]
                   extension = GetExtension(baseName)
                   baseName = baseName.replace(extension, "")
                   fileName = "%s%s_qsphere_transformation.xml" % (self.InitDirByFile, baseName)
                   zLOG = open(fileName, "w")
                   zLOG.write(bufferXML)
                   zLOG.close()

        
        from xmlISOparser import *
        self.listImportCategories = []
        myISO = xmlISOparser(fileName, None, 'MEDDE', self.langueTR)

        zCond = myISO.getTagDictionnary()
        if not zCond :
           zMsg = QApplication.translate("QSphere","XML dictionnary file for QSphere !", None, QApplication.UnicodeUTF8)
           zMsg1 = QApplication.translate("QSphere","Open or add this file with the dictionnary interface (list of contacts) !", None, QApplication.UnicodeUTF8)
           SendMessage(self, "information" , "%s<br>%s" % (zMsg, zMsg1), QgsMessageBar.WARNING, self.duration_warning) 
           return                

        self.ReloadDataFromXML(myISO, fileName, zIndex)

    def BadMyISO(self):
           zMsg = QApplication.translate("QSphere","Invalid XML document !", None, QApplication.UnicodeUTF8)
           SendMessage(self, "information" , zMsg, QgsMessageBar.WARNING, self.duration_warning)        

    def ReloadDataFromXML(self, myISO, fileName, zIndex):
        self.NewSheet()
        if myISO == None :
               self.BadMyISO()
               return False
        
        myISO.createISOdataStructure(True)
        
        zorderkeys = ("intitule", "resume", "typedata", "tablelocalisator", "identificator", "tablelangues", "tableformats", "tablecarac", \
                      "tablecategories", "tablecategories:0", "tablemotsclefsf", "tablescr", "tableemprises", "tableetenduetemporelle", "groups:dates", \
                      "genealogie", "coherence", "grouperesolutionscale", "tablespecifications", "groupedroits", "licence", "tableroles:1", "tableroles:2", "tableroles:3", \
                      "datemetada", "langmetada")
        
        zWidgetValues = {"intitule": myISO.title , "resume" : myISO.abstract, "typedata": myISO.typedata, "tablelocalisator" : myISO.localisators, \
                         "identificator" : myISO.UUID, "tablelangues" : myISO.languesjdd, "tableformats" : myISO.formatsjdd, "tablecarac": myISO.tablecarac,  \
                         "tablecategories" : myISO.categories, "tablecategories:0" : myISO.codecategories, "tablemotsclefsf" : myISO.keywordsF, \
                         "tablescr" : myISO.scr, "tableemprises" : myISO.boundingboxcoordinates, \
                         "tableetenduetemporelle" : myISO.timeperiodes, "groups:dates" : myISO.dates, \
                         "genealogie" : myISO.genealogie, "coherence" : myISO.coherence, "grouperesolutionscale" : myISO.scalesEC, \
                         "tablespecifications": myISO.conformities, "groupedroits" : myISO.accessconstraints, "licence" : myISO.legalconstraints, \
                         "tableroles:1" : myISO.pointsofcontactMDD, "tableroles:2" : myISO.pointsofcontact, "tableroles:3" : myISO.pointsofcontactCust, \
                         "datemetada" : (myISO.datemdd, myISO.datetmdd ), "langmetada" : myISO.languemdd
                         }

        self.tabWidget.setVisible(False)
        self.progressBar.setVisible(True)
        zBounds, i = len(zorderkeys), 0
        for i in range(zBounds):
            key = zorderkeys[i]
            self.UpdateWidget(key, zWidgetValues[key], myISO)
            self.progressBar.setValue(int(100 * i/zBounds))
            i+= 1

        self.ReinitIHM(fileName, zIndex)
        return True


    def UpdateWidget(self, zkeyWidget, zIsoXML, myISO):
        if not (zIsoXML) : return
        
        if zkeyWidget.startswith("groups:"):
           zGroupTarget = zkeyWidget.split(":")[1]
           zGroups = {"dates": {"c" : "datecredata", "r" : "daterevdata", "p" : "tabledatepubdata"}}
           zGroup = zGroups[zGroupTarget]

           if zGroupTarget == "dates" :
               zObj = self.findChild(MyTableWidget, "tabledatepubdata")
               self.cleanAllObj(zObj, True)
               i=0
               for elt in zIsoXML :
                   if type(elt) == dict :
                       if DicoHasKey(elt, 'type') : return
                       if elt['type'] == "" : return
                       zType = elt['type'][0:1]
                       zObj = getWidget(self, zGroup[zType])
                       if zType in ("c", "r") : 
                           zEltsDate = elt['date'].split("-")
                           zObj.setSelectedDate(QDate(int(zEltsDate[0]), int(zEltsDate[1]), int(zEltsDate[2]) ))
                       elif zType == "p" :
                            MakeLine(self, zObj, True, False,-1, True)
                            zObj.cellWidget(i, 0).setText(elt['date'])
                            i+= 1
        elif zkeyWidget == "coherence" : self.UpdateCoherence(zkeyWidget, zIsoXML)                     
        elif zkeyWidget == "tablespecifications" : self.UpdateTableSpecifications(zkeyWidget, zIsoXML)                    
        elif zkeyWidget == "tablemotsclefsf" : self.UpdateTableKeywordsF(zkeyWidget, zIsoXML, myISO)
        elif zkeyWidget == "tableetenduetemporelle": self.UpdateEtenduesTemporelles(zkeyWidget, zIsoXML, myISO)
        elif zkeyWidget == "groupedroits": self.UpdateEtenduesRights(zkeyWidget, zIsoXML, myISO)
        elif zkeyWidget.startswith("tableroles:") : self.UpdateTableRoles(zkeyWidget, zIsoXML)
        elif zkeyWidget.startswith("tablecategories:") : self.UpdateTableCategories(zkeyWidget, zIsoXML)
        elif zkeyWidget == "grouperesolutionscale":
            if (myISO.scalesEC[0]==[]) and (myISO.scalesUM[0]==[]): return
            zObj = self.findChild(QGroupBox, "grouperesolutionscale")
            zChildren = zObj.children()

            if (myISO.scalesUM[0]!=[]) :
                zChildren[1].setChecked(True)
                zInfos = myISO.scalesUM[0]
                try : zUnits = myISO.UnitsScalesUM[0][0]['uom']
                except : zUnits = "m" 
                zChildren[3].setEnabled(True)
                zIndex = self.ListUnitsMesure.index(zUnits) if zUnits in (self.ListUnitsMesure) else 0
                zChildren[3].setCurrentIndex(zIndex) 
            else :
                zChildren[0].setChecked(True)
                zInfos = myISO.scalesEC[0]
                zChildren[3].setEnabled(False)

            zChildren[2].clearContents()
            for j in range(zChildren[2].rowCount()): zChildren[2].removeRow(0)
            for j in range(len(zInfos)):
                zChildren[2].insertRow(j)
                zValue = float(zInfos[j]) if convertSTR(zInfos[j], "float") else 0.0
                AddLineWidget(self, zChildren[2], j,  0, 4, 0, zValue)
     
        else :
            zObj = getWidget(self, zkeyWidget)
            if zObj.metaObject().className() == "QLineEdit" :
                if (zIsoXML[0])!= []: zObj.setText(zIsoXML[0][0])
                
            elif zObj.metaObject().className() == "QCalendarWidget" :
                 zDate = ""
                 for elt in zIsoXML :
                     if elt[0]!=[] : zDate = elt[0][0]
                     
                 if zDate != "":
                     sep = ""    
                     if zDate.find("T")!=-1 : sep = "T" 
                     elif zDate.find(" ")!=-1 : sep = " "
                     if sep!="" : zDate = zDate.split(sep)[0] 
                     zEltsDate = zDate.split("-")
                     try : zObj.setSelectedDate(QDate(int(zEltsDate[0]), int(zEltsDate[1]), int(zEltsDate[2])))
                     except : self.reinitDateMDD(zObj)
             
            elif zObj.metaObject().className() in ("QTextEdit", "MyTextEdit") :
                if (zIsoXML[0])!= []:
                    try :  zObj.setText(zIsoXML[0][0])
                    except :  zObj.setPlainText(zIsoXML[0][0])
                
            elif zObj.metaObject().className() == "QTableView" :
                   if zObj.accessibleName() == "tablecategories": refcol, zIsoXML[0] = 1, [item.capitalize() for item in zIsoXML[0] if item!= None]
                   elif zObj.accessibleName() == "tablelangues": refcol, zIsoXML[0] = 0, [item.lower() for item in zIsoXML[0] if item!= None]
                   else : refcol = 0
                   for i in range(zObj.model().rowCount()):
                       if zObj.model().item(i, refcol).text() in zIsoXML[0]:
                          zObj.model().item(i, 0).setCheckState(Qt.Checked)
                          self.listImportCategories.append(zObj.model().item(i, refcol).text())
                       else : zObj.model().item(i, 0).setCheckState(Qt.Unchecked)
                       
            elif zObj.metaObject().className() in ("QComboBox", "MyComboBox") :
                 try : zValue = zIsoXML[0][0]
                 except : zValue = zIsoXML[0]
                 
                 if zValue == [] : return
                 if zObj.accessibleName() == "tablecarac" :
                     if zValue != None :
                         if zValue.find("MD_CharacterSetCode_")!=-1: zValue = zValue.replace("MD_CharacterSetCode_","")
                     else : zValue == "None"    
                     zIndex = self.listCodecs.index(zValue) if zValue in (self.listCodecs) else 0
                     zObj.setCurrentIndex(zIndex)
                 if zObj.accessibleName() == "typedata" :
                     zIndex = self.TypeData.index(zValue) if zValue in (self.TypeData) else 0
                     zObj.setCurrentIndex(zIndex)
                 else :
                     zIndex = zObj.findText(zValue) if zObj.findText(zValue) !=-1 else 0
                     zObj.setCurrentIndex(zIndex)
                     
            elif zObj.metaObject().className() in ("QTableWidget", "MyTableWidget") :
                 self.cleanAllObj(zObj, True)
                 zRows = len(zIsoXML)

                 if zObj.accessibleName() == "tablelocalisator" :
                    if zIsoXML == "None" : return
                    try :
                        if zRows == 2 and zIsoXML[1]== [] :
                             zRows = len(zIsoXML[0])
                             for i in range(zRows):
                                 MakeLine(self, zObj, True, False,-1, True)
                                 try : zObj.cellWidget(i, 0).setText("%s" % (zIsoXML[0][i]))
                                 except : pass
                             return
                    except : pass        

                 
                 if zObj.accessibleName() == "tablescr" :zRows = len(zIsoXML[0])
                 for i in range(zRows):
                     if zObj.accessibleName() == "tableemprises":
                         if type(zIsoXML[i])==dict:
                             MakeLine(self, zObj, True, False,-1, True)
                             zObj.cellWidget(i, 0).setValue(float(zIsoXML[i]['north']))
                             zObj.cellWidget(i, 1).setValue(float(zIsoXML[i]['south']))
                             zObj.cellWidget(i, 2).setValue(float(zIsoXML[i]['west']))
                             zObj.cellWidget(i, 3).setValue(float(zIsoXML[i]['east']))
                     elif  zObj.accessibleName() == "tableformats":
                         if type(zIsoXML[i])==dict:
                             MakeLine(self, zObj, True, False,-1, True)
                             zObj.cellWidget(i, 0).setText("%s" % (zIsoXML[i]['name']))
                             zObj.cellWidget(i, 2).setText("%s" % (zIsoXML[i]['version']))
                         elif type(zIsoXML[i])== list :
                             self.UpdateTableFormats(zObj, zIsoXML[i])
                             return
                     elif zObj.accessibleName() == "tablelocalisator" :
                         if type(zIsoXML[i])== dict :
                             if (zIsoXML[i]['url']!= None and zIsoXML[i]['url']!=' ' and zIsoXML[i]['name']!= None) :
                                 MakeLine(self, zObj, True, False,-1, True)
                                 if zIsoXML[i]['url']!= None : zObj.cellWidget(i, 0).setText("%s" % (urllib.unquote(zIsoXML[i]['url']))) 
                                 if zIsoXML[i]['name']!= None : zObj.cellWidget(i, 1).setText("%s" % (urllib.unquote_plus(zIsoXML[i]['name'])))
                         else :
                             MakeLine(self, zObj, True, False,-1, True)
                             try : zObj.cellWidget(i, 0).setText("%s" % (zIsoXML[0][i]))
                             except : pass
                     elif zObj.accessibleName() == "tablescr" :
                         MakeLine(self, zObj, True, False,-1, True)
                         zText = zIsoXML[0][i]
                         if zText != "" :
                            try : zId = long(zText)
                            except : zId = -1
                            zCond = QgsCoordinateReferenceSystem().createFromSrid(zId)

                            if not zCond :
                               zPos = zText.find("EPSG:") 
                               if zText.find("EPSG:")!=-1:
                                   zId = zText[zPos+5:zPos+11]
                                   while not convertSTR(zId, "int"):
                                         zId = zId[:-1]
                                         if zId == "" :
                                            zId = -1
                                            break
                                   zCond = QgsCoordinateReferenceSystem().createFromSrid(long(zId))

                         if zCond : zObj.cellWidget(i, 0).setText("%s" % (zId))
                         else : zObj.cellWidget(i, 0).setText("4258")

                 if zObj.accessibleName() == "tableemprises":
                    zObj.setToolTip("%s" % (zObj.rowCount()-1))
                    self.DessCadre()

    def UpdateTableFormats(self, zObj, zList):
        for k in range(len(zList)):
            MakeLine(self, zObj, True, False,-1, True)
            zObj.cellWidget(k, 0).setText("%s" % (zList[k]))

    def UpdateCoherence(self, zkeyWidget, zIsoXML):
        zObj = self.findChild(MyTextEdit, "coherence")
        import ast
        try : mydict = ast.literal_eval("%s" % (zIsoXML))
        except : mydict = None
       
        if mydict!= None :
           if type(mydict)== dict :
               if DicoHasKey(mydict, 'TopologyLevelCode') and DicoHasKey(mydict, 'GeometricObjectTypeCode'): zObj.setPlainText("{'TopologyLevelCode':'%s', 'GeometricObjectTypeCode':'%s'}" % (mydict['TopologyLevelCode'],mydict['GeometricObjectTypeCode']))
               else : zObj.setPlainText("{'TopologyLevelCode':'unknow', 'GeometricObjectTypeCode':'unknow'}")
           elif type(mydict)== list :
               if len(mydict)== 2 and type(mydict[0])==list and type(mydict[1])==list:
                  try : zTopologyLevelCode = mydict[0][0]
                  except : zTopologyLevelCode = 'unknow'
                  try : zGeometricObjectTypeCode = mydict[1][0]
                  except: zGeometricObjectTypeCode = 'unknow'
                  zObj.setPlainText("{'TopologyLevelCode':'%s', 'GeometricObjectTypeCode':'%s'}" % (zTopologyLevelCode, zGeometricObjectTypeCode)) 
               else : zObj.setPlainText("{'TopologyLevelCode':'unknow', 'GeometricObjectTypeCode':'unknow'}")
        else : zObj.setPlainText("{'TopologyLevelCode':'unknow', 'GeometricObjectTypeCode':'unknow'}")
        

    def UpdateEtenduesRights(self, zkeyWidget, zIsoXML, myISO):
        if type(zIsoXML[0])==list:
            if zIsoXML[0]==[]: return
            if zIsoXML[0][0] == "otherRestrictions" : 
                counter=0
                zObj = getWidget(self, zkeyWidget)
                zConstraints = myISO.otherconstraints[0]
                zChild = zObj.children()[2]
                zModel = zChild.model()
                for j in range(len(zConstraints)):
                    zCond, zIndex = self.isContraintsIn(zConstraints[j], zModel)
                    if zCond :
                       zChild.model().item(zIndex, 0).setCheckState(Qt.Checked)
                       counter+= 1
                if counter > 0 : zObj.children()[1].setChecked(True)

    def isContraintsIn(self, zContraintText, zModel):
        zCond, zIndex = False, -1
        #First, check the model ...
        for i in range(zModel.rowCount()):
            if zContraintText.find(zModel.item(i, 0).text())!=-1 or  zContraintText.find(zModel.item(i, 1).text())!=-1  : return True, i
        #Second test, on list INSPIRE
        listContraints = ("(a) the confidentiality of the proceedings of public authorities, where such confidentiality is provided for by law.", \
                          "(b) international relations, public security or national defence.", \
                          "(c) the course of justice, the ability of any person to receive a fair trial or the ability of a public authority to conduct an enquiry of a criminal or disciplinary nature", \
                          "(d) the confidentiality of commercial or industrial information, where such confidentiality is provided for by national or Community law to protect a legitimate economic interest, including  the  public  interest  in  maintaining  statistical confidentiality and tax secrecy.", \
                          "(e) intellectual property rights", \
                          "(f) the confidentiality of personal data and/or files relating to a natural person where that person has not consented to the disclosure of  the information to the public, where such confidentiality is provided for by national or Community law.", \
                          "(g) the interests or protection of any person who supplied the information requested on a voluntary basis without being under, or capable of being put under, a legal obligation to do so, unless that person has consented to the release of the information concerned.", \
                          "(h) the protection of the environment to which such information relates, such as the location of rare species.")
        for i in range(len(listContraints)):
            if listContraints[i].find(zContraintText)!=-1 or zContraintText.find(listContraints[i])!=-1 : return True, i
        return zCond, zIndex


    def UpdateTableSpecifications(self, zkeyWidget, zIsoXML):
        zDim = len(zIsoXML)
        zObj = self.findChild(MyTableWidget, zkeyWidget)
        if not zObj : return
        self.cleanAllObj(zObj, True)
        for i in range(zDim):
            if zIsoXML[i]==[]:pass
            else :
                if type(zIsoXML[i])==dict:
                    MakeLine(self, zObj, True, False,-1, True)
                    try :
                        zObj.cellWidget(i, 0).setText(zIsoXML[i]['text'])
                        zObj.cellWidget(i, 1).setText(zIsoXML[i]['date'])
                        try : zIndex = ("creation","revision","publication").index(zIsoXML[i]['typedate'].lower())
                        except : zIndex = 0
                        if zIndex == -1 : zIndex = 0
                        zObj.cellWidget(i, 2).setCurrentIndex(zIndex)

                        if type(zIsoXML[i]['conformity'])== str :
                           zIndex = 0 if zIsoXML[i]['conformity'].lower() == 'true' else 1 
                        else : zIndex = 2                
                        zObj.cellWidget(i, 3).setCurrentIndex(zIndex)
                    except : pass

    def UpdateEtenduesTemporelles(self, zkeyWidget, zIsoXML, myISO):
        zObj = self.findChild(MyTableWidget, zkeyWidget)
        if not zObj : return
        self.cleanAllObj(zObj, True)
        if type(zIsoXML[0])== dict :
           zDim = len(zIsoXML) 
           for i in range(zDim):
               MakeLine(self, zObj, True, False,-1, True)
               zLine = zObj.rowCount()-1
               zObj.cellWidget(zLine, 0).setText("%s %s" % (zIsoXML[i]['start'], zIsoXML[i]['end']))
        else :
           if len(zIsoXML[0])>0: 
              for i in range(0, len(zIsoXML[0]), 2):
                   MakeLine(self, zObj, True, False,-1, True)
                   zLine = zObj.rowCount()-1
                   zObj.cellWidget(zLine, 0).setText("%s %s" % (zIsoXML[0][i], zIsoXML[0][i+1]))


    def UpdateTableKeywordsF(self, zkeyWidget, zIsoXML, myISO):
        zDim = len(zIsoXML)
        zObj = self.findChild(MyTableWidget, zkeyWidget)
        if not zObj : return
        
        if zIsoXML == 'None' :
           zIsoXML = myISO.keywordsFNC
           zDim = len(zIsoXML[0])

           for i in range(zDim):
               if type(zIsoXML[0]) == list:
                 if zIsoXML[0][i]!=None :
                     if zIsoXML[0][i]!="" and zIsoXML[0][i].capitalize() not in (self.listImportCategories) :
                        MakeLine(self, zObj, True, False,-1, True)
                        zLine = zObj.rowCount()-1

                        zObj.cellWidget(zLine, 0).setText("%s" % (zIsoXML[0][i]))
                        zObj.cellWidget(zLine, 1).setChecked(False)
                        
                        for k in range(2,5):
                            zItemEditLine = zObj.cellWidget(zLine, k)
                            try : zItemEditLine.setEnabled(False)
                            except : pass

        else :
            zkeys = {'keyword':0,'thesaurus':2,'date':3,'typedate':4}
            for i in range(zDim):
                if type(zIsoXML[i])== dict :
                   if zIsoXML[i]['keyword']!=None : 
                       if zIsoXML[i]['keyword'].capitalize() not in (self.listImportCategories): 
                           MakeLine(self, zObj, True, False,-1, True)
                           zLine = zObj.rowCount()-1

                           for key in zIsoXML[i] :
                               ikey = zkeys[key]
                               if zObj.cellWidget(zLine, ikey).metaObject().className() in ("QComboBox", "MyComboBox") :
                                  try : zIndex = ("creation","revision","publication").index(zIsoXML[i][key])
                                  except : zIndex = 0
                                  if zIndex == -1 : zIndex = 0
                                  zObj.cellWidget(zLine, ikey).setCurrentIndex(zIndex)
                               else :
                                   zObj.cellWidget(zLine, ikey).setText("%s" % (zIsoXML[i][key]))
                                   if ikey == 2 :
                                      if zIsoXML[i][key] != "" : zObj.cellWidget(zLine, 1).setChecked(True)
                                       
                else :
                     if type(zIsoXML[i])== list and zIsoXML[i]!= []:
                         zLine = 0
                         for keyword in zIsoXML[i] :
                            if i == 0 : MakeLine(self, zObj, True, False,-1, True)
                            if zObj.cellWidget(zLine, i).metaObject().className() in ("QComboBox", "MyComboBox") :
                               try : zIndex = ("creation","revision","publication").index(keyword)
                               except : zIndex = 0
                               if zIndex == -1 : zIndex = 0
                               zObj.cellWidget(zLine, i).setCurrentIndex(zIndex)
                            else : zObj.cellWidget(zLine, i).setText(keyword)
                            zLine+= 1
                        
                      

    def UpdateTableCategories(self, zkeyWidget, zIsoXML):
        if zIsoXML!=[[]]:
           zObj = self.findChild(QTableView, zkeyWidget.split(":")[0])
           if not zObj : return
           zcategories = zIsoXML[0]

           for i in range(len(zcategories)):
               zcategorie = zcategories[i]
               for k in range(zObj.model().rowCount()):
                   if zObj.model().item(k, 2).text().find("(%s)" % (zcategorie))!= -1 :
                       if zObj.model().item(k, 0).checkState() == Qt.Unchecked :
                          zObj.model().item(k, 0).setCheckState(Qt.Checked) 
                       break
             

    def UpdateTableRoles(self, zkeyWidget, zIsoXML):
         zDim = len(zIsoXML)
         zkeyWidget = zkeyWidget.split(":")[0]
         zObj = self.findChild(MyTableWidget, zkeyWidget)
         if not zObj : return

         zkeys = {'ville': 5, 'name': 1, 'pays': 3, 'adresse': 2, 'codepostal': 4, 'mail': 6, 'role': 0, 'phone' : 7, 'url' : 8}
         zinvkeys = {0: 'role', 1: 'name', 2: 'adresse', 3: 'pays', 4 : 'codepostal', 5: 'ville', 6: 'mail', 7: 'phone', 8 : 'url'}

         firstOwner = False

         for i in range(zDim):
             if type(zIsoXML[i])== dict :
                 if zIsoXML[i]['role'] == None : break
                 if  zIsoXML[i]['role'].lower() == "pointofcontact" : zLine = 1
                 else :
                      if zIsoXML[i]['role'].lower() == "owner" and not firstOwner :
                          zLine, firstOwner = 0, True
                      else :        
                         MakeLine(self, zObj, True, False,-1, True)
                         zLine = zObj.rowCount()-1
                             
                 for key in zIsoXML[i] :
                     ikey = zkeys[key]
                     if zObj.cellWidget(zLine, ikey).metaObject().className() in ("QComboBox", "MyComboBox") :
                         if key == "role":
                             zIndexes = [keyitem for keyitem, value in self.DicoListOfRules.items() if value == zIsoXML[i][key]] 
                             if zIndexes!=[] : zIndex = zIndexes[0]  
                         else : zIndex = zObj.cellWidget(zLine, ikey).findText(zIsoXML[i][key].capitalize())
                         if zIndex == -1 : zIndex = 0
                         zObj.cellWidget(zLine, ikey).setCurrentIndex(zIndex) 
                     else : zObj.cellWidget(zLine, ikey).setText("%s" % (zIsoXML[i][key]))
                     ikey+= 1
                     
             elif type(zIsoXML[i])== list :
                 firstOwner = False

                 for k in range(len(zIsoXML[0])):

                     if zIsoXML[k] == [] : zLine = 1
                     else :
                         if zIsoXML[k][0] == None : zLine = 1
                         else : 
                             if zIsoXML[k][0].lower()=="owner" and firstOwner == False : zLine, firstOwner = 0, True
                             elif zIsoXML[k][0].lower() == "pointofcontact" : zLine = 1
                             else : 
                                  MakeLine(self, zObj, True, False,-1, True)
                                  zLine = zObj.rowCount()-1
                          
                     for j in range(zDim):
                         if zIsoXML[j]!=[] :
                             if zIsoXML[j][k]!= None :
                                 if zObj.cellWidget(zLine, j).metaObject().className() in ("QComboBox", "MyComboBox") :
                                         zIndex = 0
                                         if zinvkeys[j] == "role":
                                             zIndexes = [keyitem for keyitem, value in self.DicoListOfRules.items() if value == zIsoXML[j][k]] 
                                             if zIndexes!=[] : zIndex = zIndexes[0]  
                                         else : zIndex = zObj.cellWidget(zLine, j).findText(zIsoXML[j][k].capitalize())
                                         if zIndex == -1 : zIndex = 0
                                         zObj.cellWidget(zLine, j).setCurrentIndex(zIndex)
                                 else : zObj.cellWidget(zLine, j).setText("%s" % (zIsoXML[j][k]))
                 break

    def ChangeOptionScale(self):
        zIndex = self.tabWidget.currentIndex()
        self.sender().parent().children()[3].setEnabled(self.sender().parent().children()[1].isChecked())
        if self.sender().parent().children()[0].isChecked():
           ztoolTip = self.sender().parent().children()[0].toolTip() 
           cible = 1 
        else :
           ztoolTip = self.sender().parent().children()[1].toolTip() 
           cible = 0 
        valuesObj = None

        if ztoolTip.find("|")!=-1: valuesObj = ztoolTip.split("|")
        else:
            if is_number_float(ztoolTip): valObj = float(ztoolTip)
            else : valObj = 0.0
        zObject = self.sender().parent().children()[2] 
        zRow = zObject.rowCount()
        valuesObjsave = ""
        for i in range(zRow):
            Obj = zObject.cellWidget(i, 0)
            zSepa = "" if valuesObjsave == "" else "|"
            valuesObjsave+= "%s%s" % (zSepa, Obj.value())
            
            if self.sender().parent().children()[0].isChecked(): PropertiesDoubleSpinBox(self, Obj, 0, 0, 10000000, 1000)
            else: PropertiesDoubleSpinBox(self, Obj, 4, 0, 1000, 10)
            
            if valuesObj == None : Obj.setValue(valObj)
            else :
                if i <= (len(valuesObj)-1): Obj.setValue(float(valuesObj[i]))
                else : Obj.setValue(float(valuesObj[len(valuesObj)-1]))

        if valuesObjsave!= "" : self.sender().parent().children()[cible].setToolTip("%s" % (valuesObjsave))
        self.tabWidget.setCurrentIndex(zIndex) #self.listeOnglets.setCurrentIndex(zIndex)
            
    def ChangeOptionRights(self): self.sender().parent().children()[2].setEnabled(self.sender().parent().children()[1].isChecked())

    def testURL(self): testURL(self)
    def goToLocalisator(self): goToLocalisator(self)
    def AfficheHelp(self): AfficheHelp(self)

    def AfficheRessources(self):
        #Not implemented in current version
        #Action for QCommandLink Button
        d = doUI.LoadDialogViewer(self, self.iface,  "%s" % (self.sender().toolTip()), False, [], self.langueTR, self, None, "open.png", False)
        self.childswindows.append(d)
        self.nb_window_childs.setText("%s" % (len(self.childswindows)))

    def CallSelectorConformityInfos(self):
        zObj = self.findChild(MyTextEdit, "coherence")
        dialog = TopologyDialog(zObj.toPlainText())
        MakeWindowIcon(dialog, "qsp.png")
        if dialog.exec_(): zObj.setPlainText("%s" % (dialog.infosTopology()))
        
    def CallQgsProjectionSelector(self):
         zObj = self.findChild(MyTableWidget, "tablescr")
         zIndex = int(self.sender().accessibleName().split("_")[2])
         zItemEditLine = zObj.cellWidget(zIndex,0)
         ChangeButtonIcon(self, self.sender(),"projectionactivate.png", 18, 16)
         dialog = SRSDialog(zItemEditLine.text())
         MakeWindowIcon(dialog, "projection.png")
         dialog.setWindowTitle(QApplication.translate("QSphere","Coordinate Reference System Selector", None, QApplication.UnicodeUTF8))
         if dialog.exec_(): zItemEditLine.setText("%s" % (dialog.epsg()))
         ChangeButtonIcon(self, self.sender(),"projection.png", 18, 16)

    def ChooseContact(self):
        d = doUI.DialogContacts(self, True)
        d.exec_()
         
    def CallFormatSelector(self):
        zObj = self.findChild(MyTableWidget, "tableformats")
        zIndex = int(self.sender().accessibleName().split("_")[2])
        zItemEditLine = zObj.cellWidget(zIndex,0)
        ChangeButtonIcon(self, self.sender(),"formatactivate.png", 18, 16)
        dialog = FormatDialog(self.formats, zItemEditLine.text())
        MakeWindowIcon(dialog, "format.png")
        if dialog.exec_(): zItemEditLine.setText("%s" % (dialog.format()))
        ChangeButtonIcon(self, self.sender(),"format.png", 18, 16)

    def CheckInfosRoles(self): CheckInfosRoles(self)

    def ChangePatternZipPostalCode(self): ChangePatternZipPostalCode(self)

    def LoadListOfValues(self): LoadListOfValues(self)

    def FixeToolTipCalendar(self):
        zObjCalendar = self.findChild(QCalendarWidget, "%s" % (self.sender().accessibleName()))
        zToolTip = MakeToolTipCalendar(self, zObjCalendar)

    def ChangeAccessibility(self, checked): ChangeAccessibility(self, checked)

    def checkSelectKeyWords(self):
        zObj = self.findChild(QTableView, "tablecategories")
        zObjTarget = self.findChild(MyTableWidget, "tablemotsclefso")
        for row in range(zObj.model().rowCount()):
            zItem = zObj.model().item(row, 1)
            item = zObj.model().item(row, 0)
            if item.checkState() == Qt.Checked : 
                MakeLine(self, zObjTarget, True, False,-1, True)
                zItemTarget = zObjTarget.cellWidget(zObjTarget.rowCount()-1, 0)
                zItemTarget.setEnabled(True)
                zItemTarget.setCurrentIndex(0)
                zItemTarget.setEnabled(False)
                zItemTarget = zObjTarget.cellWidget(zObjTarget.rowCount()-1, 1)
                for i in range(zItemTarget.count()):
                    zEltList = zItemTarget.itemText(i)
                    if zEltList.upper() == zItem.text().upper():
                       zItemTarget.setCurrentIndex(i)
                       zItemTarget.setEnabled(False)
                       break

                
    def SelectKeyWord(self, item):
        zObj = self.findChild(QTableView, "tablecategories")
        zItem = zObj.model().item(item.row(), 1)
        zObjTarget = self.findChild(MyTableWidget, "tablemotsclefso")

        if item.checkState() == Qt.Checked : 
            MakeLine(self, zObjTarget, True, False,-1, True)
            zItemTarget = zObjTarget.cellWidget(zObjTarget.rowCount()-1, 0)    
            zItemTarget.setEnabled(True)
            zItemTarget.setCurrentIndex(0)
            zItemTarget.setEnabled(False)
            zItemTarget = zObjTarget.cellWidget(zObjTarget.rowCount()-1, 1)
            for i in range(zItemTarget.count()):
                zEltList = zItemTarget.itemText(i)
                if zEltList.upper() == zItem.text().upper():
                   zItemTarget.setCurrentIndex(i)
                   zItemTarget.setEnabled(False)
                   break
        else:
            for line in range(zObjTarget.rowCount()):
                zItemTarget = zObjTarget.cellWidget(line, 1)
                if zItemTarget == None : break
                if zItemTarget.currentText().upper() == zItem.text().upper():
                   zObjTarget.removeRow(line)
                   break
        countItems(self, "tablemotsclefso", zObjTarget)

    def majItemLangues(self, item): self.CountLangues()
        
    def CountLangues(self):
        zObjLabel = self.findChild(QLabel, "Lbltablelangues")
        if not zObjLabel : return
        zObj = self.findChild(QTableView, "tablelangues")
        if not zObj : return
        zRows, counter, listlangues = zObj.model().rowCount(), 0, ""
        for i in range(zRows):
            if zObj.model().item(i, 0).checkState()== Qt.Checked:
                counter+= 1
                zNewline = "<br>" if counter % 4 == 0 else ""
                listlangues+= "<b>%s</b> %s" % (zObj.model().item(i, 0).text(), zNewline)
        zRacLabel = QApplication.translate("QSphere","Language(s) for the resource : ", None, QApplication.UnicodeUTF8)
        zObjLabel.setText("(<b><u>%s</u></b>) %s<br>%s" % (counter, zRacLabel, listlangues))


    def cleanAllObj(self, zObj, doCount):
        if not zObj : return
        zObj.clearContents()
        for i in range(zObj.rowCount()): zObj.removeRow(0)
        if doCount : countItems(self, zObj.accessibleName(), zObj)        

    def doDessCadre(self, currentRow, currentColumn, previousRow, previousColumn):
        if currentRow!= previousRow : self.DessCadre()
                    
    def DessCadre(self):
        zBorneLong = int(self.EmpriseLong/2)
        zBorneLat = int(self.EmpriseLat/2)
        zIndexEmp = -1

        if self.sender()==None or self.sender().objectName()=="" or self.sender().objectName() == "mActionMetadata" :
           zObj = self.findChild(MyTableWidget, "tableemprises")
           zIndexEmp = GetIndex(zObj)
        else:
           zNameObj = "%s" % (self.sender().objectName())
           zObj = self.findChild(MyTableWidget, "tableemprises")

           if zObj != None : zIndexEmp = zObj.currentRow()

        if zIndexEmp == -1: return
        zItem = zObj.cellWidget(zIndexEmp,0)        
        if zItem == None : return
       
        zItem = zObj.cellWidget(zIndexEmp,2)
        XposD = int(zItem.value())+ zBorneLong

        zItem = zObj.cellWidget(zIndexEmp,3)
        XposF = int(zItem.value())+zBorneLong
       
        zItem = zObj.cellWidget(zIndexEmp,0)
        YposD = zBorneLat-int(zItem.value())

        zItem = zObj.cellWidget(zIndexEmp,1)
        YposF = zBorneLat-int(zItem.value())

        self.zCadre.setGeometry(QRect(XposD, YposD, (XposF-XposD), (YposF - YposD)))
        self.zMireH.setGeometry(QRect(XposD + int((XposF-XposD)/2), 0, 1, self.EmpriseLat)) 
        self.zMireW.setGeometry(QRect(0, YposD - int((YposD-YposF)/2), self.EmpriseLong, 1))


    def AddDragDropLine(self, Obj, data):
        MakeLine(self, Obj, True, False, -1, True)
        zWidget = Obj.cellWidget(Obj.rowCount()-1, 0)
        if not zWidget : return
        if zWidget.metaObject().className() == "MySpinBox" :
           try : zWidget.setValue(float(data))
           except :
               try : zWidget.setValue(int(data))
               except : pass
        elif zWidget.metaObject().className() in ("QComboBox", "MyComboBox") :
             zOrIndex = zWidget.currentIndex()
             zIndex = zWidget.findText("%s" % (data))
             if zIndex == -1 and zOrIndex == -1 : zIndex = 0
             else : zIndex = zOrIndex
             zWidget.setCurrentIndex(zIndex)             
        else : zWidget.setText("%s" % (data))

def CleanSheetTable(self, zObjTable, zFileData, zLinkedTable): 
     zItems = []
     for k in range(zObjTable.model().rowCount()):
         zItem = zObjTable.model().item(k, 0)
         if zItem.checkState()== Qt.Checked: zItems.append(k)
     zObjTable.clearSpans()

     if zLinkedTable != None : 
        zObjKeyListWords = self.findChild(MyTableWidget, zLinkedTable)
        if zObjKeyListWords :
           zObjKeyListWords.clearContents()
           zObjKeyListWords.setRowCount(0)

     self.tableModel = QStandardItemModel(self)
     SizeW, zCols, iLine = LoadFile(self, zObjTable, zObjTable.accessibleName(), zFileData, 3, self.tableModel)
     zObjTable.setModel(self.tableModel)
     for k in range(len(zItems)):
         zItem = zObjTable.model().item(zItems[k], 0)
         zItem.setCheckState(Qt.Checked)


def CheckInfosRoles(self):
    if self.ShowWarning :
        zObj = self.sender()
        zObjParent = self.findChild(MyTableWidget, "tableroles")
        if zObj.currentIndex() == 6 and zObjParent.rowCount()>2 :
           zTitle = QApplication.translate("QSphere", "Warning" , None, QApplication.UnicodeUTF8) 
           zMsg = QApplication.translate("QSphere"," One owner or PointOfContact ! Please ...", None, QApplication.UnicodeUTF8)
           try : SendMessage(self, zTitle, zMsg, QgsMessageBar.WARNING, self.duration_warning)
           except : pass
           zObj.setCurrentIndex(1)

def AddLine(self):
    if self.objectName() == "DialogMetaData" : zIndex = self.tabWidget.currentIndex() 
    zObjectName = "%s" % (self.sender().objectName())
    zSplit = zObjectName.split("_")
    zRac = zSplit[0]
    zType = int(zSplit[1])
    zCible = zSplit[2]
    
    if zCible.startswith("groupe"): zObj = self.findChild(QGroupBox, zCible)
    else : zObj = self.findChild(MyTableWidget, zCible)
 
    if self.objectName() == "DialogMetaData" : self.tabWidget.setCurrentIndex(zIndex) 
    
    if zObj == None : return
    if zObj.metaObject().className() == "QGroupBox" : zObj = getWidget(self.tabWidget.currentWidget(), "tableechelles")

    row = -1 if zRac != "AjouterAfter" else (zObj.currentRow()+1)

    MakeLine(self, zObj, True, False, row, True)

    if self.objectName() == "DialogMetaData" : RenameAllWidgets(self, zObj)
    zObj.selectRow(row)
    zObj.setFocus()
    if self.objectName() == "DialogMetaData" : self.tabWidget.setCurrentIndex(zIndex) 


def MakeLine(self, zObj, zDrawResult, zReinit, zRow, isCount):
    zCollection = []
    zObjWidgets = []

    zkey = zObj.accessibleName()
    if not DicoHasKey(self.ParamsLineWidget, zkey): return
    if zRow == -1 : zRow = zObj.rowCount()

    zParams = self.ParamsLineWidget[zkey]
    
    if zObj.accessibleName() in ("tablescr", "tableformats", "tablelocalisator", "tableemprises", "tabledatepubdata", "tableechelles") :
       zObj.insertRow(zRow)
       for i in range(len(zParams)):
           zObjWidget = AddLineWidget(self, zObj, zRow, i, zParams[i][0], zParams[i][1], zParams[i][2])
           zObjWidgets.append(zObjWidget)
       zCollection.append(zObjWidgets)    

       if zObj.accessibleName() == "tableemprises" :
          zObj.setToolTip("%s" % (zRow))
          if zDrawResult and self.objectName() == "DialogMetaData" : self.DessCadre()

    elif zObj.accessibleName() in ("tableetenduetemporelle", "tablemotsclefso", "tablemotsclefsf", "tablespecifications") :
       if not zReinit :
           FixeCheckBox = False
           zObj.insertRow(zRow)
           for i in range(len(zParams)):
               zObjWidget = AddLineWidget(self, zObj, zRow, i, zParams[i][0], zParams[i][1], zParams[i][2])
               zObjWidgets.append(zObjWidget)
               if zParams[i][0] == 6 and zObj.accessibleName() == "tablemotsclefsf" :
                   FixeCheckBox = True
                   zObjCheckBox, zDefaultValue = zObjWidget, zParams[i][2]

           if FixeCheckBox :
              if type(zDefaultValue)!= int : zDefaultValue = 2
              zObjCheckBox.setCheckState(zDefaultValue)
              zObjCheckBox.toggled.emit(False)
               
           zCollection.append(zObjWidgets)

       if zObj.accessibleName() == "tablespecifications" :
           if zReinit : 
              for k in range(len(self.ListOfConformities)):
                  zObj.insertRow(zRow)
                  for i in range(len(zParams)):
                      zObjWidget = AddLineWidget(self, zObj, zRow, i, zParams[i][0], zParams[i][1], zParams[i][2])
                      zObjWidgets.append(zObjWidget)
                  zCollection.append(zObjWidgets)
                      
                  for j in range(4):
                      zItemEditLine = zObj.cellWidget(zRow, j)
                      if zItemEditLine.metaObject().className() in ("QLineEdit", "MySimpleWidgetLineEdit", "MyWidgetLineEdit"): zItemEditLine.setText(self.ListOfConformities[k][j])
                      elif zItemEditLine.metaObject().className() in ("QComboBox", "MyComboBox"):
                          try : zItemEditLine.setCurrentIndex(int(self.ListOfConformities[k][j]))
                          except : zItemEditLine.setCurrentIndex(0)
           
    
    elif zObj.accessibleName() == "tableroles" :
       zObj.insertRow(zRow)
       if zRow == 0 : zValue = 2
       elif zRow == 1 : zValue = 6
       else : zValue = 1

       for i in range(len(zParams)):
           if i== 0 : zObjWidget = AddLineWidget(self, zObj, zRow, i, zParams[i][0], zParams[i][1], zValue)
           else : zObjWidget =  AddLineWidget(self, zObj, zRow, i, zParams[i][0], zParams[i][1], zParams[i][2])
           zObjWidgets.append(zObjWidget)
       zCollection.append(zObjWidgets)
       
       if zReinit :
          zRow = zObj.rowCount()
          zObj.insertRow(zRow)
          for i in range(len(zParams)):
              if i== 0 and zRow == 1: zObjWidget = AddLineWidget(self, zObj, zRow, i, zParams[i][0], zParams[i][1], 6)
              else : zObjWidget = AddLineWidget(self, zObj, zRow, i, zParams[i][0], zParams[i][1], zParams[i][2])
              zObjWidgets.append(zObjWidget)
          zCollection.append(zObjWidgets)
                
    if isCount : countItems(self, zObj.accessibleName(), zObj)

    return zObjWidgets

def DelLineProcess(self, zObject, zLastLine):
    if zObject == "" : return
    zSplit = zObject.split("_")
    if CountCaractere(zObject, "_", False, False)!=2 : return
    zType = int(zSplit[1])
    zCible = zSplit[2]
    
    if zCible.startswith("groupe"): zObj = self.findChild(QGroupBox, zCible)
    else : zObj = self.findChild(MyTableWidget, zCible)    
    
    zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)

    if zObj == None : return
    
    if zType !=8 :      
        if zObj.rowCount()==0 :
           zMsg = QApplication.translate("QSphere","Nothing to delete.", None, QApplication.UnicodeUTF8)
           SendMessage(self, zTitle , zMsg, QgsMessageBar.WARNING, self.duration_warning)
           return

    if zCible == "tableroles" :
       zMinRow, zMsg = 2, QApplication.translate("QSphere","Two reference information must be defined !", None, QApplication.UnicodeUTF8) 
    else :
       if zCible in("tablemotsclefso", "tablemotsclefsf", "tableetenduetemporelle", "tablespecifications", "tableformats") : zMinRow, zMsg = 0, QApplication.translate("QSphere","Information must be set at least !", None, QApplication.UnicodeUTF8)
       else : zMinRow, zMsg = 1, QApplication.translate("QSphere","Information must be set at least !", None, QApplication.UnicodeUTF8)
    
    if zType == 8: zObj = zObj.children()[2]
    if zObj.rowCount() > zMinRow :
        if zLastLine : zIndex = (zObj.rowCount()-1)
        else :
           if zObj.rowCount()>0 : zIndex = 0 if zObj.currentRow()== -1 else zObj.currentRow()
        if zCible == "tableroles" :
           if zIndex < 2 :
              zMsg = QApplication.translate("QSphere","Can delete the current line.", None, QApplication.UnicodeUTF8)
              SendMessage(self, zTitle , zMsg, QgsMessageBar.WARNING, self.duration_warning)
              return
        if zCible == "tablemotsclefso" :
              if zObj.cellWidget(zIndex, 0).isEnabled()==False and zObj.cellWidget(zIndex, 1).isEnabled()==False :
                  zMsg = QApplication.translate("QSphere","Can delete the current line.", None, QApplication.UnicodeUTF8)
                  zMsg1 = QApplication.translate("QSphere","Use thematic selection to delete this line.", None, QApplication.UnicodeUTF8)
                  SendMessage(self, zTitle , "%s<br>%s" % (zMsg, zMsg1), QgsMessageBar.WARNING, self.duration_warning)
                  return
            
        zObj.removeRow(zIndex) 
        if zCible == "tableemprises":
           zObj.setToolTip("%s" % (zObj.currentRow())) 
           if self.objectName() == "DialogMetaData" : self.DessCadre()
    else:
        zMsg = QApplication.translate("QSphere","Can not delete the last line.", None, QApplication.UnicodeUTF8)+ "<br>%s" % (zMsg)
        SendMessage(self, zTitle , zMsg, QgsMessageBar.WARNING, self.duration_warning)
    countItems(self, zCible, zObj)
    RenameAllWidgets(self, zObj)
    zObj.selectRow(zObj.currentRow()) 
    zObj.setFocus()

def MoveLineUpProcess(self, zObject):
    if zObject == "" : return
    zSplit = zObject.split("_")
    if CountCaractere(zObject, "_", False, False)!=2 : return
    zType = int(zSplit[1])
    zCible = zSplit[2]
    
    if zCible.startswith("groupe"): zObj = self.findChild(QGroupBox, zCible)
    else : zObj = self.findChild(MyTableWidget, zCible)
    
    if zObj == None : return
    
    if zObj.metaObject().className() == "QGroupBox" :
       zCible = "tableechelles"
       zObj = getWidget(self.tabWidget.currentWidget(), zCible)
    if type(zObj ) != MyTableWidget : return
    if zObj.rowCount() == 0 : return
   
    row = zObj.currentRow()
    if row > 0:
        if self.objectName() == "DialogMetaData" : self.ShowWarning = False
        NewCollectionObjWidget = MakeLine(self, zObj, True, False, row-1, False)
        
        for i in range(zObj.columnCount()):
           OriginalWidget = (zObj.cellWidget(row+1,i))
           if OriginalWidget == None : OriginalWidget = (zObj.item(row+1,i))
           NewObjWidget = NewCollectionObjWidget[i]
           if OriginalWidget.metaObject().className() in ("QLineEdit", "MySimpleWidgetLineEdit", "MyWidgetLineEdit", "MySimpleWidgetLineEditST") : NewObjWidget.setText(OriginalWidget.text())
           elif OriginalWidget.metaObject().className() in ("QCheckBox", "MyCheckBox") : NewObjWidget.setChecked(OriginalWidget.isChecked())
           elif OriginalWidget.metaObject().className() == "MyComboBox" :
                  if zCible!= "tableroles" or i != 0 : NewObjWidget.setCurrentIndex(OriginalWidget.currentIndex())
           elif OriginalWidget.metaObject().className() == "MySpinBox" : NewObjWidget.setValue(OriginalWidget.value())     
        
        zObj.selectRow(row-1)
        zObj.removeRow(row+1)
        if zCible == "tableroles" : self.CheckTable(zObj)          
        if self.objectName() == "DialogMetaData" : self.ShowWarning = True            
        RenameAllWidgets(self, zObj)

        if zCible == "tableechelles" and self.objectName() == "DialogMetaData" : self.tabWidget.setCurrentIndex(4) 


           
def MoveLineDownProcess(self, zObject):
    if zObject == "" : return
    zSplit = zObject.split("_")
    if CountCaractere(zObject, "_", False, False)!=2 : return
    zRac = zSplit[0]
    zType = int(zSplit[1])
    zCible = zSplit[2]

    if zCible.startswith("groupe"): zObj = self.findChild(QGroupBox, zCible)
    else : zObj = self.findChild(MyTableWidget, zCible)    

    if zObj == None : return
    
    if zObj.metaObject().className() == "QGroupBox" :
       zCible = "tableechelles"
       zObj = getWidget(self.tabWidget.currentWidget(), zCible)
    if type(zObj ) != MyTableWidget : return
    if zObj.rowCount() == 0 : return

    row = zObj.currentRow()
    if row == -1 : row = 0
    zBorne = zObj.rowCount()-1 if zRac == "MoveDown" else zObj.rowCount()
    if row < 0 and zRac == "CloneLine" : return

    if row < zBorne :
        rowcible = (row+2) if zRac == "MoveDown" else (row+1)
        if self.objectName() == "DialogMetaData" : self.ShowWarning = False
        NewCollectionObjWidget = MakeLine(self, zObj, True, False, rowcible, False) 
        for i in range(zObj.columnCount()):
           OriginalWidget = zObj.cellWidget(row,i)
           NewObjWidget = NewCollectionObjWidget[i]
           if OriginalWidget == None : OriginalWidget = zObj.item(row,i)
           if OriginalWidget.metaObject().className() in ("QLineEdit", "MySimpleWidgetLineEdit", "MyWidgetLineEdit", "MySimpleWidgetLineEditST") : NewObjWidget.setText(OriginalWidget.text())
           elif OriginalWidget.metaObject().className() in ("QCheckBox", "MyCheckBox") : NewObjWidget.setChecked(OriginalWidget.isChecked())
           elif OriginalWidget.metaObject().className() == "MyComboBox" :
                  if zCible!= "tableroles" or i != 0 : NewObjWidget.setCurrentIndex(OriginalWidget.currentIndex())
           elif OriginalWidget.metaObject().className() == "MySpinBox" : NewObjWidget.setValue(OriginalWidget.value())                      
       
        if zRac == "MoveDown" :
            zObj.selectRow(rowcible)
            zObj.removeRow(row)
        if zCible == "tableroles" : self.CheckTable(zObj)          
        if self.objectName() == "DialogMetaData" : self.ShowWarning = True
        RenameAllWidgets(self, zObj)

        if zCible == "tableechelles" and self.objectName() == "DialogMetaData" : self.tabWidget.setCurrentIndex(4) 

def RenameAllWidgets(self, zObj):
    for zRow in range(zObj.rowCount()):
        for zCol in range(zObj.columnCount()):
            ObjWidget = zObj.cellWidget(zRow, zCol)
            zName = ObjWidget.accessibleName()
            if CountCaractere(zName, "_", False, False)==2 :
               zName = zName.split("_")
               zFullNameWidget = "%s_%s_%s" % (zName[0], zName[1], zRow)
            elif CountCaractere(zName, "_", False, False)==3 :
               zName = zName.split("_") 
               zFullNameWidget = "%s_%s_%s_%s" % (zName[0], zName[1], zRow, zCol)
            else : zFullNameWidget = zName   
            ObjWidget.setObjectName(zFullNameWidget) 
            ObjWidget.setAccessibleName(zFullNameWidget)
    countItems(self, zObj.accessibleName(), zObj)


def callInitSizeCols(self): 
      nameObj = self.sender().objectName().split("_")[2]
      zObj = self.findChild(MyTableWidget, nameObj)
      if DicoHasKey(self.zTablesWidget, nameObj):
         zDim = self.zTablesWidget[nameObj][0]
         initSizeCols(self, zObj, zDim)

         
def LoadListOfValues(self):
    if self.sender().accessibleName() == "" : return
    zNameObjRac = self.sender().accessibleName().split("_")[0]
    zRowCombo = int(self.sender().accessibleName().split("_")[2])
    zIndexThesaurus = self.sender().currentIndex()

    zObj = self.findChild(MyTableWidget, zNameObjRac)
    if zObj != None :
        zObjWidget = zObj.cellWidget(zRowCombo, 1)
        if zObjWidget :
           zObjWidget.clear()
           SizeW, zCols, iLine = LoadFile(self, zObjWidget, "", "file:200:thesaurus_%s_%s.csv:0:0" % (zIndexThesaurus, self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]), 1, None) 

def LoadGeoLocalisator(self): 
    if self.objectName() == "DialogMetaData" : self.DessCadre()
    zObj = self.findChild(MyTableWidget, "tableemprises")
    if zObj == None : return
    zRow = int(self.sender().objectName().split("_")[2])
    if zRow==-1 : zObj.selectRow(0)
    else : zObj.selectRow(zRow)
    zEmprise = []
    for j in range(zObj.columnCount()-1): zEmprise.append(zObj.cellWidget(zObj.currentRow(),j).value())
    ChangeButtonIcon(self, self.sender(),"voiractivate.png", 24, 24)

    zLang = self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]
    d = doUI.LoadDialogViewer(self, self.iface, "file:geolocalisator_%s.html" % (zLang), False, zEmprise, self.langueTR, self, None, "voir.png", True)
    ChangeButtonIcon(self, self.sender(),"voir.png", 18, 16)

def ChangeAccessibility(self, checked):
    if self.sender()==None or self.sender().objectName()=="": return
    else:
       zNameObj = "%s" % (self.sender().accessibleName())
       zObj = self.findChild(MyTableWidget, "tablemotsclefsf")
       if zNameObj.find("tablemotsclefsf_action_")!=-1: zIndexLine = int(zNameObj.split("_")[2])
       else: zIndexLine = GetIndex(zObj)

       for i in range(2,5):
           zItemEditLine = zObj.cellWidget(zIndexLine, i)
           try : zItemEditLine.setEnabled(checked)
           except : pass

def ChangePatternZipPostalCode(self): 
    if self.sender().accessibleName() == "" : return
    zNameObjRac = self.sender().accessibleName().split("_")[0]
    zRowCombo = int(self.sender().accessibleName().split("_")[2])
    zObj = self.findChild(MyTableWidget, zNameObjRac)
    if zObj != None :
        zObjWidget = zObj.cellWidget(zRowCombo, 4)
        if zObjWidget==None: return
        zKeyTarget = self.sender().currentText()
        if DicoHasKey(self.listCountriesCode, zKeyTarget):
            zObjWidget.setInputMask("")
            zObjWidget.setInputMask(self.listCountriesCode[zKeyTarget][1])
            zObjWidget.regex = QRegExp(r"%s" % (self.listCountriesCode[zKeyTarget][0]), Qt.CaseSensitive)
        else :
            zObjWidget.setInputMask("")
            zObjWidget.setInputMask("XXXxxxxxxx;X")
            zObjWidget.regex = QRegExp(r"(^+[a-zA-Z_0-9\s]{3,10}$)", Qt.CaseSensitive) 

def AfficheHelp(self):
    zChange = False
    ChangeButtonIcon(self, self.sender(),"infoactivate.png", 24, 24)

    if type(self.sender())== MyPushButton : zHelpFile = self.sender().accessibleDescription().replace("%s", self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]) 
    elif type(self.sender())== QAction :    zHelpFile = self.sender().toolTip().replace("%s", self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]) 
    
    if type(self.sender())== MyPushButton : d = doUI.LoadDialogViewer(self, self.iface,  zHelpFile, False, [], self.langueTR, self, self.sender(), "info.png", False)
    elif type(self.sender())== QAction : d = doUI.LoadDialogViewer(self, self.iface,  zHelpFile, False, [], self.langueTR, self, None, "info.png", False)
    self.childswindows.append(d)
    self.nb_window_childs.setText("%s" % (len(self.childswindows)))

   

def testURL(self):
    self.startMovie()
    
    zObj = self.findChild(MyTableWidget, "tablelocalisator")
    if zObj == None : return
    
    if zObj.currentRow()==-1: zObj.selectRow(0)
    zWidget = zObj.cellWidget(zObj.currentRow(),0)
  
    sites = [('%s' % (zWidget.text()), 'GET', {'Content-Type': 'application/xml'}, 'None')] 
    try : isValidURL = multi_get(self.movie, self.status_txt, sites, self.duration_timeout)[0][1]
    except : isValidURL = None

    if isValidURL != None :
       zTitle = QApplication.translate("QSphere", "Information" , None, QApplication.UnicodeUTF8) 
       zTextIsValid = QApplication.translate("QSphere", "Valid", None, QApplication.UnicodeUTF8)
       zPicto = QgsMessageBar.INFO
       zDuration = self.duration_info
    else :
       zTitle = QApplication.translate("QSphere", "Warning" , None, QApplication.UnicodeUTF8) 
       zTextIsValid = QApplication.translate("QSphere", "Not valid", None, QApplication.UnicodeUTF8)
       zPicto = QgsMessageBar.WARNING
       zDuration = self.duration_warning
    zMsg = "%s [%s %s]:<br>%s<br>%s." % (QApplication.translate("QSphere", "Current URL", None, QApplication.UnicodeUTF8), \
                                     QApplication.translate("QSphere", "row", None, QApplication.UnicodeUTF8), \
                                     zObj.currentRow(), zWidget.text(), zTextIsValid)
    SendMessage(self, zTitle, zMsg, zPicto, zDuration)
    self.stopMovie()

def RestoreComments(self): 
     if self.windowTitle() != self.racWindowTitle :
        fileName = self.windowTitle().replace(self.racWindowTitle, "")
        if fileName!="":
            config = ConfigParser.ConfigParser()
            config.read(fileName)
            
            zObj = self.findChild(MyTableWidget, "tabledico")
            if zObj == None : return
            
            zTest, zRows, zCols = AnaInfosObj(self, config, zObj, "tabledico")
            if zRows == 0 : return

            zBorne = zObj.rowCount() if zObj.rowCount()<= zRows else zRows
            
            for i in range(zBorne):
                try : zInfos = config.get("tabledico",'zRow_%s' % (i))
                except : zInfos = ""
                zClassWidgetValues = zInfos.split("|")
                if len(zClassWidgetValues)== zCols :
                   zWidget = zObj.cellWidget(i, 1)
                   zNameField =  zWidget.text() if zWidget != None else zObj.item(i, 1).text()
                   if zNameField == zClassWidgetValues[1]: 
                       zItemComment = QTableWidgetItem()
                       zItemComment.setText("%s" %(zClassWidgetValues[zCols-1]))
                       zObj.setItem(i,5,zItemComment)
                       zObj.item( i, 5 ).setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled)
                else : pass 

def goToLocalisator(self):
    isModal = False if self.objectName()=="DialogMetaData" else True
    zObj = self.findChild(MyTableWidget, "tablelocalisator")
    if zObj == None : return
    
    if zObj.currentRow()==-1: zObj.selectRow(0)
    zWidget = zObj.cellWidget(zObj.currentRow(),0)
    if zWidget.styleSheet()== "background-color:#AEEE00;" :
       d = doUI.LoadDialogViewer(self, self.iface,  zWidget.text(), False, [], self.langueTR, self, None, "urllocalisator.png", isModal)
       if not isModal :
           self.childswindows.append(d)
           self.nb_window_childs.setText("%s" % (len(self.childswindows)))
    else :
       zTitle = QApplication.translate("QSphere", "Warning" , None, QApplication.UnicodeUTF8) 
       zMsg = QApplication.translate("QSphere","The URL you entered is incomplete or invalid ! Please correct the line : ", None, QApplication.UnicodeUTF8)
       try : SendMessage(self, zTitle, "%s%s" % (zMsg, zObj.currentRow()), QgsMessageBar.WARNING, self.duration_warning)
       except : pass    

def makeTABWidgets(self, tab, zIndex, SizeLabelW, SizeLabelH, SizeWW, SizeWH):
        refSizeWW, refSizeWH = SizeWW, SizeWH
  
        if zIndex == 1 :
            Widgets = {"A_TITLE" : (0,0,"titletab1", 1, -1, (), True, False),
                       "B_Intitule" : (self.width()-530,0,"intitule", 2, 5, (), True, False),
                       "C_Resume" : (self.width()-530,100, "resume", 3, 0, (),  True, False),
                       "D_Type" : (self.width()-530, 0, "typedata", 4, 1, self.listTypeRessources, True, False),
                       "E_Localisator" : (self.width()-530, 15, "tablelocalisator", 5, 6, (), True, False),
                       "F_Identificator" : (300, 0, "identificator", 8, 5, (), True, False),
                       "G2_lang" : (0, 0, "tablelangues", 9, 3, "txt:", True, False),
                       "H_format" : (220, 12, "tableformats", 10, 6, (), True, True),
                       "I_carac" : (120, 0, "tablecarac", 14, 1, self.listCodecs, True, True) 
                      }
        elif zIndex == 2 :
             Widgets = {"A_TITLE" : (0, 0,"titletab2_1", 16, -1, (), True, False),
                        "B_Categorie" : (0, 180,"tablecategories", 15, 3, "file:300:categories_thematiques_%s.csv:1:0" % (self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]), True, False),
                        "C_TITLE" : (0, 0,"titletab2_2", 18, -1, (), True, False),
                        "D_MotsClefsO" : (self.width()-530, 11,"tablemotsclefso", 19, 6, (), True, False),
                        "E_MotsClefsF" : (self.width()-530, 18,"tablemotsclefsf", 22, 6, (), True, False)
                       }
   
        elif zIndex == 3 :
             Widgets = {"A_TITLE" : (0, 0, "titletab3_1", 29, -1, (), True, False),
                        "B_TITLE" : (0, 0,"subtitletab3_1", 30, -2, (), True, False),
                        "C_TableSCR" :(self.width()-530, 20,"tableemprises", 31, 6, (), True, False),
                        "D_TITLE" : (0, 0,"subtitletab3_2", 37, -2, (), True, False),
                        "E_TableScr" :(self.width()-905, 0,"tablescr", 38, 6, "EPSG:4258", True, False)
                       }

             zMap = QLabel(tab)
             zMap.setMinimumSize(QSize(360, 180))
             zMap.setMaximumSize(QSize(360, 180))
             zMap.setGeometry(QRect(415, 310, 360, 180))
             myDefPathIcon = getThemeIcon("world.png")
             carIcon = QImage(myDefPathIcon) 
             zMap.setPixmap(QPixmap.fromImage(carIcon))

             self.zCadre = MyLabel(zMap)
             self.zMireH = MyLabel(zMap)
             self.zMireW = MyLabel(zMap)

        elif zIndex == 4 : 
            Widgets = {"A_TITLE" : (0, 0,"titletab4_1", 42, -1, (), True, False),
                       "B_Etendue" : (160, 15,"tableetenduetemporelle", 43, 6, (), True, True),
                       "C_DatePub" : (120, 15, "tabledatepubdata", 46, 6, (), True, False),
                       "D_DateCre" : (0, 0, "datecredata", 49, 4, (), True, False),
                       "E_DateRev" : (0, 0, "daterevdata", 50, 4, (), True, False),
                       "F_SysRefTemp" : (0, 0, "sysreftemp", 51, 1, self.listTemporalSystem, True, False) 
                      }
        elif zIndex == 5 :
            Widgets = {"A_TITLE" : (0, 0,"titletab5_1", 53, -1, (), True, False),
                       "B_TITLE" : (0, 0,"subtitletab5_1", 54, -2, (), True, False),
                       "C_Genealogie" : (self.width()-530, 100,"genealogie", 55, 0, (),  True, False),
                       "D_TITLE" : (0, 0,"subtitletab5_2", 56, -2, (), True, False),
                       "E_Echelle" : (400, 160, "grouperesolutionscale", 57, 8, ((self.libelles[57][2]+" 1/","resolution_scale",25000.00),(QApplication.translate("QSphere","Equivalent scale in unit of measure ", None, QApplication.UnicodeUTF8),"resolution_pixel",2.0)), True, False),
                       "F_Coherence" : (self.width()-530, 0,"coherence", 58, 0, "{'TopologyLevelCode':'unknow', 'GeometricObjectTypeCode':'unknow'}", False, False),
                       "G_TITLE" : (0, 0,"subtitletab5_3", 59, -1, (), True, False),
                       "H_Conformite" : (self.width()-530, 15,"tablespecifications", 60, 6, (), True, False)
                      }


        elif zIndex == 6 :
            Widgets = {"A_TITLE" : (0, 0,"titletab6_1", 66, -1, (), True, False),
                       "B_droits" : (self.width()-530, self.height()-160,"groupedroits", 67, 8, \
                                     ((QApplication.translate("QSphere","No restriction for public access in INSPIRE", None, QApplication.UnicodeUTF8),"norestriction_droits",25000.00), \
                                      (QApplication.translate("QSphere","With restriction for public access in INSPIRE (Directive 2007/2/CE)", None, QApplication.UnicodeUTF8),"restriction_droits",2.0)), True, False), \
                       "C_Licence" : (self.width()-530, 40,"licence", 68, 0, "%s" % ((QApplication.translate("QSphere","Open Licence", None, QApplication.UnicodeUTF8))), True, False)
                      }
   
        elif zIndex == 7 : 
            Widgets = {"A_TITLE" : (0, 0,"titletab7_1", 70, -1, (), True, False),
                       "B_TableRole" :(self.width()-530, 40,"tableroles", 71, 6, (), True, False) 
                      }
            
        elif zIndex == 8 : 
            Widgets = {"A_TITLE" : (0, 0,"titletab8_1", 82, -1, (), True, False),
                       "B_DateMetadata" : (0, 0, "datemetada", 83, 4, (), True, False),
                       "C_LangMetadata" : (80, 0, "langmetada", 84, 1, self.languesDico, True, False) 
                      }
        elif zIndex == 9 :
            Widgets = {"A_TITLE" : (0, 0,"titletab9_1", 86,  -1, (), True, False),
                       "B_NameLayer" : (self.width()-530,0,"namelayer", 87, 5, (), False, False),
                       "C_TypeLayer" : (200,0,"typelayer", 88, 5, (), False, False),
                       "D_Metadata" : (self.width()-530, 150,"metadata", 89, 0, (), True, False),
                       "E_TableDico" :(self.width()-530, 45,"tabledico", 90, 6, (), True, False)
                       }
        else : return
        
        posX, posY = 200, 10
           
         
        zListitems = ShortDic(Widgets)
        for j in range(len(zListitems)):    
            key = zListitems[j]
            ListPropertiesObj = Widgets[key]
            SizeWW =  ListPropertiesObj[0] if ListPropertiesObj[0] != 0 else refSizeWW
            SizeWH =  ListPropertiesObj[1] if ListPropertiesObj[1] != 0 else refSizeWH
            nameObj, indexObj = ListPropertiesObj[2], ListPropertiesObj[3]
            typeObj, valObj   = ListPropertiesObj[4], ListPropertiesObj[5]
            isEnabled, isVertical = ListPropertiesObj[6], ListPropertiesObj[7]
            corPosY = makeWidget(self, tab, nameObj, typeObj, valObj, posX, posY, SizeWW, SizeWH, refSizeWH, isEnabled, isVertical, indexObj)
            if isVertical : posX+= SizeWW + 200
            else:
               posY+= 30 if corPosY == 0 else corPosY
               posX = 200
            

def makeWidget(self, tab, nameObj, typeObj, valObj, posX, posY, SizeW, SizeH, SizeRefH, zEnable, zVerticalObj, indexObj):
        lblObj = QLabel(tab)
        lblObj.setObjectName("Lbl%s" % (nameObj))
        lblObj.setAccessibleName("Lbl%s" % (nameObj))
        corPosY = 0

        tooltipObj = QApplication.translate("QSphere", self.libelles[indexObj][3], None, QApplication.UnicodeUTF8) if DicoHasKey(self.libelles, indexObj) else ""
        txtObj = QApplication.translate("QSphere", self.libelles[indexObj][2], None, QApplication.UnicodeUTF8) if DicoHasKey(self.libelles, indexObj) else ""
        zUrl = self.libelles[indexObj][5]

        if typeObj in( -1, -2) :
            lblObj.setGeometry(10,posY+5,self.width(),SizeH)
            if typeObj == -1 :
                lblObj.setAlignment(Qt.AlignLeft)
                lblObj.setStyleSheet("QLabel { background-color : #5D5D5D; color : white; }")
                txtObj = ">> %s" % (txtObj)
            else :
                lblObj.setAlignment(Qt.AlignCenter)
                lblObj.setStyleSheet("QLabel { background-color : #CCCCCC; color : black; }")
            lblObj.setText(txtObj)
            corPosY = SizeH+10 
        else :
            if nameObj=="tablelangues" : lblObj.setGeometry(posX-170,posY+5, 170, SizeH*4)
            else : lblObj.setGeometry(posX-170,posY+5, 170,self.SizeWH*2)
            lblObj.setAlignment(Qt.AlignRight)
            lblObj.setText(txtObj)
            lblObj.setWordWrap(True)
            lblObj.setAccessibleDescription(txtObj)
        
        if typeObj == 0:
            Obj = MyTextEdit(tab)
            Obj.initTextEdit(200, 25, 10, 50, nameObj, True, True, False, False, True)
            Obj.setWordWrapMode(QTextOption.WordWrap)
            zType = "%s" % (type(valObj))
            if zType == "<type 'str'>" : Obj.setText("%s" % (valObj))
            corPosY = SizeH+10   
                
        elif typeObj == 1:
            Obj = QComboBox(tab)
            itemtarget = 0 if nameObj != "sysreftemp" else 1
            if type(valObj) == str :
               if valObj.find("file:")!=-1 :
                   SizeW, zCols, iLine = LoadFile(self, Obj, nameObj, valObj, typeObj, None)
               else :
                   Obj.addItem("%s" % (valObj))
                   SizeW = int(SizeW / 2)
            elif type(valObj) == tuple :
               Obj.insertItems (0, valObj)
               SizeW = int(SizeW / 2)
            elif type(valObj) == dict :    
                myelts = ShortDic(valObj)
                if nameObj == "langmetada" : 
                    mylang = QLocale.languageToString(self.langue)
                    itemtarget = MakeListLangues(self, Obj, mylang)
            elif type(valObj) == list :
                if nameObj == "tablecarac" :
                    valObj.sort()
                    Obj.insertItems (0, valObj)
                    itemtarget = valObj.index("utf8")
            Obj.setCurrentIndex(itemtarget)

        
        elif typeObj == 3:
            self.tableModel = QStandardItemModel(self)
            Obj = QTableView(tab)
            if self.SizeWW == SizeW : SizeW =  self.width()-posX - 330
            iLine, zCols = 0, 1

            if type(valObj) == str :
                if valObj.startswith("file:"): 
                   SizeHOld = SizeH
                   SizeH, zCols, iLine = LoadFile(self, Obj, nameObj, valObj, typeObj, self.tableModel)
                   if SizeHOld != SizeRefH: SizeH = SizeHOld
                elif valObj.startswith("txt:"):
                   data_icons = os.path.dirname(__file__).replace("\\","/") +"/ressources/images/"
                   zCols, i = 2, 0
                   mylans = ShortDic(self.languesDico)
                   mylang = QLocale.languageToString( self.langue )
                   for elt in mylans :
                        if len(elt)==3 :
                            language_codeiso = elt
                            language_name = self.languesDico[elt]['french']
                            for j in range(zCols):
                                zIcon = QIcon(data_icons+language_codeiso+".png")
                                item = QStandardItem() if j == 0 else QStandardItem(zIcon, "")
                                zText = language_codeiso if j == 0 else language_name
                                item.setText(zText)
                                if j == 0 :
                                   item.setCheckable(True)
                                   item.setCheckState(Qt.Unchecked)
                                   if  nameObj == "tablelangues" and self.languesDico[elt]['english'] == mylang : item.setCheckState(Qt.Checked)
                                item.setEditable(False)    
                                self.tableModel.setItem(i,j,item)
                            i+= 1
                SizeH = SizeH + 70

   
            elif type(valObj) == list :
                #This case not active in current version - keep and save
                zCols = 2
                for i in range(len(valObj)):
                    language = valObj[i]
                    language_name = QLocale.languageToString( language ) 
                    language_codeiso = QLocale( language ).name().split("_")[0]
                    language_index_target = QLocale.languageToString( language ) 
           
                    for j in range(zCols):
                        item = QStandardItem()
                        zText = language_codeiso if j == 0 else language_name
                        if j == 0 :
                            item.setCheckable(True)
                            item.setCheckState(Qt.Unchecked)
                            if self.languageIndex == language_index_target: item.setCheckState(Qt.Checked)
                        item.setEditable(False)    
                        item.setText(zText)
                        self.tableModel.setItem(i,j,item)
                SizeH = SizeH + 70
                
            else :
                #This case not active in current version - keep and save
                for i in range(len(valObj)):
                    if type(valObj[i]) == str :
                        item = QStandardItem()
                        item.setCheckable(True)
                        item.setCheckState(Qt.Unchecked)
                        zText = "%s" % (valObj[i][j])
                        item.setText(zText)
                        item.setEditable(False)
                        self.tableModel.setItem(iLine,0,item)
                        
                    elif type(valObj[i]) == tuple :
                        zCols = len(valObj[i])
                        for j in range(len(valObj[i])):
                            item = QStandardItem() 
                            zText = "%s" % (valObj[i][j])
                            item.setText(zText)                            
                            if j == 0 :
                                item.setCheckable(True)
                                item.setCheckState(Qt.Unchecked)
                                #This case not active in current version - keep and save
                                #old sample flag language - keep and save
                                if nameObj == "tablelangues" and item.text().startswith(self.langueTR): item.setCheckState(Qt.Checked)
                            item.setEditable(False)    
                            self.tableModel.setItem(iLine,j,item)
                      
                    iLine+= 1
                SizeH = SizeH * (iLine+1) + 30

            for i in range(zCols): Obj.setColumnWidth(i, int(SizeW/zCols)-10)
            Obj.horizontalHeader().setDefaultSectionSize(int(SizeW/zCols)-10)
            if nameObj == "tabledroits" : Obj.verticalHeader().setDefaultSectionSize(60)
            Obj.horizontalHeader().setVisible(False)
            Obj.setDragDropMode(QAbstractItemView.DragOnly)
            Obj.verticalHeader().setVisible(False) 
            Obj.setModel(self.tableModel)

            if nameObj=="tablelangues": Obj.model().itemChanged.connect(self.majItemLangues) 
            
            corPosY =  SizeH + 10


        elif typeObj == 4:    
            Obj = QCalendarWidget(tab)
            Obj.setStyleSheet("""QMenu { font-size:12px; width: 150px; left: 16px; background-color:qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #5D5D5D);}"""
                              """QToolButton {icon-size: 20px, 20px;background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #5D5D5D); height: 20px; width: 200px;}"""
                              """QAbstractItemView {selection-background-color: rgb(255, 174, 0);}"""
                              """QToolButton::menu-arrow {}"""
                              """QToolButton::menu-button {}"""
                              """QToolButton::menu-indicator{width: 5px;}"""
                              """QToolButton::menu-indicator:pressed,"""
                              """QToolButton::menu-indicator:open{top:10px; left: 20px;}"""
                              """QListView {background-color:white;}"""
                              """subcontrol-position: top right; width:50px; border-image: url(icons:arrow_up_n.png);}"""
                              """border-width: 1px; width:25px;}"""
                              )
       

            Obj.setGridVisible(True)
            Obj.showToday()
            Obj.selectionChanged.connect(self.FixeToolTipCalendar)
            tooltipObj = MakeToolTipCalendar(self, Obj)
            SizeH = 170 
            corPosY = SizeH + 10 
            SizeW = SizeW + 35

        elif typeObj in(5, 50):
            if typeObj == 5 : Obj = QLineEdit(tab)
            elif typeObj == 50 :
                 Obj = MyWidgetLineEdit(tab)
                 zText = valObj.split(":")
                 zType = int(zText[0])
                 Obj.initType(zType)
                 if zType == 1: Obj.setInputMask("9999-99-99 9999-99-99;X")
                 elif zType == 2: Obj.setInputMask("99999;X")
                 elif zType == 5: Obj.setInputMask("9999-99-99;X")
                 valObj = zText[1]
                 Obj.setAlignment(Qt.AlignCenter)
                 Obj.textChanged.connect(self.VerifExpReg)
            Obj.setText("") if nameObj != "identificator" else Obj.setText("%s-%s-%s" % (self.langueTR.upper(), datetime.datetime.now().year, getRandowId(self)))


        elif typeObj == 6 : 
            if DicoHasKey(self.zTablesWidget, nameObj):
                Obj = TableWidgetMaker(self, nameObj, tab, True)
                if nameObj == "tableemprises" : Obj.currentCellChanged.connect(self.doDessCadre) 
                SizeH = (SizeH * 7) + 30
                corPosY = posY + SizeH if nameObj not in("tabledico", "tableformats", "tablelocalisator", "tableemprises", "tablemotsclefso", "tablemotsclefsf", "tableroles") else SizeH + 10

        elif typeObj == 8:
            Obj = QGroupBox(tab)
            yypos = 5
            for i in range(len(valObj)):
                zProps = valObj[i]
                zRadioButton = QRadioButton(Obj)
                zRadioButton.setObjectName(zProps[1])
                zRadioButton.setAccessibleName(zProps[1])
                zRadioButton.setText("%s" % (zProps[0]))
                if nameObj == "grouperesolutionscale" : zToolTip = "%s" % (zProps[2])
                else : zToolTip = QApplication.translate("QSphere","Constraints", None, QApplication.UnicodeUTF8)
                zRadioButton.setToolTip(zToolTip)
                zRadioButton.setGeometry(QRect(5,yypos,540,25))
                if i == 0 :  zRadioButton.setChecked(True)
                if nameObj == "grouperesolutionscale" : zRadioButton.clicked.connect(self.ChangeOptionScale) 
                elif nameObj == "groupedroits" : zRadioButton.toggled.connect(self.ChangeOptionRights) 
                yypos+= 25
                
            if nameObj == "grouperesolutionscale": 
               zSubObj = MyTableWidget(1,1, Obj)
               zSubObj.refDialog = self
               zSubObj.setObjectName("tableechelles")
               zSubObj.setAccessibleName("tableechelles")
               zSubObj.setStyleSheet("""QTableWidget {selection-background-color: rgb(50, 125, 180); }""")
               zSubObj.horizontalHeader().setVisible(False)
               zSubObj.verticalHeader().setVisible(False)
               zSubObj.setGeometry(QRect(240,0,140,SizeH-10))
               AddLineWidget(self, zSubObj, 0,  0, 4, 0, -1)
            elif nameObj == "groupedroits":
               self.tableModel = QStandardItemModel(self)
               zSubObj = QTableView(Obj)
               zNameTable = "table%s" % (nameObj)
               zSubObj.setObjectName(zNameTable)
               zSubObj.setAccessibleName(zNameTable)
               iLine, zCols = 0, 1
               SizezSubObjH, zCols, iLine = LoadFile(self, zSubObj, zNameTable, "file:280:contraintes_%s.csv:1:0" % (self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]), 3, self.tableModel)
               zSubObj.setGeometry(QRect(10,60, (SizeW-20), SizeH-70))
               if zCols  == 0 : return SizeH + 10
               
               for i in range(zCols): zSubObj.setColumnWidth(i, int((SizeW-20)/zCols)-10)
               zSubObj.horizontalHeader().setDefaultSectionSize(int((SizeW-20)/zCols)-10)
               zSubObj.verticalHeader().setDefaultSectionSize(60)
               zSubObj.horizontalHeader().setVisible(False) 
               zSubObj.verticalHeader().setVisible(False) 
               zSubObj.setModel(self.tableModel)
               zSubObj.setEnabled(False)

            if nameObj == "grouperesolutionscale": 
                zChildInfo = QComboBox(Obj)
                zChildInfo.addItems(self.ListUnitsMesure) 
                zChildInfo.setGeometry(QRect(100,60, 80,25))
                zChildInfo.setObjectName("unitsofscale")
                zChildInfo.setAccessibleName("unitsofscale")
                zChildInfo.setEnabled(False)
            corPosY = SizeH + 10

      
        if typeObj == 11:
           Obj = QCommandLinkButton(tab)
           Obj.setText(tooltipObj)
           Obj.setToolTip(zUrl)
           Obj.clicked.connect(self.AfficheRessources)
           SizeW = 1.5 * SizeW
           SizeH = 1.5 * SizeH

        if typeObj != -1 and  typeObj != -2 :
            if txtObj == "" and typeObj != 11:
               posX = 20
               SizeW+= 180

            Obj.setGeometry(QRect(posX,posY,SizeW, SizeH))
            if typeObj != 11 : Obj.setToolTip(tooltipObj)
            Obj.setObjectName(nameObj)
            Obj.setAccessibleName(nameObj)
            Obj.setAccessibleDescription("Informations blocs XML INSPIRE")
            Obj.setEnabled(zEnable)

            zBut = MyPushButton(tab)
            zIcon = getThemeIcon(self.libelles[100][4]) 
            zToolTip = QApplication.translate("QSphere", self.libelles[100][3], None, QApplication.UnicodeUTF8)
            zBut.initPushButton(24, 24, (posX + SizeW + 5), posY, "help_%s" % (nameObj), "", zToolTip, True, zIcon, 24, 24, True)
            zBut.setAccessibleDescription(zUrl)
            zBut.clicked.connect(self.AfficheHelp)

            if typeObj in (6,8) and nameObj != "groupedroits" :
                
                zIcon = getThemeIcon(self.libelles[101][4]) 
                zToolTip = QApplication.translate("QSphere", self.libelles[101][3], None, QApplication.UnicodeUTF8)
                zBut = MyPushButton(tab) 
                zBut.initPushButton(40, 24, (posX + SizeW-5), posY + 30, "ActionsButton_%s" % (nameObj), "", zToolTip, True, zIcon, 40, 24, True)                

                contextMnuMDDActions(self, tab, Obj, nameObj, typeObj, zBut, zUrl)

                if typeObj != 8 and not nameObj in ("tablescr", "tableetenduetemporelle", "tabledatepubdata", "tabledico") :

                   zIcon = getThemeIcon(self.libelles[102][4]) 
                   zToolTip = QApplication.translate("QSphere", self.libelles[102][3], None, QApplication.UnicodeUTF8)
                   zBut = MyPushButton(tab) 
                   zBut.initPushButton(40, 24, (posX + SizeW-5), posY + 60, "OpenWizard_%s_%s" % (typeObj, nameObj), "", zToolTip, True, zIcon, 40, 24, True)                

                   contextMnuMDDWizards(self, tab, Obj, nameObj, typeObj, zBut, zUrl)
                   
                   if nameObj == "tablemotsclefsf" :
                       zBut = MyPushButton(tab)
                       zIcon = getThemeIcon(self.libelles[103][4]) 
                       zToolTip = QApplication.translate("QSphere", self.libelles[103][3], None, QApplication.UnicodeUTF8) 
                       zBut.initPushButton(24, 24, (posX + SizeW + 5), posY + 90, "OpenLusTRE_%s_%s" % (typeObj, nameObj), "", zToolTip, True, zIcon, 24, 24, True) 
                       zBut.clicked.connect(self.OpenLusTRE)
                       
               
            if nameObj == "coherence" and typeObj == 0 :
               zBut = MyButton(tab)
               zToolTip = QApplication.translate("QSphere","Call the topology conformity dialog box", None, QApplication.UnicodeUTF8) 
               zBut.initButton(35, 25, (posX + SizeW - 35), posY, "topo_"+nameObj, "...", zToolTip, True, True) 
               zBut.clicked.connect(self.CallSelectorConformityInfos)

        font = QFont()
        font.setPointSize(8) 
        font.setWeight(8)
        try : Obj.setFont(font)
        except : pass
                
        if zVerticalObj : corPosY = 0
        if nameObj == "tableemprises" : Obj.setToolTip("0")
        return corPosY

def TableWidgetMaker(zDialog, nameObj, tab, zMakeLine):
    zDim = zDialog.zTablesWidget[nameObj][0]
    zListHeaders, i = [], 0
    cKey = "%s_c%s" % (nameObj, i)

    for key, values in zDialog.libelles.iteritems() :
        if cKey in values :
            zListHeaders.append(QApplication.translate("QSphere", values[2], None, QApplication.UnicodeUTF8))
            i+= 1
            cKey = "%s_c%s" % (nameObj, i)

    zCols = 1 if type(zDim)== int else len(zDim)
    Obj = MyTableWidget(0, zCols, tab)
    Obj.refDialog = zDialog
    Obj.setObjectName(nameObj)
    Obj.setAccessibleName(nameObj)
    Obj.setStyleSheet("""QTableWidget {selection-background-color: rgb(50, 125, 180); }""")

    initSizeCols(zDialog, Obj, zDim)

    if zMakeLine : MakeLine(zDialog, Obj, False, True,-1, True) 
    if zListHeaders!= []: Obj.setHorizontalHeaderLabels(zListHeaders)
    Obj.verticalHeader().setVisible(False)
    Obj.setTabKeyNavigation(False)

    return Obj

def contextMnuMDDWizards(self, tab, Obj, nameObj, typeObj, zButtonAction, zUrl):
    contextMnu_MDDWizards = QMenu()

    menuIcon = getThemeIcon("wizards_tab.png")
    zText = QApplication.translate("QSphere","Call the wizard Tables ...", None, QApplication.UnicodeUTF8) 
    zAction = QAction(QIcon(menuIcon), zText, self)
    zAction.setObjectName("OpenViewer_%s" % (nameObj))
    contextMnu_MDDWizards.addAction(zAction)
    self.restore_tabledico = zAction
    zAction.triggered.connect(self.OpenViewerTable)

    menuIcon = getThemeIcon("wizards_form.png")
    zText = QApplication.translate("QSphere","Call the form wizard Tables ...", None, QApplication.UnicodeUTF8) 
    zAction = QAction(QIcon(menuIcon), zText, self)
    zAction.setObjectName("OpenForm_%s" % (nameObj))
    contextMnu_MDDWizards.addAction(zAction)
    self.restore_tabledico = zAction
    zAction.triggered.connect(self.OpenFormTable)

    zButtonAction.setMenu(contextMnu_MDDWizards)
           

def contextMnuMDDActions(self, tab, Obj, nameObj, typeObj, zButtonAction, zUrl):

    contextMnu_MDDActions = QMenu()

    if typeObj==6 and nameObj=="tabledico" :
           contextMnu_MDDActions.addSeparator() 
           
           menuIcon = getThemeIcon("attributrestore.png")
           zText = QApplication.translate("QSphere","Reload the comments from Project", None, QApplication.UnicodeUTF8) 
           zAction = QAction(QIcon(menuIcon), zText, self)
           zAction.setObjectName("restore_%s" % (nameObj))
           zAction.setEnabled(False)
           contextMnu_MDDActions.addAction(zAction)
           self.restore_tabledico = zAction
           zAction.triggered.connect(self.RestoreComments)

           contextMnu_MDDActions.addSeparator()
           
           menuIcon = getThemeIcon("tab_sizecol.png")
           zText = QApplication.translate("QSphere","Original size for the columns", None, QApplication.UnicodeUTF8)
           zAction = QAction(QIcon(menuIcon), zText, self)
           zAction.setObjectName("Size_%s_%s" % (typeObj, nameObj))
           contextMnu_MDDActions.addAction(zAction)
           zAction.triggered.connect(self.callInitSizeCols)

    if typeObj in(6, 8, 9) and not nameObj in ("tabledico", "groupedroits") :

       contextMnu_MDDActions.addSeparator()

       menuIcon = getThemeIcon("tab_addline.png")
       zText = QApplication.translate("QSphere","Add a Line", None, QApplication.UnicodeUTF8)
       if self.objectName() not  in ("ViewerTableWidget", "formTableWidget") : zText = "%s%s" % (zText, "F11".rjust(60-len(zText)))
       zAction = QAction(QIcon(menuIcon), zText, self)
       zAction.setObjectName("Ajouter_%s_%s" % (typeObj, nameObj))
       if self.objectName()  in ("ViewerTableWidget", "formTableWidget") : zAction.setShortcut(QKeySequence("F11"))
       contextMnu_MDDActions.addAction(zAction)
       zAction.triggered.connect(self.AddLine)

       menuIcon = getThemeIcon("tab_addaftercurrentline.png")
       zText = QApplication.translate("QSphere","Add a Line after the current line", None, QApplication.UnicodeUTF8)
       zAction = QAction(QIcon(menuIcon), zText, self)
       zAction.setObjectName("AjouterAfter_%s_%s" % (typeObj, nameObj))
       if self.objectName()in ("ViewerTableWidget", "formTableWidget") : zAction.setShortcut(QKeySequence("Ctrl++"))
       contextMnu_MDDActions.addAction(zAction)
       zAction.triggered.connect(self.AddLine)

       menuIcon = getThemeIcon("tab_clonecurrentline.png")
       zText = QApplication.translate("QSphere","Duplicate the current line", None, QApplication.UnicodeUTF8)
       zAction = QAction(QIcon(menuIcon), zText, self)
       zAction.setObjectName("Clone_%s_%s" % (typeObj, nameObj))
       if self.objectName() in ("ViewerTableWidget", "formTableWidget") : zAction.setShortcut(QKeySequence("Ctrl+C"))
       contextMnu_MDDActions.addAction(zAction)
       zAction.triggered.connect(self.MoveLineDown)

       contextMnu_MDDActions.addSeparator()

       menuIcon = getThemeIcon("tab_delcurrentline.png")
       zText = QApplication.translate("QSphere","Delete the current line", None, QApplication.UnicodeUTF8)
       zAction = QAction(QIcon(menuIcon), zText, self)
       zAction.setObjectName("Effacerc_%s_%s" % (typeObj, nameObj))
       if self.objectName() in ("ViewerTableWidget", "formTableWidget") : zAction.setShortcut(QKeySequence("Ctrl+X"))
       contextMnu_MDDActions.addAction(zAction)
       zAction.triggered.connect(self.DelCurrentLine)

       menuIcon = getThemeIcon("tab_delline.png")
       zText = QApplication.translate("QSphere","Delete the last line", None, QApplication.UnicodeUTF8)
       if self.objectName() not  in ("ViewerTableWidget", "formTableWidget") : zText = "%s%s" % (zText, "F12".rjust(60-len(zText)))
       zAction = QAction(QIcon(menuIcon), zText, self)
       zAction.setObjectName("Effacer_%s_%s" % (typeObj, nameObj))
       if self.objectName() in ("ViewerTableWidget", "formTableWidget") : zAction.setShortcut(QKeySequence("F12"))
       contextMnu_MDDActions.addAction(zAction)
       zAction.triggered.connect(self.DelLine)

       contextMnu_MDDActions.addSeparator()

       menuIcon = getThemeIcon("tab_linemoveup.png")
       zText = QApplication.translate("QSphere","Move the line up", None, QApplication.UnicodeUTF8)
       zAction = QAction(QIcon(menuIcon), zText, self)
       zAction.setObjectName("MoveUp_%s_%s" % (typeObj, nameObj))
       if self.objectName() in ("ViewerTableWidget", "formTableWidget") : zAction.setShortcut(QKeySequence.MoveToPreviousPage)
       contextMnu_MDDActions.addAction(zAction)
       zAction.triggered.connect(self.MoveLineUp)

       menuIcon = getThemeIcon("tab_linemovedown.png")
       zText = QApplication.translate("QSphere","Move the line down", None, QApplication.UnicodeUTF8)
       zAction = QAction(QIcon(menuIcon), zText, self)
       zAction.setObjectName("MoveDown_%s_%s" % (typeObj, nameObj))
       if self.objectName() in ("ViewerTableWidget", "formTableWidget") : zAction.setShortcut(QKeySequence.MoveToNextPage)
       contextMnu_MDDActions.addAction(zAction)
       zAction.triggered.connect(self.MoveLineDown)

       if self.objectName() == "DialogMetaData" :
           
           contextMnu_MDDActions.addSeparator()

           if type(Obj) != QGroupBox :    
               menuIcon = getThemeIcon("tab_sizecol.png")
               zText = QApplication.translate("QSphere","Original size for the columns", None, QApplication.UnicodeUTF8)
               zAction = QAction(QIcon(menuIcon), zText, self)
               zAction.setObjectName("Size_%s_%s" % (typeObj, nameObj))
               contextMnu_MDDActions.addAction(zAction)
               zAction.triggered.connect(self.callInitSizeCols)

       if nameObj == "tablelocalisator" :
           contextMnu_MDDActions.addSeparator() 
           
           menuIcon = getThemeIcon("urlvalid.png")
           zText = QApplication.translate("QSphere","Test the URL", None, QApplication.UnicodeUTF8) 
           zAction = QAction(QIcon(menuIcon), zText, self)
           zAction.setObjectName("testURL_%s_%s" % (typeObj, nameObj))
           zAction.setToolTip(zUrl)
           contextMnu_MDDActions.addAction(zAction)
           zAction.triggered.connect(self.testURL)

           menuIcon = getThemeIcon("urllocalisator.png")
           zText = QApplication.translate("QSphere","View the localisator", None, QApplication.UnicodeUTF8)
           zAction = QAction(QIcon(menuIcon), zText, self)
           zAction.setObjectName("URL_%s_%s" % (typeObj, nameObj))
           zAction.setToolTip(zUrl)
           contextMnu_MDDActions.addAction(zAction)
           zAction.triggered.connect(self.goToLocalisator)
       
    zButtonAction.setMenu(contextMnu_MDDActions)

    if typeObj == 6 : Obj.fixeMenu(contextMnu_MDDActions)
    elif typeObj==8 and nameObj=="grouperesolutionscale" :
        zSubObj = getWidget(tab, "tableechelles")
        if zSubObj : zSubObj.fixeMenu(contextMnu_MDDActions)
    


#========================================================
# FUNCTIONS CONSTRUCT LIST LAYERS / EXTRACT INFOS LAYERS
#========================================================
def MakeListLayer(self, zModel, zCombo):
   nLayers = self.iface.legendInterface().layers()
   self.Tableaux.clear()
   zCombo.clear()
   zDefaultValue = QApplication.translate("QSphere","No layer", None, QApplication.UnicodeUTF8)
   zModel.appendRow([QStandardItem(zDefaultValue), QStandardItem(0)])
   self.Tableaux[0], maxdim = [], len(zDefaultValue)
   for i in range(0, len(nLayers)):
       zLayer = nLayers[i]
       if zLayer.isValid():
          if not DicoHasKey(self.Tableaux, zLayer.id()): dim = AppendItemInModel(self, zModel, zLayer)
          maxdim = max(maxdim, dim)
   zCombo.setModelColumn(0)
   zCombo.show()
   zCombo.setCurrentIndex(-1)
   return maxdim

def AppendItemInModel(self, zModel, zLayer):
   zModel.appendRow([QStandardItem(zLayer.name()), QStandardItem(zLayer.id())])
   self.Tableaux[zLayer.id()] = []
   return len(zLayer.name())

def GetzLayerCombo(self, zCombo, zInLegend):
   zLayer = None
   if zCombo.currentIndex()!= -1 :
       zText = zCombo.model().item(zCombo.currentIndex(),1).text()
       if zInLegend : tLayers = self.iface.legendInterface().layers()
       nLayers = len(tLayers) if zInLegend  else  self.iface.mapCanvas().layerCount()
       for i in range(0, nLayers):
           zLayer = tLayers[i] if zInLegend else self.iface.mapCanvas().layer(i)
           if str(zLayer.id()) == str(zText): break
   return zLayer

def DefzTransform(zLayer, zProj4Dest):
    destinationCRS = QgsCoordinateReferenceSystem()
    destinationCRS.createFromId(zProj4Dest)
    sourceCRS = zLayer.crs()
    zTransform = QgsCoordinateTransform()
    zTransform.setSourceCrs(sourceCRS)
    zTransform.setDestCRS(destinationCRS)
    return zTransform


#======================================
# TEST GENERIC VIEWER FOR QTableWidget
#======================================
class TableWidgetDialog(QDialog):
      def  __init__(self, TableWidget, parent):
         QDialog.__init__(self)
         self.setWindowTitle(QApplication.translate("QSphere","Wizard Table Widget Composer", None, QApplication.UnicodeUTF8))
         self._W, self._H = 500, 300
         self.setMinimumSize(QSize(self._W,self._H))
         self.setWindowFlags(Qt.WindowMaximizeButtonHint)
         self.setAccessibleName("ViewerTableWidget")
         self.setObjectName("ViewerTableWidget")

         self.groupStyleSheet = """QGroupBox {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E0E0E0, stop: 1 #FFFFFF);""" \
                                   """border: 2px solid gray; border-radius: 5px; margin-top: 1ex; })"""       

         self.parent = parent
         self.ShowWarning = self.parent.ShowWarning
         
         MakeWindowIcon(self, "wizards_tab.png")
         MakePropertiesForWindow(self, self.parent)
         
         self.iface = self.parent.iface
         self.originalW, self.originalH, self.originalX, self.originalY = TableWidget.width(), TableWidget.height(), TableWidget.x(), TableWidget.y()

         
         self.ParamsLineWidget = self.parent.ParamsLineWidget
         self.zTablesWidget = self.parent.zTablesWidget
         self.duration_warning = self.parent.duration_warning
         self.duration_info = self.parent.duration_info
         self.duration_timeout = self.parent.duration_timeout
         self.ListOfThesaurus = self.parent.ListOfThesaurus
         self.DateListOfThesaurus = self.parent.DateListOfThesaurus
         self.ListTypeDates = self.parent.ListTypeDates
         self.ListDegres = self.parent.ListDegres

         zIcon = getThemeIcon("actions.png")
         zToolTip = QApplication.translate("QSphere","Actions for the metadata...", None, QApplication.UnicodeUTF8)
         self.buttonActions = MyPushButton(self) 
         self.buttonActions.initPushButton(40, 24, 0, 0, "ActionsButton_%s" % (TableWidget.accessibleName()), "", zToolTip, True, zIcon, 40, 24, True)

         if TableWidget.accessibleName()!= "tableemprises":
             self.OpenNavigatorButton = MyPushButton(self)
             self.OpenNavigatorButton.initPushButton(24, 24, 5, 5, "OpenNavigatorButton", "", QApplication.translate("QSphere","Web navigator ...", None, QApplication.UnicodeUTF8), True, getThemeIcon("navigatorweb.png"), 24, 24, True)


         self.labelTableWidget = QLabel(self)
         self.labelTableWidget.setAccessibleName("Lbl%s" % (TableWidget.accessibleName()))
         self.labelTableWidget.setObjectName("Lbl%s" % (TableWidget.accessibleName()))

         self.tableWidget = self.MakeCopy(TableWidget)
         self.fromTableWidget = TableWidget
         self.tableWidget.setStyleSheet("""QTableWidget {selection-background-color: rgb(50, 125, 180); }""")

         if DicoHasKey(self.zTablesWidget, self.tableWidget.accessibleName()):
             self.dims = self.zTablesWidget[self.tableWidget.accessibleName()][0]

         self.status_txt = QLabel(self)
         self.movie = QMovie(getThemeIcon("sablier.gif"))
         self.status_txt.setMovie(self.movie)
         self.status_txt.setLayout(QHBoxLayout())
         self.status_txt.layout().addWidget(QLabel(''))
         self.status_txt.setVisible(False)

         self.barInfo = QgsMessageBar(self)
         self.barInfo.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )

         self.groupBoxActionsMeta = QGroupBox(self)
         self.groupBoxActionsMeta.setStyleSheet(self.groupStyleSheet)

         zToolTip = QApplication.translate("QSphere","Move down", None, QApplication.UnicodeUTF8)
         self.MoveDown = MyPushButton(self.groupBoxActionsMeta) 
         self.MoveDown.initPushButton(24, 24, 5, 5, "MoveDown", "", zToolTip, True, getThemeIcon("movedown.png"), 24, 24, True)
         self.MoveDown.setAutoRepeat(True)
         self.MoveDown.setShortcut(QKeySequence.MoveToNextLine)

         self.labelPosition = QLabel(self.groupBoxActionsMeta)
         self.labelPosition.setGeometry(40, 5, 100, 25)
         self.labelPosition.setText("%s :" % (QApplication.translate("QSphere","Current contact", None, QApplication.UnicodeUTF8)))
        
         self.CurrentItem = QLabel(self.groupBoxActionsMeta)
         self.CurrentItem.setGeometry(140, 5, 40, 25)

         zToolTip = QApplication.translate("QSphere","Move up", None, QApplication.UnicodeUTF8)
         self.MoveUp = MyPushButton(self.groupBoxActionsMeta) 
         self.MoveUp.initPushButton(24, 24, 180, 5, "MoveUp", "", zToolTip, True, getThemeIcon("moveup.png"), 24, 24, True)
         self.MoveUp.setAutoRepeat(True)
         self.MoveUp.setShortcut(QKeySequence.MoveToPreviousLine)
                        
         self.SaveButton = MyPushButton(self)
         self.SaveButton.initPushButton(100, 24, 5, 5, "SaveButton", "", QApplication.translate("QSphere", "Save", None, QApplication.UnicodeUTF8), True, getThemeIcon("sendtotable.png"), 100, 24, False)
         self.SaveButton.setShortcut(QKeySequence("Ctrl+S"))

         self.CloseButton = QPushButton(self)
         self.CloseButton.setObjectName("CloseButton")
         self.CloseButton.setText(QApplication.translate("QSphere", "Close", None, QApplication.UnicodeUTF8))

         zIcon = getThemeIcon("qspherehelp.png")
         self.HelpButton = MyPushButton(self) 
         self.HelpButton.initPushButton(48, 48, -50, -50, "HelpButton", "", "", True, zIcon, 48, 48, True)
         self.HelpButton.setShortcut(QKeySequence("F1"))

         self.MoveUp.clicked.connect(self.MoveSelUp)
         self.MoveDown.clicked.connect(self.MoveSelDown)
         self.SaveButton.clicked.connect(self.SaveTable)
         self.CloseButton.clicked.connect(self.close)
         self.HelpButton.clicked.connect(self.clickHelp)
         
         if TableWidget.accessibleName()!= "tableemprises": self.OpenNavigatorButton.clicked.connect(self.OpenNavigator) 
         
         self.tableWidget.selectRow(self.tableWidget.currentRow()+1)
         self.FixeCurrentItem()

      def OpenNavigator(self):
          d = doUI.LoadDialogViewer(self, self.iface, "#blank", False, [], self.langueTR, self, None, "navigatorweb.png", True)

      def clickHelp(self): makeHelp(self)
 
      def FixeCurrentItem(self):
          self.CurrentItem.setText("%s / %s" % ((self.tableWidget.currentRow()+1), self.tableWidget.rowCount()))
          self.groupBoxActionsMeta.setEnabled(False) if self.tableWidget.rowCount()== 0 else self.groupBoxActionsMeta.setEnabled(True)
          
      def MoveSelUp(self):
          if self.tableWidget.rowCount()== 0 : return
          if self.tableWidget.currentRow() > 0 : self.tableWidget.selectRow(self.tableWidget.currentRow()-1)
          self.FixeCurrentItem()

      def MoveSelDown(self):
          if self.tableWidget.rowCount()== 0 : return
          if self.tableWidget.currentRow() <  (self.tableWidget.rowCount()-1) : self.tableWidget.selectRow(self.tableWidget.currentRow()+1)
          self.FixeCurrentItem()


      def CheckInfosRoles(self): CheckInfosRoles(self)
      def startMovie(self):
            self.status_txt.setVisible(True)
            self.movie.start()
            self.status_txt.repaint()

      def stopMovie(self):
            self.movie.stop()
            self.status_txt.setVisible(False)
          
      def AddLine(self):
          AddLine(self)
          self.FixeCurrentItem()
      def testURL(self): testURL(self)
      def goToLocalisator(self): goToLocalisator(self)
      def AfficheHelp(self): AfficheHelp(self)
      def MoveLineUp(self):
          MoveLineUpProcess(self, "%s" % (self.sender().objectName()))
          self.FixeCurrentItem()
      def MoveLineDown(self):
          MoveLineDownProcess(self, "%s" % (self.sender().objectName()))
          self.FixeCurrentItem()
      def DelLine(self):
          DelLineProcess(self, "%s" % (self.sender().objectName()), True)
          self.FixeCurrentItem()
      def DelCurrentLine(self):
          DelLineProcess(self, "%s" % (self.sender().objectName()), False)
          self.FixeCurrentItem()
      def callInitSizeCols(self): callInitSizeCols(self)
      def LoadListOfValues(self): LoadListOfValues(self)
      def ChangeAccessibility(self, checked): ChangeAccessibility(self, checked)
      def ChangePatternZipPostalCode(self): ChangePatternZipPostalCode(self)
      def LoadGeoLocalisator(self): LoadGeoLocalisator(self)

      def CheckTable(self, zObj):
            for i in range(zObj.rowCount()):
                if i in (0, 1) :
                    zObj.cellWidget(i,0).setEnabled(False)
                    if i == 0 : zObj.cellWidget(i,0).setCurrentIndex(2)
                    else : zObj.cellWidget(i,0).setCurrentIndex(6)
                else :
                    zObj.cellWidget(i,0).setEnabled(True)
                    if zObj.cellWidget(i,0).currentIndex() in (2,6) : zObj.cellWidget(i,0).setCurrentIndex(1)

      def CallFormatSelector(self):
          zObj = self.findChild(MyTableWidget, "tableformats")
          if zObj == None : return
          zIndex = int(self.sender().accessibleName().split("_")[2])
          zItemEditLine = zObj.cellWidget(zIndex,0)
          ChangeButtonIcon(self, self.sender(),"formatactivate.png", 18, 16)
          dialog = FormatDialog(self.formats, zItemEditLine.text())
          MakeWindowIcon(dialog, "format.png")
          if dialog.exec_(): zItemEditLine.setText("%s" % (dialog.format()))
          ChangeButtonIcon(self, self.sender(),"format.png", 18, 16)

      def CallSelectorConformityInfos(self):
          zObj = self.findChild(MyTableWidget, "coherence")
          if zObj == None : return
          dialog = TopologyDialog(zObj.toPlainText())
          MakeWindowIcon(dialog, "qsp.png")
          if dialog.exec_(): zObj.setPlainText("%s" % (dialog.infosTopology()))
        
      def CallQgsProjectionSelector(self):
           zObj = self.findChild(MyTableWidget, "tablescr")
           if zObj == None : return
           zIndex = int(self.sender().accessibleName().split("_")[2])
           zItemEditLine = zObj.cellWidget(zIndex,0)
           ChangeButtonIcon(self, self.sender(),"projectionactivate.png", 18, 16)
           dialog = SRSDialog(zItemEditLine.text())
           MakeWindowIcon(dialog, "projection.png")
           dialog.setWindowTitle(QApplication.translate("QSphere","Coordinate Reference System Selector", None, QApplication.UnicodeUTF8))
           if dialog.exec_(): zItemEditLine.setText("%s" % (dialog.epsg()))
           ChangeButtonIcon(self, self.sender(),"projection.png", 18, 16)

    
      def MakeCopy(self, TableWidget):
         zCopyTableWidget = TableWidgetMaker(self.parent, TableWidget.accessibleName(), self, False)
         for zRow in range(TableWidget.rowCount()):
             MakeLine(self, zCopyTableWidget, True, False, zRow, False)
             for zCol in range(TableWidget.columnCount()):
                   OriginalWidget = TableWidget.cellWidget(zRow, zCol) if TableWidget.cellWidget(zRow, zCol)!= None else TableWidget.item(zRow, zCol)
                   TargetObjWidget = zCopyTableWidget.cellWidget(zRow, zCol) if zCopyTableWidget.cellWidget(zRow, zCol)!= None else zCopyTableWidget.item(zRow, zCol)
                   if OriginalWidget.metaObject().className() in ("QLineEdit", "MySimpleWidgetLineEdit", "MyWidgetLineEdit", "MySimpleWidgetLineEditST") : TargetObjWidget.setText(OriginalWidget.text())
                   elif OriginalWidget.metaObject().className() in ("QCheckBox", "MyCheckBox") : TargetObjWidget.setChecked(OriginalWidget.isChecked())
                   elif OriginalWidget.metaObject().className() == "MyComboBox" :
                       TargetObjWidget.setCurrentIndex(OriginalWidget.currentIndex())
                       TargetObjWidget.setEnabled(OriginalWidget.isEnabled())
                   elif OriginalWidget.metaObject().className() == "MySpinBox" : TargetObjWidget.setValue(OriginalWidget.value())
         countItems(self, zCopyTableWidget.accessibleName(), zCopyTableWidget)
         contextMnuMDDActions(self, 0, zCopyTableWidget, "%s" % (zCopyTableWidget.accessibleName()), 6, self.buttonActions, "")         
         return  zCopyTableWidget   

      def SaveTable(self) :
         DimSource = self.fromTableWidget.rowCount()
         DimNew = self.tableWidget.rowCount()
         if DimSource > DimNew :
              for zRow in range(DimNew, DimSource): self.fromTableWidget.removeRow(self.fromTableWidget.rowCount()-1)
         elif DimSource < DimNew :
              for zRow in range(DimSource, DimNew):  MakeLine(self.parent, self.fromTableWidget, True, False, self.fromTableWidget.rowCount(), False)
        
         for zRow in range(self.tableWidget.rowCount()):    
              for zCol in range(self.tableWidget.columnCount()):
                  OriginalWidget = self.tableWidget.cellWidget(zRow, zCol) if self.tableWidget.cellWidget(zRow, zCol)!= None else self.tableWidget.item(zRow, zCol)
                  TargetObjWidget = self.fromTableWidget.cellWidget(zRow, zCol) if self.fromTableWidget.cellWidget(zRow, zCol)!= None else self.fromTableWidget.item(zRow, zCol)
                  if OriginalWidget.metaObject().className() in ("QLineEdit", "MySimpleWidgetLineEdit", "MyWidgetLineEdit", "MySimpleWidgetLineEditST") : TargetObjWidget.setText(OriginalWidget.text())
                  elif OriginalWidget.metaObject().className() in ("QCheckBox", "MyCheckBox") : TargetObjWidget.setChecked(OriginalWidget.isChecked())
                  elif OriginalWidget.metaObject().className() == "MyComboBox" :
                      TargetObjWidget.setCurrentIndex(OriginalWidget.currentIndex())
                      TargetObjWidget.setEnabled(OriginalWidget.isEnabled())                      
                  elif OriginalWidget.metaObject().className() == "MySpinBox" : TargetObjWidget.setValue(OriginalWidget.value())
         countItems(self.parent, self.fromTableWidget.objectName(), self.fromTableWidget)
  
      def close(self):  self.reject()   
  
      def resizeEvent(self,ev):
         zSize = ev.size()
         self.labelTableWidget.setGeometry(5, 5,  25, 25)
         self.tableWidget.setGeometry(30, 5,  zSize.width()-70, zSize.height()-40)
         self.buttonActions.setGeometry(zSize.width()-45, 5, 40, 24)

         try : self.OpenNavigatorButton.setGeometry(zSize.width()-35, 45, 24, 24)
         except : pass

         self.groupBoxActionsMeta.setGeometry(zSize.width()-490, zSize.height()-30, 220, 28)
         
         self.SaveButton.setGeometry(zSize.width()-250, zSize.height()-30, 25, 25)
         self.CloseButton.setGeometry(zSize.width()-140, zSize.height()-30, 100, 25)
         self.status_txt.setGeometry(int(zSize.width()/2)-64, int(zSize.height()/2)-64, 64, 64)
         self.barInfo.setGeometry(QRect(0, 0, zSize.width(), 90))

         try : ResizeCols(self, self.tableWidget, self.dims, (zSize.width()-70)/float(self.originalW))
         except : pass


class formWidgetDialog(QDialog):
      def  __init__(self, TableWidget, parent):
         QDialog.__init__(self)
         self.setWindowTitle(QApplication.translate("QSphere","Wizard Table Widget Composer", None, QApplication.UnicodeUTF8))
         self.setAccessibleName("formTableWidget")
         self.setObjectName("formTableWidget")

         self.parent = parent
         self.ShowWarning = self.parent.ShowWarning
         
         MakeWindowIcon(self, "wizards_form.png")
         MakePropertiesForWindow(self, self.parent)
         
         self.iface = self.parent.iface
         self.ParamsLineWidget = self.parent.ParamsLineWidget
         self.zTablesWidget = self.parent.zTablesWidget
         self.duration_warning = self.parent.duration_warning
         self.duration_info = self.parent.duration_info
         self.duration_timeout = self.parent.duration_timeout
         self.ListOfThesaurus = self.parent.ListOfThesaurus
         self.DateListOfThesaurus = self.parent.DateListOfThesaurus
         self.ListTypeDates = self.parent.ListTypeDates
         self.ListDegres = self.parent.ListDegres


         self.labelTableWidget = QLabel(self)
         self.labelTableWidget.setAccessibleName("Lbl%s" % (TableWidget.accessibleName()))
         self.labelTableWidget.setObjectName("Lbl%s" % (TableWidget.accessibleName()))

         self.tableWidget = TableWidget

         if self.tableWidget.accessibleName()=="tableemprises" : self.deconnectObj(self.tableWidget)
         
         self.barInfo = QgsMessageBar(self)
         self.barInfo.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )
            
         if DicoHasKey(self.zTablesWidget, self.tableWidget.accessibleName()):
             self.dims = self.zTablesWidget[self.tableWidget.accessibleName()][0]
             self.libelles = self.zTablesWidget[self.tableWidget.accessibleName()][1]
             self.paramsWidget = self.ParamsLineWidget[self.tableWidget.accessibleName()]

         dimAll = (max(5, len(self.dims))+1)*35

         self._W, self._H = 500, dimAll
         self.setMinimumSize(QSize(self._W,self._H))
         self.setMaximumSize(QSize(self._W * 1.5,self._H))
         self.setWindowFlags(Qt.WindowMaximizeButtonHint)
         
         zRow = self.tableWidget.currentRow()
         if zRow == -1 : zRow = 0
         self.widgets = []

         zkey = self.tableWidget.objectName()
         
         for zColumn in range(self.tableWidget.columnCount()):
             zRefWidget = self.tableWidget.cellWidget(zRow, zColumn)

             if zRefWidget != None :

                 if zkey =="tablemotsclefso" and type(zRefWidget) == MyComboBox and zRefWidget.isEnabled() and zColumn == 1 :
                     zRefParentWidget = self.tableWidget.cellWidget(zRow, zColumn-1)
                     self.zWidget = AddLineWidget(self, self.tableWidget, -1,  zColumn,  self.paramsWidget[zColumn][0], self.paramsWidget[zColumn][1], (zRefParentWidget.currentIndex(), zRefWidget.currentIndex()))
                 else :
                     self.zWidget = AddLineWidget(self, self.tableWidget, -1,  zColumn,  self.paramsWidget[zColumn][0], self.paramsWidget[zColumn][1], self.paramsWidget[zColumn][2])
                     
                 self.zWidget.setObjectName("%s_%s_%s" % (self.tableWidget.accessibleName(), zRow, zColumn))
                 self.zWidget.setAccessibleName("%s_%s_%s" % (self.tableWidget.accessibleName(), zRow, zColumn))
                 
                 if self.zWidget != None :
                    if type(self.zWidget) not in (MyPushButton, QPushButton, MyCheckBox, QCheckBox) :
                        zLabel = QLabel(self)
                        zLabel.setObjectName("Lbl%s" % (zRefWidget.objectName()))
                        zLabel.setGeometry(10, 10+(zColumn*30), 140, 30)
                        zLabel.setText("%s :" % self.libelles[zColumn])
                        zLabel.setAlignment(Qt.AlignRight)
                        zLabel.setStyleSheet("border: 2px solid grey; border-radius: 5px; color: white; background-color: #5d5d5d; font-family : Times New Roman, Times, serif; font-size : 8pt; text-align: center;")
                    self.zWidget.setGeometry(150, 10+(zColumn*30), 300, 30)
                    self.setValue(zRefWidget, self.zWidget)
                    self.widgets.append(self.zWidget)

         for obj in self.widgets :
             if type(obj) == MyCheckBox :
                self.ChangeAccessibility(obj.isChecked())
                break

        
         zIcon = getThemeIcon("actions.png")
         zToolTip = QApplication.translate("QSphere","Actions for the metadata...", None, QApplication.UnicodeUTF8)
         self.buttonActions = MyPushButton(self) 
         self.buttonActions.initPushButton(40, 24, 0, 0, "ActionsButton_%s" % (TableWidget.accessibleName()), "", zToolTip, True, zIcon, 40, 24, True)

         contextMnuMDDActions(self, 0, self.tableWidget, "%s" % (self.tableWidget.accessibleName()), 6, self.buttonActions, "")

         self.SaveButton = MyPushButton(self)
         self.SaveButton.initPushButton(100, 25, self._W - 250, self._H - 45, "SaveButton", "", QApplication.translate("QSphere", "Save", None, QApplication.UnicodeUTF8), True, getThemeIcon("sendtotable.png"), 100, 25, True)
         self.SaveButton.setShortcut(QKeySequence("Ctrl+S"))

         self.CloseButton = QPushButton(self)
         self.CloseButton.setObjectName("CloseButton")
         self.CloseButton.setText(QApplication.translate("QSphere", "Close", None, QApplication.UnicodeUTF8))
         self.CloseButton.setShortcut(QKeySequence("Ctrl+Q"))

         self.groupStyleSheet = """QGroupBox {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E0E0E0, stop: 1 #FFFFFF);""" \
                                   """border: 2px solid gray; border-radius: 5px; margin-top: 1ex; })"""  

         self.groupBoxActionsMeta = QGroupBox(self)
         self.groupBoxActionsMeta.setStyleSheet(self.groupStyleSheet)
         self.groupBoxActionsMeta.setGeometry(10, self._H - 50, 220, 40)

         zToolTip = QApplication.translate("QSphere","Move down", None, QApplication.UnicodeUTF8)
         self.MoveDown = MyPushButton(self.groupBoxActionsMeta) 
         self.MoveDown.initPushButton(24, 24, 10, 10, "MoveDown", "", zToolTip, True, getThemeIcon("movedown.png"), 24, 24, True)
         self.MoveDown.setAutoRepeat(True)
         self.MoveDown.setShortcut(QKeySequence.MoveToNextLine)

         self.labelPosition = QLabel(self.groupBoxActionsMeta)
         self.labelPosition.setGeometry(40, 10, 100, 25)
         self.labelPosition.setText("%s :" % (QApplication.translate("QSphere","Current contact", None, QApplication.UnicodeUTF8)))
        
         zToolTip = QApplication.translate("QSphere","Move up", None, QApplication.UnicodeUTF8)
         self.MoveUp = MyPushButton(self.groupBoxActionsMeta) 
         self.MoveUp.initPushButton(24, 24, 180, 10, "MoveUp", "", zToolTip, True, getThemeIcon("moveup.png"), 24, 24, True)
         self.MoveUp.setAutoRepeat(True)
         self.MoveUp.setShortcut(QKeySequence.MoveToPreviousLine)
       
         self.CurrentItem = QLabel(self.groupBoxActionsMeta)
         self.CurrentItem.setGeometry(140, 10, 40, 25)

         self.status_txt = QLabel(self)
         self.movie = QMovie(getThemeIcon("sablier.gif"))
         self.status_txt.setMovie(self.movie)
         self.status_txt.setLayout(QHBoxLayout())
         self.status_txt.layout().addWidget(QLabel(''))
         self.status_txt.setVisible(False)

         self.barInfo = QgsMessageBar(self)
         self.barInfo.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )

         self.SaveButton.clicked.connect(self.sendDataToTable)
         self.CloseButton.clicked.connect(self.close)
         self.MoveUp.clicked.connect(self.MoveSelUp)
         self.MoveDown.clicked.connect(self.MoveSelDown)
         
         self.tableWidget.selectRow(0) if self.tableWidget.currentRow()==-1 else self.tableWidget.selectRow(self.tableWidget.currentRow())
         self.row = self.tableWidget.currentRow()
         self.rowCount = self.tableWidget.rowCount()
         self.FixeCurrentItem()


      def close(self):
          self.connectObj(self.tableWidget)  
          self.reject()

      def deconnectObj(self, tableWidget):
          for zRow in range(self.tableWidget.rowCount()):
              for zColumn in range(self.tableWidget.columnCount()):
                      zRefWidget = self.tableWidget.cellWidget(zRow, zColumn)
                      if type(zRefWidget) == MySpinBox : zRefWidget.removeEventFilter(zRefWidget) 
          
      def connectObj(self, tableWidget):
          for zRow in range(self.tableWidget.rowCount()):
              for zColumn in range(self.tableWidget.columnCount()):
                      zRefWidget = self.tableWidget.cellWidget(zRow, zColumn)
                      if type(zRefWidget) == MySpinBox : zRefWidget.installEventFilter(zRefWidget)
          
      
      def resizeEvent(self, ev):
         posX = ev.size().width()
         for obj in self.widgets :  obj.setGeometry(obj.x(), obj.y(), posX-200, 30)
         self.buttonActions.setGeometry(posX - 50, 10, 40, 24)
         self.CloseButton.setGeometry(posX - 140, self._H - 45, 100, 25)
         self.SaveButton.setGeometry(posX - 250, self._H - 45, 100, 25)
          
      def startMovie(self):
            self.status_txt.setVisible(True)
            self.movie.start()
            self.status_txt.repaint()

      def stopMovie(self):
            self.movie.stop()
            self.status_txt.setVisible(False)

      def OpenNavigator(self):
          d = doUI.LoadDialogViewer(self, self.iface, "#blank", False, [], self.langueTR, self, None, "navigatorweb.png", True)

      def clickHelp(self): makeHelp(self)

      def testURL(self): testURL(self.parent)
      def goToLocalisator(self):
          d = doUI.LoadDialogViewer(self, self.iface, self.widgets[0].text(), False, [], self.langueTR, self, None, "urllocalisator.png", True)
          
      def AddLine(self):
          AddLine(self.parent)
          self.refreshData()
          
      def MoveLineUp(self):
          MoveLineUpProcess(self.parent, "%s" % (self.sender().objectName()))
          self.refreshData()
          
      def MoveLineDown(self):
          MoveLineDownProcess(self.parent, "%s" % (self.sender().objectName()))
          self.refreshData()
          
      def DelLine(self):
          if self.tableWidget.rowCount()> 1 :
              DelLineProcess(self.parent, "%s" % (self.sender().objectName()), True)
              self.refreshData()

      def DelCurrentLine(self):
          if self.tableWidget.rowCount()> 1 :
              DelLineProcess(self.parent, "%s" % (self.sender().objectName()), False)
              self.refreshData()
      
      def FixeCurrentItem(self):  self.CurrentItem.setText("%s / %s" % (self.row+1, self.tableWidget.rowCount()))

      def refreshData(self):
          self.row = self.tableWidget.currentRow()
          self.tableWidget.selectRow(self.row)
          self.loadData()
          self.FixeCurrentItem()
      
      def MoveSelUp(self):
        if self.row > 0 :
           self.row = self.row - 1    
           self.tableWidget.selectRow(self.row)
           self.loadData()
           self.FixeCurrentItem()
                  
      def MoveSelDown(self):
        if self.row <  (self.tableWidget.rowCount()-1) :
           self.row= self.row + 1    
           self.tableWidget.selectRow(self.row)
           self.loadData()
           self.FixeCurrentItem()

      def loadData(self):
          try :
              for zColumn in range(self.tableWidget.columnCount()):
                  zRefWidget = self.tableWidget.cellWidget(self.row, zColumn)
                  if zRefWidget != None : self.setValue(zRefWidget, self.widgets[zColumn])
          except : pass  

      def sendDataToTable(self):
          try : 
              zColumn = 0
              for obj in self.widgets :
                  zObjDest = self.tableWidget.cellWidget(self.row, zColumn)
                  if zObjDest!= None and obj != None : self.setValue(obj, zObjDest)
                  zColumn+= 1
          except : pass        
          
      def setValue(self, zObjSource, zObjDest):
          zObjDest.setEnabled(zObjSource.isEnabled())
          if type(zObjSource)==MyCheckBox :
              zObjDest.setCheckState(zObjSource.checkState())
          try : zObjDest.setValue(zObjSource.value())
          except :
              try : zObjDest.setText(zObjSource.text())
              except :
                      try : zObjDest.setCurrentIndex(zObjSource.currentIndex())
                      except : pass
                              
      def LoadListOfValues(self):
            if self.sender().accessibleName() == "" : return
            zIndexThesaurus = self.sender().currentIndex()
            i = 0
            for obj in self.widgets :
                if self.sender() == obj : break
                i+= 1
            try :     
                zObjWidget = self.widgets[i+1]
                if zObjWidget != None :
                   zObjWidget.clear()
                   SizeW, zCols, iLine = LoadFile(self, zObjWidget, "", "file:200:thesaurus_%s_%s.csv:0:0" % (zIndexThesaurus, self.parent.MainPlugin.dicoLangs[self.parent.MainPlugin.indexLang]), 1, None) 
            except : pass
            
      def ChangeAccessibility(self, checked):
          for obj in self.widgets :
              if self.sender() == obj :
                 obj.setCheckState(self.sender().checkState())
                 break          
          for i in range(2,5):
               try : self.widgets[i].setEnabled(checked)
               except : pass
               
      def ChangePatternZipPostalCode(self):
          i = 0
          for obj in self.widgets :
              if self.sender() == obj :
                 break
              i+= 1  
          zObj = self.widgets[i+1]
          if zObj==None: return
          zKeyTarget = self.sender().currentText()
          if DicoHasKey(self.listCountriesCode, zKeyTarget):
                zObj.setInputMask("")
                zObj.setInputMask(self.listCountriesCode[zKeyTarget][1])
                zObj.regex = QRegExp(r"%s" % (self.listCountriesCode[zKeyTarget][0]), Qt.CaseSensitive)
          else :
                zObj.setInputMask("")
                zObj.setInputMask("XXXxxxxxxx;X")
                zObj.regex = QRegExp(r"(^+[a-zA-Z_0-9\s]{3,10}$)", Qt.CaseSensitive) 

          
      def LoadGeoLocalisator(self):
          zEmprise = []
          for i in range(0,4): zEmprise.append(self.widgets[i].value())
          ChangeButtonIcon(self, self.sender(),"voiractivate.png", 24, 24)
          zLang = self.MainPlugin.dicoLangs[self.MainPlugin.indexLang]
          d = doUI.LoadDialogViewer(self, self.iface, "file:geolocalisator_%s.html" % (zLang), False, zEmprise, self.langueTR, self, None, "voir.png", True)
          ChangeButtonIcon(self, self.sender(),"voir.png", 18, 16)

      def CheckInfosRoles(self): pass
          
      def CheckTable(self, zObj):
            for i in range(zObj.rowCount()):
                if i in (0, 1) :
                    zObj.cellWidget(i,0).setEnabled(False)
                    if i == 0 : zObj.cellWidget(i,0).setCurrentIndex(2)
                    else : zObj.cellWidget(i,0).setCurrentIndex(6)
                else :
                    zObj.cellWidget(i,0).setEnabled(True)
                    if zObj.cellWidget(i,0).currentIndex() in (2,6) : zObj.cellWidget(i,0).setCurrentIndex(1)

      def CallFormatSelector(self):
          i = 0  
          for obj in self.widgets :
              if self.sender() == obj : break
              i+= 1

          zObj = self.widgets[i-1]
          ChangeButtonIcon(self, self.sender(),"formatactivate.png", 18, 16)
          dialog = FormatDialog(self.formats, zObj.text())
          MakeWindowIcon(dialog, "format.png")
          if dialog.exec_(): zObj.setText("%s" % (dialog.format()))
          ChangeButtonIcon(self, self.sender(),"format.png", 18, 16)


