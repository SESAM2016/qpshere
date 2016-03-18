# -*- coding:utf-8 -*-

try:
    from osgeo import gdal, ogr
    from osgeo import osr
    from osgeo.gdalconst import *
except:
    import gdal, ogr
    import osr

import sys
import os
import codecs
import string
import datetime
import ConfigParser
from random import sample

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from qsphere_objmaker import *
import textwrap

from threading import Thread, enumerate
from time import sleep

import webbrowser
import urllib2
import urllib

import socket
import gc
import ast

from math import (floor, log, pow)
from xml.dom.minidom import parseString

UPDATE_INTERVAL = 0.01


def makeListXSLT(self):
    listeXSLT = []
    path = CorrigePath(os.path.dirname(__file__))
    path = "%s/xml/xsl" % (path)
    for dirname, dirnames, filenames in os.walk(path):
        for fileName in filenames:
            zName = "%s" % (os.path.basename(fileName))
            textension = os.path.splitext(fileName)
            extension = textension[len(textension)-1].lower()
            if extension!="" and extension == ".xsl": listeXSLT.append(zName)
    return listeXSLT

def NetHTML(HTML):
    #QXmlPattern not support CDATA section
    if HTML != None :
        HTML = HTML.replace('&amp;', '&')
        HTML = HTML.replace('&gt;', '>')
        HTML = HTML.replace('&lt;', '<')
    return HTML

def DicoHasKey(dico, key):
    cond = False
    try :
       cond = dico.has_key(key)
    except :
       cond = (key in dico)
    return cond

def convertSize(size):
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = 0
   if size > 0 :
      i = int(floor(log(size,1024)))
      p = pow(1024,i)
      s = round(size/p,2)
   else :
      s = 0
   return '%s %s' % (s,size_name[i])

    
def prettify_xml(xml):
    if xml.count('\n') > 5:  
        return xml
    else:
        if xml.startswith('http'): return xml
        else: return parseString(xml).toprettyxml()


def getSelConnexion(self):
  mySettings = QSettings()
  value = mySettings.value("/qsphere/connections/selected")
  return value

def isoNameSpaces(key):
    namespace_dict = {
        'atom'  :   'http://www.w3.org/2005/Atom',
        'csw'   :   'http://www.opengis.net/cat/csw/2.0.2',
        'dc'    :   'http://purl.org/dc/elements/1.1/',
        'dct'   :   'http://purl.org/dc/terms/',
        'dif'   :   'http://gcmd.gsfc.nasa.gov/Aboutus/xml/dif/',
        'draw'  :   'gov.usgs.cida.gdp.draw',
        'fes'   :   'http://www.opengis.net/fes/2.0',
        'fgdc'  :   'http://www.opengis.net/cat/csw/csdgm',
        'gco'   :   'http://www.isotc211.org/2005/gco',
        'gmd'   :   'http://www.isotc211.org/2005/gmd',
        'gmi'   :   'http://www.isotc211.org/2005/gmi',
        'gml'   :   'http://www.opengis.net/gml',
        'gml311':   'http://www.opengis.net/gml',
        'gml32' :   'http://www.opengis.net/gml/3.2',
        'gmx'   :   'http://www.isotc211.org/2005/gmx',
        'gts'   :   'http://www.isotc211.org/2005/gts',
        'ogc'   :   'http://www.opengis.net/ogc',
        'om'    :   'http://www.opengis.net/om/1.0',
        'om10'  :   'http://www.opengis.net/om/1.0',
        'om100' :   'http://www.opengis.net/om/1.0',
        'om20'  :   'http://www.opengis.net/om/2.0',
        'ows'   :   'http://www.opengis.net/ows',
        'ows100':   'http://www.opengis.net/ows',
        'ows110':   'http://www.opengis.net/ows/1.1',
        'ows200':   'http://www.opengis.net/ows/2.0',
        'rim'   :   'urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0',
        'rdf'   :   'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'sa'    :   'http://www.opengis.net/sampling/1.0',
        'sml'   :   'http://www.opengis.net/sensorML/1.0.1',
        'sml101':   'http://www.opengis.net/sensorML/1.0.1',
        'sos'   :   'http://www.opengis.net/sos/1.0',
        'sos20' :   'http://www.opengis.net/sos/2.0',
        'srv'   :   'http://www.isotc211.org/2005/srv',
        'swe'   :   'http://www.opengis.net/swe/1.0.1',
        'swe10' :   'http://www.opengis.net/swe/1.0',
        'swe101':   'http://www.opengis.net/swe/1.0.1',
        'swe20' :   'http://www.opengis.net/swe/2.0',
        'swes'  :   'http://www.opengis.net/swes/2.0',
        'tml'   :   'ttp://www.opengis.net/tml',
        'wfs'   :   'http://www.opengis.net/wfs',
        'wfs20' :   'http://www.opengis.net/wfs/2.0',
        'wcs'   :   'http://www.opengis.net/wcs',
        'wps'   :   'http://www.opengis.net/wps/1.0.0',
        'wps100':   'http://www.opengis.net/wps/1.0.0',
        'xlink' :   'http://www.w3.org/1999/xlink',
        'xs'    :   'http://www.w3.org/2001/XMLSchema',
        'xs2'   :   'http://www.w3.org/XML/Schema',
        'xsi'   :   'http://www.w3.org/2001/XMLSchema-instance',
        'none'  :   ''
    }

    retval = None
    if key in namespace_dict: retval = namespace_dict[key]
    return retval

def appendNameSpace(self, path):
    nameSpaceAppendedPath = ''
    pathElements = path.split('/')
    count = 0
    for element in pathElements:
            try:					
                    if ':' in element:						
                            splitElement = element.split(':')
                            nsPrefix,nsElement = splitElement[0],splitElement[1]
                    else:
                            nsPrefix = self.defaultIsoNamespace()
                            nsElement = element
                    if count == 0: appendedPath = '{%s}%s' % (isoNameSpaces(nsPrefix) , nsElement)
                    else: appendedPath = '%s/{%s}%s' % (appendedPath , isoNameSpaces(nsPrefix) , nsElement)
                    count += 1
            except:	appendedPath = 'null'
    nameSpaceAppendedPath = appendedPath.replace('{}','')
    return nameSpaceAppendedPath


class RequestWithMethod(urllib2.Request):
    def __init__(self, method, *args, **kwargs):
        self._method = method
        urllib2.Request.__init__(self, *args, **kwargs)
    def get_method(self): return self._method

class RestRequest(object):
    def __init__(self, base_url):
        self.base_url = base_url
    def request(self, url, method, headers={"Content-Type" : "application/xml"}, data=None):
        request = RequestWithMethod(url=url, method=method, headers=headers) 
        try : response = urllib2.urlopen(request, data=data)
        except : response = None
        return response

class URLThread(Thread):
    def __init__(self, url, method, headers, data=None):
        super(URLThread, self).__init__()
        self.response = None
        self.timeOut = False
        self.url = url
        self.method = method
        self.headers = headers
        self.data = data

    def run(self): 
        request = RequestWithMethod(url=self.url, method="POST", headers={"Content-Type" : "application/xml"})
        try : self.response = urllib2.urlopen(request, data=self.data)
        except : self.response = None
   
def multi_get(anim, ctrlanim, uris, timeout): 
    def alive_count(lst, i):
        anim.jumpToFrame(i)
        ctrlanim.repaint()
        alive = map(lambda x : 1 if x.isAlive() else 0, lst)
        return reduce(lambda a,b : a + b, alive)
    threads = [ URLThread(uri[0], uri[1], uri[2], uri[3]) for uri in uris ]
    for thread in threads:
        thread.start()
        i = 0
    while alive_count(threads, i) > 0 and timeout > 0.0:
        i = i+1 if i < (anim.frameCount()-1) else 0
        timeout = timeout - UPDATE_INTERVAL
        sleep(UPDATE_INTERVAL)
    return [ (x.url, x.response) for x in threads ]


class URLThreadRequests(Thread):
    def __init__(self, url):
        super(URLThreadRequests, self).__init__()
        self.response = None
        self.timeOut = False
        self.url = url

    def run(self):
        hdr = {'User-Agent': 'OpenAnything/1.0 +http://somepage.org/', 'Connection': 'keep-alive'}
        try : 
            request = urllib2.Request(self.url, headers=hdr)
            opener = urllib2.build_opener()  
            self.response = opener.open(request).read()
        except : self.response = None

        
def multi_getRequests(anim, ctrlanim, uris, timeout): 
    def alive_count(lst, i):
        anim.jumpToFrame(i)
        ctrlanim.repaint()
        alive = map(lambda x : 1 if x.isAlive() else 0, lst)
        return reduce(lambda a,b : a + b, alive)
    threads = [ URLThreadRequests(uri[0]) for uri in uris ]
    for thread in threads:
        thread.start()
        i = 0
    while alive_count(threads, i) > 0 and timeout > 0.0:
        i = i+1 if i < (anim.frameCount()-1) else 0
        timeout = timeout - UPDATE_INTERVAL
        sleep(UPDATE_INTERVAL)
    return [ (x.url, x.response) for x in threads ]

