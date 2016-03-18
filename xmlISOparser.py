
from xml.etree import ElementTree as ET
import urllib,os,sys
from qsphere_tools import appendNameSpace

class xmlISOparser:
	def __init__(self, filenameIP, dataXML, isoFormat, langue):				
		self.inputXMLfile = filenameIP
		self.dataXML = dataXML
		self.isoFormatToExtract = isoFormat
		self.langueTR = langue

        def getTagDictionnary(self):
                if self.dataXML == None and self.inputXMLfile == None : return False
                else : self.root = self.getIsoXML(self.inputXMLfile, self.dataXML)
		if self.root is None : return False
		
		self.importISOxmlDefinition(self.isoFormatToExtract)
                self.dictionnary = self.getElementVal(self.isoModel.dictionnary())
              
                return (self.dictionnary==[[]])

		
	def createISOdataStructure(self, isMetaData):
		if isMetaData :
                        try : self.UUID = self.getElementVal(self.isoModel.identificator())
                        except : self.UUID = [[]]
                        
                        try : self.title = self.getElementVal(self.isoModel.intitule())
                        except : self.title = [[]]
                        
                        try : self.abstract = self.getElementVal(self.isoModel.resume())
                        except : self.abstract = [[]]
                        
                        try : self.typedata = self.getElementVal(self.isoModel.typedata())
                        except : self.typedata = [[]]
                        
                        try : self.localisators = self.getElementVal(self.isoModel.tablelocalisator())
                        except : self.localisators = [[]]
                        
                        try : self.tablecarac = self.getElementVal(self.isoModel.tablecarac())
                        except : self.tablecarac = [[]]
                        
                        try : self.rs_identifier = self.getElementVal(self.isoModel.rs_identifier())
                        except : self.rs_identifier = [[]]
                        
                        try : self.languesjdd = self.getElementVal(self.isoModel.tablelangues())
                        except : self.languesjdd = [[]]
                        
                        try : self.categories = self.getElementVal(self.isoModel.tablecategories())
                        except : self.categories = [[]]

                        #TOTO 2.8.0
                        try : self.codecategories = self.getElementVal(self.isoModel.ax_tablecategories())
                        except : self.codecategories = [[]]
                        
                        try : self.keywordsF = self.getElementVal(self.isoModel.tablemotsclefsf())
                        except : self.keywordsF = [[]]
                        
                        try : self.keywordsFNC = self.getElementVal(self.isoModel.ax_tablemotsclefsf())
                        except : self.keywordsFNC = [[]]
                        
                        try : self.timeperiodes = self.getElementVal(self.isoModel.tableetenduetemporelle())
                        except : self.timeperiodes = [[]]
                   
                        try : self.dates = self.getElementVal(self.isoModel.dates())
                        except : self.dates = [[]]
                        
                        try : self.formatsjdd = self.getElementVal(self.isoModel.tableformats())
                        except : self.formatsjdd = [[]]
                        
                        try : self.boundingboxcoordinates = self.getElementVal(self.isoModel.tableemprises())
                        except : self.boundingboxcoordinates = [[]]
                        
                        try : self.scr = self.getElementVal(self.isoModel.tablescr())
                        except : self.scr = [[]]
                        
                        try : self.genealogie = self.getElementVal(self.isoModel.genealogie())
                        except : self.genealogie = [[]]
                        
                        try : self.coherence = self.getElementVal(self.isoModel.coherence())
                        except : self.coherence = [[]]
                        
                        try : self.scalesEC = self.getElementVal(self.isoModel.grouperesolutionscale())
                        except : self.scalesEC = [[]]
                        
                        try : self.scalesUM = self.getElementVal(self.isoModel.ax_grouperesolutionscale())
                        except : self.scalesUM = [[]]
                        
                        try : self.UnitsScalesUM = self.getElementVal(self.isoModel.UnitsScalesUM())
                        except : self.UnitsScalesUM = [[]]
                        
                        try : self.conformities = self.getElementVal(self.isoModel.tablespecifications())
                        except : self.conformities = [[]]
                        
                        try : self.legalconstraints = self.getElementVal(self.isoModel.licence())
                        except : self.legalconstraints = [[]]
                        
                        try : self.accessconstraints = self.getElementVal(self.isoModel.groupedroits())
                        except : self.accessconstraints = [[]]
                        
                        try : self.otherconstraints = self.getElementVal(self.isoModel.otherconstraints())
                        except : self.otherconstraints = [[]]
                        
                        try : self.authors = self.getElementVal(self.isoModel.authors())
                        except : self.authors = [[]]

                        try : self.pointsofcontact = self.getElementVal(self.isoModel.tableroles())
                        except : self.pointsofcontact = [[]]
                        
                        try : self.pointsofcontactMDD = self.getElementVal(self.isoModel.bx_tableroles())
                        except : self.pointsofcontactMDD = [[]]
                        
                        try : self.pointsofcontactCust  = self.getElementVal(self.isoModel.ax_tableroles())
                        except : self.pointsofcontactCust = [[]]
                        
                        try : self.languemdd = self.getElementVal(self.isoModel.langmetada())
                        except : self.languemdd = [[]]
                        
                        try : self.datetmdd = self.getElementVal(self.isoModel.ax_datemetada())
                        except : self.datetmdd = [[]]
                        
                        try : self.datemdd = self.getElementVal(self.isoModel.datemetada())
                        except : self.datemdd = [[]]
                else :
                        self.pointsofcontact = self.getElementVal(self.isoModel.tableroles())
                        self.pointsofcontactCust = self.getElementVal(self.isoModel.ax_tableroles())
		return True

	def boundingDateRange(self,boundingDatesList):
		allDates, returnDates = [], {}
		for outer in boundingDatesList:
			for inner in outer.keys():
				if outer[inner] is not None:
					if outer[inner] != 'None': allDates.append(outer[inner])
                if allDates != []:
                    returnDates['start'] = min(allDates)
                    returnDates['end'] = max(allDates)
		return returnDates


	def importISOxmlDefinition(self,format):
		if format == 'MEDDE':
		   from xmlISOreaderTag import xmlISOreaderTag as isoModel
		self.isoModel = isoModel()
			
	def getElementVal(self,keyMethod):
		returnValList, returnVal, dataStruct, counter =[], 'None', {}, 0
		valueList, ordering, zTempoData = [], False, ""
                
		for i in keyMethod:
                        if type(i) is dict:
                           for j in i.keys():
                               dataStruct[counter]=j
                               if j=='order': ordering = True
                        if type(i) is str:
                                dataStruct[counter] = i
                                if i=='order': ordering = True
                        counter = counter + 1
		

		for i in dataStruct.keys()[1:]:
			thisData = keyMethod[i][dataStruct[i]]
                        if 'basilexpath' in thisData.keys():
                                returnVal =  self.returnBaliseElt(thisData['basilexpath'])
                                valueList.append(returnVal)                                

                        if 'basilexpathvalue' in thisData.keys():
                                returnVal =  self.returnBaliseEltValue(thisData['basilexpathvalue'])
                                valueList.append(returnVal)
			
			if 'baseXpath' in thisData.keys():
                                returnVal = self.returnDependantElementVal(thisData['baseXpath'],thisData['elValXpath'],thisData['depValXpath'],thisData['depVal'])
                                valueList.append(returnVal)
								
			if 'xpath' in thisData.keys():
                                returnVal =  self.returnSimpleElementVal(thisData['xpath'])
                                zTempoData = thisData['xpath']
                                if returnVal == [] and zTempoData == "gmd:contact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode" :
                                        if 'baseXpath' in thisData.keys():
                                                returnVal = self.returnDependantElementVal(thisData['baseXpath'],thisData['elValXpath'],thisData['depValXpath'],thisData['depVal'])
                                                valueList.append(returnVal)
				else : valueList.append(returnVal)
                
                        if ordering : orderingList = thisData
                        else: pass

                if [] in valueList : return valueList

		if ordering:
			checkCompLnth = len(valueList[0])
			index=0

			for list in valueList:
				if len(list) != checkCompLnth:
                                        if len(list)> checkCompLnth:
                                           zElt = ""
                                           for elt in list : zElt+= " %s" % (elt)
                                           list=[]
                                           list.append(zElt)
                                           valueList[index] = list
                                        else :
                                           while len(list)< checkCompLnth:
                                                 list.append('')          
                                           valueList[index]=list      
       
                                if zTempoData.startswith('gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo') or zTempoData.startswith('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact'):
                                   pos=0
                                   for item in list :
                                       if item==None :
                                          if index==0 : valueList[index][pos] = "pointOfContact"
                                          elif index==3 and self.langueTR=="fr": valueList[index][pos] = "France"
                                          else : valueList[index][pos] = ""
                                       pos+= 1   
                                index+=1

                        
			outer = []

                              
			for localPos in range(0,checkCompLnth):
				inner=[]
				for listPos in range(0,len(valueList)):
                                    try :
                                         inner.append(valueList[listPos][localPos]) if valueList[listPos][localPos]!=None else inner.append(" ")
                                    except :
                                         inner.append(" ") 
				outer.append(inner)
		
			for returnedList in outer:
				orderedValsSub = {}
				if len(returnedList) != len(orderingList): returnValList.append('None')
				else:		
          		            for i in orderingList.keys(): orderedValsSub[i] = returnedList[orderingList[i]-1] 
   				    returnValList.append(orderedValsSub)
			return returnValList
			
		else:
			return valueList
			
			

	def returnDependantElementVal(self,baseXpath,elXpath,depXpath,depValReqd):
		baseXpath = appendNameSpace(self, baseXpath)
		resDependantVal = []
		try: rootEl = self.root.findall(baseXpath)
		except: return 'None'

		for el in rootEl:
			thisElXpth = appendNameSpace(self, elXpath)
			thisEl = self.doFindall(el,thisElXpth)
		        if thisEl != 'None':
				elVal = thisEl[0].text 
                		thisEldepXpth = appendNameSpace(self, depXpath)					
				thisDepEl = self.doFindall(el,thisEldepXpth)								
				if thisDepEl != 'None':
        				depVal = thisDepEl[0].text
			                resDependantVal.append(elVal)
		return resDependantVal

	def returnBaliseElt(self,xpath):
		xpathNS = appendNameSpace(self, xpath)
		resElementVal = []
		try: rootEl = self.root.findall(xpathNS)
		except: return ['None']
		for elVal in rootEl:
		    if elVal is None: resElementVal.append('None')
		    else:
                       if elVal.attrib == {}:
                          for childItem in elVal :
                              if childItem.tag.find("Boolean")!=-1 : resElementVal.append(childItem.text)
                       else : resElementVal.append(elVal.attrib)
                return resElementVal        

	def returnBaliseEltValue(self,xpath):
		xpathNS = appendNameSpace(self, xpath)
		resElementVal = []
		try: rootEl = self.root.findall(xpathNS)
		except: return ['None']
		for elVal in rootEl:
		    if elVal is None: resElementVal.append('None')
		    else:
                       if elVal.attrib == {}:
                          for childItem in elVal :
                              if childItem.tag.find("Boolean")!=-1 : resElementVal.append(childItem.text)
                       else : resElementVal.append(elVal.attrib['codeListValue'])
                return resElementVal
                       
		
	def returnSimpleElementVal(self, xpath):
		xpathNS = appendNameSpace(self, xpath)
		resElementVal = []
		try: rootEl = self.root.findall(xpathNS)
		except: return ['None']
		for elVal in rootEl:
			if elVal is None: resElementVal.append('None')
			else: resElementVal.append(elVal.text)
		return resElementVal

	def doFindall(self,el,thisElXpth):
		try:
			thisElXpthEl = el.findall(thisElXpth)
			if len(thisElXpthEl) == 0: thisElXpthEl = 'None'
		except: thisElXpthEl = 'None'
		return thisElXpthEl

	def getXmlVal(self,paths):
		xmlVals = []
		for path in paths:
			try: xmlVals.append(self.root.find(path).text)			
			except:	xmlVals.append('null')
		return xmlVals					
		
	def defaultIsoNamespace(self):  return 'gmd'
	
	def getIsoXML(self, file, dataXML):
		etree = ET.parse(file) if file!= None else ET.parse(dataXML)
		root = etree.getroot()
		if root.tag != '{http://www.isotc211.org/2005/gmd}MD_Metadata':	return None
		return root
