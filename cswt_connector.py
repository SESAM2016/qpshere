#implement futur migration to Python 3
"""
try:
    from StringIO import StringIO as BytesIO  # Python 2
except ImportError:
    from io import BytesIO  # Python 3
"""

from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.gui import *

from qsphere_tools import *
from cswt_templates import *
import datetime, time

class cswtConnection(object):
    def __init__(self, parent, name, urlserver, urlauthserver): 
        self.parent = parent
        self._name = name
        self._service = "CSW"
        self._version = "2.0.2"
        self._server = urlserver

        self._versiongeonetwork = 2100 if urlauthserver.endswith("j_spring_security_check") else 3000
        self._headers = {'Content-Type': 'application/xml'}
        self._session = None
        
        self._authserver = urlauthserver
        self._user = None
        self._password = None
        self._connected = False
        self._reporting = ""
        self._allreporting = ""
        self.filtersCSW = ["EqualTo", "Like", "LessThan", "GreaterThan", "LessThanEqualTo", "LessThanOrEqualTo", "GreaterThanEqualTo", \
                           "GreaterThanOrEqualTo", "NotEqualTo", "Between", "NullCheck"]
        self.dict_CSWT = {0:GET_CAPABILITIES_TEMPLATE, 1:INSERT_METADATA_TEMPLATE, 2:UPDATE_METADATA_TEMPLATE, -1:DELETE_METADATA_TEMPLATE , 6:GET_RECORDS, 8:GET_RECORD_BYID, 9:AUTHENTICATION_TEMPLATE}


        self._valid_xpaths = [appendNameSpace(self,'ows:ExceptionReport'),
                              appendNameSpace(self,'csw:Capabilities'),
                              appendNameSpace(self,'csw:DescribeRecordResponse'),
                              appendNameSpace(self,'csw:GetDomainResponse'),
                              appendNameSpace(self,'csw:GetRecordsResponse'),
                              appendNameSpace(self,'csw:GetRecordByIdResponse'),
                              appendNameSpace(self,'csw:HarvestResponse'),
                              appendNameSpace(self,'csw:TransactionResponse')
                             ]

        try : self.duration_info = self.parent.SliderINFO.value()
        except : self.duration_info = self.parent.duration_info
        finally : self.duration_info = 2

        try : self.duration_timeout = self.parent.SliderTIMEOUT.value()
        except : self.duration_timeout = self.parent.duration_timeout
        finally : self.duration_timeout = 5


    def defaultIsoNamespace(self):  return 'csw'
    def name(self): return self._name
    def service(self): return self._service
    def version(self): return self._version
    def server(self): return self._server
    def authserver(self): return self._authserver

    def user(self): return self._user 
    def password(self): return self._password
    
    def headers(self): return self._headers 
    def reporting(self): return self._reporting
    def allreporting(self): return self._allreporting
    def connected(self): return self._connected

    def closeSession(self):
        if self._connected :
            zreturn_status_code = 200
            if self._session != None :
                response_close = self._session.post(url=self._authserver.replace("j_spring_security_check","j_spring_security_logout"), headers={'Connection': 'close'})
                zreturn_status_code = response_close.status_code
                
            if zreturn_status_code == 200 : 
                self._session = None
                self._user = None
                self._password = None           
                self._connected = False

        
    def initSession(self, user, password, initReporting) :
        import requests
        import base64
       
        self._allreporting = ""
        self._allreporting+= "CSW init session : %s\n" % (datetime.datetime.now().replace(microsecond=0).strftime("%d/%m/%Y %Hh:%Mm:%Ss"))
        self._user = user
        self._password = password
         
        if self._versiongeonetwork == 2100 :
           self._session = requests.Session()
           params = {'username': '%s' % self._user, 'password': '%s' % self._password}
           try : response_server_initsession = self._session.post(self._authserver, data=params)
           except requests.exceptions.ConnectionError as e:
                zMsg = QApplication.translate("QSphere","Unable to establish connection to", None, QApplication.UnicodeUTF8)
                msg = "%s %s" % (zMsg, self._authserver)
                self._allreporting+= msg
                return None
               
        else :
           self._session = None
           params = base64.b64encode(user + "%s:%s" % (self._user, self._password))
           dataxml = AUTHENTICATION_TEMPLATE % (self._user, self._password)
           self._headers = {'Content-Type': 'application/xml','Accept': 'application/xml','Authorization': 'Basic %s' % (params)}
           try : response_server_initsession = requests.post(self._authserver, dataxml, self._headers)
           except requests.exceptions.ConnectionError as e:
                zMsg1 = QApplication.translate("QSphere","Unable to establish connection to", None, QApplication.UnicodeUTF8)
                zMsg2 = QApplication.translate("QSphere","HTTP error", None, QApplication.UnicodeUTF8)
                msg = "%s %s\n%s : %s" % (zMsg1, self._authserver, zMsg2, e)
                self._allreporting+= msg
                return None
            
        self._connected = True if response_server_initsession.status_code == 200 else False
        self._allreporting+= "%s : %s\n" % (self._authserver, QApplication.translate("QSphere","Successfull !", None, QApplication.UnicodeUTF8) if response_server_initsession.status_code== 200 else QApplication.translate("QSphere","Error", None, QApplication.UnicodeUTF8))

        if self._connected == False : response_server_initsession = None
        return response_server_initsession 


    def notAuthentified(self):
        #ADD TEST FOR ows:ExceptionReport !
        xml = """<?xml version="1.0" encoding="UTF-8"?>
                    <ows:ExceptionReport xmlns:ows="http://www.opengis.net/ows" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0.0" xsi:schemaLocation=  "http://www.opengis.net/ows http://schemas.opengis.net/ows/1.0.0/owsExceptionReport.xsd">
                      <ows:Exception exceptionCode="NoApplicableCode">
                        <ows:ExceptionText>Cannot process transaction: User not authenticated.</ows:ExceptionText>
                      </ows:Exception>
                    </ows:ExceptionReport>"""


    def getCapabilities(self) :
        import requests
        paramsXML = None 
        dataXML = self.dict_CSWT[0] % paramsXML if paramsXML != None else self.dict_CSWT[0]
        headers = {'Content-Type': 'application/xml'}
        self._session = requests.Session()
        response_getCapabilities = self._session.post(self._server.replace("csw-publication","csw"), data=dataXML, headers=headers)
        self._reporting = "%s\n%s\n" % (response_getCapabilities.status_code, response_getCapabilities.text)
        self._session = None
        return response_getCapabilities

    
    def metadata_csw_publication(self, ucase, paramsXML, initReporting) :
        if self._session == None and self._versiongeonetwork == 2100 : return self.notAuthentified()
        self._reporting = ""
        libUcase = {1:"ADD RECORD",2:"UPDATE RECORD",-1:"DELETE RECORD", 6:"GET RECORDS"}
        self._reporting+= "CSW Action %s : %s\n\n" % (libUcase[ucase], datetime.datetime.now().replace(microsecond=0).strftime("%d/%m/%Y %Hh:%Mm:%Ss"))
        dataXML = self.dict_CSWT[ucase] % paramsXML if paramsXML != None else self.dict_CSWT[ucase]

        import requests
        if self._versiongeonetwork == 2100 :
            try : response_csw_publication = self._session.post(self._server, data=dataXML, headers=self._headers)
            except requests.exceptions.ConnectionError as e:
                zMsg = QApplication.translate("QSphere","Unable to establish connection to", None, QApplication.UnicodeUTF8)
                msg = "%s %s" % (zMsg, self._server)
                self._allreporting+= msg
                return None                
        else :
            import base64
            params = base64.b64encode("%s:%s" % (self._user, self._password))
            headers = {'Content-Type': 'application/xml','Accept': 'application/xml','Authorization': 'Basic %s' % (params)}
            try : response_csw_publication = requests.post(self._server, data=dataXML, headers=headers)
            except requests.HTTPError as e:
                zMsg1 = QApplication.translate("QSphere","Unable to establish connection to", None, QApplication.UnicodeUTF8)
                zMsg2 = QApplication.translate("QSphere","HTTP error", None, QApplication.UnicodeUTF8)
                zMsg3 = QApplication.translate("QSphere","message", None, QApplication.UnicodeUTF8)
                msg = "%s %s\n%s : %s\n%s : %s " % (zMsg1, self._server, zMsg2, e.code, zMsg3, e.msg)
                self._allreporting+= msg
                return None
            

        if self._versiongeonetwork == 2100 :
           zEncoding = getEncodingCar("", response_csw_publication.text)
           try : self._reporting+= "%s\n%s\n" % (response_csw_publication.status_code, response_csw_publication.text.decode(zEncoding))
           except : self._reporting+= "%s\n%s\n" % (response_csw_publication.status_code, response_csw_publication.text)
        else :
           zEncoding = getEncodingCar("", response_csw_publication.content)  
           try : self._reporting+= "%s\n%s\n" % (response_csw_publication.status_code, response_csw_publication.content.decode(zEncoding))
           except : self._reporting+= "%s\n%s\n" % (response_csw_publication.status_code, response_csw_publication.content)
           
        self._allreporting+= self._reporting
        return response_csw_publication
        

    def analyseResponse(self, ucase, response):
        analyseResponse, cswID = False, None
        if response == None :
            self.errAnalyseResponse(response)
            return (analyseResponse, cswID)

        from xml.etree import ElementTree as ET
        from cStringIO import StringIO

        if self._versiongeonetwork == 2100 : zcontent = StringIO(response.text)
        else : zcontent = StringIO(response.content)

        try : etree = ET.parse(zcontent)
        except : return False, None
            
	self.root = etree.getroot()
	
        if self.root == None : return (False, None)
        if self.root.tag not in self._valid_xpaths : return (False, None)
       
	dict_Resp_CSWT = {1:"csw:TransactionSummary/csw:totalInserted", 2:"csw:TransactionSummary/csw:totalUpdated", -1:"csw:TransactionSummary/csw:totalDeleted"}
        xpathNS = appendNameSpace(self, dict_Resp_CSWT[ucase])

        rootEl = self.root.findall(xpathNS) 
        try :    
            if rootEl :
               analyseResponse = (int(rootEl[0].text)==1)
               if ucase == 1 :
                  xpathNS = appendNameSpace(self, "csw:InsertResult/csw:BriefRecord") 
                  try  : cswID = self.root.findall("%s/identifier" % (xpathNS))[0].text
                  except : cswID = None
            zTitle = QApplication.translate("QSphere", "Information" , None, QApplication.UnicodeUTF8)
            zMsg = QApplication.translate("QSphere","Transaction completely released with the server", None, QApplication.UnicodeUTF8)
            if ucase == 1 and cswID != None : zMsg+= "\n%s : %s" % (QApplication.translate("QSphere","Add record to the server with UUID", None, QApplication.UnicodeUTF8), cswID)
            SendMessage(self.parent, zTitle, "%s :\n%s" % (zMsg, response), QgsMessageBar.INFO, self.duration_info)
            self._reporting+= "%s :\n%s" % (zMsg, response)
            self._allreporting+= "%s :\n%s" % (zMsg, response)
        except : self.errAnalyseResponse(response)

        return (analyseResponse, cswID)

    def errAnalyseResponse(self, response):
        zTitle = QApplication.translate("QSphere", "Warning" , None, QApplication.UnicodeUTF8)
        zMsg = QApplication.translate("QSphere","No Querying possible with the server response", None, QApplication.UnicodeUTF8)
        SendMessage(self.parent, zTitle, "%s :\n%s" % (zMsg, response), QgsMessageBar.WARNING, self.duration_info)
        self._reporting+= "%s :\n%s" % (zMsg, response)
        self._allreporting+= "%s :\n%s" % (zMsg, response)