#================================================
# FUNCTION TO FORCE / VERIFY EXTENSION
#================================================
def FileNameWithExtension(self, fileName, selectedFilter):
    extension = ""
    file = QFileInfo(fileName)
    extensionfind = ".%s" % (file.suffix())

    if selectedFilter.find("(")!=-1 :
        s = selectedFilter.find("*")+1
        e = selectedFilter.find(" ", s)
        e2 = selectedFilter.find(")", s)
        if (e == -1 and e2 < e) : e = e2 
        extension = selectedFilter[s:e].replace("*","")
    else :
        if selectedFilter.find("*.")!=-1 : extension = selectedFilter.replace("*","")
        
    if(file.suffix()=="") or (extensionfind.find(extension)==-1) : fileName+= "%s" % (extension)

    return fileName

#================================================
# FUNCTIONS TO RESTORE SIZE COLUMNS QTABLEWIDGET
#================================================
def initSizeCols(self, Obj, zDim):
    if type(zDim) == int : Obj.setColumnWidth(0, zDim)
    else :
        for i in range(len(zDim)): Obj.setColumnWidth(i, zDim[i])

def ResizeCols(self, Obj, zDim, zProrata):
    if type(zDim) == int : Obj.setColumnWidth(0, int(zDim * zProrata))
    else :
        for i in range(len(zDim)): Obj.setColumnWidth(i, int(zDim[i] * zProrata))   

def makeGetOptions(self):
    self.serverMetadata, self.serverKeywords, self.serverNavigator, self.InitDir, self.duration_info, self.duration_warning, self.duration_timeout, \
                    self.autoCorrect, self.byStream, self.byFile, self.InitDirByFile, self.silentMode, self.reportingCSWT  = getOptions()

def getOptions():
    serverMetadata = []
    serverKeywords = []
    serverNavigator = []
    InitDir = os.path.dirname(__file__)
    duration_info = duration_warning = duration_timeout = 5
    autoCorrect = byStream = byFile = silentMode = reportingCSWT = False
    InitDirByFile = os.path.dirname(__file__)

    savefile = os.path.join(os.path.dirname(__file__),"ressources/options.ini")
    if os.path.exists(savefile):

         config = ConfigParser.ConfigParser()
         config.read(savefile)
         zSections = config.sections()

         for section in zSections :
             if section == "serverMetadata" :
                zItemCount = int(config.get(section,'Items').rstrip())
                for k in range(zItemCount): serverMetadata.append(config.get(section,'Item_%s' % (k)))
             elif section == "serverKeywords" :
                zItemCount = int(config.get(section,'Items').rstrip())
                for k in range(zItemCount): serverKeywords.append(config.get(section,'Item_%s' % (k)))                
             elif section == "serverNavigator" :
                 zItemCount = int(config.get(section,'Items').rstrip())
                 for k in range(zItemCount): serverNavigator.append(config.get(section,'Item_%s' % (k)))
             elif section == "txtRep" :
                 InitDir = config.get(section,'InitDir')
                 if InitDir=="" or not (os.path.exists(InitDir)) : InitDir = os.path.dirname(__file__) 
             elif section == "SliderINFO" :
                 try : duration_info = int(config.get(section,'value'))
                 except : pass
             elif section == "SliderWARNING" :
                 try : duration_warning = int(config.get(section,'value'))
                 except : pass
             elif section == "SliderTIMEOUT" :
                 try : duration_timeout = int(config.get(section,'value'))
                 except : pass
             elif section == "checkAutoCorrect" :
                 try : autoCorrect = ast.literal_eval(config.get(section,'state'))
                 except : pass
             elif section == "radioStream" :
                 try : byStream = ast.literal_eval(config.get(section,'state'))
                 except : pass                 
             elif section == "radioFile" :
                 try : byFile = ast.literal_eval(config.get(section,'state'))
                 except : pass
             elif section == "txtRepXML" :
                 InitDirByFile = config.get(section,'InitDir')
                 if InitDirByFile=="" or not (os.path.exists(InitDirByFile)) : InitDirByFile = os.path.dirname(__file__) 
             elif section == "checkSilentMode" :   
                 try : silentMode = ast.literal_eval(config.get(section,'state'))
                 except : pass  
             elif section == "checkReportingCSWT" :   
                 try : reportingCSWT = ast.literal_eval(config.get(section,'state'))
                 except : pass                  

    return serverMetadata, serverKeywords, serverNavigator, InitDir, duration_info, duration_warning, duration_timeout, \
           autoCorrect, byStream, byFile, InitDirByFile, silentMode, reportingCSWT


def GetExtension(fileName):
    zName = "%s" % (os.path.basename(fileName))
    textension = os.path.splitext(fileName)
    extension = textension[len(textension)-1].lower()
    return extension

def getEncodingCar(FileXML, dataXML):
    EncondingCar = "utf8"
    if FileXML!= "" and dataXML == None:
       if  os.path.exists(FileXML):
           f = open(FileXML, "r")
           tEncondingCar = f.readline()
           f.close()
    else :
        if dataXML != None : tEncondingCar = dataXML
        else : return EncondingCar    
    posD = posF = 0     
    posD = tEncondingCar.find("encoding=\"")
    if posD > 0 :
       posF = tEncondingCar.lower().find("\"", posD+10)
       if posF > posD :  EncondingCar = tEncondingCar[posD+10:posF].lower().replace("-","")
    return EncondingCar


def ChangeButtonIcon(self, zButton, zIcon, zSizeWIcon, zSizeHIcon):
    zIcon = getThemeIcon(zIcon)
    zButton.setIcon(QIcon(zIcon))

#============================
# FUNCTIONS SEARCH WEB FILES
#============================
def listdirectoryWeb(self, path, zlistwidget, counter):
    i, countfiles = 0, 0
    zDirs = []

    font = QtGui.QFont()
    font.setPointSize(8) 
    font.setWeight(10) 
    font.setBold(True)

    Qicondir = QIcon(getThemeIcon("open.png"))
    extension = self.Filters.currentText().replace("*.","")
    extension = extension.replace("*","")
    menuIcon = getThemeIcon("%s.png" % (extension))
    if menuIcon == "" : menuIcon = getThemeIcon("unknow.png")
    QmenuIcon = QIcon(menuIcon)
    
    self.listdirectories = {}
    self.listdirectories["%s" % (path)]= (self.layers_item, [])
    
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames: i, zDirs, countfiles = scandirectoryWeb(self, path, dirname, os.path.join(dirname, filename), zlistwidget, counter, i, zDirs, font, Qicondir, QmenuIcon, countfiles)
    return countfiles, len(zDirs)+1

def scandirectoryWeb(self, path, dirname, currentFile, zlistwidget, counter, i, zDirs, fontDirs, Qicondir, QmenuIcon, countfiles):
        if os.path.isfile(currentFile):
            textension = os.path.splitext(currentFile)
            extension = textension[len(textension)-1].lower()[1:]
            if self.filter.exactMatch(currentFile) :

                zTarget = dirname.replace(path, "").replace("\\", "/")
                zItem = QListWidgetItem(Qicondir, "%s" % (textwrap.fill(zTarget, 50)), None, 1)
                zItem.setFont(fontDirs)
                zItem.setBackground(QBrush(QColor(200,200,200,125),Qt.SolidPattern))
                zItem.setFlags(Qt.ItemIsEnabled)
                zItem.setToolTip(zTarget) 
                if zTarget != "" and not zTarget in zDirs :
                    zlistwidget.addItem(zItem)
                    zDirs.append(zTarget)
                    
                groupItems = self.layers_item
                if zTarget!="" :
                    abspath = os.path.dirname(currentFile)
                    tpath, refpath = abspath.split("/"), ""
                    for i in range(len(tpath)-1): refpath+= tpath[i]+"/"
                    dirname = abspath.rsplit("/",1)[1].replace("\\", "/")+"/"
                    tdirname = dirname.split("/")
                    compath = ""

                    for  i in range(len(tdirname)):
                        if tdirname[i]!= "" :
                            compath+=  tdirname[i]+"/"
                            zkey = ("%s%s" % (refpath, compath))
                            if not DicoHasKey(self.listdirectories, zkey) :
                                if groupItems == None :
                                  zkeyrefpath = "%s" % (refpath)
                                  groupItems = self.listdirectories[zkeyrefpath][0]
                                  
                                groupItemsSub = QTreeWidgetItem()
                                groupItemsSub.setIcon(0, Qicondir)
                                groupItemsSub.setText(0, "%s" % (tdirname[i]))
                                groupItemsSub.setToolTip(0, "")
                                groupItems.addChild(groupItemsSub)

                                self.listdirectories[zkey] = (groupItemsSub, []) 
                                groupItems = groupItemsSub
                            else:
                                groupItems = self.listdirectories[zkey][0]
                                if zkey == abspath :
                                   zListFiles = self.listdirectories[zkey][1]
                                   zListFiles.append(currentFile)
                                   zkey = "%s" % (abspath)
                                   self.listdirectories[zkey]= (groupItems, zListFiles)                        

                zItem = QListWidgetItem(QmenuIcon, "%s" % (os.path.basename(currentFile)), None, 0)
                zItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                zItem.setToolTip(currentFile)
                zlistwidget.addItem(zItem)
                countfiles+= 1
                self.refreshCounter(countfiles, len(zDirs))

                if groupItems!= None :
                   FileItem = QTreeWidgetItem()
                   FileItem.setIcon(0, QmenuIcon) 
                   FileItem.setText(0, "%s" % (os.path.basename(currentFile)))
                   FileItem.setToolTip(0, currentFile)
                   groupItems.addChild(FileItem)  
                
            i = i+1 if i < (counter-1) else 0
            self.movie.jumpToFrame(i)
            self.status_txt.repaint()
                
        return i, zDirs, countfiles
                

