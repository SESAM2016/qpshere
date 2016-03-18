# -*- coding:utf-8 -*- 
from PyQt4 import QtCore, QtGui
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from qgis.core import *
from qgis.gui import *
from datetime import date
from qsphere_tools import *

#-------------------------
# CLASSES
#-------------------------
class FindDialog(QDialog):

    findNext = QtCore.pyqtSignal(str, int)
    findPrevious = QtCore.pyqtSignal(str, int)
  
    def __init__(self, *args, **kwargs):
        super(FindDialog, self).__init__(*args, **kwargs)
        self.setMinimumSize(QSize(400, 200))
        self.setMaximumSize(QSize(400, 200))

        self.groupBoxSearch = QGroupBox(self)
        self.groupBoxSearch.setGeometry(5, 5, 390, 140)
        
        self.label = QLabel(self)
        self.label.setText(QApplication.translate("QSphere", "Search for:", None, QApplication.UnicodeUTF8))
        self.label.setGeometry(10, 15, 80, 25)
        self.label.setAlignment(Qt.AlignRight)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(100, 10, 280, 20)
        self.ret = 0
  
        self.caseCheckBox = QCheckBox(self)
        self.caseCheckBox.setText(QApplication.translate("QSphere", "Match case", None, QApplication.UnicodeUTF8))
        self.caseCheckBox.setGeometry(100, 40, 180, 20)
        
        self.wholeWordCheckBox = QCheckBox(self)
        self.wholeWordCheckBox.setText(QApplication.translate("QSphere", "Match whole word", None, QApplication.UnicodeUTF8))
        self.wholeWordCheckBox.setGeometry(100, 60, 180, 20)

        self.model = QStandardItemModel()
        self.view = QTableView()
        self.view.setModel( self.model )
        self.view.horizontalHeader().setVisible(False)
        self.view.verticalHeader().setVisible(False)
        self.view.setColumnHidden(1, True)
        self.view.horizontalHeader().setDefaultSectionSize(400)
        self.view.verticalHeader().setDefaultSectionSize(20)
        self.view.setStyleSheet("""QTableView {selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5, stop: 0 %s, stop: 1 %s);}""" % ("#FFFFFF", "#000000"))
        self.view.setShowGrid(False)
        self.view.setMinimumSize(500, 40)

        self.ComboLines = QComboBox(self)
        self.ComboLines.setGeometry(100, 90, 280, 40)
        self.ComboLines.setObjectName("ComboLines")
        self.ComboLines.setAccessibleName("ComboLines")
        self.ComboLines.setModel(self.model)
        self.ComboLines.setView(self.view)

        self.countButton = QPushButton(self)
        self.countButton.setText("&%s" % (QApplication.translate("QSphere", "Find", None, QApplication.UnicodeUTF8)))
        self.countButton.setGeometry(10, 90, 80, 25)
        self.countButton.setEnabled(False)
  
        self.closeButton = QPushButton(self)
        self.closeButton.setText("&%s" % (QApplication.translate("QSphere", "Close", None, QApplication.UnicodeUTF8)))
        self.closeButton.setGeometry(290, 160, 100, 25)
  
        self.lineEdit.textChanged.connect(self.enableFindButton)
        self.ComboLines.currentIndexChanged.connect(self.gotoLine)
        self.countButton.clicked.connect(self.countFindClicked)
        self.closeButton.clicked.connect(self.closeme)

        self.setWindowTitle(QApplication.translate("QSphere", "Search word", None, QApplication.UnicodeUTF8))
        self.lineEdit.setFocus()
        

    def enableFindButton(self, text): self.countButton.setEnabled(not text=="")
    def closeme(self): self.close()
    
    def gotoLine(self):
        if self.ComboLines.currentIndex() == -1 : return
        model = self.ComboLines.model()
        try : pos = model.item(self.ComboLines.currentIndex(),1).text()
        except : pos = "0|0"
        coord = pos.split("|")
        try : line = int(coord[0])
        except : line = 0
        try : index = int(coord[1])
        except : index = 0

        zText = self.getFindText()
        self.parent().editor.setCursorPosition(line-1,index-len(zText))
        self.parent().editor.findFirst(self.getFindText(), True, self.isCaseSensitive(), self.isWholeWord(), True, True, line-1, index-len(zText))

    def countFindClicked(self):
        zText, ignoreCase, wholeWord = self.getFindText(), self.isCaseSensitive(), self.isWholeWord()
        line = index = 0
        lstPos = []
        self.ComboLines.clear()

        self.parent().editor.setCursorPosition(line,index)
        
        bFind = self.parent().editor.findFirst(zText, True, ignoreCase, wholeWord, True, True, line, index)
        line, index = self.parent().editor.getCursorPosition()
        
        while bFind and not (line, index) in lstPos :
            lstPos.append((line, index))
            self.AppendItemInModel(self.model, self.parent().editor.text(line), "%s|%s" % (line+1, index))
            bFind = self.parent().editor.findFirst(zText, True, ignoreCase, wholeWord, True, True, line, index)
            line, index = self.parent().editor.getCursorPosition()

        from qsphere_tools import SendMessage
        self.parent().editor.setCursorPosition(0,0)
        zTitle = QApplication.translate("QSphere", "Information", None, QApplication.UnicodeUTF8)
        zMsg = QApplication.translate("QSphere","Count", None, QApplication.UnicodeUTF8)
        SendMessage(self.parent(), zTitle , "%s : <u><i>%s</i></ul>" % (zMsg, len(lstPos)), QgsMessageBar.INFO, self.parent().duration_info)

        self.gotoLine()
        self.ret = len(lstPos)

        
    def getFindText(self): return self.lineEdit.text()
    def isCaseSensitive(self): return self.caseCheckBox.isChecked()
    def isWholeWord(self): return self.wholeWordCheckBox.isChecked()
    def AppendItemInModel(self, zModel, line, elt):
        if (elt == "") : return
        import textwrap
        zModel.appendRow([QStandardItem(textwrap.fill(line.strip(),50)), QStandardItem(elt)])


