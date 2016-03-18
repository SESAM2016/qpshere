"""
Class to hold methods that define the tuples holding xpath information to be used with the iso accessor class to 
return information for various parameters needed to complete the NDG Discovery Service database as part of the MEDIN
Upgraded ingest system.

Base on original developpements by Steve Donegan Dec/Jan 2009/2010 (difConvertedto_ISO19139).
Additionnal developpements and corrections : SESAM@2014
"""

class xmlISOreaderTag:
	
	def __init__(self): pass

        def dictionnary(self): return (self.dictionnary.__name__,{1:{'xpath':'gmd:qspheredictionnary/gco:CharacterString'}})

	def identificator(self): return (self.identificator.__name__,{1:{'xpath':'gmd:fileIdentifier/gco:CharacterString'}})
	
	def intitule(self): return (self.intitule.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/title/gco:CharacterString'}})
	
	def resume(self):return (self.resume.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString'}})
	
	def typedata(self):return (self.typedata.__name__,{1:{'xpath':'gmd:hierarchyLevel/gmd:MD_ScopeCode'}})
	
	def tablecarac(self):return (self.tablecarac.__name__,{1:{'xpath':'gmd:characterSet/gmd:MD_CharacterSetCode'}})

        def tablelocalisator(self): return (self.tablelocalisator.__name__,{1:{'xpath':'gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:linkage/gmd:URL'}},
                                                                   {2:{'xpath':'gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gco:CharacterString'}},
                                                                   {'order':{'url':1,'name':2}})
	
	def rs_identifier(self):return (self.rs_identifier.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:RS_Identifier/gmd:code/gco:CharacterString'}})

	def genealogie(self):return (self.genealogie.__name__,{1:{'xpath':'gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString'}})

	def coherence(self):return (self.coherence.__name__,{1:{'basilexpathvalue':'gmd:spatialRepresentationInfo/gmd:MD_VectorSpatialRepresentation/gmd:topologyLevel/gmd:MD_TopologyLevelCode'}},
                                                            {2:{'basilexpathvalue':'gmd:spatialRepresentationInfo/gmd:MD_VectorSpatialRepresentation/gmd:geometricObjects/gmd:MD_GeometricObjects/gmd:geometricObjectType/gmd:MD_GeometricObjectTypeCode'}},
                                                            {'order':{'TopologyLevelCode':1,'GeometricObjectTypeCode':2}})
	
	def authors(self): return (self.authors.__name__,{1:{'xpath':'gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'}})  #individualName before ??

	def tableemprises(self):
	    return (self.tableemprises.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal'}},
							 {2:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal'}},
							 {3:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal'}},
							 {4:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal'}},
							 {'order':{'north':1,'south':2,'east':3,'west':4}})

        def tablescr(self) : return (self.tablescr.__name__,{1:{'xpath':'gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString'}})
        
	def tableformats(self): return (self.tableformats.__name__,{1:{'xpath':'gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:name/gco:CharacterString'}},
                                                               {2:{'xpath':'gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:version/gco:CharacterString'}},
                                                               {'order':{'name':1,'version':2}})
        def tablelangues(self) : return (self.tablelangues.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode'}})
        
        def langmetada(self) : return (self.langmetada.__name__,{1:{'xpath':'gmd:language/gmd:LanguageCode'}})
        
        def ax_datemetada(self) : return (self.ax_datemetada.__name__,{1:{'xpath':'gmd:dateStamp/gco:DateTime'}})
        
        def datemetada(self) : return (self.datemetada.__name__,{1:{'xpath':'gmd:dateStamp/gco:Date'}})
        
        def tablecategories(self) : return (self.tablecategories.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString'}})

        def ax_tablecategories(self) : return (self.ax_tablecategories.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode'}}) 
        
        def tablemotsclefsf(self): return (self.tablemotsclefsf.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString'}},
					    {2:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString'}},
					    {3:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date'}},
					    {4:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode'}},
					    {'order':{'keyword':1,'thesaurus':2,'date':3,'typedate':4}})

	def ax_tablemotsclefsf(self): return (self.ax_tablemotsclefsf.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString'}})

        """
        def keywordsFisThesaurus(self): return (self.keywordsFisThesaurus.__name_, {1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString'}})

        def keywordsFThesaurusDate(self): return (self.keywordsFisThesaurus.__name_,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date'}},
                                                                                    {2:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:thesaurusName/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode'}},
                                                                                    {'order':{'date':1, 'typedate':2}})
        """                                                                                    
	def tableetenduetemporelle(self): return (self.tableetenduetemporelle.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition'}},
                                                                   {2:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition'}},
					                           {'order':{'start':1,'end':2}}) 
							
	def dates(self): return (self.dates.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode'}},
                                                     {2:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date'}},
                                                     {'order':{'type':1,'date':2}})
	
	def datest(self): return (self.datest.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode'}},
                                                     {2:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date'}},
                                                     {'order':{'type':1,'date':2}})
	
        def grouperesolutionscale(self) : return (self.grouperesolutionscale.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer'}})

        def ax_grouperesolutionscale(self) : return (self.ax_grouperesolutionscale.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance'}})

        def UnitsScalesUM(self) : return (self.scalesUM.__name__,{1:{'basilexpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance'}})
        
        def tablespecifications(self) : return (self.tablespecifications.__name__,{1:{'xpath':'gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:specification/gmd:CI_Citation/gmd:title/gco:CharacterString'}},
                                                                    {2:{'xpath':'gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:specification/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date'}},
                                                                    {3:{'basilexpathvalue':'gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:specification/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode'}},
                                                                    {4:{'basilexpath':'gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:pass'}},
                                                                    {'order':{'text': 1, 'date':2, 'typedate':3, 'conformity':4}})

        def licence(self): return (self.licence.__name__, {1: {'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString'}})

        def groupedroits(self): return (self.groupedroits.__name__, {1: {'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode'}})

        def otherconstraints(self): return (self.otherconstraints.__name__, {1: {'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:otherConstraints/gco:CharacterString'}})

	def tableroles(self):
            return (self.tableroles.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode'}},  
                                                  {2:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'}},
                                                  {3:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'}},
                                                  {4:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString'}},
                                                  {5:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString'}},
                                                  {6:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString'}},
                                                  {7:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'}},
                                                  {8:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'}},
                                                  {9:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL'}},
                                                  {'order':{'role': 1, 'name':2, 'adresse':3, 'pays': 4, 'codepostal': 5, 'ville':6, 'mail': 7, 'phone' : 8, 'url' : 9}})

	def ax_tableroles(self):
            return (self.ax_tableroles.__name__,{1:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage/gmd:userContactInfo/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode'}},
                                                     {2:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage/gmd:userContactInfo/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'}},
                                                     {3:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage/gmd:userContactInfo/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'}},
                                                     {4:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage/gmd:userContactInfo/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString'}},
                                                     {5:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage/gmd:userContactInfo/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString'}},
                                                     {6:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage/gmd:userContactInfo/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString'}},
                                                     {7:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage/gmd:userContactInfo/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'}},
                                                     {8:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage/gmd:userContactInfo/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'}},
                                                     {9:{'xpath':'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage/gmd:userContactInfo/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL'}},
                                                     {'order':{'role': 1, 'name':2, 'adresse':3, 'pays': 4, 'codepostal': 5, 'ville':6, 'mail': 7, 'phone' : 8, 'url' : 9}})

	def bx_tableroles(self):
            return (self.bx_tableroles.__name__,{1:{'xpath':'gmd:contact/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode'}},
                                                     {2:{'xpath':'gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString'}},
                                                     {3:{'xpath':'gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'}},
                                                     {4:{'xpath':'gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString'}},
                                                     {5:{'xpath':'gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString'}},
                                                     {6:{'xpath':'gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString'}},
                                                     {7:{'xpath':'gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'}},
                                                     {8:{'xpath':'gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString'}},
                                                     {9:{'xpath':'gmd:contact/gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL'}},
                                                     {'order':{'role': 1, 'name':2, 'adresse':3, 'pays': 4, 'codepostal': 5, 'ville':6, 'mail': 7, 'phone' : 8, 'url' : 9}})