#=================================
# FUNCTIONS FIXE VALUE AND WIDGET
#=================================
def GetIndex(zObj):
    try : zIndexEmp = int(zObj.toolTip())
    except : zIndexEmp = -1
    if zIndexEmp == -1 : zIndexEmp = 0
    return zIndexEmp

def MakeToolTipCalendar(self, zObjCalendar):
    TheDate = ReturnDate(self, zObjCalendar)
    zMsg = QApplication.translate("QSphere","Present Value : ", None, QApplication.UnicodeUTF8) + TheDate 
    zObjCalendar.setToolTip(zMsg)
    return zMsg

def SetTextWidget(self, zCible, zText, isValue):
    zObj = getWidget(self, zCible)     
    if zObj!=None:
       if not isValue : zObj.setText(zText)
       else :  zObj.setValue(float(zText))

def FixeLayerType(self, layertype):
    index = int(layertype)
    ztypes = ("vector", "raster", "plugin")
    return ztypes[index]

def GetTextWidget(self, zCible, isValue):
    zObj = getWidget(self, zCible)
    zValue, zText = "", ""
    if zObj == None : return zValue, zText
    
    zClassObjName = "%s" % (zObj.metaObject().className())
    if zClassObjName in ("QLineEdit", "MyWidgetLineEdit"):    
        zValue = "%s" % (CorrigeText(zObj.text()))
        zText = "%s" % (CorrigeText(zObj.text()))
    elif zClassObjName=="QCalendarWidget" :
        zValue = ReturnDate(self, zObj)
        zText = zValue        
    elif zClassObjName in ("QComboBox", "MyComboBox") :
        zValue = "%s" % (zObj.currentText())
        zValue = zValue.lower()
        zText = "%s" % (zObj.currentText())
    elif zClassObjName in ("QTextEdit", "MyTextEdit") :
        zValue = "%s" % (CorrigeText(zObj.toPlainText()))
        zText = zValue
    return zValue, zText

def CorrigeText(TextIn):
    TextOut = TextIn.replace('&', '&amp;')
    TextOut = TextOut.replace('>', '&gt;')
    TextOut = TextOut.replace('<', '&lt;')
    return TextOut

def getWidget(self, zCible):
    zObj = None
    if self.objectName() in ("DialogMetaData", "DialogOptions") : 
        zTabs = self.tabWidget.count()
        for i in range(zTabs):
            self.tabWidget.setCurrentIndex(i)
            zTab = self.tabWidget.currentWidget()
            zObjs = zTab.children()
            for j in range(len(zObjs)):
                if zObjs[j].accessibleName() == zCible :
                   zObj = zObjs[j]
                   return zObj
                elif type(zObjs[j]) == QGroupBox :
                     for subchild in zObjs[j].children() :
                         zName = ""
                         try : zName = subchild.accessibleName()
                         except : zName = subchild.objectName()
                         if zName == zCible : return subchild   
    else:
       
        for child in self.children() :
          if type(child) == QGroupBox :
             for subchild in child.children() :
                 zName = ""
                 try : zName = subchild.accessibleName()
                 except : zName = subchild.objectName()
                 if zName == zCible : return subchild
          else :
             zName = ""
             try : zName = child.accessibleName()
             except : zName = child.objectName()
             if zName == zCible : return child
    
    return zObj

#==========================
# FUNCTIONS BUILDING LISTS
#==========================
def MakeListCountries(self):
    ListCountries, ListCountriesCode, indexCountry, zCible = [], {}, 0, ""
    isHD = False
    ZIPREG = {"UnitedStates" : ("^\d{5}([\-]?\d{4})?$","99999-9999;X"), \
              "United States" : ("^\d{5}([\-]?\d{4})?$","99999-9999;X"), \
              "UnitedKingdom"  : ("^[A-Z]{1,2}[0-9]{1,2}[A-Z]?\s[0-9][A-Z][A-Z]$","XXXXXXXX;X"), \
              "United Kingdom"  : ("^[A-Z]{1,2}[0-9]{1,2}[A-Z]?\s[0-9][A-Z][A-Z]$","XXXXXXXX;X"), \
              "Germany" : ("^(\d{5}$)", "99999;X"), \
              "Canada" : ("(^+[A-VXY][0-9][A-Z] +[0-9][A-Z][0-9]$)", "XXX XXX;X"), \
              "France" : ("(^(([0-8][0-9])|(9[0-5]))[0-9]{3}$)","99999;X") , \
              "Italy" : ("^(\d{5})$", "99999;X"), \
              "Italia" : ("^(\d{5}$)", "99999;X"), \
              "Australia" : ("^(\d{3})$", "999;X"), \
              "Netherlands" : ("^[0-9]{4} [A-Z]{2}", "9999XX;X"), \
              "Spain" : ("^(\d{5}$)", "99999;X"), \
              "Denmark" : ("^([D-d][K-k])?( |-)?[1-9]{1}[0-9]{3}$","X999;X"), \
              "Sweden" : ("^(\d{3} \d{2})$","999 99;X"), \
              "Belgium" : ("^[1-9]{1}[0-9]{3}$","9999;X"), \
              "India" : ("^\d{6}$","999999;X")
              } 

    if QT_VERSION <= 263937 :
        isHD = False    
        langlocale = self.localeFullName
    else :
        isHD = True
        langlocale = []
        zLangLocaleFullName = self.localeFullName
        if zLangLocaleFullName.find("-")==-1: zLangLocaleFullName = zLangLocaleFullName.replace("-","_")
        if zLangLocaleFullName.find("_")==-1: zLangLocaleFullName+= "_%s" % (zLangLocaleFullName.upper())
        langlocale.append("%s" % (zLangLocaleFullName)) 

  
    for lid in range(QLocale.C, QLocale.LastLanguage + 1):
        lang = QLocale.Language(lid)
        countries = QLocale.countriesForLanguage(lang)
        for country in countries:
            locale = QLocale(lang, country)
            
            if isHD : label = locale.nativeCountryName()    
            else : label = "%s" % (QLocale.countryToString(country))
            
            if (label not in ListCountries and not label in ("", "Default")) :

               if langlocale == locale.name(): zCible = label
               if type(langlocale)== list :
                   if locale.name() in langlocale : zCible = label
               else :
                   if langlocale == locale.name(): zCible = label
               try :
                    ListCountries.append(label)
                    if DicoHasKey(ZIPREG, label):    
                       ListCountriesCode[label] = ZIPREG[label] 
                    else :  ListCountriesCode[label] = ("(^+[a-zA-Z_0-9\s]{3,10}$)","XXXxxxxxxx;X")  
               except : pass                     
    ListCountries.sort()
    
    if zCible != "" and zCible in ListCountries : indexCountry = ListCountries.index(zCible)
    return ListCountries, indexCountry, ListCountriesCode    

def MakeListLangues(self, zObj, mylang):
    myelts = ShortDic(self.languesDico)
    i = iIndex = 0
    for elt in myelts :
        if len(elt)==3 :
           zObj.addItem(self.languesDico[elt]['bibliographic'])
           if self.languesDico[elt]['english'] == mylang : iIndex = i
           i+= 1
    return iIndex

def MakeListTypeRessources(self):
    ListTypeRessources = (QApplication.translate("QSphere","Spatial Dataset", None, QApplication.UnicodeUTF8), \
                           QApplication.translate("QSphere","Spatial data series", None, QApplication.UnicodeUTF8), \
                           QApplication.translate("QSphere","Spatial data service", None, QApplication.UnicodeUTF8)
                  )
    return ListTypeRessources

