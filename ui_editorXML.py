# -*- coding: utf-8 -*-
#===================================================
# base on code by : Eli Bendersky (eliben@gmail.com)
# --> qsci_simple_pythoneditor.py
# This code is in the public domain
#===================================================
import codecs, os.path
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from qsphere_tools import *
from qsphere_objmaker import FindDialog
import xml.etree.ElementTree as ET
import textwrap

class xmlEditor(QDialog):

  find_text = None
  find_forward = True
  
  def __init__(self, parent, fichier):
   
    self.ARROW_MARKER_NUM = 8
    
    try:
      from PyQt4 import Qsci
      from PyQt4.Qsci import QsciScintilla, QsciScintillaBase, QsciLexerXML
    except:
      zTitle = QApplication.translate("QSphere", "Error", None, QApplication.UnicodeUTF8)
      zMsg = QApplication.translate("QSphere", "QScintilla library not detected or installed !", None, QApplication.UnicodeUTF8)
      if parent!=None : SendMessage(parent, zTitle , zMsg, QgsMessageBar.WARNING, self.duration_warning)
      return

    self.fichier = fichier
    self.parent = parent
    flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint 
    QDialog.__init__(self, parent, flags)

    self.setObjectName("DialogEditorXML")
    self.setAccessibleName("DialogEditorXML")

    makeGetOptions(self)

    self._W, self._H = 800, 520
    self.setMinimumSize(QSize(self._W,self._H))
    self.resize(QSize(QRect(0,0,self._W,self._H).size()).expandedTo(self.minimumSizeHint()))
    self.setModal(True)

    self.myPathPrint, self.myPathSave = "print.png", "save.png"
    self.myPathSizeUp, self.myPathSizeDown = "sizeup.png", "sizedown.png"

    self.racTitle = QApplication.translate("QSphere","File", None, QApplication.UnicodeUTF8)
    self.zorderkeys = ("intitule", "resume", "typedata", "tablelocalisator", "identificator", "tablelangues", "tableformats", "tablecarac", \
                  "tablecategories", "tablecategories:0", "tablemotsclefsf", "tablescr", "tableemprises", "tableetenduetemporelle", "groups:dates", \
                  "genealogie", "coherence", "grouperesolutionscale", "tablespecifications", "groupedroits", "licence", "tableroles:1", "tableroles:2", "tableroles:3", \
                  "datemetada", "langmetada")

    self.tableModel = QStandardItemModel(self)
    self.listBaliseXML = QTableView(self)
    for i in range(len(self.zorderkeys)):
        key = self.zorderkeys[i]
        item = QStandardItem()
        item.setText("%s" % (key))
        item.setCheckable(False)
        item.setEditable(False)
        self.tableModel.setItem(i,0,item)
        
    self.listBaliseXML.setColumnWidth(0, 240)
    self.listBaliseXML.horizontalHeader().setDefaultSectionSize(240)
    self.listBaliseXML.horizontalHeader().setVisible(False) 
    self.listBaliseXML.verticalHeader().setVisible(False) 
    self.listBaliseXML.setModel(self.tableModel)
    self.listBaliseXML.setSelectionMode(QAbstractItemView.SingleSelection)
    self.listBaliseXML.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.listBaliseXML.setVisible(False)
    self.listBaliseXML.setToolTip(QApplication.translate("QSphere", "Internal controls QSphere.", None, QApplication.UnicodeUTF8))

    self.valueElt =  MyTextEdit(self)
    self.valueElt.initTextEdit(200, 25, 10, 50, "valueElt", True, False, True, False, True)
    self.valueElt.setStyleSheet("color: black; background-color: #C0C0C0")
    self.valueElt.setToolTip(QApplication.translate("QSphere", "Content for the item.", None, QApplication.UnicodeUTF8))

    
    self.editor = QsciScintilla(self)
    self.editor.findDialog = FindDialog(self)
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

    self.racMSG = QApplication.translate("QSphere","QSphere XML inspector", None, QApplication.UnicodeUTF8)
    self.xmlInspector = MyPushButton(self)
    self.xmlInspector.initPushButton(48, 24, 5, 5, "FilesNavigatorButton", "", "%s %s" % (QApplication.translate("QSphere","View", None, QApplication.UnicodeUTF8), self.racMSG), True, getThemeIcon("xmlparser_true.png"), 48, 24, True)
    self.xmlInspector.setShortcut(QKeySequence("Ctrl+I"))

    self.PrintToolButton = MyPushButton(self)
    self.PrintToolButton.initPushButton(48, 24, 5, 5, "PrintToolButton", "", QApplication.translate("QSphere", "Print ToolTip", None, QApplication.UnicodeUTF8), True, getThemeIcon("printtooltip.png"), 48, 24, True)
    self.PrintToolButton.setShortcut(QKeySequence("Ctrl+Shift+P"))

    self.findprevious = MyPushButton(self)
    self.findprevious.initPushButton(48, 24, 5, 5, "findprevious", "", QApplication.translate("QSphere", "Find previous", None, QApplication.UnicodeUTF8), True, getThemeIcon("leftarrow.png"), 48, 24, True)
    self.findprevious.setShortcut(QKeySequence("F2"))

    self.searchbutton = MyPushButton(self)
    self.searchbutton.initPushButton(24, 24, 5, 5, "searchbutton", "", QApplication.translate("QSphere", "Search word", None, QApplication.UnicodeUTF8), True, getThemeIcon("find.png"), 24, 24, True)
    self.searchbutton.setShortcut(QKeySequence("Ctrl+F"))

    self.findnext = MyPushButton(self)
    self.findnext.initPushButton(48, 24, 5, 5, "findnext", "", QApplication.translate("QSphere", "Find next", None, QApplication.UnicodeUTF8), True, getThemeIcon("rightarrow.png"), 48, 24, True)
    self.findnext.setShortcut(QKeySequence("F3"))
    
    self.LoadButton = MyPushButton(self)
    self.LoadButton.initPushButton(24, 24, 5, 5, "LoadButton", "", QApplication.translate("QSphere", "Open Files", None, QApplication.UnicodeUTF8), True, getThemeIcon("open.png"), 24, 24, True)
    self.LoadButton.setShortcut(QKeySequence("Ctrl+O"))

    self.PrintButton = MyPushButton(self)
    self.PrintButton.initPushButton(24, 24, 5, 5, "PrintButton", "", QApplication.translate("QSphere", "Print", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathPrint), 24, 24, True)
    self.PrintButton.setShortcut(QKeySequence("Ctrl+P"))

    self.SaveButton = MyPushButton(self)
    self.SaveButton.initPushButton(24, 24, 5, 5, "SaveButton", "", QApplication.translate("QSphere", "Save", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathSave), 24, 24, True)
    self.SaveButton.setShortcut(QKeySequence("Ctrl+S"))

    self.ActionsSaveButton = MyPushButton(self) 
    self.ActionsSaveButton.initPushButton(56, 24, 5, 5, "ActionsSaveButton", "", QApplication.translate("QSphere","Other saving actions ...", None, QApplication.UnicodeUTF8), True, getThemeIcon("saveactions.png"), 56, 24, True)

    self.CloseButton = QPushButton(self)
    self.CloseButton.setObjectName("CloseButton")
    self.CloseButton.setText(QApplication.translate("QSphere", "Close", None, QApplication.UnicodeUTF8))

    self.ZoomInButton = MyPushButton(self)
    self.ZoomInButton.initPushButton(56, 24, 5, 5, "ZoomInButton", "", QApplication.translate("QSphere", "Zoom in", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathSizeUp), 56, 24, True)
    self.ZoomInButton.setAutoRepeat(True)
    self.ZoomInButton.setShortcut(Qt.Key_Plus)

    self.ZoomOutButton = MyPushButton(self)
    self.ZoomOutButton.initPushButton(56, 24, 5, 5, "ZoomOutButton", "", QApplication.translate("QSphere", "Zoom out", None, QApplication.UnicodeUTF8), True, getThemeIcon(self.myPathSizeDown), 56, 24, True)
    self.ZoomOutButton.setAutoRepeat(True)
    self.ZoomOutButton.setShortcut(Qt.Key_Minus)

    zIcon = getThemeIcon("qspherehelp.png")
    self.HelpButton = MyPushButton(self) 
    self.HelpButton.initPushButton(48, 48, -50, -50, "HelpButton", "", "", True, zIcon, 48, 48, True)
    self.HelpButton.setShortcut(QKeySequence("F1"))    

    self.status_txt = QLabel(self)
    self.movie = QMovie(getThemeIcon("sablier.gif"))
    self.status_txt.setMovie(self.movie)
    self.status_txt.setLayout(QHBoxLayout())
    self.status_txt.layout().addWidget(QLabel(''))
    self.status_txt.setVisible(False)

    self.editor.find_text = ""

    self.barInfo = QgsMessageBar(self)
    self.barInfo.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed ) 

    self.listBaliseXML.selectionModel().currentRowChanged.connect(self.whatItem)
    self.findprevious.clicked.connect(self.findPrevious)
    self.searchbutton.clicked.connect(self.find)
    self.findnext.clicked.connect(self.findNext)
    self.xmlInspector.clicked.connect(self.viewHideInspector)
    self.ZoomInButton.clicked.connect(self.editor.zoomIn)
    self.ZoomOutButton.clicked.connect(self.editor.zoomOut)
    self.LoadButton.clicked.connect(self.loadTheFile)
    self.PrintToolButton.clicked.connect(self.printToolTip)
    self.PrintButton.clicked.connect(self.printFile)
    self.SaveButton.clicked.connect(self.saveChanges)
    self.CloseButton.clicked.connect(self.close)
    self.HelpButton.clicked.connect(self.clickHelp)

    self.contextMnuSaveActions()

    self.findprevious.setEnabled(False)
    self.findnext.setEnabled(False)
    if fichier == "" : return
    if not self.checkProperties():
            self.BadMyISO()
            return

    self.installEventFilter(self)    

  def eventFilter(self, obj, event):
     if not event : return False
     if event == None : return False
     if event.type() == QEvent.WindowActivate : makeGetOptions(self)
     return QtGui.QDialog.eventFilter(self, obj, event) 

  def wheelEvent(self, ev):
            # Use ctrl+wheel to zoom in/out
            if Qt.ControlModifier & ev.modifiers():
                if ev.delta() > 0:
                    self.editor.zoomIn()
                else:
                    self.editor.zoomOut()
            else:
                try : return super(self.editor, self).wheelEvent(ev)
                except : pass

  def contextMnuSaveActions(self):
        contextMnu_SaveActions = QMenu()

        menuIcon = getThemeIcon("saveas.png")
        zText = QApplication.translate("QSphere","Save as ...", None, QApplication.UnicodeUTF8)
        self.SaveAsButton = QAction(QIcon(menuIcon), zText, self)
        self.SaveAsButton.setObjectName("SaveAsButton")
        self.SaveAsButton.setShortcut(QKeySequence("Ctrl+Shift+S"))
        contextMnu_SaveActions.addAction(self.SaveAsButton)
        self.SaveAsButton.triggered.connect(self.SaveCopyAs)

        contextMnu_SaveActions.addSeparator()
        
        menuIcon = getThemeIcon("savecopy.png")
        zText = QApplication.translate("QSphere","Save as a copy ...", None, QApplication.UnicodeUTF8)
        self.SaveCopyAsButton = QAction(QIcon(menuIcon), zText, self)
        self.SaveCopyAsButton.setObjectName("SaveCopyAsButton")
        self.SaveCopyAsButton.setShortcut(QKeySequence("Ctrl+Shift+C"))
        contextMnu_SaveActions.addAction(self.SaveCopyAsButton)
        self.SaveCopyAsButton.triggered.connect(self.SaveCopyAs)


        self.ActionsSaveButton.setMenu(contextMnu_SaveActions)


  def clickHelp(self): makeHelp(self)

  def startMovie(self):
     self.status_txt.setVisible(True)
     self.movie.start()
     self.status_txt.repaint()

  def stopMovie(self):
     self.movie.stop()
     self.status_txt.setVisible(False)

  def enableFindPrevNextButton(self):
    self.findprevious.setEnabled(not self.editor.find_text=="")
    self.findnext.setEnabled(not self.editor.find_text=="")

  def find(self):
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

  def isBfind(self, bfind):          
      if not bfind:
         zTitle = QApplication.translate("QSphere", "Information", None, QApplication.UnicodeUTF8)
         zMsg = QApplication.translate("QSphere","Not found", None, QApplication.UnicodeUTF8)
         SendMessage(self, zTitle , "%s :<br><u><i>%s</i></ul>" % (zMsg, self.editor.find_text), QgsMessageBar.INFO, self.duration_info)
         
  def whatItem(self, newIndex, oldIndex): self.FixeValueElt(newIndex)
      
  def FixeValueElt(self, index):
      try :
          if self.myISO == None : return
      except : return
      
      if index.row()==-1:return    
      zkey = index.sibling(index.row(), 0).data()
      if DicoHasKey(self.WidgetValues, zkey) :
         if type(self.WidgetValues[zkey])== tuple :
            zValues = [item for item in self.WidgetValues[zkey] if item!= None]
            self.valueElt.setPlainText("%s" % (zValues))
         else : self.valueElt.setPlainText("%s" % (self.WidgetValues[zkey]))

         if zkey.find("groups:")!=-1: zkey = zkey.replace("groups:", "")
         if zkey.find(":")!=-1: zkey = zkey.split(":")[0]
         zProperties=""
         for elt in ("","ax_", "bx_"):
             try : zEval = eval("self.myISO.isoModel.%s%s()" % (elt, zkey))
             except : zEval = None
             sEval = str(zEval)
             zText = QApplication.translate("QSphere", "Alternative mode", None, QApplication.UnicodeUTF8) if zProperties!="" else QApplication.translate("QSphere", "First mode", None, QApplication.UnicodeUTF8)
             zText = "<br><i><b><u>%s</u></b></i> : <br>" % zText
             zProperties+= "%s<br>%s<br>" % (zText, textwrap.fill(sEval, 100))
         zToolTip = "<table bgcolor='#ffffcc'><tr><td><h3>%s </h3><h2>[<b><font color='#0000ff'>%s</b></font>]</h2>%s</td></tr><tr><td><br><hr color='#000099'></td></tr></table>" % (QApplication.translate("QSphere", "Content for the item.", None, QApplication.UnicodeUTF8), zkey, zProperties)
         self.valueElt.setToolTip(zToolTip)
  
  def viewHideInspector(self):
      self.listBaliseXML.setVisible(not self.listBaliseXML.isVisible())
      zcond = "%s" % (not self.listBaliseXML.isVisible())
      self.xmlInspector.setToolTip("%s %s" % (QApplication.translate("QSphere","Hide", None, QApplication.UnicodeUTF8),self.racMSG)) if self.listBaliseXML.isVisible() else self.xmlInspector.setToolTip("%s %s" % (QApplication.translate("QSphere","View", None, QApplication.UnicodeUTF8), self.racMSG))
      ChangeButtonIcon(self, self.sender(),"xmlparser_%s.png" % (zcond.lower()), 48, 24)
      if not self.listBaliseXML.isVisible(): self.editor.setGeometry(QRect(10, 10,  self.width()-20, self.height()-60))
      else : self.editor.setGeometry(QRect(260, 10,  self.width()-20, self.height()-60))

  def loadTheFile(self):
      zTitle = QApplication.translate("QSphere","View a file (XML ISO 19139, HTML ...)", None, QApplication.UnicodeUTF8)
      InitDir = os.path.dirname(__file__) if self.InitDir == "" else self.InitDir
      MyFileDialog = QFileDialog(self, zTitle)
      zElt0 = QApplication.translate("QSphere","files", None, QApplication.UnicodeUTF8).title()
      MyFileDialog.setNameFilters(("%s eXtensible Markup Language (*.xml *.XML)" % (zElt0), )) 
      MyFileDialog.setViewMode(QFileDialog.Detail)
      MyFileDialog.setDirectory(InitDir)
      MyFileDialog.setFileMode(QFileDialog.ExistingFile) 
      MyFileDialog.setAcceptMode(QFileDialog.AcceptOpen)

      FixeLabelsFileDialog(self, MyFileDialog, 0, True)
      
      if MyFileDialog.exec_():
          fileName = "%s" % (MyFileDialog.selectedFiles()[0])
          if fileName!="" :
              self.fichier = fileName
              self.setWindowTitle("%s : %s" % (self.racTitle, fileName))
              self.LoadFile()
              self.InitDir = os.path.dirname(fileName)
              if not self.checkProperties():
                    self.BadMyISO()
                    return
              
  def BadMyISO(self):
      if not self.silentMode :
          zMsg = QApplication.translate("QSphere","Invalid XML document !", None, QApplication.UnicodeUTF8)
          SendMessage(self, "information" , zMsg, QgsMessageBar.WARNING, self.duration_warning)  
    
  def checkProperties(self):
    self.myISO = None
    self.valueElt.setPlainText("")
    if self.fichier == "" :
       self.majAllFalse()
       return False
    try : tree = ET.parse(self.fichier)
    except :
         self.majAllFalse()
         return False   
    root = tree.getroot()

    if root.tag != '{http://www.isotc211.org/2005/gmd}MD_Metadata':
       self.majAllFalse()
       return False   

    from xmlISOparser import *
    self.myISO = xmlISOparser(self.fichier, None, 'MEDDE', 'FR')
    zCond = self.myISO.getTagDictionnary()
    self.majCheckInfos(zCond)
    self.FixeValueElt(self.listBaliseXML.currentIndex())
    return True


  def majCheckInfos(self, zCond):
    if self.myISO == None : return
    self.myISO.createISOdataStructure(True)
    if zCond :
        self.WidgetValues = {"intitule": self.myISO.title , "resume" : self.myISO.abstract, "typedata": self.myISO.typedata, "tablelocalisator" : self.myISO.localisators, \
                         "identificator" : self.myISO.UUID, "tablelangues" : self.myISO.languesjdd, "tableformats" : self.myISO.formatsjdd, "tablecarac": self.myISO.tablecarac,  \
                         "tablecategories" : self.myISO.categories, "tablecategories:0" : self.myISO.codecategories, "tablemotsclefsf" : self.myISO.keywordsF, \
                         "tablescr" : self.myISO.scr, "tableemprises" : self.myISO.boundingboxcoordinates, \
                         "tableetenduetemporelle" : self.myISO.timeperiodes, "groups:dates" : self.myISO.dates, \
                         "genealogie" : self.myISO.genealogie, "coherence" : self.myISO.coherence, "grouperesolutionscale" : self.myISO.scalesEC, \
                         "tablespecifications": self.myISO.conformities, "groupedroits" : self.myISO.accessconstraints, "licence" : self.myISO.legalconstraints, \
                         "tableroles:1" : self.myISO.pointsofcontactMDD, "tableroles:2" : self.myISO.pointsofcontact, "tableroles:3" : self.myISO.pointsofcontactCust, \
                         "datemetada" : (self.myISO.datemdd, self.myISO.datetmdd ), "langmetada" : self.myISO.languemdd
                         }
    else :
       self.WidgetValues = {"tableroles:2": self.myISO.pointsofcontact, "tableroles:3": self.myISO.pointsofcontactCust}
     
    for row in range(len(self.zorderkeys)):  
        key = self.zorderkeys[row]
        if DicoHasKey(self.WidgetValues, key) :
            if self.WidgetValues[key]!=[[]] :
              self.listBaliseXML.model().item(row, 0).setCheckState(Qt.Checked)
              self.listBaliseXML.model().item(row, 0).setEnabled(True)          
            else :
              self.listBaliseXML.model().item(row, 0).setCheckState(Qt.Unchecked)
              self.listBaliseXML.model().item(row, 0).setEnabled(False)
        else :              
              self.listBaliseXML.model().item(row, 0).setCheckState(Qt.Unchecked)
              self.listBaliseXML.model().item(row, 0).setEnabled(False)    

  def majAllFalse(self):
      for row in range(self.listBaliseXML.model().rowCount()):
          self.listBaliseXML.model().item(row, 0).setCheckState(Qt.Unchecked)
          self.listBaliseXML.model().item(row, 0).setEnabled(False)
          
  def LoadFile(self):
     if self.fichier != "" :
        self.startMovie()
        zEncoding = getEncodingCar(self.fichier, None)
        self.editor.setText( codecs.open(self.fichier,'r',zEncoding,'replace').read() )
        self.stopMovie()
     else : self.editor.setText(self.fichier)   

  def resizeEvent(self,ev):
     zSize = ev.size()
     
     self.listBaliseXML.setGeometry(10, 10, 245, zSize.height()-265)
     self.listBaliseXML.setColumnWidth(0, 240)
     self.listBaliseXML.horizontalHeader().setDefaultSectionSize(240)

     self.valueElt.setGeometry(12, zSize.height()-250, 245, 198)
    
     self.status_txt.setGeometry(int(zSize.width()/2)-64, int(zSize.height()/2)-64, 64, 64)

     self.ZoomInButton.setGeometry(zSize.width()-580, zSize.height()-30, 56, 25)
     self.ZoomOutButton.setGeometry(zSize.width()-520, zSize.height()-30, 56, 25)
     self.barInfo.setGeometry(0, 0, zSize.width(), 90) 
     self.xmlInspector.setGeometry(10, zSize.height()-30, 48, 24)

     self.PrintToolButton.setGeometry(70, zSize.height()-30, 48, 24)

     self.findprevious.setGeometry(zSize.width()-430, zSize.height()-30, 48, 25)
     self.searchbutton.setGeometry(zSize.width()-380, zSize.height()-30, 25, 25)
     self.findnext.setGeometry(zSize.width()-350, zSize.height()-30, 48, 25)
     
     self.LoadButton.setGeometry(zSize.width()-300, zSize.height()-30, 25, 25)
     self.PrintButton.setGeometry(zSize.width()-260, zSize.height()-30, 25, 25)
     self.SaveButton.setGeometry(zSize.width()-220, zSize.height()-30, 25, 25)

     self.ActionsSaveButton.setGeometry(zSize.width()-190, zSize.height()-30, 56, 25)     
     self.CloseButton.setGeometry(zSize.width()-120, zSize.height()-30, 100, 25)

     if not self.listBaliseXML.isVisible(): self.editor.setGeometry(QRect(10, 10,  self.width()-20, self.height()-60))
     else : self.editor.setGeometry(QRect(260, 10,  self.width()-20, self.height()-60))

  def close(self): self.reject()

  def printToolTip(self):
        printer = QPrinter()
        printer.setPageSize(QPrinter.A4)
        printer.setOrientation(QPrinter.Landscape) 
        printer.setPageMargins(5, 10, 5, 10, QPrinter.Millimeter) 
        printer.setOutputFormat(QPrinter.NativeFormat)

        editor = QWebView()
        editor.setHtml(self.valueElt.toolTip())
        
        printDialog = QPrintPreviewDialog(printer)
        MakeWindowIcon(printDialog, "print.png")
        printDialog.setWindowTitle(QApplication.translate("QSphere", "Print ToolTip", None, QApplication.UnicodeUTF8))
        printDialog.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint)

        printDialog.paintRequested.connect(editor.print_)
        printDialog.exec_() 

  def printFile(self):
        printer = QPrinter()
        printer.setPageSize(QPrinter.A4)
        printer.setOrientation(QPrinter.Landscape) 
        printer.setPageMargins(5, 10, 5, 10, QPrinter.Millimeter) 
        printer.setOutputFormat(QPrinter.NativeFormat)

        editor = QTextEdit()
        editor.setAcceptRichText(True)
        editor.setPlainText(self.editor.text())
        
        printDialog = QPrintPreviewDialog(printer)
        MakeWindowIcon(printDialog, "print.png")
        printDialog.setWindowTitle(QApplication.translate("QSphere", "Print current file", None, QApplication.UnicodeUTF8))
        printDialog.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint)

        printDialog.paintRequested.connect(editor.print_)
        printDialog.exec_() 


  def SaveCopyAs(self):
        if self.editor.text()!= "" :
            zElt0 = QApplication.translate("QSphere","files", None, QApplication.UnicodeUTF8).title()
            self.Listfiltres = ("%s TXT (*.txt)" % (zElt0), "%s eXtensible Markup Language (*.xml)" % (zElt0), "%s (*.*)" % (zElt0))
            self.NamedFiltres = {"txt": "%s TXT (*.txt)" % (zElt0), "xml" : "%s eXtensible Markup Language (*.xml)" % (zElt0), "all" : "%s (*.*)" % (zElt0)}

            if self.sender() == self.SaveAsButton : zTitle = QApplication.translate("QSphere","Save as a file", None, QApplication.UnicodeUTF8)
            else : zTitle = QApplication.translate("QSphere","Save as a copy ...", None, QApplication.UnicodeUTF8)
            
            MyFileDialog = QFileDialog(self, zTitle)
            MyFileDialog.setNameFilters(self.Listfiltres)
            MyFileDialog.selectNameFilter(self.NamedFiltres["xml"])
            MyFileDialog.setViewMode(QFileDialog.Detail)
            MyFileDialog.setDirectory(self.InitDir)
            MyFileDialog.setAcceptMode(QFileDialog.AcceptSave)
            MyFileDialog.selectFile("")

            FixeLabelsFileDialog(self, MyFileDialog, 1, True)
            
            if MyFileDialog.exec_():
                fichier = FileNameWithExtension(self, MyFileDialog.selectedFiles()[0], MyFileDialog.selectedNameFilter())
                with codecs.open(fichier,'w','utf8') as f: 
                  f.write( self.editor.text() )
                if f!= None : f.close()

                if self.sender()== self.SaveAsButton : 
                    self.fichier = fichier
                    self.saveChanges()
                    self.setWindowTitle("%s : %s" % (self.racTitle, self.fichier))
                    self.InitDir = os.path.dirname(self.fichier)

                else :
                    zTitle = QApplication.translate("QSphere", "Information", None, QApplication.UnicodeUTF8)
                    zMsg = QApplication.translate("QSphere","The file xml was saved as", None, QApplication.UnicodeUTF8)
                    SendMessage(self, zTitle , "%s :<br><u><i>%s</i></ul>" % (zMsg, fichier), QgsMessageBar.INFO, self.duration_info)
            

  def saveChanges(self):
    if self.editor.text()== "" :  return
    result = False
    
    if self.fichier!= "" :
        with codecs.open(self.fichier,'w','utf8') as f: 
          f.write( self.editor.text() )
        if f!= None : f.close()  
        if not self.checkProperties():
            self.BadMyISO()
            zTitle = QApplication.translate("QSphere", "Warning", None, QApplication.UnicodeUTF8)
            zMsg1 = QApplication.translate("QSphere","The file xml was saved as", None, QApplication.UnicodeUTF8)
            zMsg2 = QApplication.translate("QSphere","Error on unsupported content :", None, QApplication.UnicodeUTF8)
            SendMessage(self, zTitle , "%s :<br><u><i>%s</i></ul><br>%s : XML." % (zMsg1, self.fichier, zMsg2), QgsMessageBar.WARNING, self.duration_warning)
            self.listBaliseXML.setVisible(True)

        
        if self.parent!=None :  
            if self.parent.objectName()!= "DialogMetaData" :
                self.parent.selfActiveLink(self.fichier)
                if (self.parent.parent)!= None and self.parent.parent.objectName()=="DialogMetaData" :
                    sFichier = "%s" % (self.fichier)
                    sTargetFichier = "%s" % (self.parent.parent.windowTitle().replace(self.parent.parent.racWindowTitle, ""))
                    if sFichier ==sTargetFichier :
                        zIndex = self.parent.parent.tabWidget.currentIndex()
                        self.parent.parent.listImportCategories = []
                        result = self.parent.parent.ReloadDataFromXML(self.myISO, self.fichier, zIndex)
                        self.parent.parent.passChangeMode()

                    if self.parent.objectName()== "DialogViewer" : self.parent.reloadPageURL()
                    
            else :
                zIndex = self.parent.tabWidget.currentIndex()
                self.parent.listImportCategories = []
                result = self.parent.ReloadDataFromXML(self.myISO, self.fichier, zIndex)
            
        zTitle = QApplication.translate("QSphere", "Information", None, QApplication.UnicodeUTF8)
        zMsg = QApplication.translate("QSphere","The metadata record was saved as", None, QApplication.UnicodeUTF8)
        if self.parent!=None :
           if result :
              SendMessage(self.parent, zTitle , "%s :<br><u><i>%s</i></ul>" % (zMsg, self.fichier), QgsMessageBar.INFO, self.parent.duration_info)
              SendMessage(self, zTitle , "%s :<br><u><i>%s</i></ul>" % (zMsg, self.fichier), QgsMessageBar.INFO, self.duration_info)
        else : SendMessage(self, zTitle , "%s :<br><u><i>%s</i></ul>" % (zMsg, self.fichier), QgsMessageBar.INFO, self.duration_info)

    else :
        zElt0 = QApplication.translate("QSphere","files", None, QApplication.UnicodeUTF8).title()
        self.Listfiltres = ("%s TXT (*.txt)" % (zElt0), "%s eXtensible Markup Language (*.xml)" % (zElt0), "%s (*.*)" % (zElt0))
        self.NamedFiltres = {"txt": "%s TXT (*.txt)" % (zElt0), "xml" : "%s eXtensible Markup Language (*.xml)" % (zElt0), "all" : "%s (*.*)" % (zElt0)}
        zTitle = QApplication.translate("QSphere","Save as a file", None, QApplication.UnicodeUTF8)
        
        MyFileDialog = QFileDialog(self, zTitle)
        MyFileDialog.setNameFilters(self.Listfiltres)
        MyFileDialog.selectNameFilter(self.NamedFiltres["xml"])
        MyFileDialog.setViewMode(QFileDialog.Detail)
        MyFileDialog.setDirectory(self.InitDir)
        MyFileDialog.setAcceptMode(QFileDialog.AcceptSave)
        MyFileDialog.selectFile("")

        FixeLabelsFileDialog(self, MyFileDialog, 1, True)
        
        if MyFileDialog.exec_():
            self.fichier = FileNameWithExtension(self, MyFileDialog.selectedFiles()[0], MyFileDialog.selectedNameFilter())
            self.saveChanges()
            self.setWindowTitle("%s : %s" % (self.racTitle, self.fichier))
            self.InitDir = os.path.dirname(self.fichier)


  def on_margin_clicked(self, nmargin, nline, modifiers):
    if self.editor.markersAtLine(nline) != 0: self.editor.markerDelete(nline, self.ARROW_MARKER_NUM)
    else: self.editor.markerAdd(nline, self.ARROW_MARKER_NUM)