class FilteredComboBox(QComboBox):
    def __init__(self, parent=None):
        super(FilteredComboBox, self).__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        self.completer = QCompleter(self.pFilterModel, self)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        def filter(text): self.pFilterModel.setFilterFixedString("%s" % (text))

        self.lineEdit().textEdited[unicode].connect(filter)
        self.completer.activated.connect(self.on_completer_activated)

    def on_completer_activated(self, text):
        if text:
            index = self.findText("%s" % (text))
            self.setCurrentIndex(index)

    def setModel(self, model):
        super(FilteredComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(FilteredComboBox, self).setModelColumn(column)

class LusTREDialog(QDialog):
       def  __init__(self, parent, serverLusTRE, isModal):
         QDialog.__init__(self)
         self.setWindowTitle("LusTRE %s ..." % (QApplication.translate("QSphere","Web services", None, QApplication.UnicodeUTF8)))
         self._W, self._H = 580, 400
         self.setMinimumSize(QSize(self._W,self._H))
         self.setMaximumSize(QSize(self._W*2,self._H*2))
         self.resize(QSize(QRect(0,0,self._W,self._H).size()).expandedTo(self.minimumSizeHint()))
         layout = QVBoxLayout(self)

         self.parent = parent
         self.serverLusTRE = serverLusTRE
         self.isModal = isModal
         self.countkeywords = 0
         self.groupLusTREInfo = QGroupBox(self)

         from qsphere_tools import getThemeIcon
         zIcon = getThemeIcon("servers.png")
         carIcon = QImage(zIcon)
         self.ImgServerLusTRE = QLabel(self.groupLusTREInfo)
         self.ImgServerLusTRE.setObjectName("ImgServerLusTRE")
         self.ImgServerLusTRE.setAlignment(Qt.AlignCenter)
         self.ImgServerLusTRE.setPixmap(QPixmap.fromImage(carIcon).scaled(42,42))
         

         self.labelServerLusTRE = QLabel(self.groupLusTREInfo)
         self.labelServerLusTRE.setObjectName("labelServerLusTRE")
         self.labelServerLusTRE.setAlignment(Qt.AlignLeft)
         self.labelServerLusTRE.setWordWrap(True)
         self.labelServerLusTRE.setText(self.serverLusTRE)

         self.labelKeywordForLusTRE = QLabel(self.groupLusTREInfo)
         self.labelKeywordForLusTRE.setText("%s : " % (QApplication.translate("QSphere","Keyword", None, QApplication.UnicodeUTF8)))
         self.labelKeywordForLusTRE.setObjectName("labelUserServerCSWT")
         self.labelKeywordForLusTRE.setAlignment(Qt.AlignRight)    

         self.keywordForLusTRE = MyWidgetLineEdit(self.groupLusTREInfo)
         self.keywordForLusTRE.initType(6)
         self.keywordForLusTRE.setObjectName("keywordForLusTRE")
         self.keywordForLusTRE.setAccessibleName("keywordForLusTRE")
         self.keywordForLusTRE.textChanged.connect(self.keywordForLusTRE.VerifExpReg)

         zIcon = getThemeIcon("find.png") 
         zToolTip = QApplication.translate("QSphere","Get suggestion from the server", None, QApplication.UnicodeUTF8)
         self.getSuggestionButton = MyPushButton(self.groupLusTREInfo) 
         self.getSuggestionButton.initPushButton(24, 24, 50, 50, "getSuggestionButton", "", "%s %s" % (zToolTip, "LusTRE"), True, zIcon, 24, 24, True)  


         self.labelParamNbKeywords = QLabel(self.groupLusTREInfo)
         self.labelParamNbKeywords.setObjectName("labelParamNbKeywords")
         self.labelParamNbKeywords.setAlignment(Qt.AlignRight)
         self.labelParamNbKeywords.setWordWrap(True)
         self.labelParamNbKeywords.setText("%s :" % (QApplication.translate("QSphere","Num max results", None, QApplication.UnicodeUTF8)))
         self.labelParamNbKeywords.setGeometry(100, 75, 120, 25)

         self.paramNbKeywords = QSpinBox(self.groupLusTREInfo)
         self.paramNbKeywords.setGeometry(220, 70, 40, 25)
         self.paramNbKeywords.setMinimum(10)
         self.paramNbKeywords.setMaximum(100)
         self.paramNbKeywords.setValue(10)
         self.paramNbKeywords.setSingleStep(5)
         self.paramNbKeywords.setObjectName("paramNbKeywords")

         self.labelParamLangKeywords = QLabel(self.groupLusTREInfo)
         self.labelParamLangKeywords.setObjectName("labelParamLangKeywords")
         self.labelParamLangKeywords.setAlignment(Qt.AlignRight)
         self.labelParamLangKeywords.setWordWrap(True)
         self.labelParamLangKeywords.setText("%s :" % (QApplication.translate("QSphere","Language", None, QApplication.UnicodeUTF8)))
         self.labelParamLangKeywords.setGeometry(260, 75, 80, 25)

         self.ParamLangKeywords = QComboBox(self.groupLusTREInfo)
         self.ParamLangKeywords.setGeometry(340, 70, 40, 25)
         self.ParamLangKeywords.addItems(sorted(self.parent.MainPlugin.dicoLangs))
         self.ParamLangKeywords.setEditable(True)
         self.ParamLangKeywords.setInsertPolicy(QComboBox.InsertAlphabetically)
         self.ParamLangKeywords.setObjectName("ParamLangKeywords")

         self.allChildsActive = QCheckBox(self.groupLusTREInfo)
         self.allChildsActive.setGeometry(390, 70, 150, 25)
         self.allChildsActive.setText(QApplication.translate("QSphere","All children are activated", None, QApplication.UnicodeUTF8))
         self.allChildsActive.setObjectName("allChildsActive")
         self.allChildsActive.setChecked(False)         

         self.treeWidgetExpand = MyPushButton(self.groupLusTREInfo)
         self.treeWidgetExpand.initPushButton(40, 24, 5, 70, "treeWidgetExpand", "", QApplication.translate("QSphere", "Expand all", None, QApplication.UnicodeUTF8), True, getThemeIcon("tree_expand.png"), 40, 24, True)
        
         self.treeWidgetReduce = MyPushButton(self.groupLusTREInfo)
         self.treeWidgetReduce.initPushButton(40, 24, 45, 70, "treeWidgetReduce", "", QApplication.translate("QSphere", "Reduce all", None, QApplication.UnicodeUTF8), True, getThemeIcon("tree_reduce.png"), 40, 24, True)


         zLanguage = self.parent.MainPlugin.dicoLangs[self.parent.MainPlugin.indexLang]
         zIndex = self.ParamLangKeywords.findText(zLanguage) if self.ParamLangKeywords.findText(zLanguage) !=-1 else 0
         self.ParamLangKeywords.setCurrentIndex(zIndex)

         self.treeKeywords = QTreeWidget(self.groupLusTREInfo)
         self.treeKeywords.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
         self.treeKeywords.setObjectName("treeKeywords")
         self.treeKeywords.headerItem().setText(0, "1")
         self.treeKeywords.header().setVisible(False)
         self.treeKeywords.header().setDefaultSectionSize(200)

         self.treeKeywords.setStyleSheet("* { font-size:12px; background-color: rgb(255,255,255); padding: 4px ; color: black}"
                                     "QTreeWidget::item:selected {background-color: #5D5D5D; color: rgb(255,255,255); }")

         self.labelResultKeywords = QLabel(self)
         self.labelResultKeywords.setAlignment(Qt.AlignLeft)
         self.labelResultKeywords.setObjectName("labelResultKeywords")
         self.labelResultKeywords.setAccessibleName("labelResultKeywords")
         self.labelResultKeywords.setText("")

         self.status_txt = QLabel(self)
         self.movie = QMovie(getThemeIcon("sablier.gif"))
         self.status_txt.setMovie(self.movie)
         self.status_txt.setLayout(QHBoxLayout())
         self.status_txt.layout().addWidget(QLabel(''))
         self.status_txt.setVisible(False)         

         self.barInfo = QgsMessageBar(self)
         self.barInfo.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )

         self.buttonBox = QDialogButtonBox()
         self.quitButton = self.buttonBox.addButton(QApplication.translate("QSphere","Close", None, QApplication.UnicodeUTF8), QDialogButtonBox.RejectRole)
         self.buttonBox.rejected.connect(self.closeme)
        
         layout.addWidget(self.groupLusTREInfo) 
         layout.addWidget(self.buttonBox) 
         self.setLayout(layout)
         self.initTreeKeywords()
         self.refreshCounter(self.countkeywords)

         self.getSuggestionButton.clicked.connect(self.getSuggestion)
         self.treeWidgetExpand.clicked.connect(self.expandTreeWidget)
         self.treeWidgetReduce.clicked.connect(self.expandTreeWidget)         
         self.treeKeywords.itemDoubleClicked.connect(self.addKeyword)
    

       def resizeEvent(self,ev):
                zSize = ev.size()

                self.groupLusTREInfo.setGeometry(10, 10, zSize.width()-20, zSize.height()-50)

                self.ImgServerLusTRE.setGeometry(40, 2, 48, 48)
                self.labelServerLusTRE.setGeometry(90, 10, zSize.width()-110, 40)
                         
                self.labelKeywordForLusTRE.setGeometry(10, 45, 80, 25)
                self.keywordForLusTRE.setGeometry(90, 40, zSize.width()-150, 25)
                self.getSuggestionButton.setGeometry(zSize.width()-55, 40, 24, 24)

                self.treeKeywords.setGeometry(10, 100, zSize.width()-40, zSize.height()-160)
                self.status_txt.setGeometry(int(zSize.width()/2)-64, int(zSize.height()/2)-64, 64, 64)
                self.barInfo.setGeometry(0, 0, zSize.width(), 90)

                self.labelResultKeywords.setGeometry(10, zSize.height()-40, 200, 25)

       def expandTreeWidget(self):
               if self.sender() == self.treeWidgetExpand : self.treeKeywords.expandAll()
               else :
                   self.treeKeywords.collapseAll()
                   self.treeKeywords.expandItem(self.treeKeywords.itemAt(0, 0))

       def refreshCounter(self, countkeywords):
               sKeywords = QApplication.translate("QSphere", "keywords", None, QApplication.UnicodeUTF8) if countkeywords > 1 else QApplication.translate("QSphere", "keyword", None, QApplication.UnicodeUTF8) 
               self.labelResultKeywords.setText("%s %s %s %s [%s]." % (countkeywords, sKeywords, \
                                                             QApplication.translate("QSphere", "in", None, QApplication.UnicodeUTF8), QApplication.translate("QSphere", "language", None, QApplication.UnicodeUTF8), \
                                                             self.ParamLangKeywords.currentText()))  

       def startMovie(self):
              self.status_txt.setVisible(True)
              self.movie.start()
              self.status_txt.repaint()

       def stopMovie(self):
              self.movie.stop()
              self.status_txt.setVisible(False)


       def initTreeKeywords(self):
               self.results_items = None
               self.results_items = QTreeWidgetItem()
               self.results_items.setText(0, QApplication.translate("QSphere", "Results", None, QApplication.UnicodeUTF8))

               self.treeKeywords.addTopLevelItem(self.results_items)
               self.treeKeywords.expandAll()
               self.treeKeywords.resizeColumnToContents(0)
               self.treeKeywords.resizeColumnToContents(1)
               self.countkeywords = 0

       def testURL(self, ucase):
              from qsphere_tools import getThemeIcon, multi_getRequests 
              import urllib       

              if self.keywordForLusTRE.text() == "" :
                 self.MakeMsgNotValid(self.keywordForLusTRE.text())
                 return    

              self.startMovie()       
              libelleDict = {1: "suggestions"}
              libelleSubDicts = {1: ("title", "language", "conceptUri", "source")}
              zLanguage = self.parent.MainPlugin.dicoLangs[self.parent.MainPlugin.indexLang]


              try : searchkeywords = urllib.quote(self.keywordForLusTRE.text())
              except : searchkeywords = self.keywordForLusTRE.text().encode('utf-8')
       
              if ucase == 0 : zUrl = self.serverLusTRE
              elif ucase == 1 : zUrl = "%stfes/rest/GetSuggestions?keyword=%s&maxCount=%s&languages=%s&source=true" % (self.serverLusTRE, searchkeywords, self.paramNbKeywords.value(), self.ParamLangKeywords.currentText())
                     
              sites = [('%s' % (zUrl), 'GET', {'Content-Type': 'application/html'}, 'None')]
              isValidURL = multi_getRequests(self.movie, self.status_txt, sites, 10)[0][1]
              
              mycodelang = self.parent.languesDico[zLanguage]['bibliographic']               
              menuIcon = getThemeIcon("dkeywords.png")
              menuIconMetadata = getThemeIcon("metadata.png")
              menuIconSource = getThemeIcon("source.png")
              menuIconLanguage = getThemeIcon("ressources/images/%s.png" % (mycodelang))

              if isValidURL != None :

                 if ucase > 0 :

                        import ast
                        zTest = True
                        try : mydict = ast.literal_eval(isValidURL)
                        except :
                              self.MakeMsgNotValid(zUrl)
                              zTest = False

                        if zTest :     
                               self.treeKeywords.clear()
                               self.initTreeKeywords()

                               zListSubDicts = mydict[libelleDict[ucase]]
                               for dicts in zListSubDicts :
                                   keywordItem = None 
                                   for i in range(len(libelleSubDicts[ucase])):
                                       if i == 0 :  
                                          keywordItem = QTreeWidgetItem()
                                          keywordItem.setIcon(0, QIcon(menuIcon))
                                          if libelleSubDicts[ucase][0] in dicts : keywordItem.setText(0, "%s" % (dicts[libelleSubDicts[ucase][0]].decode('utf-8')))
                                          if libelleSubDicts[ucase][2] in dicts : keywordItem.setToolTip(0,  "%s" % (dicts[libelleSubDicts[ucase][2]]))
                                          
                                       else :
                                          if keywordItem != None and libelleSubDicts[ucase][i] in dicts :    
                                             keywordItemMeta = QTreeWidgetItem()

                                             if libelleSubDicts[ucase][i] in ("language", "source") :
                                                if libelleSubDicts[ucase][i]== "language" : keywordItemMeta.setIcon(0, QIcon(menuIconLanguage))
                                                else : keywordItemMeta.setIcon(0, QIcon(menuIconSource))
                                                keywordItemMeta.setText(0, "%s : %s" % (QApplication.translate("QSphere", libelleSubDicts[ucase][i], None, QApplication.UnicodeUTF8), dicts[libelleSubDicts[ucase][i]].decode('utf-8')))            
                                             else :
                                                keywordItemMeta.setIcon(0, QIcon(menuIconMetadata))    
                                                keywordItemMeta.setText(0, "%s" % (dicts[libelleSubDicts[ucase][i]].decode('utf-8')))           
                                             keywordItem.addChild(keywordItemMeta)
                                   self.results_items.addChild(keywordItem)
                                   self.countkeywords+= 1
                            
              else :
                self.MakeMsgNotValid(zUrl)
 
              self.refreshCounter(self.countkeywords)
              self.stopMovie()
      
              return isValidURL

       def MakeMsgNotValid(self, zUrl):
           from qsphere_tools import SendMessage  
           zTitle = QApplication.translate("QSphere", "Warning" , None, QApplication.UnicodeUTF8) 
           zMsg = QApplication.translate("QSphere", "Not valid", None, QApplication.UnicodeUTF8)
           zPicto = QgsMessageBar.WARNING
           zDuration = self.parent.duration_warning
           zMsg = "<b><u>%s</u></b><br><i>%s</i>." % (zUrl, zMsg)
           SendMessage(self, zTitle, zMsg, zPicto, zDuration)

       def getCapabilities(self): self.testURL(0)
       def getSuggestion(self) : self.testURL(1)

       def addKeyword(self, Item):
           if Item == None : return
           if Item.toolTip(0)=="":
              language =  "%s : " % (QApplication.translate("QSphere", "language", None, QApplication.UnicodeUTF8))
              source =  "%s : " % (QApplication.translate("QSphere", "source", None, QApplication.UnicodeUTF8))
              if not self.allChildsActive.isChecked():
                 if not (Item.text(0).startswith(language) or Item.text(0).startswith(source)) : self.parent.getDialogViewerFromAnother(Item.text(0))
              else :   
                 if Item.text(0).startswith(language) : zUrl = "https://www.google.fr/?gws_rd=ssl#q=%s+language+wiki" % (Item.text(0).replace(language,""))
                 elif Item.text(0).startswith(source) : zUrl = "https://www.google.fr/?gws_rd=ssl#q=%s+thesaurus+wiki" % (Item.text(0).replace(source,""))
                 else : zUrl = Item.text(0)
                 self.parent.getDialogViewerFromAnother(zUrl)
              return

           zState = Item.isExpanded()          

           zCommand = self.parent.findChild(QAction,"%s_6_%s" % ("Ajouter", "tablemotsclefsf"))
           if zCommand != None : zCommand.triggered.emit(True)

           zObj = self.parent.findChild(MyTableWidget,"tablemotsclefsf")
           if zObj != None :
              ObjWidget = zObj.cellWidget(zObj.rowCount()-1, 0)
              ObjWidget.setText(Item.text(0))
              ObjWidget = zObj.cellWidget(zObj.rowCount()-1, 1)
              ObjWidget.setChecked(True)
              ObjWidget = zObj.cellWidget(zObj.rowCount()-1, 2)
              zTextSource = Item.child(2).text(0)
              zTextToReplace = "%s : " % (QApplication.translate("QSphere", "source", None, QApplication.UnicodeUTF8))
              ObjWidget.setText(zTextSource.replace(zTextToReplace, ""))
              ObjWidget = zObj.cellWidget(zObj.rowCount()-1, 3)
              import datetime
              ObjWidget.setText(datetime.datetime.now().replace(microsecond=0).strftime("%Y-%m-%d"))

              self.parent.passChangeMode()
              
           Item.setExpanded(not zState)


       def closeme(self): self.killWindow()
       def killWindow(self):
               if self.parent != None  and not self.isModal :
                  try :
                      if (self) in self.parent.childswindows :
                          self.parent.childswindows.remove(self)
                          self.parent.nb_window_childs.setText("%s" % (len(self.parent.childswindows)))
                  except: pass
               self.reject()
               
                         