def MakeListTemporalSystem(self):
    zListTemporalSystem = (QApplication.translate("QSphere","Ethiopian", None, QApplication.UnicodeUTF8), \
                           QApplication.translate("QSphere","Gregorian", None, QApplication.UnicodeUTF8), \
                           QApplication.translate("QSphere","Hegirian", None, QApplication.UnicodeUTF8), \
                           QApplication.translate("QSphere","Persan", None, QApplication.UnicodeUTF8), \
                           QApplication.translate("QSphere","Vikram Samvat", None, QApplication.UnicodeUTF8)
                  )
    return zListTemporalSystem
    

def MakeListEncoders(self):
    from encodings.aliases import aliases
    return aliases.keys()


def getRandowId(self):
    pop = string.ascii_letters + string.digits
    k=12
    generateId = ''.join( sample(pop, k) )
    today = datetime.datetime.now() 
    generateId+= today.strftime("_%m%d%HH%MM%SS")
    return generateId

def getisocodes_dict(data_path):
    data_path = os.path.dirname(__file__).replace("\\","/") +"/ressources/"+data_path
    D = {}
    if os.path.exists(data_path) :
        f = codecs.open(data_path, 'rb', 'utf-8')
        for line in f:
            iD = {}
            iD['bibliographic'], iD['terminologic'], iD['alpha2'], iD['english'], iD['french'] = line.strip().split('|')
            D[iD['bibliographic']] = iD
            if iD['terminologic']:  D[iD['terminologic']] = iD
            if iD['alpha2']: D[iD['alpha2']] = iD
            for k in iD: iD[k] = iD[k] or None
        f.close()
    return D

def MakeListFormats(self):
    zListFormats = {}
    for iDriver in range(ogr.GetDriverCount()):
        poDriver = ogr.GetDriver(iDriver)
        poValue = poDriver.GetName()
        driver = gdal.GetDriverByName("%s" % (poValue))
        zListFormats = SetEltListFormats(self, zListFormats, driver, poValue)

    for iDriver in range(gdal.GetDriverCount()):
        poDriver = gdal.GetDriver(iDriver)
        poValue = poDriver.ShortName
        driver = gdal.GetDriverByName("%s" % (poValue))
        zListFormats = SetEltListFormats(self, zListFormats, driver, poValue)

    zListitems = ShortDic(zListFormats)    
    return zListitems

def SetEltListFormats(self, zListFormats, driver, poValue):
       if driver :
            poDriverMetadata = driver.GetMetadata()
            if DicoHasKey(poDriverMetadata, gdal.DMD_LONGNAME):    
               poFormat = poDriverMetadata[gdal.DMD_LONGNAME]
               zListFormats[poFormat]=poFormat
            elif DicoHasKey(poDriverMetadata, gdal.DMD_MIMETYPE):    
               poFormat = poDriverMetadata[gdal.DMD_MIMETYPE]
               zListFormats[poFormat]= poFormat
            elif DicoHasKey(poDriverMetadata, gdal.DMD_EXTENSION):    
               poFormat = poDriverMetadata[gdal.DMD_EXTENSION] 
               zListFormats[poFormat]= poFormat
       else : zListFormats[poValue]=poValue
       return zListFormats

def MakeListLangs(self):
    languages=[]
    myLangs = [QLocale(lang).language() for lang in languages]
    for language in range(QLocale.C, QLocale.Chewa + 1):
        if language not in (QLocale.C, QLocale.Chewa + 1):
           if languages and (language not in languages): continue
           myLangs.append( language )
    return myLangs

def getUILangIndex(self):
    myLang = QLocale().language()
    myLangName = unicode( QLocale.languageToString( myLang ))
    return myLang, myLangName

def ShortDic(zDic):
    keylist = zDic.keys()
    keylist.sort()
    return keylist

def ReLOADTableView(self, config, zObj, zSection, percentDeb, zDelta):
    zInfos = config.get(zSection,'Indexes')
    zInfos = zInfos.rstrip()
    zInfosItem = config.get(zSection,'ItemCount')
    zItemCount = int(zInfosItem.rstrip())
    zDiff =  zObj.model().rowCount() - zItemCount
    percentDeb, zDelta = float(percentDeb), float(zDelta)

    if zSection == "tablelangues" :  data_icons = "%s/ressources/images/" % (os.path.dirname(__file__).replace("\\","/"))
    
    if zDiff > 0 :
       while zDiff > 0 :
           zObj.model().removeRow(zObj.model().rowCount()-1)
           zDiff-= 1 
    
    for j in range(zItemCount):
        zValues = config.get(zSection,'Item_%s' % (j))

        self.progressBar.setValue(percentDeb + (float(j)/float(zItemCount))*zDelta)
        
        zValuesTAB = None
        if zValues.find("|")!=-1: zValuesTAB = zValues.split("|")
        zColCount = len(zValuesTAB) if zValuesTAB != None else 1 
        for l in range(zColCount):
           if zSection == "tablelangues" :
              zIcon = QIcon("%s%s%s" % (data_icons, zValuesTAB[0], ".png"))
              item = QStandardItem() if l == 0 else QStandardItem(zIcon, "")
           else : item = QStandardItem()
           item.setText("%s" % (zValuesTAB[l])) if zValuesTAB != None else item.setText("%s" % zValues)
           if zSection == "groupedroits" : item.setToolTip(textwrap.fill("%s" % (zValuesTAB[zColCount-1]),50))
           if l == 0 :
               item.setCheckState(Qt.Unchecked)
               item.setCheckable(True)
           item.setEditable(False)
           zObj.model().setItem(j, l, item)

    if zInfos.find("|")!=-1 :
       zEltsDate = zInfos.split("|")
       for j in range(len(zEltsDate)): zObj.model().item(int(zEltsDate[j]), 0).setCheckState(Qt.Checked)
    else:
       if zInfos!="": zObj.model().item(int(zInfos), 0).setCheckState(Qt.Checked)
       

def ReLOADTableWidget(self, config, zObj, zSection):
    zTitle = "Information"
    zTest, zRows, zCols = AnaInfosObj(self, config, zObj, zSection)
    zRefCols = zObj.columnCount()
    self.cleanAllObj(zObj, False)
    if zRows == 0 : return
   
    if zTest :
        if zCols > zRefCols :
            zMsg = QApplication.translate("QSphere","Columns number invalide for Object : ", None, QApplication.UnicodeUTF8)
            SendMessage(self, zTitle , "%s%s" % (zMsg, zSection), QgsMessageBar.WARNING, self.duration_warning)
        else :
            zTest = True
            if zObj.rowCount()>0 :
                for k in range(zCols) :
                    zInfos = config.get(zSection,'zWidget_%s' % (k))
                    zClassWidgetInfos = zInfos.rstrip().split("|")
                    if zObj.cellWidget(0, k)!= None :
                        zClassWidgetInfo = "%s" % (zClassWidgetInfos[0])
                        if zClassWidgetInfo != zObj.cellWidget(0, k).metaObject().className():
                           if zObj.cellWidget(0, k).metaObject().className() != "MySimpleWidgetLineEdit" :
                              zTest = False
                              break

            if not zTest :
               zMsg = QApplication.translate("QSphere","Sub-Widgets not support in the current version of QSphere for : " , None, QApplication.UnicodeUTF8)
               SendMessage(self, zTitle , "%s%s" % (zMsg, zSection), QgsMessageBar.WARNING, self.duration_warning)
            else :

                if zRows > 0 :
                    zItem = {}
                   
                    for j in range(zRows):
                        try : zInfos = config.get(zSection,'zRow_%s' % (j))
                        except : break
                        zClassWidgetValues = zInfos.split("|")
                        
                        if len(zClassWidgetValues)< zCols : break


                        if not (zSection == "tablemotsclefso" and zClassWidgetValues[0] == "0") :
                            try : zObj.insertRow(j)
                            except : break 
                            
                            for k in range(zCols) :
                                zInfos = config.get(zSection,'zWidget_%s' % (k))
                                zClassWidgetInfos = zInfos.rstrip().split("|")
                                zClassWidgetInfo = "%s" % (zClassWidgetInfos[0])
                                if zClassWidgetInfo == "standard" :
                                    zItem[k] = QTableWidgetItem()
                                    zItem[k].setText("%s" % (zClassWidgetValues[k]))
                                    zObj.setItem(j,k, zItem[k])
                                else :
                                    if is_number_int(zClassWidgetValues[k]) and zClassWidgetInfos[0] not in("QLineEdit","MySimpleWidgetLineEdit", "MyWidgetLineEdit") : zValue = int(zClassWidgetValues[k])
                                    elif is_number_float(zClassWidgetValues[k]) and zClassWidgetInfos[0] not in("QLineEdit", "MySimpleWidgetLineEdit", "MyWidgetLineEdit") : zValue = float(zClassWidgetValues[k])
                                    else : zValue = "%s" % (zClassWidgetValues[k])

                                    if int(zClassWidgetInfos[2])!= -1 : objWidget = AddLineWidget(self, zObj, j,  k, int(zClassWidgetInfos[1]), int(zClassWidgetInfos[2]), zValue)                                      
                                    else : objWidget = AddLineWidget(self, zObj, j,  k, int(zClassWidgetInfos[1]), int(zClassWidgetInfos[2]), ("%s" % (zClassWidgetValues[k-1]), zValue))

                                if zObj.accessibleName() == "tablemotsclefso":
                                   zItemTarget = zObj.cellWidget(j, k)
                                   if zItemTarget != None : 
                                       for irole in range(zItemTarget.count()) : zItemTarget.setItemData(irole, 33, Qt.UserRole -1)
                                       zItemTarget.setItemData(0, 0, Qt.UserRole -1)
                                       if int(zClassWidgetValues[0])==0 : zItemTarget.setEnabled(False)

                        if zCols < zRefCols :
                          for k in range(zCols, zRefCols, 1) :
                              zParams = self.ParamsLineWidget[zObj.accessibleName()] 
                              zObjWidget = AddLineWidget(self, zObj, j, k, zParams[k][0], zParams[k][1], zParams[k][2])

                        if zObj.accessibleName() == "tableemprises":
                           zObj.setToolTip("%s" % (zObj.rowCount()-1))
                           self.DessCadre()

                        countItems(self, zObj.accessibleName(), zObj)

          
    else :
        zMsg = QApplication.translate("QSphere","Rows and Columns not find for Object : ", None, QApplication.UnicodeUTF8)
        SendMessage(self, zTitle , "%s%s" % (zMsg, zSection), QgsMessageBar.WARNING, self.duration_warning)



