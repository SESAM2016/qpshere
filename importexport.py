# -*- coding:utf-8 -*-

import ConfigParser
import os.path
from qsphere_tools import *

from PyQt4 import QtCore, QtGui
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from qgis.core import *
from qgis.gui import *

import urllib
import datetime

   
#==================================================
# FUNCTIONS TO LOAD (IMPORT) AND SAVE / EXPORT QSP
#==================================================
#==================================================
# NEW FORMAT XQSP - XML QSP PROJECT
#==================================================
def SaveXQSP(self, zFile):
    zIndex = self.tabWidget.currentIndex()
    zLOG = open(zFile, "w")
    zTabs = self.tabWidget.count()
    WriteInLOG(zLOG, '<?xml version="1.0" encoding="UTF-8"?>\n')
    WriteInLOG(zLOG, '<gmd:MD_Metadata xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://schemas.opengis.net/iso/19139/20060504/gmd/gmd.xsd" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" xmlns:xlink="http://www.w3.org/1999/xlink">\n')
    WriteInLOG(zLOG, '<gmd:qsphereproject>\n')
    WriteInLOG(zLOG, '\t<gco:file>\n')
    WriteInLOG(zLOG, '\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zFile))
    WriteInLOG(zLOG, '\t</gco:file>\n')
    WriteInLOG(zLOG, '\t<gmd:language>\n')
    WriteInLOG(zLOG, '\t\t<gmd:LanguageCode codeList="http://www.loc.gov/standards/iso639-1/" codeListValue="%s">%s</gmd:LanguageCode>\n' % (self.langueTR, self.langueTR))
    WriteInLOG(zLOG, '\t</gmd:language>\n')
    MakeDateStampXML(self, 1, False,  None)
    WriteInLOG(zLOG, '</gmd:qsphereproject>\n')

    for i in range(zTabs):
        self.tabWidget.setCurrentIndex(i)
        zTab = self.tabWidget.currentWidget()
       
        WriteInLOG(zLOG, "\t<%s id='%s' name='%s'>\n" % (zTab.metaObject().className(), i, urllib.quote(zTab.accessibleName())))

        zObjs = zTab.children()
        for j in range(len(zObjs)):
            zNameObj = "%s" % (zObjs[j].accessibleName())
            if zNameObj != "" and (not zObjs[j].metaObject().className()=="QLabel") and zNameObj.find("help_")==-1 and zNameObj.find("Ajouter_")==-1 and zNameObj.find("Effacer_")==-1 :
                zClassObjName = "%s" % (zObjs[j].metaObject().className()) 
                WriteInLOG(zLOG, "\t\t<%s name='%s' x='%s' y='%s' width='%s' height='%s'>\n" % (zClassObjName, urllib.quote(zObjs[j].accessibleName()), zObjs[j].x(), zObjs[j].y(), zObjs[j].width(), zObjs[j].height()))

                if zClassObjName=="QCalendarWidget" : MakeDateStampXML(self, 3, False,  zObjs[j])
                elif zClassObjName in ("QTextEdit", "MyTextEdit") :
                    WriteInLOG(zLOG, '\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (urllib.quote(EncodeText(zObjs[j].toPlainText()))))
                elif zClassObjName in ("QLineEdit", "MySimpleWidgetLineEdit", "MyWidgetLineEdit") :
                    WriteInLOG(zLOG, '\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (urllib.quote(EncodeText(zObjs[j].text()))))
                elif zClassObjName=="QTableView" :  MakeBlocXQSPTableView(self, zObjs[j], zLOG, 3, False)
                elif zClassObjName in ("QTableWidget", "MyTableWidget") : MakeBlocQSPTableWidget(self, zObjs[j], zLOG, 3, False)
                elif zClassObjName in ("QComboBox", "MyComboBox") : MakeBlocXQSPComboBox(self, zObjs[j], zLOG, 3, False)
                elif zClassObjName=="QGroupBox" :
                     zChildren = zObjs[j].children()
                     for i in range(len(zChildren)):
                         zChild = zChildren[i]
                         zChildClassName = "%s" % (zChild.metaObject().className())
                         if zChildClassName == "QRadioButton" :
                            WriteInLOG(zLOG, '\t\t\t<%s id="%s" name="%s" checked="%s">\n' % (zChild.metaObject().className(), i, zChild.accessibleName(), (zChild.isChecked())))  
                            WriteInLOG(zLOG, '\t\t\t</%s>\n' % (zChild.metaObject().className()))
                         elif zChildClassName in ("QComboBox", "MyComboBox") : MakeBlocXQSPComboBox(self, zChild, zLOG, 3, True)
                         elif zChildClassName == "QTableView": MakeBlocXQSPTableView(self, zChild, zLOG, 3, True)
                         elif zChildClassName in ("QTableWidget", "MyTableWidget") : MakeBlocQSPTableWidget(self, zChild, zLOG, 3, True)
                             
                    
                WriteInLOG(zLOG, "\t\t</%s>\n" % (zObjs[j].metaObject().className()))

        WriteInLOG(zLOG, "\t</%s>\n" % (zTab.metaObject().className()))
        
    WriteInLOG(zLOG, "</gmd:MD_Metadata>\n" )
    self.tabWidget.setCurrentIndex(zIndex) #self.listeOnglets.setCurrentIndex(zIndex)


def MakeBlocXQSPCheckBox(self, zObj, zLOG, zTab, isSubWidget):
    sTab=""
    for k in range(zTab): sTab+="\t"

    if isSubWidget:
       sTabRef = sTab
       sTab+="\t"         
       WriteInLOG(zLOG, "%s<%s name='%s' checked='%s'>\n" % (sTabRef, zObj.metaObject().className(), urllib.quote(zObj.accessibleName()), zObj.checkState()()))
       
    WriteInLOG(zLOG, '%s\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zWidget.text()))   

    if isSubWidget:  WriteInLOG(zLOG, "%s</%s>\n" % (sTabRef, zObj.metaObject().className()))
    

def MakeBlocXQSPComboBox(self, zObj, zLOG, zTab, isSubWidget):
    sTab=""
    for k in range(zTab): sTab+="\t"

    if isSubWidget:
       sTabRef = sTab
       sTab+="\t"         
       WriteInLOG(zLOG, "%s<%s name='%s' editable='%s'>\n" % (sTabRef, zObj.metaObject().className(), urllib.quote(zObj.accessibleName()), zObj.isEditable()))
       
    for k in range(zObj.count()):
        WriteInLOG(zLOG, '%s\t<item id="%s" checked="%s">\n' % (sTab, k, (zObj.currentIndex()==k)))
        try : zText = urllib.quote(EncodeText(zObj.itemText(k)))
        except : zText = EncodeText(zObj.itemText(k))
        WriteInLOG(zLOG, '%s\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zText))
        WriteInLOG(zLOG, '%s\t</item>\n' % (sTab))
        
    if isSubWidget:  WriteInLOG(zLOG, "%s</%s>\n" % (sTabRef, zObj.metaObject().className()))


def MakeBlocQSPTableWidget(self, zObj, zLOG, zTab, isSubWidget):
    sTab=""
    for k in range(zTab): sTab+="\t"

    if isSubWidget:
       sTabRef = sTab
       sTab+="\t"         
       WriteInLOG(zLOG, "%s<%s name='%s'>\n" % (sTabRef, zObj.metaObject().className(), urllib.quote(zObj.accessibleName())))
    
    for k in range(zObj.rowCount()):
        WriteInLOG(zLOG, '%s<row id="%s">\n' % (sTab, k))
        for l in range(zObj.columnCount()):
            WriteInLOG(zLOG, '%s\t<col id="%s">\n' % (sTab, l))

            zWidget = zObj.cellWidget(k, l)
            if zWidget != None :
                  if zWidget.metaObject().className() in ("QComboBox", "MyComboBox") :  MakeBlocXQSPComboBox(self, zWidget, zLOG, (zTab+2), True)
                  elif zWidget.metaObject().className() in ("QCheckBox", "MyCheckBox") : WriteInLOG(zLOG, '%s\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zWidget.checkState()))
                  elif zWidget.metaObject().className()=="MySpinBox" : WriteInLOG(zLOG, '%s\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zWidget.value()))
                  elif zWidget.metaObject().className() in ("QPushButton", "MyButton") : WriteInLOG(zLOG, '%s\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, "action"))
                  
                  else : WriteInLOG(zLOG, '%s\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, urllib.quote(EncodeText(zWidget.text()))))
            else:
                  WriteInLOG(zLOG, '%s\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, urllib.quote(EncodeText(zObj.item(k, l).text()))))

            WriteInLOG(zLOG, '%s\t</col>\n'  % (sTab))
        WriteInLOG(zLOG, '%s</row>\n' % (sTab))

    if isSubWidget:  WriteInLOG(zLOG, "%s</%s>\n" % (sTabRef, zObj.metaObject().className()))
    
def MakeBlocXQSPTableView(self, zObj, zLOG, zTab, isSubWidget):
    sTab=""
    for k in range(zTab): sTab+="\t"

    if isSubWidget:
       sTabRef = sTab
       sTab+="\t"         
       WriteInLOG(zLOG, "%s<%s name='%s'>\n" % (sTabRef, zObj.metaObject().className(), urllib.quote(zObj.accessibleName())))
    
    for k in range(zObj.model().rowCount()):
        WriteInLOG(zLOG, '%s<row id="%s" checked="%s">\n' % (sTab, k, (zObj.model().item(k, 0).checkState()== Qt.Checked))) 
        for l in range(zObj.model().columnCount()):
            WriteInLOG(zLOG, '%s\t<col id="%s">\n' % (sTab, l))   
            WriteInLOG(zLOG, '%s\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, urllib.quote(EncodeText(zObj.model().item(k, l).text()))))
            WriteInLOG(zLOG, '%s\t</col>\n'  % (sTab))
        WriteInLOG(zLOG, '%s</row>\n' % (sTab))

    if isSubWidget:  WriteInLOG(zLOG, "%s</%s>\n" % (sTabRef, zObj.metaObject().className()))
    
#==================================================
# END NEW FORMAT XQSP - XML QSP PROJECT
#==================================================    
def SaveQSP(self, zFile):
    zIndex = self.tabWidget.currentIndex()
    if zFile != "" : zLOG = open(zFile, "w")
    Config = ConfigParser.ConfigParser()
    
    zTabs = self.tabWidget.count()
    zObj = None
    for i in range(zTabs):
        self.tabWidget.setCurrentIndex(i)
        zTab = self.tabWidget.currentWidget()
        zObjs = zTab.children()
        for j in range(len(zObjs)):
            zNameObj = "%s" % (zObjs[j].accessibleName())
            if not type(zObjs[j]) in (QCommandLinkButton, MyPushButton, QLabel) and zNameObj != "" :
               Config.add_section(zNameObj)
               zClassObjName = "%s" % (zObjs[j].metaObject().className())
               Config.set(zNameObj,'Type',zClassObjName)
               if zClassObjName=="QCalendarWidget" : Config.set(zNameObj,'Date', "%s" % (ReturnDate(self, zObjs[j])))
               elif zClassObjName in ("QTextEdit", "MyTextEdit") : Config.set(zNameObj,'Text','%s' % (EncodeText(zObjs[j].toPlainText())))
               elif zClassObjName in ("QLineEdit", "MySimpleWidgetLineEdit", "MyWidgetLineEdit") : Config.set(zNameObj,'Text', "%s" % (EncodeText(zObjs[j].text())))
               elif zClassObjName in ("QComboBox", "MyComboBox") :
                   Config.set(zNameObj,'ItemCount',"%s" % zObjs[j].model().rowCount())
                   for k in range(zObjs[j].model().rowCount()): Config.set(zNameObj,'Item_%s' % (k), "%s" % (zObjs[j].itemText(k)))
                   Config.set(zNameObj,'Index',"%s" % zObjs[j].currentIndex())
               elif zClassObjName=="QGroupBox" :
                    zChildren = zObjs[j].children()
                    for i in range(len(zChildren)):
                        zChild = zChildren[i]
                        zChildClassName = "%s" % (zChild.metaObject().className())
                        if zChildClassName == "QRadioButton" and zChild.isChecked(): Config.set(zNameObj, "radio","%s" % (i))
                        elif zChildClassName in ("QComboBox", "MyComboBox") : Config.set(zNameObj,'Index', zChild.currentIndex())
                        elif zChildClassName in ("QTableWidget", "MyTableWidget") :
                             Config.set(zNameObj,'subtype', zChildClassName)
                             Config.set(zNameObj,'zRows', zChild.rowCount())
                             Config.set(zNameObj,'zCols', zChild.columnCount())
                             for k in range(zChild.rowCount()):
                                  zWidget = zChild.cellWidget(k, 0)
                                  Config.set(zNameObj,'zRow_%s' % (k), "%s" % (zWidget.value()))
                        elif zChildClassName == "QTableView":
                             Config.set(zNameObj,'subtype', zChildClassName)
                             zItems = ""
                             Config.set(zNameObj,'ItemCount',"%s" % zChild.model().rowCount())
                             for k in range(zChild.model().rowCount()):
                                 zValues = ""
                                 for l in range(zChild.model().columnCount()): zValues+= "%s" % (EncodeText(zChild.model().item(k, l).text())) if zValues == "" else "|%s" % (EncodeText(zChild.model().item(k, l).text()))
                                 Config.set(zNameObj,'Item_%s' % (k),zValues)
                                 zItem = zChild.model().item(k, 0)
                                 if zItem.checkState()== Qt.Checked: zItems+= "%s" % (k) if zItems=="" else "|%s" % (k)  
                             Config.set(zNameObj,'Indexes',zItems)                                      
                   
               elif zClassObjName=="QTableView" :
                   zItems = ""
                   Config.set(zNameObj,'ItemCount',"%s" % zObjs[j].model().rowCount())
                   for k in range(zObjs[j].model().rowCount()):
                       zValues = ""
                       for l in range(zObjs[j].model().columnCount()): zValues+= "%s" % (EncodeText(zObjs[j].model().item(k, l).text())) if zValues == "" else "|%s" % (EncodeText(zObjs[j].model().item(k, l).text()))
                       Config.set(zNameObj,'Item_%s' % (k),zValues)
                       zItem = zObjs[j].model().item(k, 0)
                       if zItem.checkState()== Qt.Checked: zItems+= "%s" % (k) if zItems=="" else "|%s" % (k)  
                   Config.set(zNameObj,'Indexes', "%s" % zItems)

               
               elif zClassObjName in ("QTableWidget", "MyTableWidget") :
                  Config.set(zNameObj,'zRows',"%s" % zObjs[j].rowCount())
                  Config.set(zNameObj,'zCols',"%s" % zObjs[j].columnCount())
                  for z in range(zObjs[j].columnCount()):
                      zObj = zObjs[j].cellWidget(0, z)
                      if zObj != None :
                          zClassWidgetName = zObjs[j].cellWidget(0, z).metaObject().className()
                          Config.set(zNameObj,'zWidget_%s' % (z), "%s|%s" % (zClassWidgetName, zObjs[j].cellWidget(0, z).accessibleDescription()))
                      else: Config.set(zNameObj,'zWidget_%s' % (z), "standard")   

                  for k in range(zObjs[j].rowCount()):
                      zLine = ""
                      for z in range(zObjs[j].columnCount()):
                          zWidget = zObjs[j].cellWidget(k, z)
                          if zWidget != None :
                              if zWidget.metaObject().className() in ("QComboBox", "MyComboBox") :
                                  if zWidget.isEditable() : zLine+= "%s" % (returnText(zWidget.currentText())) if zLine == "" else "|%s" % (returnText(zWidget.currentText()))  
                                  else : zLine+= "%s" % (zWidget.currentIndex()) if zLine == "" else "|%s" % (zWidget.currentIndex())
                              elif zWidget.metaObject().className() in ("QCheckBox", "MyCheckBox") : zLine+= "%s" % (zWidget.checkState()) if zLine == "" else "|%s" % (zWidget.checkState())
                              elif zWidget.metaObject().className()=="MySpinBox" : zLine+= "%s" % (zWidget.value()) if zLine == "" else "|%s" % (zWidget.value())
                              elif zWidget.metaObject().className() in ("QPushButton", "MyButton") : zLine+= "action" if zLine == "" else "|action"
                              else : zLine+= "%s" % (returnText(zWidget.text())) if z==0 else "|%s" % (returnText(zWidget.text()))
                          else:
                              zCell = zObjs[j].item(k, z)
                              if zCell != None : zLine+= "%s" % (returnText(zObjs[j].item(k, z).text())) if zLine == "" else  "|%s" % (returnText(zObjs[j].item(k, z).text()))
                              else : zLine+= "" if (zLine == "" and z == 0) else  "|"  

                      Config.set(zNameObj,'zRow_%s' % (k), "%s" % zLine)

    self.tabWidget.setCurrentIndex(zIndex) 
    
    if zFile != "" :
       Config.write(zLOG)
       CloseLOG(zLOG)
    else :
       zHTML = ""
       for section in Config.sections():    
          zHTML+=  MarkerText(self,"[%s]\n" % section)
          for option in Config.options(section):
              try : zHTML+=  MarkerText(self, "%s = %s\n" % (option, Config.get(section, option).strip()))
              except :
                  try : zHTML+=  MarkerText(self, "%s = %s\n" % (option, Config.get(section, option)))
                  except : zHTML+=  MarkerText(self, "%s =\n" % (option))
          zHTML+= "<br>"  
       return zHTML
    

def EncodeText(zText):
    try : zText = zText.encode("cp1252")
    except : pass
    return zText 

def returnText(zText):
    if zText == "" : zText = " "
    return EncodeText(zText)

def LoadQSP(self, zFile):
    zFile = os.path.abspath(zFile)
    zTitle = "Information"
    
    config = ConfigParser.ConfigParser()
    config.read(zFile)
    zSections = config.sections()

    self.tabWidget.setVisible(False)
    self.progressBar.setVisible(True)
    zBounds = len(zSections)
    
    zMsg1 = QApplication.translate("QSphere","Object ", None, QApplication.UnicodeUTF8)

    zMapType = {"QTableWidget": MyTableWidget, "MyTableWidget": MyTableWidget, \
                "QCheckBox"   : MyCheckBox,    "MyCheckBox"   : MyCheckBox, \
                "QTextEdit"   : MyTextEdit,    "MyTextEdit"   : MyTextEdit, \
                "QLineEdit"   : QLineEdit,     "MySimpleWidgetLineEdit" : QLineEdit, "MyWidgetLineEdit" : QLineEdit, \
                "QComboBox"    : QComboBox,    "MyComboBox" : MyComboBox, \
                "QTableView"  : QTableView,    "QCalendarWidget" : QCalendarWidget, \
                "QGroupBox"   : QGroupBox, 
                }
    
    for i in range(zBounds):
        zSection = zSections[i]
        zType = config.get(zSection,'Type')
        self.progressBar.setValue(int(100 * i/zBounds))

        if DicoHasKey(zMapType, zType) :    
            zClassObj = zMapType[zType]
            zObj = self.findChild(zClassObj, zSection)

            if zObj !=None :
                    if zClassObj == QCalendarWidget :                         
                        zInfos = config.get(zSection,'Date')
                        zInfos = zInfos.rstrip()
                        if zInfos!="" and zInfos.find("-")!=-1:
                           zEltsDate = zInfos.split("-")
                           zObj.setSelectedDate(QDate(int(zEltsDate[0]), int(zEltsDate[1]), int(zEltsDate[2]) ))
                        else: zObj.showToday()

                    elif zClassObj in (QTextEdit, MyTextEdit) :
                        zInfos = config.get(zSection,'Text')
                        zInfos = zInfos.rstrip()
                        if zSection != "coherence" : zObj.setPlainText(zInfos)
                        else : self.UpdateCoherence(zSection, zInfos)

                    elif zClassObj in (QLineEdit, MySimpleWidgetLineEdit, MyWidgetLineEdit) :    
                        zInfos = config.get(zSection,'Text')
                        zInfos = zInfos.rstrip()
                        zObj.setText(zInfos)

                    elif zClassObj in (QComboBox, MyComboBox) :    
                        zInfos = config.get(zSection,'Index')
                        zIndexObj = int(zInfos.rstrip())
                        zInfosItem = config.get(zSection,'ItemCount')
                        zItemCount = int(zInfosItem.rstrip())
                        zObj.clear()
                        for k in range(zItemCount):
                            zItem = config.get(zSection,'Item_%s' % (k))
                            zItem = zItem.replace("jeux", "séries".decode('utf-8'))
                            zItem = zItem.replace("Jeu", "Série".decode('utf-8'))
                            zObj.addItem(zItem)
                        zObj.setCurrentIndex(zIndexObj)

                    elif zClassObj == QTableView : ReLOADTableView(self, config, zObj, zSection, int(100 * i/zBounds), int(100 * 1/zBounds))
                         
                    elif zClassObj == QGroupBox :    
                        zChildren = zObj.children()
                        zInfos = "%s" % (config.get(zSection, "radio"))
                        zIndexObj = int(zInfos.rstrip())
                        try : zChildren[zIndexObj].setChecked(True)
                        except : pass

                        for child in zChildren :
                            if child.metaObject().className()== "QTableView" : ReLOADTableView(self, config, child, zSection, int(100 * i/zBounds), int(1/zBounds))
                            elif child.metaObject().className() in ("QTableWidget", "MyTableWidget") :
                                child.clearContents()
                                for j in range(child.rowCount()): child.removeRow(0)
                                zRows = int(config.get(zSection,'zRows'))
                                for j in range(zRows):
                                     child.insertRow(j)
                                     zInfos = float(config.get(zSection,'zRow_%s' % (j)))
                                     AddLineWidget(self, child, j,  0, 4, 0, zInfos)
                            elif child.metaObject().className() in ("QComboBox", "MyComboBox") :
                                zIndexCombo = int(config.get(zSection, "Index"))
                                child.setCurrentIndex(zIndexCombo)

                    elif zClassObj in (QTableWidget, MyTableWidget) :                        
                                ReLOADTableWidget(self, config, zObj, zSection)
                                if zObj.accessibleName() == "tablemotsclefsf":
                                   for i in range(zObj.rowCount()):
                                       zCheckBox = zObj.cellWidget(i, 1)
                                       for j in range(2,5):
                                           zItemEditLine = zObj.cellWidget(i, j)
                                           try : zItemEditLine.setEnabled(zCheckBox.isChecked())
                                           except : pass

            else :
                zMsg2 = QApplication.translate("QSphere","'s properties not similar. Import data aborded.", None, QApplication.UnicodeUTF8)
                SendMessage(self, zTitle , "%s%s%s" % (zMsg1, zSection, zMsg2), QgsMessageBar.WARNING, self.duration_warning)
        else :
            if DicoHasKey(zMapType, zType) :    
                zMsg2 = QApplication.translate("QSphere"," not find in the QSphere's collection.", None, QApplication.UnicodeUTF8)
                SendMessage(self, zTitle , "%s%s%s" % (zMsg1, zSection, zMsg2), QgsMessageBar.WARNING, self.duration_warning)

    
#==============================
# FONCTION TO WRITE XML EXPORT       
#==============================
def ExportDictionnaryToXML(self, zFile):

    zFullXML = ''
    zFullXML+= MakeEnteteXML(self)

    zFullXML+= '<gmd:qspheredictionnary>\n'
    zFullXML+= '<gco:CharacterString>dictionnary</gco:CharacterString>\n'
    zFullXML+='</gmd:qspheredictionnary>\n'
    
    zFullXML+= '<gmd:identificationInfo>\n'
    zFullXML+= '<gmd:MD_DataIdentification>\n'
    zObj = getWidget(self, "tablecontacts")
    for i in range(zObj.rowCount()):
        zValue = self.DicoListOfRules[zObj.cellWidget(i, 0).currentIndex()]
        zFullXML+= MakeBlocRole(self, zObj, zValue, i, False, 0) 
    zFullXML+= '</gmd:MD_DataIdentification>\n' 
    zFullXML+= '</gmd:identificationInfo>\n'
    zFullXML+= MakeEndXML(self)

    zLOG = file(zFile, "w")
    if not zLOG : return
    else : WriteInLOG(zLOG, zFullXML)
    CloseLOG(zLOG)
    
def ExportToXML(self, zFile):
    zIndex = self.tabWidget.currentIndex()

    zFullXML = ''
    zFullXML+= MakeEnteteXML(self)
    zFullXML+= MakeFileIdentifierXML(self)
    zFullXML+= MakeFileLanguageXML(self)
    zFullXML+= MakeCharacterSetCodeXML(self)
    zFullXML+= MakeHierarchyLevelXML(self)
    zFullXML+= MakeContactXML(self)
    zFullXML+= MakeDateStampXML(self, 1, True, None)
    zFullXML+= MakeMetadataStandardNameXML(self,)
    zFullXML+= MakeMetadataStandardVersionXML(self)
    zFullXML+= MakeSpatialRepresentation(self)    
    zFullXML+= MakeReferenceSystemInfoXML(self)
    zFullXML+= MakeIdentificationInfoXML(self)
    zFullXML+= MakeDistributionInfoXML(self)
    zFullXML+= MakeDataQualityInfoXML(self)
    zFullXML+= MakeEndXML(self)

    self.tabWidget.setCurrentIndex(zIndex) 

    if zFile != None :
        zLOG = file(zFile, "w")
        if not zLOG : return
        else : WriteInLOG(zLOG, zFullXML)
        CloseLOG(zLOG)
        return None
    else : return  zFullXML.encode("utf-8")   
    

def ExportCatToXML(self, zFile):
    zIndex = self.tabWidget.currentIndex()
    zFullXML = ''
    
    zFullXML+= MakeEnteteCatXML(self)
    zFullXML+= MakeNameCat(self)
    zFullXML+= MakeScopeCat(self)
    zFullXML+= MakeVersionCat(self)
    zFullXML+= MakeDateCat(self)
    zFullXML+= MakeProductorCat(self)
    zFullXML+= MakeFieldMapXML(self)
    zFullXML+= MakeEndCatXML(self)

    self.tabWidget.setCurrentIndex(zIndex) 

    zLOG = file(zFile, "w")
    if not zLOG : return
    else : WriteInLOG(zLOG, zFullXML)
    CloseLOG(zLOG)    
    
    
#------------------------------------
# FONCTION TO WRITE BLOCX XML EXPORT       
#------------------------------------
def MakeEnteteCatXML(self):
    zPath = os.path.dirname(__file__).replace("\\","/")
    zXML = ""
    zObj = getWidget(self, "namelayer")
    zXML+= '<?xml version="1.0" encoding="UTF-8"?>' \
                     '%s' \
                     '<gfc:FC_FeatureCatalogue uuid="CA_%s" xmlns:gfc="http://www.isotc211.org/2005/gfc" xmlns:gmd="http://www.isotc211.org/2005/gmd"' \
                     ' xmlns:gco="http://www.isotc211.org/2005/gco"' \
                     ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' \
                     ' xsi:schemaLocation="http://www.isotc211.org/2005/gfc http://www.isotc211.org/2005/gfc/gfc.xsd">\n' % (zXML, zObj.text())
    return zXML

def MakeEndCatXML(self):
     zXML = ''
     zXML+= '</gfc:FC_FeatureCatalogue>'
     return zXML

def MakeNameCat(self):
     zXML = ''
     zValue, zText = GetTextWidget(self, "namelayer", False)
     zXML+= '\t<gfc:name>\n'
     zXML+= '\t\t<gco:CharacterString>%s - %s</gco:CharacterString>\n' % (zValue,"Catalogue d'attributs")
     zXML+= '\t</gfc:name>\n'
     return zXML

def MakeScopeCat(self):
    zXML = ''
    zObj = getWidget(self, "namelayer")
    zXML+= '\t<gfc:scope>\n'
    zXML+= '\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj.text())
    zXML+= '\t</gfc:scope>\n'
    return zXML

def MakeVersionCat(self):
    zXML = ''
    zXML+= '\t<gfc:versionNumber>\n'
    zXML+= '\t\t<gco:CharacterString>NC</gco:CharacterString>\n'
    zXML+= '\t</gfc:versionNumber>\n'
    return zXML

def MakeDateCat(self):
    zXML = ''
    zObj = getWidget(self, "datecredata")
    zXML+= '\t<gfc:versionDate>\n'
    zXML+= '\t\t<gco:Date>%s</gco:Date>\n' % (ReturnDate(self, zObj))
    zXML+= '\t</gfc:versionDate> \n'
    return zXML

def MakeProductorCat(self):
    zXML = ''
    zObj = getWidget(self, "tableroles")
    for i in range(zObj.rowCount()):
        zValue = self.DicoListOfRules[zObj.cellWidget(i, 0).currentIndex()]
        if zValue == "pointOfContact" : 
            zXML+= '\t<gfc:producer>\n'
            zXML+= MakeResponsibleParty(self, zObj, zValue, i, True, 2) 
            zXML+= '\t</gfc:producer>\n'
            return zXML
    
def MakeFieldMapXML(self):
    zXML = ''
    zXML+= '\t<gfc:featureType>\n'
    zXML+= '\t\t<gfc:FC_FeatureType>\n'
    zXML+= '\t\t\t<gfc:typeName><gco:LocalName>%s</gco:LocalName></gfc:typeName>\n' % (self.ComboLayers.currentText())
    zXML+= '\t\t\t<gfc:definition><gco:CharacterString>%s</gco:CharacterString></gfc:definition>\n' % ("")

    zObj = getWidget(self, "tabledico")
    for i in range(zObj.rowCount()):
        zXML+= '\t\t\t<gfc:carrierOfCharacteristics>\n'
        zXML+= '\t\t\t\t<gfc:FC_FeatureAttribute>\n'
        zXML+= '\t\t\t\t\t<gfc:memberName>\n'
        zXML+= '\t\t\t\t\t\t<gco:LocalName>%s</gco:LocalName>\n' % (zObj.item( i, 1 ).text())
        zXML+= '\t\t\t\t\t</gfc:memberName>\n'
        zXML+= '\t\t\t\t\t<gfc:definition><gco:CharacterString>%s</gco:CharacterString></gfc:definition>\n' % (zObj.item( i, 5 ).text())
        zXML+= '\t\t\t\t\t<gfc:cardinality>\n'
        zXML+= '\t\t\t\t\t\t<gco:Multiplicity>\n'
        zXML+= '\t\t\t\t\t\t\t<gco:range>\n'
        zXML+= '\t\t\t\t\t\t\t\t<gco:MultiplicityRange>\n'
        zXML+= '\t\t\t\t\t\t\t\t\t<gco:lower>\n'
        zXML+= '\t\t\t\t\t\t\t\t\t\t<gco:Integer>1</gco:Integer>\n'
        zXML+= '\t\t\t\t\t\t\t\t\t</gco:lower>\n'
        zXML+= '\t\t\t\t\t\t\t\t\t<gco:upper>\n'
        zXML+= '\t\t\t\t\t\t\t\t\t\t<gco:UnlimitedInteger isInfinite="false">1</gco:UnlimitedInteger>\n'
        zXML+= '\t\t\t\t\t\t\t\t\t</gco:upper>\n'
        zXML+= '\t\t\t\t\t\t\t\t</gco:MultiplicityRange>\n'
        zXML+= '\t\t\t\t\t\t\t</gco:range>\n'
        zXML+= '\t\t\t\t\t\t</gco:Multiplicity>\n'
        zXML+= '\t\t\t\t\t</gfc:cardinality>\n'
        zXML+= '\t\t\t\t\t<gfc:valueType>\n'
        zXML+= '\t\t\t\t\t\t<gco:TypeName>\n'
        zXML+= '\t\t\t\t\t\t\t<gco:aName>\n'
        zXML+= '\t\t\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj.item( i, 2 ).text())
        zXML+= '\t\t\t\t\t\t\t</gco:aName>\n'
        zXML+= '\t\t\t\t\t\t</gco:TypeName>\n'
        zXML+= '\t\t\t\t\t</gfc:valueType>\n'
        zXML+= '\t\t\t\t</gfc:FC_FeatureAttribute>\n'
        zXML+= '\t\t\t</gfc:carrierOfCharacteristics>\n'

    zXML+= '\t\t</gfc:FC_FeatureType>\n'
    zXML+= '\t</gfc:featureType>\n'

    return zXML

 
def MakeEnteteXML(self):
    zPath = os.path.dirname(__file__).replace("\\","/")
    zXML = ""
    zXML = '<?xml version="1.0" encoding="UTF-8"?>' \
           '%s' \
           '<gmd:MD_Metadata xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://schemas.opengis.net/iso/19139/20060504/gmd/gmd.xsd"' \
           ' xmlns:gmd="http://www.isotc211.org/2005/gmd"' \
           ' xmlns:gco="http://www.isotc211.org/2005/gco"' \
           ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' \
           ' xmlns:gml="http://www.opengis.net/gml"' \
           ' xmlns:xlink="http://www.w3.org/1999/xlink">\n' % (zXML)
    return zXML

def MakeFileIdentifierXML(self):
    zObj = getWidget(self, "identificator")
    zXML = ""
    zXML+= '\t<gmd:fileIdentifier>\n'
    zXML+= '\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj.text()) 
    zXML+= '\t</gmd:fileIdentifier>\n'
    return zXML

def MakeFileLanguageXML(self):
    zObj = getWidget(self, "langmetada")
    zValue = zObj.currentText()
    zXML = ""
    zXML+= MakeBlocLangue(self, zValue, 1)
    return zXML

def MakeCharacterSetCodeXML(self):
    zObj = getWidget(self, "tablecarac")
    zValue = "MD_CharacterSetCode_%s" % (zObj.currentText().lower())
    zXML = ''    
    zXML+= '\t<gmd:characterSet>\n'
    zXML+= '\t\t<gmd:MD_CharacterSetCode codeListValue="%s" codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/gmxCodelists.xml#MD_CharacterSetCode">%s</gmd:MD_CharacterSetCode>\n' % (zValue, zValue)
    zXML+= '\t</gmd:characterSet>\n'
    return zXML

def MakeHierarchyLevelXML(self):
    zObj = getWidget(self, "typedata")
    zValue = self.TypeData[zObj.currentIndex()]
    zXML = ''
    zXML+= '\t<gmd:hierarchyLevel>\n'
    zXML+= '\t\t<gmd:MD_ScopeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/gmxCodelists.xml#MD_ScopeCode" codeListValue="%s">%s</gmd:MD_ScopeCode>\n' % (zValue, zValue)
    zXML+= '\t</gmd:hierarchyLevel>\n'
    return zXML

def MakeContactXML(self):
    zObj = getWidget(self, "tableroles")
    zXML = ''
    for i in range(zObj.rowCount()):
        zValue = self.DicoListOfRules[zObj.cellWidget(i, 0).currentIndex()]
        if zValue == "pointOfContact" :
           zXML+= MakeBlocRole(self, zObj, zValue, i, True, 1)
           return zXML

def MakeDateStampXML(self, zTab, isValue, zObj):
    sTab=""
    for k in range(zTab): sTab+="\t"
    zXML = ''
    zXML+= '%s<gmd:dateStamp>\n' % (sTab)
    if isValue :
        zValue, zText = GetTextWidget(self, "datemetada", False)
        zXML+= '%s\t<gco:Date>%s</gco:Date>\n' % (sTab, zValue)
    else :
        if zObj != None : zXML+= '%s\t<gco:Date>%s</gco:Date>\n' % (sTab, ReturnDate(self, zObj))
        else : zXML+= '%s\t<gco:Date>%s</gco:Date>\n' % (sTab, datetime.datetime.now().strftime("%d/%m/%Y %Hh%Mm%Ss"))
        
    zXML+= '%s</gmd:dateStamp>\n' % (sTab)
    return zXML

def MakeMetadataStandardNameXML(self):
    zXML = ''
    zXML+= '\t<gmd:metadataStandardName>\n'
    zXML+= '\t\t<gco:CharacterString>ISO19115</gco:CharacterString>\n'
    zXML+= '\t</gmd:metadataStandardName>\n'
    return zXML

def MakeMetadataStandardVersionXML(self):
    zXML = ''
    zXML+= '\t<gmd:metadataStandardVersion>\n'
    zXML+= '\t\t<gco:CharacterString>2003/Cor.1:2006</gco:CharacterString>\n'
    zXML+= '\t</gmd:metadataStandardVersion>\n'
    return zXML

def MakeReferenceSystemInfoXML(self):
    zObj = getWidget(self, "tablescr")
    zXML = ''
    for i in range(zObj.rowCount()): 
        zEPSG = zObj.cellWidget(i, 0).text()
        if zObj.rowCount() == 1 :  zXML+= '\t<gmd:referenceSystemInfo>\n'
        else : zXML+= '\t<gmd:referenceSystemInfo id="proj00%s">\n' % (i+1)
        zXML+= '\t\t<gmd:MD_ReferenceSystem>\n'
        zXML+= '\t\t\t<gmd:referenceSystemIdentifier>\n'        
        zXML+= '\t\t\t\t<gmd:RS_Identifier>\n'
        zCodeESPG = int(zEPSG.replace("EPSG:",""))
        zXML+= '\t\t\t\t\t<gmd:code>\n'
        zXML+= '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zCodeESPG)
        zXML+= '\t\t\t\t\t</gmd:code>\n'
        zXML+= '\t\t\t\t\t<gmd:codeSpace>\n'
        zXML+= '\t\t\t\t\t\t<gco:CharacterString>urn:ogc:def:crs:EPSG:6.11</gco:CharacterString>\n'
        zXML+= '\t\t\t\t\t</gmd:codeSpace>\n'
        zXML+= '\t\t\t\t\t<gmd:version>\n'
        zXML+= '\t\t\t\t\t\t<gco:CharacterString>6.11</gco:CharacterString>\n'
        zXML+= '\t\t\t\t\t</gmd:version>\n'
        zXML+= '\t\t\t\t</gmd:RS_Identifier>\n'
        zXML+= '\t\t\t</gmd:referenceSystemIdentifier>\n'
        zXML+= '\t\t</gmd:MD_ReferenceSystem>\n'
        zXML+= '\t</gmd:referenceSystemInfo>\n'
    return zXML

def MakeIdentificationInfoXML(self):
    zXML = ''
    zXML+= '\t<gmd:identificationInfo>\n'
    zXML+= '\t\t<gmd:MD_DataIdentification>\n'
    #CITATION BLOC
    zXML+= '\t\t\t<gmd:citation>\n'
    zXML+= '\t\t\t\t<gmd:CI_Citation>\n'
    zValue, zText = GetTextWidget(self, "intitule", False)
    zXML+= '\t\t\t\t\t<gmd:title>\n'
    zXML+= '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zValue)
    zXML+= '\t\t\t\t\t</gmd:title>\n'
    
    zObj = getWidget(self, "tabledatepubdata")
    for i in range(zObj.rowCount()):
        zValue = zObj.cellWidget(i, 0).text()
        zTypeDate = GetDateType(2, False) 
        if zValue.find("--") == -1 : zXML+= MakeBlocDate(self, zValue, zTypeDate, 5)
    
    for i in range(0, 2):
        zWidgetDate = GetDateType(i, True) 
        zTypeDate = GetDateType(i, False)
        zValue, zText = GetTextWidget(self, zWidgetDate, False)
        if zValue.find("--") == -1 : zXML+= MakeBlocDate(self, zValue, zTypeDate, 5)

    zObj = getWidget(self, "identificator")
    zXML+= '\t\t\t\t\t<gmd:identifier>\n'
    zXML+= '\t\t\t\t\t\t<gmd:MD_Identifier>\n'
    zXML+= '\t\t\t\t\t\t\t<gmd:code>\n'
    zXML+= '\t\t\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj.text())
    zXML+= '\t\t\t\t\t\t\t</gmd:code>\n'
    zXML+= '\t\t\t\t\t\t</gmd:MD_Identifier>\n'
    zXML+= '\t\t\t\t\t</gmd:identifier>\n'
    
    """
    <gmd:identifier><gmd:MD_Identifier><gmd:code><gco:CharacterString>00-478</gco:CharacterString></gmd:code></gmd:MD_Identifier></gmd:identifier>
    
    zValue, zText = GetTextWidget(self, "identificator", False)
    WriteInLOG(zLOG, '<gmd:identifier>\n')
    WriteInLOG(zLOG, '<gmd:RS_Identifier>\n')
    WriteInLOG(zLOG, '<gmd:code>\n')
    WriteInLOG(zLOG, '<gco:CharacterString>%s</gco:CharacterString>\n' % (zValue))
    WriteInLOG(zLOG, '</gmd:code>\n')
    WriteInLOG(zLOG, '<gmd:codeSpace>\n')
    WriteInLOG(zLOG, '<gco:CharacterString>Unkwon</gco:CharacterString>\n')
    WriteInLOG(zLOG, '</gmd:codeSpace>\n')
    WriteInLOG(zLOG, '</gmd:RS_Identifier>\n')
    WriteInLOG(zLOG, '</gmd:identifier>\n')
    """
               
    zXML+= '\t\t\t\t</gmd:CI_Citation>\n'
    zXML+= '\t\t\t</gmd:citation>\n'
    #End CITATION BLOC

    #ABSTRACT BLOC
    zValue, zText = GetTextWidget(self, "resume", False)
    zXML+= '\t\t\t<gmd:abstract>\n'
    zXML+= '\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zValue)
    zXML+= '\t\t\t</gmd:abstract>\n'
    #End ABSTRACT BLOC

    #ROLES BLOC
    zObj = getWidget(self, "tableroles")
    for i in range(zObj.rowCount()):
        zValue = self.DicoListOfRules[zObj.cellWidget(i, 0).currentIndex()]
        if zValue != "pointOfContact" : zXML+= MakeBlocRole(self, zObj, zValue, i, False, 3) 
    #End ROLES BLOC

    #BLOC INSPIRE optional keywords 
    zObj = getWidget(self, "tablemotsclefsf")
    for i in range(zObj.rowCount()):
        zXML+= '\t\t\t<gmd:descriptiveKeywords>\n'
        zXML+= '\t\t\t\t<gmd:MD_Keywords>\n'
        zXML+= '\t\t\t\t\t<gmd:keyword>\n'
        zXML+= '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj.cellWidget(i, 0).text())
        zXML+= '\t\t\t\t\t</gmd:keyword>\n'

        zValueTHE = zObj.cellWidget(i, 2).text()
        if zValueTHE != "" :
            zXML+= '\t\t\t\t\t<gmd:thesaurusName>\n'
            zXML+= '\t\t\t\t\t\t<gmd:CI_Citation>\n'
            zXML+= '\t\t\t\t\t\t\t<gmd:title>\n'
            zXML+= '\t\t\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zValueTHE)
            zXML+= '\t\t\t\t\t\t\t</gmd:title>\n'

            zValueDate = zObj.cellWidget(i, 3).text()
            if zValueDate.find("--")==-1:
                zValueTypeDate = GetDateType(zObj.cellWidget(i, 4).currentIndex(), False)
                zXML+= MakeBlocDate(self, zValueDate, zValueTypeDate, 7) 
               
            zXML+= '\t\t\t\t\t\t</gmd:CI_Citation>\n'
            zXML+= '\t\t\t\t\t</gmd:thesaurusName>\n'
    
        zXML+= '\t\t\t\t</gmd:MD_Keywords>\n'
        zXML+= '\t\t\t</gmd:descriptiveKeywords>\n'
    #End BLOC INSPIRE optional keywords

    #BLOC INSPIRE required keywords
    zObj = getWidget(self, "tablemotsclefso")
    for i in range(zObj.rowCount()):
        zXML+= '\t\t\t<gmd:descriptiveKeywords>\n'
        zXML+= '\t\t\t\t<gmd:MD_Keywords>\n'
        zXML+= '\t\t\t\t\t<gmd:keyword>\n'
        zXML+= '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj.cellWidget(i, 1).currentText())
        zXML+= '\t\t\t\t\t</gmd:keyword>\n'
        zXML+= '\t\t\t\t\t<gmd:thesaurusName>\n'
        zXML+= '\t\t\t\t\t\t<gmd:CI_Citation>\n'
        zXML+= '\t\t\t\t\t\t\t<gmd:title>\n'
        zXML+= '\t\t\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj.cellWidget(i, 0).currentText())
        zXML+= '\t\t\t\t\t\t\t</gmd:title>\n'

        try : zXML+= MakeBlocDate(self, self.DateListOfThesaurus[zObj.cellWidget(i, 0).currentIndex()], "publication", 7)
        except : zXML+= MakeBlocDate(self, datetime.datetime.now().strftime("%d/%m/%Y"), "publication", 7) 

        zXML+= '\t\t\t\t\t\t</gmd:CI_Citation>\n'
        zXML+= '\t\t\t\t\t</gmd:thesaurusName>\n'
        zXML+= '\t\t\t\t</gmd:MD_Keywords>\n'
        zXML+= '\t\t\t</gmd:descriptiveKeywords>\n'
    #End BLOC INSPIRE required keywords   

    #BLOC resourceConstraints
    zXML+= '\t\t\t<gmd:resourceConstraints>\n'
    zXML+= '\t\t\t\t<gmd:MD_LegalConstraints>\n'
    zObj = getWidget(self, "licence")
    zXML+= '\t\t\t\t\t<gmd:useLimitation>\n'
    zXML+= '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zObj.toPlainText())
    zXML+= '\t\t\t\t\t</gmd:useLimitation>\n'
    zObj = getWidget(self, "groupedroits")

    if zObj.children()[0].isChecked() :
        zXML+= '\t\t\t\t\t<gmd:accessConstraints>\n'
        zXML+= '\t\t\t\t\t\t<gmd:MD_RestrictionCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode" codeListValue="otherRestrictions">otherRestrictions</gmd:MD_RestrictionCode>\n'
        zXML+= '\t\t\t\t\t</gmd:accessConstraints>\n'
        zXML+= '\t\t\t\t\t<gmd:otherConstraints>\n'
        zXML+= '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (QApplication.translate("QSphere","No restriction for public access with INSPIRE", None, QApplication.UnicodeUTF8))
        zXML+= '\t\t\t\t\t</gmd:otherConstraints>\n'
    else :
        zXML+= '\t\t\t\t\t<gmd:accessConstraints>\n'
        zXML+= '\t\t\t\t\t\t<gmd:MD_RestrictionCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_RestrictionCode" codeListValue="otherRestrictions">otherRestrictions</gmd:MD_RestrictionCode>\n'
        zXML+= '\t\t\t\t\t</gmd:accessConstraints>\n'
        zChild = zObj.children()[2]
        zRows = zChild.model().rowCount()
        for i in range(zRows):
            zItem = zChild.model().item(i, 0)
            if zItem.checkState()== Qt.Checked:
                zValue = zChild.model().item(i, 1).text()
                zXML+= '\t\t\t\t\t<gmd:otherConstraints>\n'
                zXML+= '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zValue)
                zXML+= '\t\t\t\t\t</gmd:otherConstraints>\n'

    zXML+= '\t\t\t\t</gmd:MD_LegalConstraints>\n'
    zXML+= '\t\t\t</gmd:resourceConstraints>\n'
    #End BLOC resourceConstraints

    #BLOC spatialRepresentationType - not yet implemented (vector, raster, other ? ...)
    """
    WriteInLOG(zLOG, '<gmd:spatialRepresentationType>\n')
    WriteInLOG(zLOG, '<gmd:MD_SpatialRepresentationTypeCode codeList="http://librairies.ign.fr/geoportail/resources/CodeLists.xml#MD_SpatialRepresentationTypeCode" codeListValue="vector">vector</gmd:MD_SpatialRepresentationTypeCode>\n')
    WriteInLOG(zLOG, '</gmd:spatialRepresentationType>\n')
    """

    #BLOC Spatial Resolution
    zObj = getWidget(self, "grouperesolutionscale")
    zChild = zObj.children()[2]
    for i in range(zChild.rowCount()):
        zWidget = zChild.cellWidget(i, 0)
        if zObj.children()[0].isChecked() :
            zXML+= '\t\t\t<gmd:spatialResolution>\n'
            zXML+= '\t\t\t\t<gmd:MD_Resolution>\n'
            zXML+= '\t\t\t\t\t<gmd:equivalentScale>\n'
            zXML+= '\t\t\t\t\t\t<gmd:MD_RepresentativeFraction>\n'
            zXML+= '\t\t\t\t\t\t\t<gmd:denominator>\n'
            zXML+= '\t\t\t\t\t\t\t\t<gco:Integer>%s</gco:Integer>\n' % (int(zWidget.value()))
            zXML+= '\t\t\t\t\t\t\t</gmd:denominator>\n'
            zXML+= '\t\t\t\t\t\t</gmd:MD_RepresentativeFraction>\n'
            zXML+= '\t\t\t\t\t</gmd:equivalentScale>\n'
            zXML+= '\t\t\t\t</gmd:MD_Resolution>\n'
            zXML+= '\t\t\t</gmd:spatialResolution>\n'
        else:
            zValueMesureUnit = "%s" % (zObj.children()[3].currentText())
            zXML+= '\t\t\t<gmd:spatialResolution>\n'
            zXML+= '\t\t\t\t<gmd:MD_Resolution>\n'
            zXML+= '\t\t\t\t\t<gmd:distance>\n'
            zXML+= '\t\t\t\t\t\t<gco:Distance uom="%s">%s</gco:Distance>\n' % (zValueMesureUnit, zWidget.value())
            zXML+= '\t\t\t\t\t</gmd:distance>\n'
            zXML+= '\t\t\t\t</gmd:MD_Resolution>\n'
            zXML+= '\t\t\t</gmd:spatialResolution>\n'
    #End BLOC Spatial Resolution

    #BLOC Language for the resource
    zObj = getWidget(self, "tablelangues")
    zRows = zObj.model().rowCount()
    for i in range(zRows):
        zItem = zObj.model().item(i, 0)
        if zItem.checkState()== Qt.Checked:
           zValue = zObj.model().item(i, 0).text()
           zXML+= MakeBlocLangue(self, zValue, 3) 
    #End BLOC Language for the resource

    #BLOC INSPIRE category(/ISO)
    zObj = getWidget(self, "tablecategories")
    zRows = zObj.model().rowCount() 
    
    for i in range(zRows):
        zItem = zObj.model().item(i, 0)
        if zItem.checkState()== Qt.Checked:
            zXML+= '\t\t\t<gmd:topicCategory>\n'
            zXML+= '\t\t\t\t<gmd:MD_TopicCategoryCode>%s</gmd:MD_TopicCategoryCode>\n' % (MakeCAT(self, zObj.model().item(i, 2).text()))
            zXML+= '\t\t\t</gmd:topicCategory>\n'
    #End BLOC INSPIRE category(/ISO)

    #BLOC Extents
    zXML+= '\t\t\t<gmd:extent>\n'
    zXML+= '\t\t\t\t<gmd:EX_Extent>\n'
    zObj = getWidget(self, "tableemprises")
    zXML+= '\t\t\t\t\t<gmd:description>\n'
    zXML+= '\t\t\t\t\t\t<gco:CharacterString>Liste des emprises</gco:CharacterString>\n'
    zXML+= '\t\t\t\t\t</gmd:description>\n'
    for i in range(zObj.rowCount()):
        zXML+= '\t\t\t\t\t<gmd:geographicElement>\n'
        zXML+= '\t\t\t\t\t\t<gmd:EX_GeographicBoundingBox>\n'
        zXML+= '\t\t\t\t\t\t\t<gmd:westBoundLongitude>\n'
        zXML+= '\t\t\t\t\t\t\t\t<gco:Decimal>%s</gco:Decimal>\n' % (zObj.cellWidget(i, 2).value())
        zXML+= '\t\t\t\t\t\t\t</gmd:westBoundLongitude>\n'
        zXML+= '\t\t\t\t\t\t\t<gmd:eastBoundLongitude>\n'
        zXML+= '\t\t\t\t\t\t\t\t<gco:Decimal>%s</gco:Decimal>\n' % (zObj.cellWidget(i, 3).value())
        zXML+= '\t\t\t\t\t\t\t</gmd:eastBoundLongitude>\n'
        zXML+= '\t\t\t\t\t\t\t<gmd:southBoundLatitude>\n'
        zXML+= '\t\t\t\t\t\t\t\t<gco:Decimal>%s</gco:Decimal>\n' % (zObj.cellWidget(i, 1).value())
        zXML+= '\t\t\t\t\t\t\t</gmd:southBoundLatitude>\n'
        zXML+= '\t\t\t\t\t\t\t<gmd:northBoundLatitude>\n'
        zXML+= '\t\t\t\t\t\t\t\t<gco:Decimal>%s</gco:Decimal>\n' % (zObj.cellWidget(i, 0).value())
        zXML+= '\t\t\t\t\t\t\t</gmd:northBoundLatitude>\n'   
        zXML+= '\t\t\t\t\t\t</gmd:EX_GeographicBoundingBox>\n'
        zXML+= '\t\t\t\t\t</gmd:geographicElement>\n'
       
    zObj = getWidget(self, "tableetenduetemporelle")
    for i in range(zObj.rowCount()):
        zWidgetDates = "%s" % (zObj.cellWidget(i, 0).text())
        if zWidgetDates.find("-- --") == -1 :
            zDates = zWidgetDates.split(" ")
            zXML+= '\t\t\t\t\t<gmd:temporalElement>\n'
            if zObj.rowCount() == 1 :  zXML+= '\t\t\t\t\t\t<gmd:EX_TemporalExtent>\n'
            else : zXML+= '\t\t\t\t\t\t<gmd:EX_TemporalExtent gml:id="tp00%s">\n' % (i+1) 
            zXML+= '\t\t\t\t\t\t\t<gmd:extent>\n'
            zXML+= '\t\t\t\t\t\t\t\t<gml:TimePeriod xsi:type="gml:TimePeriodType">\n'
            zXML+= '\t\t\t\t\t\t\t\t\t<gml:beginPosition>%s</gml:beginPosition>\n' % (zDates[0])
            zXML+= '\t\t\t\t\t\t\t\t\t<gml:endPosition>%s</gml:endPosition>\n'  % (zDates[1])
            zXML+= '\t\t\t\t\t\t\t\t</gml:TimePeriod>\n'
            zXML+= '\t\t\t\t\t\t\t</gmd:extent>\n'
            zXML+= '\t\t\t\t\t\t</gmd:EX_TemporalExtent>\n'
            zXML+= '\t\t\t\t\t</gmd:temporalElement>\n'
    zXML+= '\t\t\t\t</gmd:EX_Extent>\n'
    zXML+= '\t\t\t</gmd:extent>\n'
    #End BLOC Extents
    
    zXML+= '\t\t</gmd:MD_DataIdentification>\n'
    zXML+= '\t</gmd:identificationInfo>\n'

    return zXML

def EncodeURLQuery(zUrl):
    from urlparse import urlparse
    if zUrl == None : return ""

    try : 
        zElts = urlparse(zUrl)
        zEncodeURL = ""
        if zElts.scheme != "" : zEncodeURL+= "%s://" % (zElts.scheme)
        else : return zEncodeURL
       
        if zElts.netloc != "" and not zElts.port in (None,"", "None") : zEncodeURL+= "%s:%s" % (zElts.netloc, zElts.port)
        elif zElts.netloc != "" and zElts.port in (None,"", "None") : zEncodeURL+= "%s" % (zElts.netloc)
        else : return zEncodeURL
        
        if zElts.path != "" : zEncodeURL+= "%s" % (zElts.path)
        if zElts.query != "" : zEncodeURL+= "?%s" % (urllib.quote(zElts.query))
        if zElts.fragment != "" : zEncodeURL+= "#%s" % (zElts.fragment)
        
        return zEncodeURL

    except :
        return zUrl

def MakeDistributionInfoXML(self):
    zXML = ''                     
    zXML+= '\t<gmd:distributionInfo>\n'
    zXML+= '\t\t<gmd:MD_Distribution>\n'
    zObj = getWidget(self, "tableformats")
    for i in range(zObj.rowCount()): zXML+= MakeBlocFormat(self, zObj, i, 3)
   
    zXML+= '\t\t\t<gmd:transferOptions>\n'
    zXML+= '\t\t\t\t<gmd:MD_DigitalTransferOptions>\n'
    zObj = getWidget(self, "tablelocalisator")
    for i in range(zObj.rowCount()):
        zXML+= '\t\t\t\t\t<gmd:onLine>\n'
        zXML+= '\t\t\t\t\t\t<gmd:CI_OnlineResource>\n'
        zXML+= '\t\t\t\t\t\t\t<gmd:linkage>\n'
        zXML+= '\t\t\t\t\t\t\t\t<gmd:URL>%s</gmd:URL>\n' % (EncodeURLQuery(zObj.cellWidget(i, 0).text()))
        zXML+= '\t\t\t\t\t\t\t</gmd:linkage>\n'
        zXML+= '\t\t\t\t\t\t\t<gmd:name>\n'
        zXML+= '\t\t\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (EncodeText(zObj.cellWidget(i, 1).text()))
        zXML+= '\t\t\t\t\t\t\t</gmd:name>\n'
        zXML+= '\t\t\t\t\t\t</gmd:CI_OnlineResource>\n'
        zXML+= '\t\t\t\t\t</gmd:onLine>\n'
    zXML+= '\t\t\t\t</gmd:MD_DigitalTransferOptions>\n'
    zXML+= '\t\t\t</gmd:transferOptions>\n'
    
    zXML+= '\t\t</gmd:MD_Distribution>\n'
    zXML+= '\t</gmd:distributionInfo>\n'

    return zXML

def MakeDataQualityInfoXML(self):
    zXML = ''
    zObj = getWidget(self, "typedata")
    zValue = self.TypeData[zObj.currentIndex()]
    
    zXML+= '\t<gmd:dataQualityInfo>\n'
    zXML+= '\t\t<gmd:DQ_DataQuality>\n'
    zXML+= '\t\t\t<gmd:scope>\n'
    zXML+= '\t\t\t\t<gmd:DQ_Scope>\n'
    zXML+= '\t\t\t\t\t<gmd:level>\n'
    zXML+= '\t\t\t\t\t\t<gmd:MD_ScopeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/gmxCodelists.xml#MD_ScopeCode" codeListValue="%s">%s</gmd:MD_ScopeCode>\n' % (zValue, zValue)
    zXML+= '\t\t\t\t\t</gmd:level>\n'
    zXML+= '\t\t\t\t</gmd:DQ_Scope>\n'
    zXML+= '\t\t\t</gmd:scope>\n'

    zObj = getWidget(self, "tablespecifications")

    if zObj.rowCount()> 0 : zXML+= '\t\t\t<gmd:report>\n'
    for i in range(zObj.rowCount()):
        zValueSPEC = zObj.cellWidget(i, 0).text() 
        if zValueSPEC != "" :
            zXML+= '\t\t\t\t<gmd:DQ_DomainConsistency xsi:type="gmd:DQ_DomainConsistency_Type">\n'
            zXML+= '\t\t\t\t\t<gmd:result>\n'
            zXML+= '\t\t\t\t\t\t<gmd:DQ_ConformanceResult xsi:type="gmd:DQ_ConformanceResult_Type">\n'
            zXML+= '\t\t\t\t\t\t\t<gmd:specification>\n'
            zXML+= '\t\t\t\t\t\t\t\t<gmd:CI_Citation>\n'
            zXML+= '\t\t\t\t\t\t\t\t\t<gmd:title>\n'
            zXML+= '\t\t\t\t\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zValueSPEC)
            zXML+= '\t\t\t\t\t\t\t\t\t</gmd:title>\n'

            zValueDate = zObj.cellWidget(i, 1).text()
            if zValueDate.find("--") == -1 :
                zValueTypeDate = GetDateType(zObj.cellWidget(i, 2).currentIndex(), False) 
                zXML+= MakeBlocDate(self, zValueDate, zValueTypeDate, 9) 

            zXML+= '\t\t\t\t\t\t\t\t</gmd:CI_Citation>\n'
            zXML+= '\t\t\t\t\t\t\t</gmd:specification>\n'
            zXML+= '\t\t\t\t\t\t\t<gmd:explanation>\n'
            zXML+= '\t\t\t\t\t\t\t\t<gco:CharacterString>See the referenced specification</gco:CharacterString>\n'
            zXML+= '\t\t\t\t\t\t\t</gmd:explanation>\n'
            
            zIndesDegre = zObj.cellWidget(i, 3).currentIndex()
            if zIndesDegre == 0 : zValue = "true"
            elif zIndesDegre : zValue = "false"
            else : zValue = ""
            if zValue != "" :
                zXML+= '\t\t\t\t\t\t\t<gmd:pass>\n'
                zXML+= '\t\t\t\t\t\t\t\t<gco:Boolean>%s</gco:Boolean>\n' % (zValue)
                zXML+= '\t\t\t\t\t\t\t</gmd:pass>\n'
            else: zXML+= '\t\t\t\t\t\t\t<gmd:pass/>\n'   
            
            zXML+= '\t\t\t\t\t\t</gmd:DQ_ConformanceResult>\n'
            zXML+= '\t\t\t\t\t</gmd:result>\n'
            zXML+= '\t\t\t\t</gmd:DQ_DomainConsistency>\n'
    if zObj.rowCount()> 0 : zXML+= '\t\t\t</gmd:report>\n'

    zObj = getWidget(self, "genealogie")
    zValue = zObj.toPlainText()
    zXML+= '\t\t\t<gmd:lineage>\n'
    zXML+= '\t\t\t\t<gmd:LI_Lineage>\n'
    zXML+= '\t\t\t\t\t<gmd:statement>\n'
    zXML+= '\t\t\t\t\t\t<gco:CharacterString>%s</gco:CharacterString>\n' % (zValue)
    zXML+= '\t\t\t\t\t</gmd:statement>\n'
    zXML+= '\t\t\t\t</gmd:LI_Lineage>\n'
    zXML+= '\t\t\t</gmd:lineage>\n'  

    zXML+= '\t\t</gmd:DQ_DataQuality>\n'
    zXML+= '\t</gmd:dataQualityInfo>\n'

    return zXML

def MakeSpatialRepresentation(self):
    zXML = ''
    zObj = getWidget(self, "coherence")
    if zObj.toPlainText() != "" :
        import ast
        try : mydict = ast.literal_eval("%s" % (zObj.toPlainText()))
        except : mydict = None

        if mydict != None and type(mydict)==dict:
            zcondTopologyLevelCode = True if DicoHasKey(mydict, 'TopologyLevelCode') and mydict['TopologyLevelCode']!= 'unknow' else False
            zcondGeometricObjectTypeCode = True if DicoHasKey(mydict, 'GeometricObjectTypeCode') and mydict['GeometricObjectTypeCode']!= 'unknow' else False

            if zcondTopologyLevelCode or zcondGeometricObjectTypeCode :
                    zXML+= '\t<gmd:spatialRepresentationInfo>\n'
                    zXML+= '\t\t<gmd:MD_VectorSpatialRepresentation>\n'
                    if zcondTopologyLevelCode :
                        zXML+= '\t\t\t<gmd:topologyLevel>\n'
                        zXML+= '\t\t\t\t<gmd:MD_TopologyLevelCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_TopologyLevelCode" codeListValue="%s">%s</gmd:MD_TopologyLevelCode>\n' % (mydict['TopologyLevelCode'], mydict['TopologyLevelCode'])
                        zXML+= '\t\t\t</gmd:topologyLevel>\n'
                    if zcondGeometricObjectTypeCode :    
                        zXML+= '\t\t\t<gmd:geometricObjects>\n'
                        zXML+= '\t\t\t\t<gmd:MD_GeometricObjects>\n'
                        zXML+= '\t\t\t\t\t<gmd:geometricObjectType>\n'
                        zXML+= '\t\t\t\t\t\t<gmd:MD_GeometricObjectTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#MD_GeometricObjectTypeCode" codeListValue="%s">%s</gmd:MD_GeometricObjectTypeCode>\n' % (mydict['GeometricObjectTypeCode'],mydict['GeometricObjectTypeCode'])
                        zXML+= '\t\t\t\t\t</gmd:geometricObjectType>\n'
                        zXML+= '\t\t\t\t</gmd:MD_GeometricObjects>\n'
                        zXML+= '\t\t\t</gmd:geometricObjects>\n'
                    zXML+= '\t\t</gmd:MD_VectorSpatialRepresentation>\n'
                    zXML+= '\t</gmd:spatialRepresentationInfo>\n'
    return zXML               

def MakeEndXML(self):
    zXML = ''                 
    zXML+= '</gmd:MD_Metadata>'
    return zXML
    
#-----------------------------
# PRIMARY BLOC FOR XML EXPORT       
#----------------------------- 
def MakeBlocFormat(self, zObj, i, zTab):
    sTab=""
    zXML = ''
    for k in range(zTab): sTab+="\t"    
    if zObj.cellWidget(i, 0).styleSheet() == "background-color:#AEEE00;" :
        zXML+= '%s<gmd:distributionFormat>\n' % (sTab)
        zXML+= '\t%s<gmd:MD_Format>\n' % (sTab)
        zXML+= '\t\t%s<gmd:name>\n' % (sTab)
        zXML+= '\t\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zObj.cellWidget(i, 0).text())
        zXML+= '\t\t%s</gmd:name>\n' % (sTab)
        zXML+= '\t\t%s<gmd:version>\n' % (sTab)
        zXML+= '\t\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zObj.cellWidget(i, 2).text())
        zXML+= '\t\t%s</gmd:version>\n' % (sTab)
        zXML+= '\t%s</gmd:MD_Format>\n' % (sTab)
        zXML+= '%s</gmd:distributionFormat>\n' % (sTab)
        """            
        WriteInLOG(zLOG, '<gmd:amendmentNumber></gmd:amendmentNumber>\n')
        WriteInLOG(zLOG, '<gmd:specification></gmd:specification>\n')
        WriteInLOG(zLOG, '<gmd:fileDecompressionTechnique></gmd:fileDecompressionTechnique>\n')
        WriteInLOG(zLOG, '<gmd:formatDistributor></gmd:formatDistributor>\n')
        """
    return zXML
    
def MakeBlocLangue(self, zValue, zTab):
    sTab=""
    zXML = ''
    for k in range(zTab): sTab+="\t"
    zXML+= '%s<gmd:language>\n' % (sTab)
    zXML+= '%s<gmd:LanguageCode codeList="http://www.loc.gov/standards/iso639-2/" codeListValue="%s">%s</gmd:LanguageCode>\n' % ("%s%s" % (sTab, "\t"),zValue, zValue)
    zXML+= '%s</gmd:language>\n' % (sTab)
    return zXML

def MakeBlocDate(self, zValue, zType, zTab):
    sTab=""
    zXML = ''
    for k in range(zTab): sTab+="\t"
    zXML+= '%s<gmd:date>\n' % (sTab)
    zXML+= '\t%s<gmd:CI_Date>\n' % (sTab)
    zXML+= '\t\t%s<gmd:date>\n' % (sTab)
    zXML+= '\t\t\t%s<gco:Date>%s</gco:Date>\n' % (sTab, zValue)
    zXML+= '\t\t%s</gmd:date>\n' % (sTab)
    zXML+= '\t\t%s<gmd:dateType>\n' % (sTab)
    zXML+= '\t\t\t%s<gmd:CI_DateTypeCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_DateTypeCode" codeListValue="%s">%s</gmd:CI_DateTypeCode>\n' % (sTab, zType, zType)
    zXML+= '\t\t%s</gmd:dateType>\n' % (sTab)
    zXML+= '\t%s</gmd:CI_Date>\n' % (sTab)
    zXML+= '%s</gmd:date>\n' % (sTab)

    return zXML                     

def MakeBlocRole(self, zObj, zValue, i, isPointOfContact, zTab):
    sTab, k, zXML = "", 0, ''
    for k in range(zTab): sTab+="\t"    
    zXML+= '%s<gmd:contact>\n' % (sTab) if isPointOfContact else '%s<gmd:pointOfContact>\n' % (sTab)
    zXML+= MakeResponsibleParty(self, zObj, zValue, i, isPointOfContact, (k+1))
    zXML+= '%s</gmd:contact>\n' % (sTab) if isPointOfContact else '%s</gmd:pointOfContact>\n' % (sTab)
    return zXML

def MakeResponsibleParty(self, zObj, zValue, i, isPointOfContact, zTab):
    sTab=""
    zXML = ''
    for k in range(zTab): sTab+="\t"     
    zXML+= '%s<gmd:CI_ResponsibleParty>\n' % (sTab)
    zXML+= '\t%s<gmd:organisationName>\n' % (sTab)
    zXML+= '\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zObj.cellWidget(i, 1).text())
    zXML+= '\t%s</gmd:organisationName>\n' % (sTab)
    zXML+= '\t%s<gmd:contactInfo>\n' % (sTab)
    zXML+= '\t\t%s<gmd:CI_Contact>\n' % (sTab)
    
    #if zObj.cellWidget(i, 7).text()!="" :
    zXML+= '\t\t\t%s<gmd:phone>\n' % (sTab)
    zXML+= '\t\t\t\t%s<gmd:CI_Telephone>\n' % (sTab)
    zXML+= '\t\t\t\t\t%s<gmd:voice>\n' % (sTab)
    zXML+= '\t\t\t\t\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zObj.cellWidget(i, 7).text() if zObj.cellWidget(i, 7).text().strip()!="" else "")
    zXML+= '\t\t\t\t\t%s</gmd:voice>\n' % (sTab)
    zXML+= '\t\t\t\t%s</gmd:CI_Telephone>\n' % (sTab)
    zXML+= '\t\t\t%s</gmd:phone>\n' % (sTab)
    
    zXML+= '\t\t\t%s<gmd:address>\n' % (sTab)
    zXML+= '\t\t\t\t%s<gmd:CI_Address>\n' % (sTab)
    zXML+= '\t\t\t\t\t%s<gmd:deliveryPoint>\n' % (sTab)
    zXML+= '\t\t\t\t\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zObj.cellWidget(i, 2).text() if zObj.cellWidget(i, 2).text().strip()!="" else "")
    zXML+= '\t\t\t\t\t%s</gmd:deliveryPoint>\n' % (sTab)
    zXML+= '\t\t\t\t\t%s<gmd:city>\n' % (sTab)
    zXML+= '\t\t\t\t\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zObj.cellWidget(i, 5).text() if zObj.cellWidget(i, 5).text().strip()!="" else "")
    zXML+= '\t\t\t\t\t%s</gmd:city>\n' % (sTab)
    zXML+= '\t\t\t\t\t%s<gmd:postalCode>\n' % (sTab)
    zXML+= '\t\t\t\t\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zObj.cellWidget(i, 4).text() if zObj.cellWidget(i, 4).text().strip()!="" else "00000")
    zXML+= '\t\t\t\t\t%s</gmd:postalCode>\n' % (sTab)
    zXML+= '\t\t\t\t\t%s<gmd:country>\n' % (sTab)
    zXML+= '\t\t\t\t\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zObj.cellWidget(i, 3).currentText().rstrip().lstrip() if zObj.cellWidget(i, 3).currentText().strip()!="" else "")
    zXML+= '\t\t\t\t\t%s</gmd:country>\n' % (sTab)
    zXML+= '\t\t\t\t\t%s<gmd:electronicMailAddress>\n' % (sTab)
    zXML+= '\t\t\t\t\t\t%s<gco:CharacterString>%s</gco:CharacterString>\n' % (sTab, zObj.cellWidget(i, 6).text() if zObj.cellWidget(i, 6).text().strip()!="" else "")
    zXML+= '\t\t\t\t\t%s</gmd:electronicMailAddress>\n' % (sTab)
    zXML+= '\t\t\t\t%s</gmd:CI_Address>\n' % (sTab)
    zXML+= '\t\t\t%s</gmd:address>\n' % (sTab)
    
    #if zObj.cellWidget(i, 8).text()!="" :
    zXML+= '\t\t\t%s<gmd:onlineResource>\n' % (sTab)
    zXML+= '\t\t\t\t%s<gmd:CI_OnlineResource>\n' % (sTab)
    zXML+= '\t\t\t\t\t%s<gmd:linkage>\n' % (sTab)
    zXML+= '\t\t\t\t\t\t%s<gmd:URL>%s</gmd:URL>\n' % (sTab, EncodeURLQuery(zObj.cellWidget(i, 8).text()) if zObj.cellWidget(i, 8).text().strip()!="" else "")
    zXML+= '\t\t\t\t\t\t%s</gmd:linkage>\n' % (sTab)
    zXML+= '\t\t\t\t%s</gmd:CI_OnlineResource>\n' % (sTab)
    zXML+= '\t\t\t%s</gmd:onlineResource>\n'  % (sTab)   
        
    zXML+= '\t\t%s</gmd:CI_Contact>\n' % (sTab)
    zXML+= '\t%s</gmd:contactInfo>\n' % (sTab)
    zXML+= '\t%s<gmd:role>\n' % (sTab)
    zXML+= '\t\t%s<gmd:CI_RoleCode codeList="http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#CI_RoleCode" codeListValue="%s">%s</gmd:CI_RoleCode>\n' % (sTab, zValue, zValue)
    zXML+= '\t%s</gmd:role>\n' % (sTab)
    zXML+= '%s</gmd:CI_ResponsibleParty>\n' % (sTab)

    return zXML
    
#-------------------------------
# FONCTIONs TO WRITE XML EXPORT       
#-------------------------------
def GetDateType(index, TheKey):
    if index > 2 : index = 0
    zDates = (("datecredata", "creation"), ("daterevdata","revision"), ("datepubdata","publication"))
    return zDates[index][0] if TheKey else zDates[index][1]
    
def MakeCAT(self, zText):
    zTemp = zText.split("(")
    zCat = zTemp[1].replace(")", "")
    return "%s" % (zCat)

def MakeLOG(self, zFile):
    zLOG = file(zFile, "w")
    return zLOG

def WriteInLOG(zLOG, zMsg):
    if zLOG != None : zLOG.write(zMsg.encode("utf-8"))
    
def WriteInLOGWithoutEncoding(zLOG, zMsg):
    if zLOG != None : zLOG.write(zMsg)

def CloseLOG(zLOG):     
    if zLOG != None : zLOG.close()

