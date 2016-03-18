AUTHENTICATION_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<request>
    <username>%s</username>
    <password>%s</password>
</request>
"""

GET_RECORD_BYID = """<?xml version="1.0"?>
<csw:GetRecordById xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" version="2.0.2" service="CSW">
    <csw:Id>%s</csw:Id>
</csw:GetRecordById>
"""

GET_RECORDS = """<?xml version="1.0"?>
<csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw/2.0.2"
    xmlns:gmd="http://www.isotc211.org/2005/gmd" service="CSW" version="2.0.2" resultType="results">
    <csw:Query typeNames="gmd:MD_Metadata">
        <csw:Constraint version="1.1.0">
            <Filter xmlns="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml"/>
        </csw:Constraint>
    </csw:Query>
</csw:GetRecords>
"""

GET_CAPABILITIES_TEMPLATE = """<?xml version="1.0"?>
<csw:GetCapabilities xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" service="CSW">
	<ows:AcceptVersions xmlns:ows="http://www.opengis.net/ows">
		<ows:Version>2.0.2</ows:Version>
	</ows:AcceptVersions>
	<ows:AcceptFormats xmlns:ows="http://www.opengis.net/ows">
	        <ows:OutputFormat>application/xml</ows:OutputFormat>
	</ows:AcceptFormats>
</csw:GetCapabilities>
"""

INSERT_METADATA_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<csw:Transaction xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" version="2.0.2" service="CSW">
  <csw:Insert>%s</csw:Insert>
</csw:Transaction>
"""

UPDATE_METADATA_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<csw:Transaction xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" version="2.0.2" service="CSW">
  <csw:Update>%s</csw:Update>
</csw:Transaction>
"""


DELETE_METADATA_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<csw:Transaction xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ogc="http://www.opengis.net/ogc" version="2.0.2" service="CSW">
  <csw:Delete>
    <csw:Constraint version="1.1.0">
      <ogc:Filter>
        <ogc:PropertyIsEqualTo>
          <ogc:PropertyName>identifier</ogc:PropertyName>
          <ogc:Literal>%s</ogc:Literal>
        </ogc:PropertyIsEqualTo>
      </ogc:Filter>
    </csw:Constraint>
  </csw:Delete>
</csw:Transaction>
"""