def countItems(self, zCible, zObj):
    zObjLabel = getWidget(self, "Lbl%s" % (zCible))
    if zObjLabel :
        if type(zObj) in (QTableWidget, MyTableWidget) : zObjLabel.setText("(<b><u>%s</u></b>) %s" % (zObj.rowCount(), zObjLabel.accessibleDescription()))
        elif type(zObj) in (MyWebComboBox, MyUserComboBox, QComboBox): zObjLabel.setText("(<b><u>%s</u></b>) %s" % (zObj.count(), zObjLabel.accessibleDescription()))

def AnaInfosObj(self, config, zObj, zSection):
    zTest, zRows, zCols = False, 0, 0
    zInfos = config.get(zSection,'zRows').rstrip()
    if zInfos!="":
       if convertSTR(zInfos, "int") :
          zRows = int(zInfos)
          zInfos = config.get(zSection,'zCols').rstrip()
          if zInfos!="":
             if convertSTR(zInfos, "int") :
                zCols = int(zInfos)
                zTest = True
    return zTest, zRows, zCols


def AddLineWidget(self, zObj, zRow,  zCol, zWidget, zSubType, zDefaultValue):

        makeOwner = False if zRow >= 0 and zCol >=0 else True
   
        if zWidget in (-1,-2) :
            if zWidget==-1 :
                ObjWidget = MySimpleWidgetLineEdit(self) if makeOwner else MySimpleWidgetLineEdit()
            else :
                ObjWidget = MySimpleWidgetLineEditST(self) if makeOwner else MySimpleWidgetLineEditST()
                
            zFullNameWidget = "%s_qlineedit_%s_%s" % (zObj.accessibleName(), zRow, zCol)
            if zDefaultValue !="" : ObjWidget.setText(zDefaultValue)
    
        if zWidget == 0 :
            ObjWidget = MyWidgetLineEdit(self) if makeOwner else MyWidgetLineEdit()
            ObjWidget.initType(zSubType)
            zFullNameWidget = "%s_mywidgetlineedit_%s_%s" % (zObj.accessibleName(), zRow, zCol)
            if zSubType == 3 : ObjWidget.setInputMask("EPSG:999999;X")
            elif zSubType == 2 : ObjWidget.setInputMask("99999;X")
            elif zSubType == 1 : ObjWidget.setInputMask("9999-99-99 9999-99-99;X")
            elif zSubType == 5 : ObjWidget.setInputMask("9999-99-99;X")
            ObjWidget.textChanged.connect(ObjWidget.VerifExpReg)
            ObjWidget.setText(zDefaultValue)
            
        if zWidget == 1 :
            ObjWidget = QPushButton(self)  if makeOwner else  QPushButton()
            zFullNameWidget = "%s_action_%s_%s" % (zObj.accessibleName(), zRow, zCol)
            zMsg = QApplication.translate("QSphere","Call the SRS QGIS Dialog box", None, QApplication.UnicodeUTF8) if zObj.accessibleName() == "tablescr" else QApplication.translate("QSphere","Call the QSphere Formats Dialog box", None, QApplication.UnicodeUTF8)
            myPathIconvView = getThemeIcon("projection.png") if zObj.accessibleName() == "tablescr" else getThemeIcon("format.png")
            ObjWidget.setToolTip(zMsg)
            ObjWidget.setIcon(QIcon(myPathIconvView))
            ObjWidget.setIconSize(QSize(18,16))
            ObjWidget.clicked.connect(self.CallQgsProjectionSelector) if zObj.accessibleName() == "tablescr" else ObjWidget.clicked.connect(self.CallFormatSelector)

        if zWidget == 2 :
           ObjWidget = MyComboBox(self) if makeOwner else MyComboBox()
           zFullNameWidget = "%s_combobox_%s_%s" % (zObj.accessibleName(), zRow, zCol)
           if zSubType == 0 :
               ObjWidget.addItems(self.ListOfRules)
               if zObj.objectName()=="tableroles" : ObjWidget.currentIndexChanged.connect(self.CheckInfosRoles) 
           elif zSubType == 1 :
               ObjWidget.addItems(self.ListOfThesaurus)
               for i in range(ObjWidget.count()) : ObjWidget.setItemData(i, 33, Qt.UserRole -1)
               ObjWidget.setItemData(0, 0, Qt.UserRole -1)
                              
               zFullNameWidget = "%s_ListItems_%s_%s" % (zObj.accessibleName(), zRow, zCol)
               ObjWidget.currentIndexChanged.connect(self.LoadListOfValues)
               if self.sender().objectName()!= "" : zDefaultValue = 1 
               
               
           elif zSubType == 2 : ObjWidget.addItems(self.ListTypeDates)
           elif zSubType == 3 : ObjWidget.addItems(self.ListDegres)
           elif zSubType == 4 : ObjWidget.addItems(self.ListFormats)
           elif zSubType == 5 :
               if not convertSTR(zDefaultValue, "int") :
                  if not zDefaultValue in self.listCountries : self.listCountries.append(u'%s' % (zDefaultValue))
                  zIndex = self.listCountries.index(u'%s' % (zDefaultValue))
               else : zIndex = zDefaultValue
               if zIndex < 0 : zIndex = 0
               ObjWidget.addItems(self.listCountries)
               ObjWidget.setEditable(True)
               ObjWidget.setCurrentIndex(zIndex)
               zFullNameWidget = "%s_ListItems_%s_%s" % (zObj.accessibleName(), zRow, zCol)
               ObjWidget.currentIndexChanged.connect(self.ChangePatternZipPostalCode)
               
           elif zSubType == -1 :
               zTemp = zDefaultValue
               zDefaultValue = zTemp[1]
               zCible = 1 if self.sender().objectName()!= "" and self.sender().objectName()!="OpenForm_tablemotsclefso" else zTemp[0]
               SizeW, zCols, iLine = LoadFile(self, ObjWidget, "None", "file:200:thesaurus_%s_%s.csv:0:0" % (zCible, self.parent.dicoLangs[self.parent.indexLang]), 1, None)
           ObjWidget.setCurrentIndex(zDefaultValue) if not ObjWidget.isEditable() else ObjWidget.setCurrentIndex(zIndex)
           if zObj.objectName()=="tableroles" and zSubType == 0 and zRow < 2 : ObjWidget.setEnabled(False)

           if not zObj.objectName().startswith("table"):
                 ObjWidget.view().setDragDropMode(QAbstractItemView.InternalMove)
                 ObjWidget.view().setDragDropMode(QAbstractItemView.OnlyDrag)
                 ObjWidget.setAcceptDrops(True)
           else : ObjWidget.view().setDragDropMode(QAbstractItemView.DragOnly)      

        if zWidget == 3 :
           zValue = (51.9, 41.36, -5.79, 9.56)
           zNameWidget = ("latituden", "latitudes", "longitudeo", "longitudee")
           ObjWidget = MySpinBox(self)  if makeOwner else MySpinBox()
           ObjWidget.initDoubleSpinBox(self, None) if makeOwner else ObjWidget.initDoubleSpinBox(zObj, self)

           if zCol in (2,3): PropertiesDoubleSpinBox(self, ObjWidget, 8, -180, 180, 1)
           else : PropertiesDoubleSpinBox(self, ObjWidget, 8, -90, 90, 1)
           zFullNameWidget = "%s_%s_%s_%s" % (zObj.accessibleName(), zNameWidget[zCol], zRow, zCol)
           if zDefaultValue==-1 : ObjWidget.setValue(zValue[zCol])
           else : ObjWidget.setValue(zDefaultValue)
           ObjWidget.setMouseTracking(True)
           ObjWidget.setKeyboardTracking(False)
           if self.objectName() == "DialogMetaData" : ObjWidget.valueChanged.connect(self.DessCadre) 
               

        if zWidget == 4 :
           #ObjWidget = MySpinBox(self, self) if makeOwner else MySpinBox(zObj, self)
           ObjWidget = MySpinBox(self)  if makeOwner else MySpinBox()
           ObjWidget.initDoubleSpinBox(self, None) if makeOwner else ObjWidget.initDoubleSpinBox(zObj, self)
           zFullNameWidget = "scalebox_line_%s" % (zRow)
           if zObj.parent().children()[0].isChecked(): 
               PropertiesDoubleSpinBox(self, ObjWidget, 0, 0, 10000000, 1000)
               if zDefaultValue==-1 : ObjWidget.setValue(25000)
               else : ObjWidget.setValue(zDefaultValue)
           else:
               PropertiesDoubleSpinBox(self, ObjWidget, 4, 0, 1000, 10)
               if zDefaultValue==-1 : ObjWidget.setValue(float(2.0))
               else : ObjWidget.setValue(zDefaultValue)


        if zWidget == 5 :
           ObjWidget = QPushButton(self)  if  makeOwner else QPushButton()
           zFullNameWidget = "%s_action_%s" % (zObj.accessibleName(), zRow)
           myPathIconvView = getThemeIcon("voir.png")
           ObjWidget.setIcon(QIcon(myPathIconvView))
           ObjWidget.setIconSize(QSize(18,16))
           ObjWidget.clicked.connect(self.LoadGeoLocalisator)

        if zWidget == 6 :
           ObjWidget = MyCheckBox(self)  if  makeOwner else MyCheckBox()
           zFullNameWidget = "%s_action_%s" % (zObj.accessibleName(), zRow)
           ObjWidget.setToolTip(QApplication.translate("QSphere","From controlled Vocabulary ", None, QApplication.UnicodeUTF8))
           ObjWidget.toggled.connect(self.ChangeAccessibility)
           if type(zDefaultValue)!= int : zDefaultValue = 2
           ObjWidget.setCheckState(zDefaultValue)
           
           
        if zWidget == 7 :
            if zObj.accessibleName() in ("tableformats","tablelocalisator", "tablescr"):
               typeObj = 6
               zIcon = getThemeIcon("supprimer.png") if zRow > 0 else getThemeIcon("supprimernone.png")
               zToolTip = QApplication.translate("QSphere","Delete the current line", None, QApplication.UnicodeUTF8) if zRow > 0 else QApplication.translate("QSphere","Can't delete the first line", None, QApplication.UnicodeUTF8)
            zNameButton = "Effacer_%s_%s_%s" % (typeObj, zObj.accessibleName(), zRow)
            ObjWidget = MyPushButton(self) if makeOwner else MyPushButton()
            ObjWidget.initPushButton(24, 24, 0, 0, zNameButton, "", zToolTip, True, zIcon, 24, 24, True)
            zFullNameWidget = "%s_mypushbutton_%s" % (zObj.accessibleName(), zRow)

            if zObj.accessibleName() in ("tableformats","tablelocalisator", "tablescr"):
               ObjWidget.clicked.connect(self.DelLineIndex) if zRow > 0 else ObjWidget.clicked.connect(self.DelLine)
               

        ObjWidget.setObjectName(zFullNameWidget) 
        ObjWidget.setAccessibleName(zFullNameWidget)
        ObjWidget.setAccessibleDescription("%s|%s" % (zWidget, zSubType))

        if not makeOwner : zObj.setCellWidget(zRow, zCol, ObjWidget)

        return ObjWidget