class AuthCSWTDialog(QDialog):
       def  __init__(self, user, pwd, serverCSWT):
         QDialog.__init__(self)
         self.setWindowTitle("%s ..." % (QApplication.translate("QSphere","Authentification for the CSW-T Server", None, QApplication.UnicodeUTF8)))
         self._W, self._H = 400, 160
         self.setMinimumSize(QSize(self._W,self._H))
         self.setMaximumSize(QSize(self._W*1.5,self._H))
         layout = QVBoxLayout(self)


         self.groupCSWTInfo = QGroupBox(self)

         from qsphere_tools import getThemeIcon
         zIcon = getThemeIcon("cswt.png")
         carIcon = QImage(zIcon)
         self.ImgServerCSWT = QLabel(self.groupCSWTInfo)
         self.ImgServerCSWT.setObjectName("ImgServerCSWT")
         self.ImgServerCSWT.setAlignment(Qt.AlignCenter)
         self.ImgServerCSWT.setPixmap(QPixmap.fromImage(carIcon).scaled(42,42))        

         self.labelServerCSWT = QLabel(self.groupCSWTInfo)
         self.labelServerCSWT.setObjectName("labelServerCSWT")
         self.labelServerCSWT.setAlignment(Qt.AlignLeft)
         self.labelServerCSWT.setWordWrap(True)
         self.labelServerCSWT.setText(serverCSWT)

         self.labelUserServerCSWT = QLabel(self.groupCSWTInfo)
         self.labelUserServerCSWT.setText("%s : " % (QApplication.translate("QSphere","User for CSW-T", None, QApplication.UnicodeUTF8)))
         self.labelUserServerCSWT.setObjectName("labelUserServerCSWT")
         self.labelUserServerCSWT.setAlignment(Qt.AlignRight)    

         self.UserCSWT = MyWidgetLineEdit(self.groupCSWTInfo)
         self.UserCSWT.initType(6)
         self.UserCSWT.setObjectName("UserCSWT")
         self.UserCSWT.setAccessibleName("UserCSWT")
         self.UserCSWT.textChanged.connect(self.UserCSWT.VerifExpReg)

         self.UserCSWT.setText(user)

         self.labelPwdUserServerCSWT = QLabel(self.groupCSWTInfo)
         self.labelPwdUserServerCSWT.setText("%s : " % (QApplication.translate("QSphere","Password for the connexion", None, QApplication.UnicodeUTF8)))
         self.labelPwdUserServerCSWT.setObjectName("labelPwdUserServerCSWT")
         self.labelPwdUserServerCSWT.setAlignment(Qt.AlignRight)  

         self.pwdUserCSWT = MyWidgetLineEdit(self.groupCSWTInfo)
         self.pwdUserCSWT.initType(9)
         self.pwdUserCSWT.setObjectName("pwdUserCSWT")
         self.pwdUserCSWT.setAccessibleName("pwdUserCSWT")
         self.pwdUserCSWT.textChanged.connect(self.pwdUserCSWT.VerifExpReg)

         self.pwdUserCSWT.setText(pwd)

         self.buttonBox = QDialogButtonBox()
         self.quitButton = self.buttonBox.addButton(QApplication.translate("QSphere","Cancel", None, QApplication.UnicodeUTF8), QDialogButtonBox.RejectRole)
         self.acceptButton = self.buttonBox.addButton(QApplication.translate("QSphere","Validate", None, QApplication.UnicodeUTF8), QDialogButtonBox.AcceptRole)
         self.buttonBox.accepted.connect(self.accept)
         self.buttonBox.rejected.connect(self.reject)

         if serverCSWT == "" or serverCSWT == None: self.acceptButton.setEnabled(False)
         
         layout.addWidget(self.groupCSWTInfo) 
         layout.addWidget(self.buttonBox) 
         self.setLayout(layout)


       def authInfos(self):
         return (self.UserCSWT.text(), self.pwdUserCSWT.text())


       def resizeEvent(self,ev):
         zSize = ev.size()

         self.groupCSWTInfo.setGeometry(10, 10, zSize.width()-20, zSize.height()-50)

         self.ImgServerCSWT.setGeometry(5, 1, 40, 40)
         self.labelServerCSWT.setGeometry(60, 10, zSize.width()-80, 40)
                  
         self.labelUserServerCSWT.setGeometry(10, 45, 180, 25)
         self.UserCSWT.setGeometry(190, 40, zSize.width()-220, 25)
     
         self.labelPwdUserServerCSWT.setGeometry(10, 75, 180, 25)
         self.pwdUserCSWT.setGeometry(190, 70, zSize.width()-220 , 25)

