# -*- coding:utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from qgis.core import *
from qgis.gui import *
from qsphere_tools import *
from qsphere_objmaker import *
from importexport import *
import ConfigParser
import os


class Ui_Dialog_Contact(object):
   
    def setupUi(self):
        self._W, self._H = 960, 580
        self.setMinimumSize(QSize(self._W,self._H))
        self.setObjectName("DialogContacts")
        self.setAccessibleName("DialogContacts")
        self.resize(QSize(QRect(0,0,self._W,self._H).size()).expandedTo(self.minimumSizeHint()))
        self.setWindowFlags(Qt.WindowMaximizeButtonHint)
        self.initDir = ""

        self.zTablesWidget = {"tableroles" : ((100, 80, 80, 80, 60, 80, 80, 80, 80),(QApplication.translate("QSphere","Role", None, QApplication.UnicodeUTF8), \
                                QApplication.translate("QSphere","Organization name", None, QApplication.UnicodeUTF8), \
                                QApplication.translate("QSphere","Address", None, QApplication.UnicodeUTF8), \
                                QApplication.translate("QSphere","Country", None, QApplication.UnicodeUTF8), \
                                QApplication.translate("QSphere","Zip code", None, QApplication.UnicodeUTF8), \
                                QApplication.translate("QSphere","City", None, QApplication.UnicodeUTF8), \
                                QApplication.translate("QSphere","E-mail", None, QApplication.UnicodeUTF8), \
                                QApplication.translate("QSphere","Phone", None, QApplication.UnicodeUTF8), \
                                "URL")), \
                              }
        self.dims = self.zTablesWidget["tableroles"][0]
        self.originalW = 800

        makeGetOptions(self)

        self.racWindowTitle = QApplication.translate("QSphere", "Contacts list file", None, QApplication.UnicodeUTF8)
        self.setWindowTitle("%s : %s" % (self.racWindowTitle, ""))
        self.groupStyleSheet = """QGroupBox {background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E0E0E0, stop: 1 #FFFFFF);""" \
                                   """border: 2px solid gray; border-radius: 5px; margin-top: 1ex; })"""        

        self.myPathPrint, self.myPathReLoadFile, self.myPathLoadFile, self.myPathAddFile = "print.png", "reload.png", "open.png", "add.png"
        self.myPathViewFile, self.myPathNewList, self.myPathSave, self.myPathSaveAs = "navigatorweb.png", "new.png", "save.png", "saveas.png"
        self.ParamsLineWidget = ((2, 0, 0),(-2, 0, ""), (-2, 0, ""), (2, 5, self.indexCountry), (0, 2, ""), (-2, 0, ""), (0, 0, ""), (-1, 0, ""), (0, 4, ""))
        zSizeW, zSizeH = self.width()-20, self.height()-50
        self.filtreQSP = "QSphere %s (*.qsp)" % (QApplication.translate("QSphere","project", None, QApplication.UnicodeUTF8))


        #Group Actions Annuaire
        self.groupBoxActionsAnnuaire = QGroupBox(self)
        self.groupBoxActionsAnnuaire.setObjectName("groupBoxActionsAnnuaire")
        self.groupBoxActionsAnnuaire.setStyleSheet(self.groupStyleSheet)

        self.labeleAnnuaire = QLabel(self.groupBoxActionsAnnuaire)
        self.labeleAnnuaire.setGeometry(QRect(10, 15,  120, 25))
        self.labeleAnnuaire.setText("%s : " % (QApplication.translate("QSphere", "List of Contacts", None, QApplication.UnicodeUTF8)))
        self.labeleAnnuaire.setAlignment(Qt.AlignRight)

        self.Annuaire = QComboBox(self.groupBoxActionsAnnuaire)
        self.Annuaire.setGeometry(125, 15, 250, 25)
        self.Annuaire.setEditable(False)
        self.Annuaire.setEnabled(True)
        self.Annuaire.setObjectName("Annuaire")
        self.Annuaire.setAccessibleName("Annuaire")
        self.Annuaire.addItem("")


        zToolTip =  QApplication.translate("QSphere", "Refresh list of contacts with current file", None, QApplication.UnicodeUTF8)
        self.ReloadAnnuaire = MyPushButton(self.groupBoxActionsAnnuaire)
        self.ReloadAnnuaire.initPushButton(24, 24, 10, 5, "ReloadAnnuaire", "", zToolTip, True, getThemeIcon(self.myPathReLoadFile), 24, 24, True)
        self.ReloadAnnuaire.setShortcut(QKeySequence("F5"))

        zToolTip = QApplication.translate("QSphere", "View current contacts list file ...", None, QApplication.UnicodeUTF8)
        self.ViewAnnuaire = MyPushButton(self.groupBoxActionsAnnuaire)
        self.ViewAnnuaire.initPushButton(24, 24, 50, 5, "ViewAnnuaire", "", zToolTip, True, getThemeIcon(self.myPathViewFile), 24, 24, True)
        self.ViewAnnuaire.setShortcut(QKeySequence("Ctrl+W"))

        zToolTip = QApplication.translate("QSphere", "Choose contacts list file ...", None, QApplication.UnicodeUTF8)
        self.LoadAnnuaire = MyPushButton(self.groupBoxActionsAnnuaire)
        self.LoadAnnuaire.initPushButton(24, 24, 90, 5, "LoadAnnuaire", "", zToolTip, True, getThemeIcon(self.myPathLoadFile), 24, 24, True)
        self.LoadAnnuaire.setShortcut(QKeySequence("Ctrl+O"))

        zToolTip =  QApplication.translate("QSphere", "New list file in current list ...", None, QApplication.UnicodeUTF8)
        self.NewAnnuaire = MyPushButton(self.groupBoxActionsAnnuaire)
        self.NewAnnuaire.initPushButton(24, 24, 130, 45, "NewAnnuaire", "", zToolTip, True, getThemeIcon(self.myPathNewList), 24, 24, True)
        self.NewAnnuaire.setShortcut(QKeySequence("Ctrl+N"))

        zToolTip = QApplication.translate("QSphere", "Add contacts list file in current list ...", None, QApplication.UnicodeUTF8)
        self.AddAnnuaire = MyPushButton(self.groupBoxActionsAnnuaire)
        self.AddAnnuaire.initPushButton(24, 24, 165, 45, "AddAnnuaire", "", zToolTip, True, getThemeIcon(self.myPathAddFile), 24, 24, True)
        self.AddAnnuaire.setShortcut(QKeySequence("Ctrl+A"))

        zToolTip = QApplication.translate("QSphere", "Import contacts from current sheet ...", None, QApplication.UnicodeUTF8)
        self.ImportResponsibleInAnnuaire = MyPushButton(self.groupBoxActionsAnnuaire)
        self.ImportResponsibleInAnnuaire.initPushButton(65, 24, 200, 45, "ImportResponsibleInAnnuaire", "", zToolTip, True, getThemeIcon("importresponsible.png"), 65, 24, True)
        self.ImportResponsibleInAnnuaire.setShortcut(QKeySequence("Ctrl+G"))

        zToolTip = QApplication.translate("QSphere", "Import contacts from QSP file in current list ...", None, QApplication.UnicodeUTF8)
        self.ImportInAnnuaire = MyPushButton(self.groupBoxActionsAnnuaire)
        self.ImportInAnnuaire.initPushButton(65, 24, 270, 45, "ImportInAnnuaire", "", zToolTip, True, getThemeIcon("importcontact.png"), 65, 24, True)
        self.ImportInAnnuaire.setShortcut(QKeySequence("Ctrl+I"))

        zToolTip = QApplication.translate("QSphere", "Save the current list", None, QApplication.UnicodeUTF8)      
        self.SaveButton = MyPushButton(self.groupBoxActionsAnnuaire)
        self.SaveButton.initPushButton(24, 24, 340, 45, "SaveButton", "", zToolTip, True, getThemeIcon(self.myPathSave), 24, 24, True)
        self.SaveButton.setShortcut(QKeySequence("Ctrl+S"))

        zIcon = getThemeIcon("qspherehelp.png")
        self.HelpButton = MyPushButton(self) 
        self.HelpButton.initPushButton(48, 48, -50, -50, "HelpButton", "", "", True, zIcon, 48, 48, True)
        self.HelpButton.setShortcut(QKeySequence("F1"))

        self.ActionsSaveButton = MyPushButton(self.groupBoxActionsAnnuaire) 
        self.ActionsSaveButton.initPushButton(56, 24, 380, 45, "ActionsSaveButton", "", QApplication.translate("QSphere","Other saving actions ...", None, QApplication.UnicodeUTF8), True, getThemeIcon("saveactions.png"), 56, 24, True)

        self.progressBar = QProgressBar(self.groupBoxActionsAnnuaire)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet(
             """QProgressBar {border: 2px solid grey; border-radius: 5px; text-align: center;}"""
             """QProgressBar::chunk {background-color: #6C96C6; width: 20px;}"""
        )
        self.progressBar.setVisible(False)
        self.progressBar.setValue(0)
        self.progressBar.setGeometry(420, 50, 320, 15)

        self.tableWidget = QTableWidget(0, 9, self)
        self.tableWidget.setTabKeyNavigation(False)
        self.tableWidget.setObjectName("tablecontacts")
        self.tableWidget.setAccessibleName("tablecontacts")
        self.tableWidget.setStyleSheet("""QTableWidget {selection-background-color: rgb(50, 125, 180); }""")

        #Group Actions to process
        self.groupBoxActions = QGroupBox(self)
        self.groupBoxActions.setObjectName("groupBoxActions")
        self.groupBoxActions.setStyleSheet(self.groupStyleSheet)

        zToolTip = QApplication.translate("QSphere","Add a Line", None, QApplication.UnicodeUTF8)
        self.AddLineWidgetContact = MyPushButton(self.groupBoxActions) 
        self.AddLineWidgetContact.initPushButton(24, 24, 15, 40, "AddLineWidgetContact", "", zToolTip, True, getThemeIcon("tab_addline.png"), 24, 24, True)
        self.AddLineWidgetContact.setShortcut(QKeySequence("F11"))

        zToolTip = QApplication.translate("QSphere","Add a Line after the current line", None, QApplication.UnicodeUTF8)
        self.AddLineAfterWidgetContact = MyPushButton(self.groupBoxActions) 
        self.AddLineAfterWidgetContact.initPushButton(24, 24, 15, 70, "AddLineAfterWidgetContact", "", zToolTip, True, getThemeIcon("tab_addaftercurrentline.png"), 24, 24, True)
        self.AddLineAfterWidgetContact.setShortcut(QKeySequence("Ctrl++"))

        zToolTip = QApplication.translate("QSphere","Duplicate the current line", None, QApplication.UnicodeUTF8)
        self.CloneLineWidgetContact = MyPushButton(self.groupBoxActions) 
        self.CloneLineWidgetContact.initPushButton(24, 24, 15, 100, "CloneLineWidgetContact", "", zToolTip, True, getThemeIcon("tab_clonecurrentline.png"), 24, 24, True)
        self.CloneLineWidgetContact.setShortcut(QKeySequence("Ctrl+C"))

        zToolTip = QApplication.translate("QSphere","Delete the current line", None, QApplication.UnicodeUTF8)
        self.DelCurrentLineWidgetContact = MyPushButton(self.groupBoxActions) 
        self.DelCurrentLineWidgetContact.initPushButton(24, 24, 15, 150, "DelCurrentLineWidgetContact", "", zToolTip, True, getThemeIcon("tab_delcurrentline.png"), 24, 24, True)
        self.DelCurrentLineWidgetContact.setShortcut(QKeySequence("Ctrl+X"))

        zToolTip = QApplication.translate("QSphere","Delete the last line", None, QApplication.UnicodeUTF8)
        self.DelLastLineWidgetContact = MyPushButton(self.groupBoxActions) 
        self.DelLastLineWidgetContact.initPushButton(24, 24, 15, 180, "DelLastLineWidgetContact", "", zToolTip, True, getThemeIcon("tab_delline.png"), 24, 24, True)
        self.DelLastLineWidgetContact.setShortcut(QKeySequence("F12"))
        
        zToolTip = QApplication.translate("QSphere","Move the line up", None, QApplication.UnicodeUTF8)
        self.MoveLineWidgetUpContact = MyPushButton(self.groupBoxActions) 
        self.MoveLineWidgetUpContact.initPushButton(24, 24, 15, 220, "MoveLineWidgetUpContact", "", zToolTip, True, getThemeIcon("tab_linemoveup.png"), 24, 24, True)
        self.MoveLineWidgetUpContact.setShortcut(QKeySequence.MoveToPreviousPage)

        zToolTip = QApplication.translate("QSphere","Move the line down", None, QApplication.UnicodeUTF8)
        self.MoveLineWidgetDownContact = MyPushButton(self.groupBoxActions) 
        self.MoveLineWidgetDownContact.initPushButton(24, 24, 15, 250, "MoveLineWidgetDownContact", "", zToolTip, True, getThemeIcon("tab_linemovedown.png"), 24, 24, True)
        self.MoveLineWidgetDownContact.setShortcut(QKeySequence.MoveToNextPage)

        zToolTip = QApplication.translate("QSphere","Original size for the columns", None, QApplication.UnicodeUTF8)
        self.ResizeColumns = MyPushButton(self.groupBoxActions) 
        self.ResizeColumns.initPushButton(24, 24, 15, 300, "Size_6_tableroles", "", zToolTip, True, getThemeIcon("tab_sizecol.png"), 24, 24, True)
        self.ResizeColumns.setShortcut(QKeySequence("Ctrl+R"))

        self.groupBoxActionsMeta = QGroupBox(self)
        self.groupBoxActionsMeta.setStyleSheet(self.groupStyleSheet)

        zToolTip = QApplication.translate("QSphere","Move down", None, QApplication.UnicodeUTF8)
        self.MoveDown = MyPushButton(self.groupBoxActionsMeta) 
        self.MoveDown.initPushButton(24, 24, 10, 10, "MoveDown", "", zToolTip, True, getThemeIcon("movedown.png"), 24, 24, True)
        self.MoveDown.setAutoRepeat(True)
        self.MoveDown.setShortcut(QKeySequence.MoveToNextLine)

        self.labelPosition = QLabel(self.groupBoxActionsMeta)
        self.labelPosition.setGeometry(40, 10, 100, 25)
        self.labelPosition.setText("%s :" % (QApplication.translate("QSphere","Current contact", None, QApplication.UnicodeUTF8)))
        
        self.CurrentContact = QLabel(self.groupBoxActionsMeta)
        self.CurrentContact.setGeometry(140, 10, 40, 25)

        zToolTip = QApplication.translate("QSphere","Move up", None, QApplication.UnicodeUTF8)
        self.MoveUp = MyPushButton(self.groupBoxActionsMeta) 
        self.MoveUp.initPushButton(24, 24, 180, 10, "MoveUp", "", zToolTip, True, getThemeIcon("moveup.png"), 24, 24, True)
        self.MoveUp.setAutoRepeat(True)
        self.MoveUp.setShortcut(QKeySequence.MoveToPreviousLine)

        zIcon = getThemeIcon("actions.png")
        zToolTip = QApplication.translate("QSphere","Actions for current contact", None, QApplication.UnicodeUTF8)
        self.Actions = MyPushButton(self.groupBoxActionsMeta) 
        self.Actions.initPushButton(60, 24, 220, 10, "Actions", "", zToolTip, True, zIcon, 60, 24, True) 
        self.FixeMenu()

        zToolTip = QApplication.translate("QSphere","Add an item", None, QApplication.UnicodeUTF8)
        self.AddOneContact = MyPushButton(self.groupBoxActionsMeta)
        self.AddOneContact.initPushButton(60, 25, 290, 10, "Ajouter_6_tableroles", "", zToolTip, True, getThemeIcon("addresponsible.png"), 60, 25, True)

        zToolTip = QApplication.translate("QSphere","Add all contacts to the sheet", None, QApplication.UnicodeUTF8)
        self.AddAllContacts = MyPushButton(self.groupBoxActionsMeta) 
        self.AddAllContacts.initPushButton(60, 25, 360, 10, "AjouterAll_6_tableroles", "", zToolTip, True, getThemeIcon("sendtoresponsible.png"), 60, 25, True)

        self.barInfo = QgsMessageBar(self)
        self.barInfo.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )
               

        self.CloseButton = QPushButton(self)
        self.CloseButton.setObjectName("CloseButton")
        self.CloseButton.setText(QApplication.translate("QSphere", "Close", None, QApplication.UnicodeUTF8))

        self.ImportResponsibleInAnnuaire.setEnabled(self.notSoloMode)          
        self.AddOneContact.setEnabled(self.notSoloMode) 
        self.AddAllContacts.setEnabled(self.notSoloMode)

        self.Annuaire.currentIndexChanged.connect(self.IsEnableButton)
        self.ViewAnnuaire.clicked.connect(self.LoadViewer)
        self.LoadAnnuaire.clicked.connect(self.LoadXMLDictionnary)
        self.ReloadAnnuaire.clicked.connect(self.LoadXMLDictionnary)
        self.ImportResponsibleInAnnuaire.clicked.connect(self.LoadContactsFromSheet)
        self.ImportInAnnuaire.clicked.connect(self.ImportQSPContacts)
        self.AddAnnuaire.clicked.connect(self.LoadXMLDictionnary)
        self.NewAnnuaire.clicked.connect(self.InitDictionnary)
        self.HelpButton.clicked.connect(self.clickHelp)

        self.AddLineWidgetContact.clicked.connect(self.AddLine)
        self.AddLineAfterWidgetContact.clicked.connect(self.AddLine)
        self.CloneLineWidgetContact.clicked.connect(self.MoveLineDown)
        self.DelLastLineWidgetContact.clicked.connect(self.DelLastLine)
        self.DelCurrentLineWidgetContact.clicked.connect(self.DelCurrentLine)
        self.MoveLineWidgetUpContact.clicked.connect(self.MoveLineUp)
        self.MoveLineWidgetDownContact.clicked.connect(self.MoveLineDown)
        self.ResizeColumns.clicked.connect(self.callInitSizeCols)

        self.MoveUp.clicked.connect(self.MoveSelUp)
        self.MoveDown.clicked.connect(self.MoveSelDown)
        self.AddOneContact.clicked.connect(self.SendToParentWidget)
        self.AddAllContacts.clicked.connect(self.SendAllToParentWidget)
        self.SaveButton.clicked.connect(self.Save)
        self.contextMnuSaveActions()
        self.CloseButton.clicked.connect(self.close)
        
        self.InitTableWidget()
        self.FixeCurrentContact()
        self.IsEnableButton()

 
    def contextMnuSaveActions(self):
        contextMnu_SaveActions = QMenu()

        menuIcon = getThemeIcon("saveas.png")
        zText = QApplication.translate("QSphere","Save as ...", None, QApplication.UnicodeUTF8)
        self.SaveAsButton = QAction(QIcon(menuIcon), zText, self)
        self.SaveAsButton.setObjectName("SaveAsButton")
        self.SaveAsButton.setShortcut(QKeySequence("Ctrl+Shift+S"))
        contextMnu_SaveActions.addAction(self.SaveAsButton)
        self.SaveAsButton.triggered.connect(self.SaveAs)

        contextMnu_SaveActions.addSeparator()
        
        menuIcon = getThemeIcon("savecopy.png")
        zText = QApplication.translate("QSphere","Save as a copy ...", None, QApplication.UnicodeUTF8)
        self.SaveCopyAsButton = QAction(QIcon(menuIcon), zText, self)
        self.SaveCopyAsButton.setObjectName("SaveCopyAsButton")
        self.SaveCopyAsButton.setShortcut(QKeySequence("Ctrl+Shift+C"))
        contextMnu_SaveActions.addAction(self.SaveCopyAsButton)
        self.SaveCopyAsButton.triggered.connect(self.SaveAs)

        self.ActionsSaveButton.setMenu(contextMnu_SaveActions)

    def clickHelp(self): makeHelp(self)

    def resizeEvent(self,ev):
        zSize = ev.size()
        self.barInfo.setGeometry(QRect(0, 0, zSize.width(), 90)) 
        self.Annuaire.setGeometry(130, 10, zSize.width()-260, 25)
        self.ReloadAnnuaire.setGeometry(zSize.width()-120, 10, 24, 24)
        self.ViewAnnuaire.setGeometry(zSize.width()-90, 10, 24, 24)
        self.LoadAnnuaire.setGeometry(zSize.width()-60, 10, 24, 24)
        self.tableWidget.setGeometry(10, 90,  zSize.width()-80, zSize.height()-140)
        self.groupBoxActionsAnnuaire.setGeometry(10, 5, zSize.width()-20, 80)
        self.groupBoxActions.setGeometry(zSize.width()-60, 90, 50, zSize.height()-140)
        self.groupBoxActionsMeta.setGeometry(zSize.width()-630, zSize.height()-50, 460, 40)
        self.CloseButton.setGeometry(zSize.width()-165, zSize.height()-40, 100, 25)

        if self.parent : ResizeCols(self, self.tableWidget, self.dims, (zSize.width()-70)/float(self.originalW))

    def callInitSizeCols(self): initSizeCols(self, self.tableWidget, self.dims)

    def IsEnableButton(self): self.ViewAnnuaire.setEnabled(self.Annuaire.currentText()!= "")

    def FixeCurrentContact(self):
        self.CurrentContact.setText("%s / %s" % (self.tableWidget.currentRow()+1, self.tableWidget.rowCount()))
        self.groupBoxActionsMeta.setEnabled(False) if self.tableWidget.rowCount()== 0 else self.groupBoxActionsMeta.setEnabled(True)

    def ChangePatternZipPostalCode(self):
        if self.sender().accessibleName() == "" : return
        zNameObjRac = self.sender().accessibleName().split("_")[0]
        zRowCombo = int(self.sender().accessibleName().split("_")[2])
        zObj = getWidget(self, zNameObjRac)
        if zObj != None :
            zObjWidget = zObj.cellWidget(zRowCombo, 4)
            if zObjWidget==None: return
            zKeyTarget = self.sender().currentText()
            if DicoHasKey(self.listCountriesCode, zKeyTarget) :                
                zObjWidget.setInputMask("")
                zObjWidget.setInputMask(self.listCountriesCode[zKeyTarget][1])
                zObjWidget.regex = QRegExp(r"%s" % (self.listCountriesCode[zKeyTarget][0]), Qt.CaseSensitive)
            else :
                zObjWidget.setInputMask("")
                zObjWidget.setInputMask("XXXxxxxxxx;X")
                zObjWidget.regex = QRegExp(r"(^+[a-zA-Z_0-9\s]{3,10}$)", Qt.CaseSensitive)          

    def InitTableWidget(self):
        zDim = (100, 80, 80, 80, 60, 80, 80, 80, 80)
        for i in range(len(zDim)): self.tableWidget.setColumnWidth(i, zDim[i])
        zListHeaders = (QApplication.translate("QSphere","Role", None, QApplication.UnicodeUTF8), \
                        QApplication.translate("QSphere","Organization name", None, QApplication.UnicodeUTF8), \
                        QApplication.translate("QSphere","Address", None, QApplication.UnicodeUTF8), \
                        QApplication.translate("QSphere","Country", None, QApplication.UnicodeUTF8), \
                        QApplication.translate("QSphere","Zip code", None, QApplication.UnicodeUTF8), \
                        QApplication.translate("QSphere","City", None, QApplication.UnicodeUTF8), \
                        QApplication.translate("QSphere","E-mail", None, QApplication.UnicodeUTF8), \
                        QApplication.translate("QSphere", "Phone", None, QApplication.UnicodeUTF8), \
                        "URL")
        self.tableWidget.setHorizontalHeaderLabels(zListHeaders)              
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def AddLine(self):
          row = (self.tableWidget.currentRow()+1) if self.sender().objectName() == "AddLineAfterWidgetContact" else self.tableWidget.rowCount()
          
          self.tableWidget.insertRow(row)
          for i in range(len(self.ParamsLineWidget)): AddLineWidget(self, self.tableWidget, row, i, self.ParamsLineWidget[i][0], self.ParamsLineWidget[i][1], self.ParamsLineWidget[i][2])
          if self.sender().objectName() == "AddLineAfterWidgetContact" : self.RenameAllWidgets(self.tableWidget)
              
          self.tableWidget.selectRow(row)
          self.FixeCurrentContact()

    
    def Menu_Actions(self):
        self.context_menu_actions = QMenu()
        menuIcon = getThemeIcon("sendtometadata.png")
        
        zIndex = self.parent.tabWidget.currentIndex()
        zWidget = getWidget(self.parent, "tableroles")
        zText = QApplication.translate("QSphere", "Organization", None, QApplication.UnicodeUTF8)
        if zWidget :
            for i in range(zWidget.rowCount()):
                zAction = self.context_menu_actions.addAction(QIcon(menuIcon), "%s %s" % (zText, i))
                zAction.setObjectName("%s %s" % (zText, i))
                zAction.triggered.connect(self.SendToParentWidget)
        self.parent.tabWidget.setCurrentIndex(zIndex) 


    def LoadContactsFromSheet(self):
        zIndex = self.parent.tabWidget.currentIndex()
        iTableWidget = getWidget(self.parent, "tableroles")
        oTableWidget = self.tableWidget

        if oTableWidget :
            self.progressBar.setVisible(True)
            for iRow in range(iTableWidget.rowCount()):
                self.AddLine()
                self.progressBar.setValue(int(100 * iRow/iTableWidget.rowCount()))
                self.MakeCellsWidget(iTableWidget, oTableWidget, iRow, oTableWidget.rowCount()-1, True)
            self.progressBar.setValue(0)
            self.progressBar.setVisible(False)
        self.parent.tabWidget.setCurrentIndex(zIndex) 

    def SendAllToParentWidget(self):
        iTableWidget = self.tableWidget
        oTableWidget = getWidget(self.parent, "tableroles")
        if oTableWidget :
            self.parent.progressBar.setVisible(True)
            self.progressBar.setVisible(True)
            for iRow in range(iTableWidget.rowCount()):
                if iRow > oTableWidget.rowCount()-1 :
                    self.parent.AddLine()
                    oRow = oTableWidget.rowCount()-1
                else : oRow = iRow    
                self.parent.progressBar.setValue(int(100 * iRow/iTableWidget.rowCount()))
                self.progressBar.setValue(int(100 * iRow/iTableWidget.rowCount()))
                self.MakeCellsWidget(iTableWidget, oTableWidget, iRow, oRow, False)
            self.parent.passChangeMode()
            self.parent.progressBar.setValue(0)
            self.progressBar.setValue(0)            
            self.parent.progressBar.setVisible(False)
            self.progressBar.setVisible(False)

    def SendToParentWidget(self):
        iRow = self.tableWidget.currentRow()
        iTableWidget = self.tableWidget 
        oTableWidget = getWidget(self.parent, "tableroles")
        if oTableWidget :
             if self.sender().objectName() in ("Ajouter_6_tableroles", "AjouterAll_6_tableroles") :
                self.parent.AddLine()
                oRow = oTableWidget.rowCount()-1
             else :
                try : oRow = int(self.sender().objectName().split(" ")[1])
                except : oRow = 0
                
             self.MakeCellsWidget(iTableWidget, oTableWidget, iRow, oRow, False)
             self.parent.passChangeMode()

    def MakeCellsWidget(self, iTableWidget, oTableWidget, iRow, oRow, isEditable):
        for j in range(oTableWidget.columnCount()):
            iWidget = iTableWidget.cellWidget(iRow, j)
            oWidget = oTableWidget.cellWidget(oRow, j)
            if oWidget.metaObject().className() in ("QComboBox", "MyComboBox"):
               if j == 0 :
                  if oRow > 1 : oWidget.setCurrentIndex(iWidget.currentIndex())
                  else :
                     if isEditable : oWidget.setCurrentIndex(iWidget.currentIndex())
               else : oWidget.setCurrentIndex(iWidget.currentIndex())   
            else : oWidget.setText(iWidget.text())
        self.FixeMenu()             

    def FixeMenu(self):
        if self.notSoloMode :
           self.Menu_Actions()
           self.Actions.setMenu(self.context_menu_actions)

    def DelLastLine(self):
        if self.tableWidget.rowCount() > 0 :
           row = self.tableWidget.rowCount()-1
           self.tableWidget.removeRow(row)
           self.FixeCurrentContact()
           row-=1
           self.tableWidget.selectRow(row)
           try : self.tableWidget.cellWidget(row, 0).setFocus()
           except : pass
           self.tableWidget.selectRow(row)

    def DelCurrentLine(self):
        if self.tableWidget.currentRow() < 0 : return
        row =  self.tableWidget.currentRow()
        if self.tableWidget.rowCount()== row+1 : self.DelLastLine()
        else :
            self.tableWidget.removeRow(row)
            self.RenameAllWidgets(self.tableWidget)
            self.tableWidget.selectRow(row)
            try : self.tableWidget.cellWidget(row, 0).setFocus()
            except : pass
            self.tableWidget.selectRow(row)
            self.FixeCurrentContact()
            

    def DelAllLines(self):
        self.progressBar.setVisible(True)
        self.tableWidget.setUpdatesEnabled(False)
        zRows = self.tableWidget.rowCount()
        for i in range(zRows, 0, -1):    
            self.progressBar.setValue(int(100 * i/zRows))
            self.tableWidget.removeRow(self.tableWidget.rowCount()-1)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)
        self.tableWidget.setUpdatesEnabled(True)
        self.FixeCurrentContact()

    def RenameAllWidgets(self, zObj):
        zWidgetName = {0:"MyComboBox", 1:"MySimpleWidgetLineEditST", 2:"MySimpleWidgetLineEditST", 3:"MyComboBox", 4: "MyWidgetLineEdit", 5: "MySimpleWidgetLineEditST", 6: "MyWidgetLineEdit", 7:"MySimpleWidgetLineEditST", 8:"MyWidgetLineEdit", 9: "MyPushButton"}
        for i in range(zObj.rowCount()):
            for j in range(zObj.columnCount()):
                ObjWidget = zObj.cellWidget(i, j)
                zFullNameWidget = "%s_%s_%s" % (zObj.accessibleName(), zWidgetName[j] ,i)
                ObjWidget.setObjectName(zFullNameWidget) 
                ObjWidget.setAccessibleName(zFullNameWidget)


    def MoveSelUp(self):
        if self.tableWidget.rowCount()== 0 : return
        if self.tableWidget.currentRow() > 0 : self.tableWidget.selectRow(self.tableWidget.currentRow()-1)

    def MoveSelDown(self):
        if self.tableWidget.rowCount()== 0 : return
        if self.tableWidget.currentRow() <  (self.tableWidget.rowCount()-1) : self.tableWidget.selectRow(self.tableWidget.currentRow()+1)
        
    def MoveLineUp(self):
        row = self.tableWidget.currentRow()
        if row > 0:
            self.tableWidget.insertRow(row-1)
            for i in range(self.tableWidget.columnCount()):
               OriginalWidget = (self.tableWidget.cellWidget(row+1,i))
               NewObjWidget = AddLineWidget(self, self.tableWidget, row-1,  i, self.ParamsLineWidget[i][0], self.ParamsLineWidget[i][1], self.ParamsLineWidget[i][2])
               if OriginalWidget.metaObject().className() in ("MyWidgetLineEdit", "MySimpleWidgetLineEditST") : NewObjWidget.setText(OriginalWidget.text()) 
               elif OriginalWidget.metaObject().className() == "MyComboBox" :
                   if i in (0,3) :
                      NewObjWidget.clear()
                      zItems = GetAllItems(OriginalWidget)
                      NewObjWidget.addItems(zItems)
                   NewObjWidget.setCurrentIndex(OriginalWidget.currentIndex())
            self.tableWidget.selectRow(row-1)

            self.tableWidget.removeRow(row+1)
            self.RenameAllWidgets(self.tableWidget)
            self.FixeCurrentContact()
               
    def MoveLineDown(self):
        row = self.tableWidget.currentRow()
        zBorne = self.tableWidget.rowCount()-1 if self.sender().objectName() == "MoveLineWidgetDownContact" else self.tableWidget.rowCount()
        if row < 0 and self.sender().objectName() == "CloneLineWidgetContact" : return
        if row < zBorne :
            rowcible = (row+2) if self.sender().objectName() == "MoveLineWidgetDownContact" else (row+1)
            self.tableWidget.insertRow(rowcible)
            for i in range(self.tableWidget.columnCount()):
               OriginalWidget = (self.tableWidget.cellWidget(row,i))
               NewObjWidget = AddLineWidget(self, self.tableWidget, rowcible,  i, self.ParamsLineWidget[i][0], self.ParamsLineWidget[i][1], self.ParamsLineWidget[i][2])
               if OriginalWidget.metaObject().className() in ("MyWidgetLineEdit", "MySimpleWidgetLineEditST") : NewObjWidget.setText(OriginalWidget.text()) 
               elif OriginalWidget.metaObject().className() == "MyComboBox" :
                   if i in (0,3) :
                      NewObjWidget.clear()
                      zItems = GetAllItems(OriginalWidget)
                      NewObjWidget.addItems(zItems)
                   NewObjWidget.setCurrentIndex(OriginalWidget.currentIndex())
                   
            if self.sender().objectName() == "MoveLineWidgetDownContact" :
               self.tableWidget.selectRow(rowcible)
               self.tableWidget.removeRow(row)
            self.RenameAllWidgets(self.tableWidget)
            self.FixeCurrentContact()
        
    def close(self): self.reject()

    def InitDictionnary(self):
        self.FixeInfos("")
        self.DelAllLines()

    def LoadViewer(self):
        if self.Annuaire.currentText()!= "" :
            from doUI import DialogViewer
            self.dnavigator = DialogViewer(self.iface, "filexml:%s" % (self.Annuaire.currentText()), False, [], self.langueTR, self, None, True)
            self.dnavigator.exec_()

    def ImportQSPContacts(self):
            zTitle = self.sender().toolTip()
            InitDir = os.path.dirname(__file__) if self.initDir == "" else self.initDir
            MyFileDialog = QFileDialog(self, zTitle)
            MyFileDialog.setNameFilters((self.filtreQSP, ))
            MyFileDialog.setViewMode(QFileDialog.Detail)
            MyFileDialog.setDirectory(InitDir)
            MyFileDialog.setFileMode(QFileDialog.ExistingFile) 
            MyFileDialog.setAcceptMode(QFileDialog.AcceptOpen)

            FixeLabelsFileDialog(self, MyFileDialog, 0, True)
            
            if MyFileDialog.exec_():
                fileName = "%s" % (MyFileDialog.selectedFiles()[0])
                if fileName!="" :
                   config = ConfigParser.ConfigParser()
                   config.read(fileName)
                   zSections = config.sections()
                   zSection = "tableroles"
                   zRows = int(config.get("tableroles","zRows"))
                   zCols = int(config.get("tableroles","zCols"))
                   
                   self.progressBar.setVisible(True)
                   
                   for j in range(zRows):
                        self.progressBar.setValue(int(100 * j/zRows))
                        self.AddLine()
                        counter = self.tableWidget.rowCount()-1
                        
                        zInfos = config.get(zSection,'zRow_%s' % (j))
                        zClassWidgetValues = zInfos.split("|")
                        
                        for k in range(zCols) :
                            zInfos = config.get(zSection,'zWidget_%s' % (k))
                            zClassWidgetInfos = zInfos.rstrip().split("|")
                            zClassWidgetInfo = "%s" % (zClassWidgetInfos[0])
                            if zClassWidgetInfo == "standard" :
                                zItem[k] = QTableWidgetItem()
                                zItem[k].setText("%s" % (zClassWidgetValues[k]))
                                zObj.setItem(counter,k, zItem[k])
                            else :
                                if is_number_int(zClassWidgetValues[k]) and zClassWidgetInfos[0] not in("QLineEdit","MySimpleWidgetLineEdit", "MyWidgetLineEdit") : zValue = int(zClassWidgetValues[k])
                                elif is_number_float(zClassWidgetValues[k]) and zClassWidgetInfos[0] not in("QLineEdit", "MySimpleWidgetLineEdit", "MyWidgetLineEdit") : zValue = float(zClassWidgetValues[k])
                                else : zValue = "%s" % (zClassWidgetValues[k])

                                if int(zClassWidgetInfos[2])!= -1 : AddLineWidget(self, self.tableWidget, counter,  k, self.ParamsLineWidget[k][0], self.ParamsLineWidget[k][1], zValue)                                      
                                else : AddLineWidget(self, self.tableWidget, counter,  k, self.Paramsself.AnnuaireLineWidget[k][0], self.ParamsLineWidget[k][1], ("%s" % (zClassWidgetValues[k-1]), zValue))

                        try : self.tableWidget.cellWidget(counter, 0).setFocus()
                        except : pass

                   self.progressBar.setVisible(False)
                   self.progressBar.setValue(0)
                   self.RenameAllWidgets(self.tableWidget)
                   self.FixeCurrentContact()
                   self.FixeInfos(fileName)

    def BadMyISO(self):
        zMsg = QApplication.translate("QSphere","Invalid XML document !", None, QApplication.UnicodeUTF8)
        SendMessage(self, "information" , zMsg, QgsMessageBar.WARNING, self.duration_warning) 
       
    def LoadXMLDictionnary(self):
        if self.sender().objectName() == "ReloadAnnuaire" :
            fileName = self.Annuaire.currentText()
            if fileName == "" : return
            self.DelAllLines()
            self.LoadDataXMLDictionnary(fileName)
        else :

            zTitle = self.sender().toolTip()
            InitDir = os.path.dirname(__file__) if self.initDir == "" else self.initDir
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
                   self.FixeInfos(fileName)
                   self.LoadDataXMLDictionnary(fileName)


    def LoadDataXMLDictionnary(self, fileName):
       from xmlISOparser import *
       self.listImportCategories = []
       myISO = xmlISOparser(fileName, None, 'MEDDE', self.langueTR)

       if myISO == None :
          self.BadMyISO()
          return 

       zCond = True 
       try : myISO.getTagDictionnary()
       except : zCond = False
       if not zCond : 
          self.BadMyISO()
          return            

       try : myISO.createISOdataStructure(False)
       except :
             zMsg =  QApplication.translate("QSphere","No contacts could be extract from the XML file !", None, QApplication.UnicodeUTF8)
             SendMessage(self, "Information" , "%s :\n%s" % (zMsg, fileName), QgsMessageBar.INFO, self.duration_info)              
             return
       
       if self.sender().objectName() == "LoadAnnuaire" : self.DelAllLines()
       DicoContacts = {"pointsofcontact" : myISO.pointsofcontact, "pointsofcontactCust" : myISO.pointsofcontactCust}

       for key in DicoContacts :
           if key in dir(myISO) : self.UpdateTableRoles("tablecontacts", DicoContacts[key])
           else :
               zMsg =  QApplication.translate("QSphere","No contacts could be extract from the XML file !", None, QApplication.UnicodeUTF8)
               SendMessage(self, "Information" , "%s :\n%s, (key : %s)" % (zMsg, fileName, key), QgsMessageBar.INFO, self.duration_info)                    

           
    def Save(self):
        fileName = self.Annuaire.currentText()
        if fileName != "" : self.MakeSave(fileName)
        else : self.SaveAs()


    def MakeSave(self, fileName):
        if self.tableWidget.rowCount()> 0 :
            ExportDictionnaryToXML(self, fileName)
            zMsg =  QApplication.translate("QSphere","The dictionnary was saved as", None, QApplication.UnicodeUTF8)
            SendMessage(self, "Information" , "%s :\n%s" % (zMsg, fileName), QgsMessageBar.INFO, self.duration_info)
           
    def SaveAs(self):
        if self.tableWidget.rowCount() == 0 : return
        
        InitDir = os.path.dirname(__file__) if self.initDir == "" else self.initDir

        zElt0 = QApplication.translate("QSphere","files", None, QApplication.UnicodeUTF8).title()
        self.Listfiltres = ("%s eXtensible Markup Language (*.xml)" % (zElt0),)
        self.NamedFiltres = {"xml" : "%s eXtensible Markup Language (*.xml)" % (zElt0)}

        if self.sender() == self.SaveAsButton : zTitle = QApplication.translate("QSphere", "Save as an XML Dictionnary", None, QApplication.UnicodeUTF8)
        else : zTitle = QApplication.translate("QSphere","Save as a copy ...", None, QApplication.UnicodeUTF8)

        if self.windowTitle()!= self.racWindowTitle:
            fileName = self.windowTitle().replace(self.racWindowTitle, "")
            self.InitName = os.path.basename(fileName).split(".")[0]
            extension = GetExtension(fileName)
            extension = extension.replace(".","")
        
        MyFileDialog = QFileDialog(self, zTitle)
        MyFileDialog.setNameFilters(self.Listfiltres)
        MyFileDialog.selectNameFilter(self.NamedFiltres["xml"])
        MyFileDialog.setViewMode(QFileDialog.Detail)
        MyFileDialog.setDirectory(self.InitDir)
        MyFileDialog.setAcceptMode(QFileDialog.AcceptSave)
        MyFileDialog.selectFile(self.InitName)

        FixeLabelsFileDialog(self, MyFileDialog, 1, True)
        
        if MyFileDialog.exec_():
            fichier = FileNameWithExtension(self, MyFileDialog.selectedFiles()[0], MyFileDialog.selectedNameFilter())
            self.MakeSave(fichier)
            if self.sender()!= self.SaveCopyAsButton :
                self.fichier = fichier
                self.setWindowTitle("%s : %s" % (self.racWindowTitle, self.fichier))
                self.InitDir = os.path.dirname(self.fichier)
                if self.Annuaire.findText(self.fichier)==-1 : self.Annuaire.addItem("%s" % (self.fichier))
                self.Annuaire.setCurrentIndex(self.Annuaire.findText(self.fichier))


    def FixeInfos(self, fileName):
        if self.sender().objectName() in ("LoadAnnuaire", "SaveButtonAs", "SaveButton") :
            self.setWindowTitle("%s : %s" % (self.racWindowTitle, os.path.basename(fileName)))
            if self.Annuaire.findText(fileName)==-1 : self.Annuaire.addItem("%s" % (fileName))
            self.Annuaire.setCurrentIndex(self.Annuaire.findText(fileName))
        if self.sender().objectName() == "NewAnnuaire" :
            self.setWindowTitle("%s : %s" % (self.racWindowTitle, ""))
            self.Annuaire.setCurrentIndex(0)
        if fileName!= "" : self.initDir = os.path.dirname(fileName)

        
    def UpdateTableRoles(self, zkeyWidget, zIsoXML):
         zDim = len(zIsoXML)
         zkeyWidget = zkeyWidget.split(":")[0]
         zObj = getWidget(self, zkeyWidget)
         if not zObj or zDim == 0 : return

         zkeys = {'ville': 5, 'name': 1, 'pays': 3, 'adresse': 2, 'codepostal': 4, 'mail': 6, 'role': 0, 'phone' : 7, 'url' : 8}
         zinvkeys = {0: 'role', 1: 'name', 2: 'adresse', 3: 'pays', 4 : 'codepostal', 5: 'ville', 6: 'mail', 7: 'phone', 8 : 'url'}
         
         self.progressBar.setVisible(True)

         
         for i in range(zDim):
             self.progressBar.setValue(int(100 * i/zDim))
             if type(zIsoXML[i])== dict :
                 if zIsoXML[i]['role'] == None : break
                 else : 
                      self.AddLine() 
                      zLine = zObj.rowCount()-1
                 for key in zIsoXML[i] :
                     ikey = zkeys[key]
                     if zObj.cellWidget(zLine, ikey).metaObject().className() in "MyComboBox" :
                         if key == "role":
                             zIndexes = [keyitem for keyitem, value in self.DicoListOfRules.items() if value == zIsoXML[i][key]] 
                             if zIndexes!=[] : zIndex = zIndexes[0]  
                         else : zIndex = zObj.cellWidget(zLine, ikey).findText(zIsoXML[i][key].capitalize())
                         if zIndex == -1 : zIndex = 0
                         zObj.cellWidget(zLine, ikey).setCurrentIndex(zIndex) 
                     else : zObj.cellWidget(zLine, ikey).setText("%s" % (zIsoXML[i][key]))
                     ikey+= 1
                     
             elif type(zIsoXML[i])== list :

                 for k in range(len(zIsoXML[0])):
                    if zIsoXML[0] == [] : break
                    if zIsoXML[0][0] == None: break
                    else :
                       self.AddLine() 
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

         self.progressBar.setVisible(False)
         self.progressBar.setValue(0)
         self.FixeCurrentContact()