def GetAllItems(zCombo): return [zCombo.itemText(i) for i in range(zCombo.count())]

def PropertiesDoubleSpinBox(self, zObj, zDec, zMin, zMax, zStep):
        zObj.setDecimals(zDec)                
        zObj.setMinimum(zMin)
        zObj.setMaximum(zMax)                
        zObj.setSingleStep(zStep)

def ReturnDate(self, zObj):
    pydate = zObj.selectedDate()
    TheDate = "%s" % (pydate.toString('yyyy-MM-dd'))
    return TheDate            


def fileRessourceExist(self, zFile):
    #MAKE A FUNCTION TO RETURN FILE IF EXISTS
    #TWO TESTS : TEST LOCAL RESSOURCE
    #IF DONT EXIST, TEST FOR GENERIC ENGLISH RESSOURCE
    #ELSE RETURN NONE
    zPath = CorrigePath(os.path.dirname(__file__))
    zPath = zPath.replace("\\","/")
    zFileName = zFile.replace("file:///","")
    zFileName = zFile.replace("file:","")

    if os.path.exists(zFileName) : return True, zFileName

    zFileCSV = "%s%s" % (zPath, zFileName)
    if os.path.exists(zFileCSV) : return True, zFileCSV

    Nb_SubElt, i = CountCaractere(zFileName, "_", False, False), 0
    if Nb_SubElt > 0 :
        zRacFileName, zListe = "", zFileName.split(".")[0].split("_")
        i=0
        while i <= (Nb_SubElt-1) :
            zRacFileName+= "_%s" % (zListe[i]) if i > 0 else "%s" % (zListe[i])
            i+=1
        PosExtension = len(zFileName.rsplit("."))
        zFileExtension = zFileName.rsplit(".")[PosExtension-1]
        zFileCSV = "%s%s.%s" % (zPath, zRacFileName, zFileExtension)

        if os.path.exists(zFileCSV) : return True, zFileCSV

    return False, ""

def LoadData(self, zFile, zType):
    zListData, zMListData, i = [], {} , 0
    zTest, zFileCSV = fileRessourceExist(self, zFile)
    
    if zFileCSV!= "" :
       f = open(zFileCSV, "r")
       while 1:
             zText = f.readline()
             if zText == "" : break
             if zText.find(";")!=-1 :
                zValue = zText.split(";")
                zVal = zValue[1].replace("\"","").rstrip()
                try : zVal = zVal.decode('utf-8')
                except : pass
                zListData.append("%s" % (zVal))
                zMListData[i]= zValue[0].replace("\"","").rstrip()
             else:
                zVal = zText.replace("\"","").rstrip()
                try : zVal = zVal.decode('utf-8')
                except : pass                
                zListData.append("%s" (zVal))
             i+= 1
       f.close()
    else:
       if zType == "roles":
           zItem0 = QApplication.translate("QSphere","Owner", None, QApplication.UnicodeUTF8)
           zItem1 = QApplication.translate("QSphere","Point of contact", None, QApplication.UnicodeUTF8)
           zListData = [zItem0, zItem1]
           zMListData[0]="owner"
           zMListData[1]="pointOfContact"
       elif zType == "langues" :
           zItem0 = QApplication.translate("QSphere","French", None, QApplication.UnicodeUTF8)
           zListData = [zItem0, zItem0]
           zMListData[0]="fra"
           zMListData[1]="fre"
       elif zType == "thesaurus":
           zListData = ["GEMET INSPIRE Themes"]
           zMListData[0]="2008-06-01"
           
    return zListData, zMListData

def LoadSimpleData(self, zFile):
    zListData = []
    zTest, zFileCSV = fileRessourceExist(self, zFile)
    
    if zFileCSV!= "" :
           f = open(zFileCSV, "r")
           while 1:
                zText = f.readline()
                if zText == "" : break
                zVal = zText.replace("\"","").rstrip()
                try : zVal = zVal.decode('utf-8')
                except : pass                     
                zListData.append("%s" % (zVal))
    return zListData
    

def LoadDefautValue(self, zFile):
    zMListData, i = {}, 0
    zTest, zFileCSV = fileRessourceExist(self, zFile)
    
    if zFileCSV!= "" :
           f = open(zFileCSV, "r")
           while 1:
                 zText = f.readline()
                 if zText == "" : break
                 if zText.find(";")!=-1 :
                    zValue = zText.split(";")
                    zListData = []
                    for j in range(len(zValue)):
                        zVal = zValue[j].replace("\"","").rstrip()
                        try : zVal = zVal.decode('utf-8')
                        except : pass                        
                        zListData.append("%s" % (zVal))
                    zMListData[i] = zListData
                 else:
                    zListData = []
                    zVal = zText.replace("\"","").rstrip()
                    try : zVal = zVal.decode('utf-8')
                    except : pass                     
                    zListData.append("%s" % (zVal))
                    zMListData[0] = zListData
                 i+= 1
           f.close()
    return zMListData