class SRSDialog(QDialog): 
       def __init__(self, ztext): 
         QDialog.__init__(self) 
         layout = QVBoxLayout(self) 
         self.selector = QgsProjectionSelector(self)
         self.selector.setSelectedAuthId(ztext)
         self._W, self._H = 500, 600
         self.setMinimumSize(QSize(self._W,self._H))

         self.buttonBox = QDialogButtonBox()
         self.quitButton = self.buttonBox.addButton(QApplication.translate("QSphere","Cancel", None, QApplication.UnicodeUTF8), QDialogButtonBox.RejectRole)
         self.acceptButton = self.buttonBox.addButton(QApplication.translate("QSphere","Validate", None, QApplication.UnicodeUTF8), QDialogButtonBox.AcceptRole)
         self.buttonBox.accepted.connect(self.accept)
         self.buttonBox.rejected.connect(self.reject)         
         
         layout.addWidget(self.selector) 
         layout.addWidget(self.buttonBox) 
         self.setLayout(layout) 
  
       def epsg(self):
         QGISVersionID = 0
         try: QGISVersionID = int(unicode( QGis.QGIS_VERSION_INT ))
         except: QGISVersionID = int(unicode( QGis.qgisVersion )[ 0 ])
         zCRS = self.selector.selectedEpsg() if QGISVersionID < 10900 else self.selector.selectedAuthId()
         return zCRS 

class FormatDialog(QDialog):
       def  __init__(self, listformats, zItemText):
         QDialog.__init__(self)
         self.setWindowTitle(QApplication.translate("QSphere","GDAL/OGR formats", None, QApplication.UnicodeUTF8))
         self._W, self._H = 500, 300
         self.setMinimumSize(QtCore.QSize(self._W,self._H))         
         layout = QVBoxLayout(self)
         self.gdalogrformats = listformats
         self.listformats = QListView(self)
         self.listformats.setGeometry(QtCore.QRect(10, 10, 200, 400))
         self.modele = QStringListModel()
         self.modele.setStringList(self.gdalogrformats)
         self.listformats.setModel(self.modele)
         self.listformats.setSelectionMode(QAbstractItemView.SingleSelection)
         self.listformats.setEditTriggers(QAbstractItemView.NoEditTriggers)
         self.buttonBox = QDialogButtonBox()
         self.quitButton = self.buttonBox.addButton(QApplication.translate("QSphere","Close", None, QApplication.UnicodeUTF8), QDialogButtonBox.RejectRole)
         self.acceptButton = self.buttonBox.addButton(QApplication.translate("QSphere","Select Item", None, QApplication.UnicodeUTF8), QDialogButtonBox.AcceptRole)
         self.buttonBox.accepted.connect(self.accept)
         self.buttonBox.rejected.connect(self.reject)
         
         layout.addWidget(self.listformats) 
         layout.addWidget(self.buttonBox) 
         self.setLayout(layout)

         if zItemText != "" :
            selection = self.listformats.model() #selectionModel()
            zIndexItem = self.gdalogrformats.index(zItemText) if zItemText in self.gdalogrformats else -1
            if zIndexItem != -1 :
                   index = selection.index(zIndexItem,0)
                   self.listformats.selectionModel().setCurrentIndex(index, QItemSelectionModel.Select)

         self.listformats.doubleClicked.connect(self.accept)

       def format(self):
         selection = self.listformats.selectionModel()
         indexElementSelectionne = int(selection.currentIndex().row())
         return "%s" % (self.gdalogrformats[indexElementSelectionne])     

class TopologyDialog(QDialog):
       def  __init__(self, dictinfosTopology):
         QDialog.__init__(self)
         self.setWindowTitle(QApplication.translate("QSphere","Topology informations :", None, QApplication.UnicodeUTF8))
         layout = QVBoxLayout(self)
         self._W, self._H = 400, 160
         self.setMinimumSize(QtCore.QSize(self._W,self._H))         
         self.zoneInfos = QTableWidget(0, 2, self)
         self.zoneInfos.setObjectName("zoneInfos")
         self.zoneInfos.setAccessibleName("zoneInfos")
         self.zoneInfos.setGeometry(QtCore.QRect(10, 10, 300, 130))

         self._listTopo = ("abstract", "full planar graph", "full surface graph", "full topology 3D", "geometryOnly", "planar graph", "surface graph", "topology1D", "topology3D", "unknow")
         self._listTypeVect = ("complex", "composite", "curve", "point", "solid", "surface","unknow")
         
         import ast
         try : mydict = ast.literal_eval("%s" % (dictinfosTopology))
         except : mydict = None

         from qsphere_tools import DicoHasKey
         
         if mydict!= None and type(mydict)== dict :
            zIndexTopo = self._listTopo.index(mydict['TopologyLevelCode']) if DicoHasKey(mydict, 'TopologyLevelCode') else 0
            zIndexTypeVect = self._listTypeVect.index(mydict['GeometricObjectTypeCode']) if DicoHasKey(mydict, 'GeometricObjectTypeCode') else 0    

         zDim = (160, 200)
         for i in range(len(zDim)): self.zoneInfos.setColumnWidth(i, zDim[i])         
         self.zoneInfos.verticalHeader().setVisible(False)
         self.zoneInfos.horizontalHeader().setVisible(False)

         self.zoneInfos.insertRow(0)

         ObjWidget = QLineEdit()
         ObjWidget.setMinimumSize(QtCore.QSize(160, 30))
         ObjWidget.setMaximumSize(QtCore.QSize(160, 30))
         ObjWidget.setText("TopologyLevelCode")
         ObjWidget.setEnabled(False)
         self.zoneInfos.setCellWidget(0, 0, ObjWidget)

         ObjWidget = QComboBox()
         ObjWidget.setMinimumSize(QtCore.QSize(200, 30))
         ObjWidget.setMaximumSize(QtCore.QSize(200, 30))
         ObjWidget.addItems(self._listTopo)
         ObjWidget.setCurrentIndex(zIndexTopo)
         self.zoneInfos.setCellWidget(0, 1, ObjWidget)

         self.zoneInfos.insertRow(1)

         ObjWidget = QLineEdit()
         ObjWidget.setMinimumSize(QtCore.QSize(160, 30))
         ObjWidget.setMaximumSize(QtCore.QSize(160, 30))
         ObjWidget.setText("GeometricObjectTypeCode")
         ObjWidget.setEnabled(False)
         self.zoneInfos.setCellWidget(1, 0, ObjWidget)

         ObjWidget = QComboBox()
         ObjWidget.setMinimumSize(QtCore.QSize(200, 30))
         ObjWidget.setMaximumSize(QtCore.QSize(200, 30))
         ObjWidget.addItems(self._listTypeVect)
         ObjWidget.setCurrentIndex(zIndexTypeVect)
         self.zoneInfos.setCellWidget(1, 1, ObjWidget)

         self.buttonBox = QDialogButtonBox()
         self.quitButton = self.buttonBox.addButton(QApplication.translate("QSphere","Cancel", None, QApplication.UnicodeUTF8), QDialogButtonBox.RejectRole)
         self.acceptButton = self.buttonBox.addButton(QApplication.translate("QSphere","Validate", None, QApplication.UnicodeUTF8), QDialogButtonBox.AcceptRole)
         self.buttonBox.accepted.connect(self.accept)
         self.buttonBox.rejected.connect(self.reject)
         
         layout.addWidget(self.zoneInfos) 
         layout.addWidget(self.buttonBox) 
         self.setLayout(layout)


       def infosTopology(self):
         return "{'TopologyLevelCode':'%s', 'GeometricObjectTypeCode':'%s'}" % (self.zoneInfos.cellWidget(0, 1).currentText(), self.zoneInfos.cellWidget(1, 1).currentText())