def LoadFile(self, zObj, nameObj, zCible, typeObj, zModel):
    iLine, zCols = 0, 0
    if zModel == None : zModel = QStandardItemModel()
    zCible = zCible.split(":")
    zTest, zFileCSV = fileRessourceExist(self, "/ressources/%s" % (zCible[2]))
    zUseModel = int(zCible[3])
    zUseIcons = int(zCible[4])

    if zFileCSV!= "" :
       if os.path.exists(zFileCSV): 
           f = open(zFileCSV, "r")
           while 1:
               zText = f.readline()
               if zText == "" : break
               
               zValue = zText.split(";")
               if zCols == 0 : zCols = len(zValue)
               if zUseModel == 1 :
                   if nameObj == "tablegroupedroits" : zToolTip = zValue[1].replace("\"","").replace(",","\n").replace(":",":\n").rstrip()
                   for i in range(zCols):
                       item = QStandardItem(True)
                       zTextItem = zValue[i].replace("\"","").rstrip()

                       try : zTextItem = zTextItem.decode('utf-8')
                       except : pass
                       
                       item.setText(zTextItem)
                       if i == 0 and typeObj == 3:    
                          item.setCheckable(True)
                          item.setCheckState(Qt.Unchecked)
                          if nameObj == "tablelangues" and zTextItem.startswith(self.langueTR): item.setCheckState(Qt.Checked)
                          
                       if nameObj == "tablegroupedroits" : item.setToolTip(textwrap.fill(zToolTip, 50)) 

                       item.setSelectable(True)
                       item.setDragEnabled(True) 
                       
                       item.setEditable(False)
                       zModel.setItem(iLine, i ,item)
               else:
                   if  typeObj == 1:
                       try : zVal = ("%s" % (zValue[0].decode('utf-8')))
                       except : zVal = ("%s" % (zValue[0]))
                       zVal = zVal.replace("\"","").rstrip()
                       if zUseIcons == 1 :
                           menuIcon = getThemeIcon("ressources/images/%s.png" % (zVal))
                           zObj.addItem(QIcon(menuIcon), zValue[1].replace("\"","").rstrip(), "%s" % (zVal) )
                       else :    
                           zObj.addItem("%s" % (zVal)) 
               iLine+= 1         
           f.close()

    if zUseModel == 1 :   
        view = QTableView()
        view.horizontalHeader().setVisible(False) 
        view.verticalHeader().setVisible(False)
        view.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        view.setSelectionBehavior(QAbstractItemView.SelectItems) 
        view.setSelectionMode(QAbstractItemView.SingleSelection)
        view.setDragDropMode(QAbstractItemView.DragOnly)        
        select = view.selectionModel()

        if typeObj == 1 :
            zObj.setView(view)
            zObj.setModel(zModel)
            zObj.show()

        if nameObj == "tablecategories" : zModel.itemChanged.connect(self.SelectKeyWord)

    return int(zCible[1]), zCols, iLine

#----------------------------------------------
#FUNCTION TO MAKEWINDOWICO AND WINDOWPROPERTIES
#----------------------------------------------
def MakeWindowIcon(qtWindow, sIcon):
    zIcon = getThemeIcon(sIcon)
    if zIcon != "" : qtWindow.setWindowIcon(QIcon(zIcon)) 

def MakePropertiesForWindow(targetObj, sourceObj):
    targetObj.iface = sourceObj.iface
    targetObj.MainPlugin = sourceObj.MainPlugin
    
    targetObj.langue = sourceObj.langue
    targetObj.languageIndex = sourceObj.languageIndex
    targetObj.langs = sourceObj.langs
    targetObj.languesDico = sourceObj.languesDico
    targetObj.formats = sourceObj.formats
    targetObj.listCodecs = sourceObj.listCodecs
    targetObj.listTemporalSystem = sourceObj.listTemporalSystem
    targetObj.listTypeRessources = sourceObj.listTypeRessources
    targetObj.listCountries = sourceObj.listCountries
    targetObj.indexCountry = sourceObj.indexCountry
    targetObj.localeFullName = sourceObj.localeFullName
    targetObj.langueTR = targetObj.localeFullName[0:2] if targetObj.localeFullName[0:2] in ("fr", "it", "fi", "es", "de") else "en"
    targetObj.listCountriesCode = sourceObj.listCountriesCode
    targetObj.ListOfRules  = sourceObj.ListOfRules
    targetObj.DicoListOfRules = sourceObj.DicoListOfRules
    targetObj.dicoLangs  = sourceObj.dicoLangs
    targetObj.indexLang = sourceObj.indexLang
    

#--------------------------------------
# FUNCTIONS FOR CORRECTION IMAGES PATH 
#--------------------------------------
def getThemeIcon(theName):
    dirs = list(sys.path)
    dirs.insert(0, "%s%s" % (CorrigePath(os.path.dirname(__file__)),"icons/"))
    dirs.insert(0, "%s%s" % (CorrigePath(os.path.dirname(__file__)),"qsphere/"))
    dirs.insert(0, "%s%s" % (CorrigePath(QgsApplication.pluginPath()),"qsphere/icons/"))
    for dir in dirs :
        myPath = CorrigePath(dir)
        myIconPath = "%s%s" % (myPath, theName)
        if QFile.exists(myIconPath): return myIconPath
    return ""

def CorrigePath(nPath):
    nPath = "%s" % (nPath)
    a = len(nPath)
    subC = "/"
    b = nPath.rfind(subC, 0, a)
    return ("%s/" % (nPath)) if a != b else nPath 

#-------------------------------------
# FUNCTIONS LOADER IMAGES FOR QSPHERE 
#-------------------------------------
def listdirectory(self, path):
    LstImages = "<table class='comment'>"
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames: LstImages+= scandirectory(self, os.path.join(dirname, filename))
    LstImages+= "</table>"    
    return LstImages       
            
def scandirectory(self, currentFile):
    zHTML = ""
    if os.path.exists(currentFile):
        if os.path.isfile(currentFile):
           zName = "%s" % (os.path.basename(currentFile))
           textension = os.path.splitext(currentFile)
           extension = textension[len(textension)-1].lower()
           if zName.find("qsphere_")!=-1 and extension!="" and extension == ".png":
              zHTML = "<tr><td><img src='./../../icons/%s'></td><td>%s</td></tr>" % (zName, zName) 
    return zHTML

def IsCorrectLayer(layer, zEnc):
    if not layer: return False
    if not layer.type() == layer.VectorLayer: return False
    if not layer.isValid() : return False
    if not zEnc :
        if layer.geometryType() != QGis.Point and layer.geometryType() != QGis.Line and layer.geometryType() != QGis.Polygon: return False
    else:
        if not layer.geometryType() == QGis.Point : return True
    return True

#-------------------------------------------------
#FUNCTION TEST IF NUMBER TYPE INT OR SUPPORT FLOAT
#-------------------------------------------------     
def is_number_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#-----------------------------------------------
#FUNCTION TEST IF NUMBER TYPE INT OR SUPPORT INT
#-----------------------------------------------    
def is_number_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#---------------------------------------
#FUNCTION TEST IF EXP IS A VALID NUMBER    
#---------------------------------------
def IsValideNumber(s, isCoord) :
    if not s : return "F"
    if is_number_int(s) :
       if s == 0 or (s == -9999 and isCoord) : return "F"
       else : return "T"
    if is_number_float(s) :
       if s == 0.0 or (s == -9999.0 and isCoord) : return "F"
       else : return "T"

#---------------------------------
# FUNCTION TO COUNT SUBSTR IN STR
#---------------------------------
def CountCaractere(zStr, zCar, ignoreCase, wholeword):
    CountCaractere = 0
    import re
    if wholeword == True : zCar = (r'\b%s\b' % (zCar))
    if ignoreCase == False : CountCaractere = len(re.findall(re.compile(zCar, re.IGNORECASE), zStr))
    else : CountCaractere = len(re.findall(zCar, zStr)) 
    return CountCaractere

#---------------------------------
#FUNCTION TEST CONVERT EXPRESSION   
#---------------------------------
def convertSTR(s, zType):
    if zType == "int" :
        try :
            zText = int(s)
            return True
        except : return False
    elif zType == "float" :        
        try :
            zText = float(s)
            return True
        except : return False
    else: return False


#---------------------------------
#FUNCTION TEST IF NUMBER TYPE FLOAT 
#---------------------------------   
def is_number_reallyfloat(s): return (type(s)== float) 