class MyComboBox(QComboBox):
      def __init__(self, *args):  QComboBox.__init__(self, *args)

      def focusInEvent(self, event):
          self.setStyleSheet("""QComboBox {color: rgb(0, 0, 0);background-color: rgba(131, 131, 131, 125)}"""
                             """QComboBox QAbstractItemView {border: 2px solid darkgray; selection-background-color: darkgray;}"""
                             )
          if self.parent().objectName()!= "formTableWidget" :
              zTableWidget = self.parent().parent()
              
              if (self.objectName().find("tablecontacts")!=-1 or self.objectName().find("tableroles")!=-1):
                     zInfos = self.objectName().split("_")
                     CurrentRow = int(zInfos[2])
                     CurrentCol = zTableWidget.currentColumn() if len(zInfos) == 4 else 0 
                     zTableWidget.setCurrentCell(CurrentRow, CurrentCol)
                     zTableWidget.selectRow(CurrentRow)

                     if zTableWidget.objectName()== "tablecontacts" : zTableWidget.parent().FixeCurrentContact()
              else :
                     if zTableWidget.parent().objectName()== "ViewerTableWidget"  :
                        zInfos = self.objectName().split("_")
                        CurrentRow = int(zInfos[2])
                        CurrentCol = zTableWidget.currentColumn() if len(zInfos) == 4 else 0 
                        zTableWidget.setCurrentCell(CurrentRow, CurrentCol)
                        zTableWidget.selectRow(CurrentRow)
                        zTableWidget.parent().FixeCurrentItem()
                 
      def focusOutEvent(self, event):
             self.setStyleSheet("""QComboBox {color: rgb(0, 0, 0);background-color: rgba(131, 131, 131, 125)}"""
                                """QComboBox QAbstractItemView {border: 2px solid darkgray; selection-background-color: darkgray;}"""
                               )



class MyAction(QAction):
      def __init__(self, zName, zText, zIcon, parent): 
         QAction.__init__(self, parent)
         self.setIcon(QIcon(zIcon))
         self.setText(zText)
         self.setObjectName(zName)

       
class MySlider(QSlider):
      def __init__(self, *args): QSlider.__init__(self, *args)

      def initSlider(self, SizeW, SizeH, zPosX, zPosY, zName, zToolTip, zGeom, zResizable, orientation, valueMin, valueMax, value):
            self.setMinimumSize(SizeW, SizeH)
            if not zResizable : self.setMaximumSize(SizeW, SizeH)
            if zGeom : self.setGeometry(zPosX, zPosY, SizeW, SizeH)
            self.setObjectName(zName)
            self.setAccessibleName(zName)
            self.setOrientation(orientation)
            self.setToolTip("%s" % (zToolTip))
            self.setMinimum(valueMin)
            self.setMaximum(valueMax)
            self.setValue(value)


class MyUserComboBox(QComboBox): 
      def __init__(self, *args):
          QComboBox.__init__(self, *args) 
          self.setStyleSheet("background-color:red;")
          self.setAcceptDrops(True)
          self.view().setDragDropMode(QAbstractItemView.DragDrop)
          
      def VerifExpReg(self):          
          self.setStyleSheet("background-color:red;")
          if self.currentText()!="" : self.setStyleSheet("background-color:#AEEE00;")    

class MyWebComboBox(FilteredComboBox): 
      def __init__(self, *args):
          FilteredComboBox.__init__(self, *args) 
          self.regex = QRegExp(r"^(http|https|ftp)\://[a-zA-Z0-9\-\.]+.[\w]{2,4}(:[a-zA-Z0-9]*)?/?([a-zA-Z0-9\-\._\?\,\'/\\\+&amp;%\$#\=~])*$", Qt.CaseSensitive)
          self.setStyleSheet("background-color:red;")
          self.setAcceptDrops(True)
          self.view().setDragDropMode(QAbstractItemView.DragDrop)
          
      def keyPressEvent(self, event):
          if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter :
             if self.parent().objectName() == "DialogViewer" :    
                zDialog = self.parent()
                zDialog.go_url()
                if zDialog.eURL.findText(zDialog.eURL.currentText())==-1 : zDialog.eURL.addItem(zDialog.eURL.currentText())
                return
          FilteredComboBox.keyPressEvent(self,event) 

      def VerifExpReg(self):          
          self.setStyleSheet("background-color:red;")
          if self.currentText().find(" ")!= -1 : self.setEditText(self.currentText().replace(" ","%20"))
          if self.regex.exactMatch(self.currentText()) : self.setStyleSheet("background-color:#AEEE00;")
          elif self.currentText()=="#blank" : self.setStyleSheet("background-color:#AEEE00;")
  

class MySimpleWidgetLineEditST(QLineEdit):
      def __init__(self, *args):
          QLineEdit.__init__(self, *args)
          self.setStyleSheet("color: rgb(0, 0, 0);background-color: rgba(131, 131, 131, 125)")
          self.setAutoFillBackground(True)
          
      def focusInEvent(self, event):
          try :
                 zInfos = self.objectName().split("_")
                 zTableWidget = self.parent().parent()
                 CurrentRow = int(zInfos[2])
                 CurrentCol = zTableWidget.currentColumn() if len(zInfos) == 4 else 0
                 zTableWidget.setCurrentCell(CurrentRow, CurrentCol)
                 zTableWidget.selectRow(CurrentRow)
                 if zTableWidget.objectName()== "tablecontacts" : zTableWidget.parent().FixeCurrentContact()
                 elif zTableWidget.parent().objectName()== "ViewerTableWidget" : zTableWidget.parent().FixeCurrentItem()
                 self.setStyleSheet("")
          except : pass             

      def focusOutEvent(self, event):
             self.setStyleSheet("color: rgb(0, 0, 0);background-color: rgba(131, 131, 131, 125)")

      def keyPressEvent(self, event):
          QLineEdit.keyPressEvent(self,event)

class MySimpleWidgetLineEdit(QLineEdit):
      def __init__(self, *args):
          QLineEdit.__init__(self, *args)
          self.setDragEnabled(True)

      def dropEvent(self, event):
          if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist") or event.mimeData().hasFormat('text/plain'):

                  if event.mimeData().hasFormat('text/plain'):
                         event.accept()
                         try : self.setText(event.mimeData().text())
                         except : pass

                  elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
                     index = self.indexAt(event.pos())
                     encoded =  event.mimeData().data("application/x-qabstractitemmodeldatalist")
                     stream = QDataStream(encoded, QIODevice.ReadOnly)
                     while not stream.atEnd():
                          row = stream.readInt()
                          column = stream.readInt()
                          map = stream.readQVariantMap()
                          if len(map.values())==1:
                                zText = "%s" % (map.values()[0])
                                if  index.row()>=0 and index.column()>=0 :
                                       try : self.item(index.row(), index.column()).setText(zText)
                                       except :
                                             try : self.cellWidget(index.row(), index.column()).setText(zText)
                                             except :
                                                 try : self.cellWidget(index.row(), index.column()).setValue(float(zText))
                                                 except :
                                                     try : self.cellWidget(index.row(), index.column()).setValue(int(zText))
                                                     except :
                                                          try :
                                                              zIndex = self.cellWidget(index.row(), index.column()).findText(zText, Qt.MatchFixedString)
                                                              if zIndex == -1 : zIndex = 0
                                                              self.cellWidget(index.row(), index.column()).setCurrentIndex(zIndex)
                                                          except : pass
                     event.accept()
          else :
                 zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
                 zMsg = QApplication.translate("QSphere","Bad format !", None, QApplication.UnicodeUTF8)
                 QMessageBox.information(None, zTitle, zMsg) 
                 event.ignore()
          
      def focusInEvent(self, event):
          try :
                 zInfos = self.objectName().split("_")
                 zTableWidget = self.parent().parent()
                 CurrentRow = int(zInfos[2])
                 CurrentCol = zTableWidget.currentColumn() if len(zInfos) == 4 else 0 
                 zTableWidget.setCurrentCell(CurrentRow, CurrentCol)
                 zTableWidget.selectRow(CurrentRow)
                 if zTableWidget.objectName()== "tablecontacts" : zTableWidget.parent().FixeCurrentContact()
                 elif zTableWidget.parent().objectName()== "ViewerTableWidget" : zTableWidget.parent().FixeCurrentItem()
          except : pass

class MyCheckBox(QCheckBox):
      def __init__(self, *args):
          QCheckBox.__init__(self, *args)
          
      def focusInEvent(self, event):
          try :
                 zInfos = self.objectName().split("_")
                 zTableWidget = self.parent().parent()
                 CurrentRow = int(zInfos[2])
                 CurrentCol = zTableWidget.currentColumn() if len(zInfos) == 4 else 0 
                 zTableWidget.setCurrentCell(CurrentRow, CurrentCol)
                 zTableWidget.selectRow(CurrentRow)
                 if zTableWidget.objectName()== "tablecontacts" : zTableWidget.parent().FixeCurrentContact()
                 elif zTableWidget.parent().objectName()== "ViewerTableWidget" : zTableWidget.parent().FixeCurrentItem()
          except : pass
     
class MyWidgetLineEdit(QLineEdit):
      def __init__(self, *args):
          QLineEdit.__init__(self, *args)
          self.setDragEnabled(True)
          self.setAcceptDrops(True)
 
      def initType(self, iType):
          if iType == 0 : self.regex = QRegExp(r"(^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,6}$)", Qt.CaseSensitive)
          elif iType == 2 : self.regex = QRegExp(r"(^(([0-8][0-9])|(9[0-5]))[0-9]{3}$)", Qt.CaseSensitive)
          elif iType == 3 : self.regex = QRegExp(r"(^EPSG:+[0-9]{4,6}$)", Qt.CaseSensitive)
          elif iType in (4, 40, 41) : self.regex = QRegExp(r"^(http|https|ftp)\://[a-zA-Z0-9\-\.]+.[\w]{2,4}(:[a-zA-Z0-9]*)?/?([a-zA-Z0-9\-\._\?\,\'/\\\+&amp;%\$#\=~])*$", Qt.CaseSensitive)
          elif iType == 9 : self.setEchoMode(QLineEdit.Password)
          self.setStyleSheet("background-color:red;") if iType != 3 else self.setStyleSheet("background-color:#AEEE00;")
          self.iType = iType

      def dragMoveEvent(self, event): pass
       
      def dragEnterEvent(self, event):
           if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist") or event.mimeData().hasFormat('text/plain'): event.accept()
           else : event.ignore()

      def dropEvent(self, event):
          if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist") or event.mimeData().hasFormat('text/plain'):
                  zObjSource = event.source()
                  first, zeroMode = False, False
                  
                  if event.mimeData().hasFormat('text/plain'):
                         event.accept()
                         try : self.setText(event.mimeData().text())
                         except : pass
                  
                  elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
                     try : index = self.indexAt(event.pos())
                     except : index = None 
                     encoded =  event.mimeData().data("application/x-qabstractitemmodeldatalist")
                     stream = QDataStream(encoded, QIODevice.ReadOnly)

                     while not stream.atEnd():
                          row = stream.readInt()
                          column = stream.readInt()
                          map = stream.readQVariantMap()
                            
                          if len(map.values())==1: zText = "%s" % (map.values()[0])
                          elif zObjSource.metaObject().className() =="QTableView" :
                               if not first :
                                  zText = zObjSource.model().item(row, column).text()
                                  first, zeroMode = True, True
                          
                          if index == None :
                             self.setText(zText)
                          else :       
                                if  index.row()>=0 and index.column()>=0 :
                                       try : self.item(index.row(), index.column()).setText(zText)
                                       except :
                                             try : self.cellWidget(index.row(), index.column()).setText(zText)
                                             except :
                                                 try : self.cellWidget(index.row(), index.column()).setValue(float(zText))
                                                 except :
                                                     try : self.cellWidget(index.row(), index.column()).setValue(int(zText))
                                                     except :
                                                          try :
                                                              zIndex = self.cellWidget(index.row(), index.column()).findText(zText, Qt.MatchFixedString)
                                                              if zIndex == -1 : zIndex = 0
                                                              self.cellWidget(index.row(), index.column()).setCurrentIndex(zIndex)
                                                          except : pass
                          if zeroMode : break   
                     event.accept()
          else :
                 zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
                 zMsg = QApplication.translate("QSphere","Bad format !", None, QApplication.UnicodeUTF8)
                 QMessageBox.information(None, zTitle, zMsg) 
                 event.ignore()

      def focusInEvent(self, event):
          try :
                 zInfos = self.objectName().split("_")
                 zTableWidget = self.parent().parent()
                 CurrentRow = int(zInfos[2])
                 CurrentCol = zTableWidget.currentColumn() if len(zInfos) == 4 else 0 
                 zTableWidget.setCurrentCell(CurrentRow, CurrentCol)
                 zTableWidget.selectRow(CurrentRow)
                 if zTableWidget.objectName()== "tablecontacts" : zTableWidget.parent().FixeCurrentContact()
                 elif zTableWidget.parent().objectName()== "ViewerTableWidget" : zTableWidget.parent().FixeCurrentItem()
          except : pass
          
      def keyPressEvent(self, event):
          if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter :
             if self.parent().objectName() == "DialogViewer" :    
                zDialog = self.parent()
                zDialog.go_url()
                return
          QLineEdit.keyPressEvent(self,event)

      def VerifExpReg(self):          
          self.setStyleSheet("background-color:red;")
          if self.iType in (0, 3, 4, 40, 41):
             zCond = False    
             if self.iType in (0, 4, 40, 41):
                zCond = True
                if self.iType in (4, 40, 41) and self.text().find(" ")!= -1 : self.setText(self.text().replace(" ","%20"))
                if self.iType == 40 : zCond = (self.text().lower().endswith("csw-publication") or self.text().lower().endswith("csw-all") or self.text().lower().endswith("csw")) 
             else :
                 zText = self.text().replace("EPSG:","")
                 if zText != "" :
                        zId = long(zText)
                        zCond = QgsCoordinateReferenceSystem().createFromSrid(zId)
             if self.regex.exactMatch(self.text()) and zCond : self.setStyleSheet("background-color:#AEEE00;")
          elif self.iType in (6,9) :
             if self.text()!= "" : self.setStyleSheet("background-color:#AEEE00;")   
          elif self.iType == 5 :
             zDate = self.text()
             zTestDate1 = verifdatechaine(zDate, "-")
             if zTestDate1 : self.setStyleSheet("background-color:#AEEE00;")
          elif self.iType == 1 :              
             zDateInf = self.text().split(" ")[0]
             zDateSup = self.text().split(" ")[1]
             zTestDate1 = verifdatechaine(zDateInf, "-")
             zTestDate2 = verifdatechaine(zDateSup, "-")
             if zTestDate1 and zTestDate2:
                L = zDateInf.split("-")
                a, m, j = int(L[0]), int(L[1]), int(L[2])
                d0 = date(a, m, j)
                L = zDateSup.split("-")
                a, m, j = int(L[0]), int(L[1]), int(L[2])
                d1 = date(a, m, j)
                delta = d1 - d0
                if (delta.days)>=0 : self.setStyleSheet("background-color:#AEEE00;")

                
          if self.iType == 2 :
              if self.regex.exactMatch(self.text()):
                 if self.regex.pattern() == "(^(([0-8][0-9])|(9[0-5]))[0-9]{3}$)" :
                    if self.text()!="00000" : self.setStyleSheet("background-color:#AEEE00;") 
                 else : self.setStyleSheet("background-color:#AEEE00;")