#-----------------------------------
#FUNCTION TEST IF NUMBER TYPE INT 
#-----------------------------------     
def is_number_reallyint(s): return (type(s)== int)

def makeHelp(self):
    zEltName = QApplication.translate("QSphere","user manual", None, QApplication.UnicodeUTF8)
    zFileName = "help/qsphere_%s_%s.pdf" % (zEltName, self.dicoLangs[self.indexLang])
    zTest, zFullFileName = fileRessourceExist(None, zFileName)
    
    if zTest : 
        try : webbrowser.open(zFullFileName)
        except : zTest = False

    if not zTest :
      zTitle = QApplication.translate("QSphere","Warning", None, QApplication.UnicodeUTF8)
      zSuccess = QApplication.translate("QSphere","Error", None, QApplication.UnicodeUTF8)
      SendMessage(self, zTitle , "%s<br>%s" % (zSuccess, zFileName), QgsMessageBar.WARNING, 5)

#------------------------
# FUNCTION QGSMESSAGEBAR
#------------------------
def SendMessage(self, zTitle , zMsg, zLevel, zDuration):
      zPicto = getThemeIcon("qsphere_msgbox.png") 
      self.editorMSG = MyTextEdit()
      self.editorMSG.initTextEdit(680, 240, 5, 150, "ViewLOG", True, False, True, False, False)
      zHTML = "<html><table border='0'><tr valign='middle'><td><img src='%s'></td><td><h4>%s</h4></td></tr></table></html>" % (zPicto, zMsg.replace("\\n", "<br>"))
      self.editorMSG.setText(zHTML)
      self.editorMSG.setGeometry(50,5, 200,50)
      try : zDuration = int(zDuration)
      except : zDuration = 2
      if zLevel == QgsMessageBar.WARNING : self.editorMSG.setStyleSheet("color: black; background-color: #FFC800; border: 0px")
      elif zLevel == QgsMessageBar.INFO : self.editorMSG.setStyleSheet("color: black; background-color: #E7F5FE; border: 0px")
      self.barInfo.pushWidget(self.editorMSG, zLevel, int(zDuration))
      return self.editorMSG

#------------------------
# FUNCTION GETINDEXLAYER
#------------------------
def GetLayerCombo(self, zCombo, zText):
   zLayer, zModel, index = None, zCombo.model(), 0
   for i in range(zCombo.count()):
       if zModel.item(i,1).text()==zText :
          index = i  
          break
   return index

#------------------------------
# FUNCTION FIXELABELSFILEDIALOG
#------------------------------
def FixeLabelsFileDialog(self, MyFileDialog, context, hasName):

    MyFileDialog.setLabelText(QFileDialog.Accept, QApplication.translate("QSphere","Open", None, QApplication.UnicodeUTF8)) if context == 0 else MyFileDialog.setLabelText(QFileDialog.Accept, QApplication.translate("QSphere","Save", None, QApplication.UnicodeUTF8))
    MyFileDialog.setLabelText(QFileDialog.Reject, QApplication.translate("QSphere","Cancel", None, QApplication.UnicodeUTF8))        
    MyFileDialog.setLabelText(QFileDialog.FileName, "%s : " % (QApplication.translate("QSphere","Name", None, QApplication.UnicodeUTF8))) if hasName else MyFileDialog.setLabelText(QFileDialog.FileName, QApplication.translate("QSphere","Folder : ", None, QApplication.UnicodeUTF8))
    MyFileDialog.setLabelText(QFileDialog.FileType, QApplication.translate("QSphere","Filters : ", None, QApplication.UnicodeUTF8))
    MyFileDialog.setLabelText(QFileDialog.LookIn, QApplication.translate("QSphere","Folder : ", None, QApplication.UnicodeUTF8))

#------------------------------
# FUNCTION MARKERTEXT
#------------------------------
def MarkerText(self, sText):
  sText = sText.replace("\n", "<br>")
  pos = sText.find("=")
  if pos != -1 :
     tText = sText.split("=")
     text0 = sText[0:pos-1]
     text1 = sText[pos+1:]
     sText = "<font style='color:#009900;'>%s</font> <b>=</b> %s" % (text0, text1) #(tText[0], tText[1])
  else :   
    sText = sText.replace("[", "[<font style='color:#FFFFCC; background-color: #0000ff; font-weight:bold'>")
    sText = sText.replace("]", "</font>]")
  return sText

#------------------------------
# FUNCTION MAKEFILEINFOSTOHTML
#------------------------------
def MakeFileInfosToHTML(self, zFile, zSuffixe):

   HTML = "<style>table {border-spacing: 0px; width: 100%}"
   HTML+= "td {padding: 5px 30px 5px 10px;border-spacing: 0px;font-size: 90%;margin: 0px;}"
   HTML+= "td {color: #737476;text-align: left;background-color: #ffffcc;border-top: 1px solid #f1f8fe; border-bottom: 1px solid #0099ff; border-right: 1px solid #0099ff;}"
   HTML+= "</style>" 

   HTML+= "<h1>%s</h1>" % (QApplication.translate("QSphere", "Double clic to open file !", None, QApplication.UnicodeUTF8))
   HTML+= "<table>"

   zIcon = getThemeIcon("%s.png" % (zSuffixe))
   if zIcon == "" : zIcon = getThemeIcon("unknow.png")
   
   HTML+= "<tr valign='middle'><td><img src='%s' width=32 height=32> %s :</td><td><h3>%s</h3></td></tr>" % (zIcon, QApplication.translate("QSphere", "file", None, QApplication.UnicodeUTF8), zFile.baseName())
   HTML+= "<tr><td>%s :</td><td>%s</td></tr>" % (QApplication.translate("QSphere", "Folder", None, QApplication.UnicodeUTF8), os.path.dirname(zFile.filePath()))
   owner = QApplication.translate("QSphere","Unknow", None, QApplication.UnicodeUTF8) if zFile.owner() == "" else zFile.owner()
   HTML+= "<tr><td>%s :</td><td>%s</td></tr>" % (QApplication.translate("QSphere", "Owner", None, QApplication.UnicodeUTF8), owner)
   HTML+= "<tr><td>%s :</td><td>%s</td></tr>" % (QApplication.translate("QSphere", "Date creation", None, QApplication.UnicodeUTF8), zFile.created().toString('yyyy-MM-dd hh:mm:ss'))
   HTML+= "<tr><td>%s :</td><td>%s</td></tr>" % (QApplication.translate("QSphere", "Date last modification", None, QApplication.UnicodeUTF8), zFile.lastModified().toString('yyyy-MM-dd hh:mm:ss'))
   HTML+= "<tr><td>%s :</td><td>%s</td></tr>" % (QApplication.translate("QSphere", "Date last access", None, QApplication.UnicodeUTF8), zFile.lastRead().toString('yyyy-MM-dd hh:mm:ss'))
   HTML+= "<tr><td>%s :</td><td>%s</td></tr>" % (QApplication.translate("QSphere", "Size", None, QApplication.UnicodeUTF8), GetFormatedSize(zFile.size()))
   HTML+= "<tr><td colspan=2><u>%s</u> :<ul>" % (QApplication.translate("QSphere", "Rights", None, QApplication.UnicodeUTF8))

   if (zFile.permission(QFile.ReadUser))  : HTML+= "<li>%s</li>" % (QApplication.translate("QSphere","I can read the file", None, QApplication.UnicodeUTF8))
   if (zFile.permission(QFile.WriteUser)) : HTML+= "<li>%s</li>" % (QApplication.translate("QSphere","I can change the file", None, QApplication.UnicodeUTF8))
   if (zFile.permission(QFile.ReadGroup)) : HTML+= "<li>%s</li>" % (QApplication.translate("QSphere","My group can read the file", None, QApplication.UnicodeUTF8))
   if (zFile.permission(QFile.WriteGroup)): HTML+= "<li>%s</li>" % (QApplication.translate("QSphere","My group can change the file", None, QApplication.UnicodeUTF8))   
   if (zFile.permission(QFile.WriteOther)): HTML+= "<li>%s</li>" % (QApplication.translate("QSphere","Orthers can change the file", None, QApplication.UnicodeUTF8))   

   HTML+= "</ul></td></tr></table>"
   HTML = "<img src='%s'><br>%s" % (getThemeIcon("qsphere_fileinfos.png"), HTML)

   return HTML


#------------------------------
# FUNCTION GETFORMATEDSIZE
#------------------------------
def GetFormatedSize(size, precision=2):
    suffixes=["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    suffixIndex = 0
    while size > 1024:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f %s" % (precision,size,suffixes[suffixIndex])

#------------------------------
# FUNCTION FILEISRASTER
#------------------------------
def FileIsRaster(fichier):
    isRaster = gdal.Open(fichier)
    return isRaster