class MyLabel(QLabel):
     def __init__(self, *args):
             QLabel.__init__(self, *args)
             self.setStyleSheet("QLabel { border-top : 1px solid yellow;  border-bottom : 1px solid yellow;  border-left: 1px solid yellow;  border-right : 1px solid yellow }")
             self.setWindowOpacity(0.5)
             self.setAutoFillBackground(False)
             self.setUpdatesEnabled(True)

class MyButton(QPushButton):
     def __init__(self, *args):  QPushButton.__init__(self, *args)
            
     def initButton(self, SizeW, SizeH, zPosX, zPosY, zName, zText, zToolTip, zEnable, zGeom):
            self.setMinimumSize(QtCore.QSize(SizeW, SizeH))
            self.setMaximumSize(QtCore.QSize(SizeW, SizeH))
            if zGeom : self.setGeometry(QtCore.QRect(zPosX, zPosY, SizeW, SizeH))
            self.setObjectName(zName)
            self.setAccessibleName(zName)
            self.setToolTip("%s" % (zToolTip))
            self.setText(zText)
            self.setEnabled(zEnable)

class MyPushButton(QPushButton):
     def __init__(self, *args):  QPushButton.__init__(self, *args)
            
     def initPushButton(self, zSizeW, zSizeH, zPosX, zPosY, zName, zText, zToolTip, zGeom, zIcon, zSizeWIcon, zSizeHIcon, zStyleSheet):
            self.setMinimumSize(QtCore.QSize(zSizeW, zSizeH))
            self.setMaximumSize(QtCore.QSize(zSizeW, zSizeH))
            if zGeom : self.setGeometry(QtCore.QRect(zPosX, zPosY, zSizeW, zSizeH))
            if zIcon != "" :
               self.setIcon(QIcon(zIcon))
               self.setIconSize(QSize(zSizeWIcon, zSizeHIcon))
            self.setToolTip(zToolTip)
            if zStyleSheet : self.setStyleSheet(""" QPushButton {border: none;}""")
            self.setObjectName(zName)
            self.setAccessibleName(zName)
            if zText != "" : self.setText(zText)


class MyPushButtonMappable(QPushButton):
     def __init__(self, *args):  QPushButton.__init__(self, *args)
            
     def initPushButton(self, zSizeW, zSizeH, zPosX, zPosY, zName, zText, zToolTip, zGeom, zIcon, zSizeWIcon, zSizeHIcon, zStyleSheet):
            self.setMinimumSize(QtCore.QSize(zSizeW, zSizeH))
            self.setMaximumSize(QtCore.QSize(zSizeW, zSizeH))
            if zGeom : self.setGeometry(QtCore.QRect(zPosX, zPosY, zSizeW, zSizeH))
            if zIcon != "" :
               self.setIcon(QIcon(zIcon))
               self.setIconSize(QSize(zSizeWIcon, zSizeHIcon))
            self.setToolTip(zToolTip)
            if zStyleSheet : self.setStyleSheet(""" QPushButton {border: none;}""")
            self.setObjectName(zName)
            self.setAccessibleName(zName)
            self.isMappable, self.MainPlugin = False, None
            if zText != "" : self.setText(zText)

     def mousePressEvent(self, event):
            if self.isMappable :
               if event.button() == Qt.LeftButton:
                  pos, index = event.pos().x(), -1
                  if 65 <= pos <= 90     : index = 0 #("fr")
                  elif 91 <= pos <= 110  : index = 1 #("en")
                  elif 111 <= pos <= 130 : index = 2 #("it")
                  elif 131 <= pos <= 155 : index = 3 #("de")
                  elif 156 <= pos <= 175 : index = 4 #("es")
                  elif 176 <= pos <= 200 : index = 5 #("fi")

                  if index != -1 :
                     if self.MainPlugin != None :    
                            self.MainPlugin.indexLang = index
                            self.indexLang = index
                            self.parent().changeLang()
                     else :
                            from qsphere_tools import SendMessage      
                            zTitle = QApplication.translate("QSphere", "Warning" , None, QApplication.UnicodeUTF8) 
                            zMsg = QApplication.translate("QSphere","Can only change the language by MainPlugin !", None, QApplication.UnicodeUTF8)
                            SendMessage(self.parent(), zTitle, "<font color='#ff0000'><b>%s</b></font>" % (zMsg), QgsMessageBar.WARNING, self.parent().duration_warning)

                   

class MySpinBox(QDoubleSpinBox):
     def __init__(self, *args):  QDoubleSpinBox.__init__(self, *args)
     
     def initDoubleSpinBox(self, parent, gui):
            self.parent = parent
            self.gui = gui 
            self.setFocusPolicy(QtCore.Qt.StrongFocus)

            self.installEventFilter(self)


     def eventFilter(self, object, event):
          if not event : return False
          if event == None : return False
          if event.type() == QEvent.FocusIn:
             zIndexEmp = int(object.accessibleName().split("_")[2])
             try :
                 self.parent.setToolTip("%s" % (zIndexEmp))
                 if self.parent.metaObject().className() in ("QTableWidget", "MyTableWidget") :
                    self.parent.selectRow(zIndexEmp)
                    if self.parent.parent().objectName() == "ViewerTableWidget" : self.parent.parent().FixeCurrentItem()
                 return True
             except : return False
          else : return False


class MyTextEdit(QTextEdit):           
     def __init__(self, *args): QTextEdit.__init__(self, *args)
     
     def initTextEdit(self, SizeW, SizeH, zPosX, zPosY, zName, zGeom, zUndoRedo, zReadOnly, zRichText, zResizable):
            self.setMinimumSize(QtCore.QSize(SizeW, SizeH))
            if not zResizable : self.setMaximumSize(QtCore.QSize(SizeW, SizeH))
            if zGeom : self.setGeometry(QtCore.QRect(zPosX, zPosY, SizeW, SizeH))
            self.setUndoRedoEnabled(zUndoRedo)
            self.setReadOnly(zReadOnly)
            self.setAcceptRichText(zRichText)
            self.setObjectName(zName)
            self.setAccessibleName(zName)
            self.setAcceptDrops(True)

     def dragEnterEvent(self, event): event.accept()
     def dragLeaveEvent(self, event): event.accept()
     def dragMoveEvent(self, event): event.accept()
     def dropEvent(self, event):
          if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist") or event.mimeData().hasFormat('text/plain'):
                  cursor = self.textCursor()
                  if event.mimeData().hasFormat('text/plain'): cursor.insertText(event.mimeData().text())
                  elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
                     encoded =  event.mimeData().data("application/x-qabstractitemmodeldatalist")
                     stream = QDataStream(encoded, QIODevice.ReadOnly)
                     while not stream.atEnd():
                          row = stream.readInt()
                          column = stream.readInt()
                          map = stream.readQVariantMap()
                          if len(map.values())==1:
                                zText = "%s" % (map.values()[0])
                                try : cursor.insertText(zText) 
                                except : pass
                     event.accept()
          else :
                 zTitle = QApplication.translate("QSphere","Information", None, QApplication.UnicodeUTF8)
                 zMsg = QApplication.translate("QSphere","Bad format !", None, QApplication.UnicodeUTF8)
                 QMessageBox.information(None, zTitle, zMsg) 
                 event.ignore()
  

class MyTableWidget(QTableWidget):           
       def __init__(self, *args):
              QTableWidget.__init__(self, *args)
              self.setDragEnabled(True)
              self.setAcceptDrops(True)
              self.setDragDropOverwriteMode(False)
              self.setDropIndicatorShown(True)
              self.setSelectionMode(QAbstractItemView.SingleSelection)
              self.setSelectionBehavior(QAbstractItemView.SelectRows) 
              self.setDragDropMode(QAbstractItemView.DragDrop) 
              self.verticalHeader().setMovable(True)
         
       def fixeMenu(self, menu): self.menu = menu

       def dropEvent(self, event):
           if event.mimeData().hasFormat('text/plain'):
              index = self.indexAt(event.pos())
              if  index.row()>=0 and index.column()>=0 :
                  try : self.item(index.row(), index.column()).setText(zText)
                  except :                     
                         try : self.cellWidget(index.row(), index.column()).setText(event.mimeData().text())
                         except :       
                                   try : self.cellWidget(index.row(), index.column()).setValue(float(event.mimeData().text()))
                                   except :
                                       try : self.cellWidget(index.row(), index.column()).setValue(int(event.mimeData().text()))
                                       except :
                                            try :
                                                zIndex = self.cellWidget(index.row(), index.column()).findText(event.mimeData().text(), Qt.MatchFixedString)
                                                if zIndex == -1 : zIndex = 0
                                                self.cellWidget(index.row(), index.column()).setCurrentIndex(zIndex)
                                            except :
                                                 try:
                                                      zItemComment = QTableWidgetItem()
                                                      zItemComment.setText("%s" % (event.mimeData().text()))
                                                      self.setItem(index.row(), index.column(), zItemComment)
                                                      self.item( index.row(), index.column() ).setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled)
                                                 except : pass
              else :
                 zIndex = self.refDialog.tabWidget.currentIndex() #self.refDialog.listeOnglets.currentIndex() 
                 self.refDialog.AddDragDropLine(self, event.mimeData().text())
                 self.refDialog.tabWidget.setCurrentIndex(zIndex) #self.refDialog.listeOnglets.setCurrentIndex(zIndex) 
                        
              event.accept()
          
           elif event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
              zObjSource = event.source()
              first, zeroMode = False, False
              
              index = self.indexAt(event.pos())
              encoded =  event.mimeData().data("application/x-qabstractitemmodeldatalist")
              stream = QDataStream(encoded, QIODevice.ReadOnly)
              
              while not stream.atEnd():
                   row = stream.readInt()
                   column = stream.readInt()
                   map = stream.readQVariantMap()

                   if len(map.values())==1: zText = "%s" % (map.values()[0])
                   elif zObjSource.metaObject().className() =="QTableView" :
                        if not first :
                           zText = zObjSource.model().item(row, column).text()
                           first, zeroMode = True, True

                   if  index.row()>=0 and index.column()>=0 :
                         try : self.item(index.row(), index.column()).setText(zText)
                         except :
                               try : self.cellWidget(index.row(), index.column()).setText(zText)
                               except :
                                   try : self.cellWidget(index.row(), index.column()).setValue(float(zText))
                                   except :
                                       try : self.cellWidget(index.row(), index.column()).setValue(int(zText))
                                       except :
                                            try :
                                                zIndex = self.cellWidget(index.row(), index.column()).findText(zText, Qt.MatchFixedString)
                                                if zIndex == -1 : zIndex = 0
                                                self.cellWidget(index.row(), index.column()).setCurrentIndex(zIndex)
                                            except : pass

                   else :
                        zIndex = self.refDialog.tabWidget.currentIndex() #self.refDialog.listeOnglets.currentIndex() 
                        self.refDialog.AddDragDropLine(self, zText)
                        self.refDialog.tabWidget.setCurrentIndex(zIndex) #self.refDialog.listeOnglets.setCurrentIndex(zIndex)

                   if zeroMode : break
                   
              event.accept()
               
           else : event.ignore()
               
       def dragMoveEvent(self, event): pass
       
       def dragEnterEvent(self, event):
           if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist") or event.mimeData().hasFormat('text/plain'): event.accept()
           else : event.ignore()
     
       def contextMenuEvent(self, event): action = self.menu.exec_(self.mapToGlobal(event.pos()))



class MyProgressBar(QProgressBar):
     def __init__(self, *args): QProgressBar.__init__(self, *args)

     def initTextEdit(self, SizeW, SizeH, zPosX, zPosY, zName, zGeom, zInitValue, zViewText, zAlign, zStyleSheet):
            self.setMinimumSize(QtCore.QSize(SizeW, SizeH))
            self.setMaximumSize(QtCore.QSize(SizeW, SizeH))
            if zGeom : self.setGeometry(QtCore.QRect(zPosX, zPosY, SizeW, SizeH))          
            self.setProperty("value", zInitValue)
            self.setAlignment(zAlign)
            self.setTextVisible(zViewText)
            self.setObjectName(zName)
            self.setAccessibleName(zName)
            if zStyleSheet == 0 :
                 self.setStyleSheet(
                      """QProgressBar {border: 2px solid grey; border-radius: 5px; text-align: center;}"""
                      """QProgressBar::chunk {background-color: #6C96C6; width: 10px; margin: 0.5px;}"""
                  )

class MyListView(QListView):           
     def __init__(self, *args): QListView.__init__(self, *args)
            
     def initListView(self, SizeW, SizeH, zPosX, zPosY, zName, zGeom):
            self.setMinimumSize(QtCore.QSize(SizeW, SizeH))
            self.setMaximumSize(QtCore.QSize(SizeW, SizeH))
            if zGeom : self.setGeometry(QtCore.QRect(zPosX, zPosY, SizeW, SizeH))
            self.setObjectName(zName)
            self.setAccessibleName(zName)
            zFontStyle = "font: 9pt \"%s\";" % (QFont().defaultFamily())
            self.setStyleSheet(zFontStyle)

class MyListWidget(QListWidget):           
     def __init__(self, *args): QListWidget.__init__(self, *args)
            
     def initListWidget(self, SizeW, SizeH, zPosX, zPosY, zName, zGeom):
            self.setMinimumSize(QtCore.QSize(SizeW, SizeH))
            self.setMaximumSize(QtCore.QSize(SizeW, SizeH))
            if zGeom : self.setGeometry(QtCore.QRect(zPosX, zPosY, SizeW, SizeH))
            self.setObjectName(zName)
            self.setAccessibleName(zName)
            zFontStyle = "font: 9pt \"%s\";" % (QFont().defaultFamily())
            self.setStyleSheet(zFontStyle)

class MyTreeView(QTreeView):
     def __init__(self, *args): QTreeView.__init__(self, *args)

     def initTreeView(self, SizeW, SizeH, zPosX, zPosY, zName, zGeom, zDragDropMode, zHeaderHidden, zWordWrap, zEditTriggers, zStyleSheet):
            self.setMinimumSize(QtCore.QSize(SizeW, SizeH))
            self.setMaximumSize(QtCore.QSize(SizeW, SizeH))
            if zGeom : self.setGeometry(QtCore.QRect(zPosX, zPosY, SizeW, SizeH))
            self.setDragDropMode(zDragDropMode)
            self.setHeaderHidden(True)
            self.setWordWrap(True)
            self.setEditTriggers(zEditTriggers)
            self.setObjectName(zName)
            self.setAccessibleName(zName)
            if zStyleSheet == 0 :
                 myPathIconvLine = getThemeIcon("vline.png") 
                 myPathIconBranchMore = getThemeIcon("branch-more.png")
                 myPathIconBranchEnd = getThemeIcon("branch-end.png") 
                 myPathIconBranchClosed = getThemeIcon("branch-closed.png")
                 myPathIconBranchOpen = getThemeIcon("branch-open.png") 
                 
                 self.setStyleSheet(
                      """QTreeView  {show-decoration-selected: 1;}"""
                      """QTreeView::title {}"""
                      """QTreeView::item  {border: 1px solid #d9d9d9; border-top-color: transparent; border-bottom-color: transparent;}"""
                      """QTreeView::item:hover  {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1); border: 1px solid #bfcde4;}"""
                      """QTreeView::item:selected  {border: 1px solid #567dbc;}"""
                      """QTreeView::item:selected:active {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);}"""
                      """QTreeView::item:selected:!active  { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);}"""
                      """QTreeView::item {margin: 5px;}"""
                      """QTreeView::branch:setDrahas-siblings:!adjoins-item  {border-image: url("""+myPathIconvLine+""") 0;}"""
                      """QTreeView::branch:has-siblings:adjoins-item  {border-image: url("""+myPathIconBranchMore+""") 0;}"""
                      """QTreeView::branch:!has-children:!has-siblings:adjoins-item  {border-image: url("""+myPathIconBranchEnd+""") 0;}"""
                      """QTreeView::branch:has-children:!has-siblings:closed, QTreeView::branch:closed:has-children:has-siblings  {border-image: none; image: url("""+myPathIconBranchClosed+""");}"""
                      """QTreeView::branch:open:has-children:!has-siblings,QTreeView::branch:open:has-children:has-siblings   { border-image: none; image: url("""+myPathIconBranchOpen+""");}"""
                  )



#----------------
# FUNCTIONS DATE 
#----------------
def bissextile(an):
    if (an % 4)==0:
        if ((an % 100)==0) and ((an % 400)<>0): return False
        else: return True
    else: return False
 
def verifdate(j,m,a):
    # correction for short date year (eg.: '09' ald '2009')
    if a<100:
        if a<0: return False  
        if a<50: a += 2000  
        else: a += 1900  
    if m<1 or m>12 or j<1: return False
    if j>(31,29,31,30,31,30,31,31,30,31,30,31)[m-1]: return False
    if (not bissextile(a)) and m==2 and j>28: return False
    return True
 
def verifdatechaine(D, sep="/"):
    L = D.split(sep)
    if len(L)!=3: return False
    try: a, m, j = int(L[0]), int(L[1]), int(L[2])
    except: return False
    return verifdate(j,m,a)
