<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
  xmlns:ctl="http://www.occamlab.com/ctl" xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xsl:output method="html" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN"
    doctype-system="http://www.w3.org/TR/html4/loose.dtd" indent="yes"/>
  <xsl:strip-space elements="*"/>
  <xsl:template match="text()"/>
  <xsl:template match="/">
    <html>
      <head>
        <title>QGIS Server Certification Report for WMS 1.3.0</title>
        <link rel="stylesheet" href="style.css" />
        <meta name="generator" content="CTL Report Generator v3"/>
        <xsl:element name="meta">
          <xsl:attribute name="name">date</xsl:attribute>
        </xsl:element>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
      </head>
      <body>
        <xsl:call-template name="tableoc"/>
      </body>
    </html>
  </xsl:template>
  <xsl:template name="tableoc">
    <div id="navbar" class="navbar">
      <div class="logo">
        <img style="height:60px" src="logo.png" alt="Logo" />
      </div>

      <h1>QGIS Server Certification Report for WMS 1.3.0</h1>

      <div class="date">
        {{TEMPLATE_DATE}}
      </div>

      <div class="about" id="color-identifier"></div>
    </div>

    <p>
      <br/>
      <br/>
      Overall result:
      <xsl:call-template name="testVerdictFromCode">
        <xsl:with-param name="resultCode" select="/execution/log[1]/endtest/@result"/>
      </xsl:call-template>
      <br/>
      <br/>
      Version: {{TEMPLATE_VERSION}}
      <br/>
      <br/>
      Commit: <a href="{{TEMPLATE_COMMIT_LINK}}">{{TEMPLATE_COMMIT}}</a>
      <br/>
      <br/>
      Level tests: BASIC, QUERYABLE, RECOMMENDATIONS
      <br/>
      <br/>
      Exhaustive description for Test Suite: <a href="http://cite.opengeospatial.org/teamengine/about/wms/1.3.0/site/wms-1_3_0-ats.html">here</a>
      <br/>
      <br/>
      This report is automatically generated thanks to <a href="https://github.com/pblottiere/pyogctest">pyogctest</a> and <a href="https://github.com/qgis/QGIS-Server-CertifSuite">QGIS-Server-CertifSuite</a>.
    </p>
    <h2>Content</h2>
    <xsl:call-template name="ispezione"/>
    <div id="toc_container">
      <!--<xsl:apply-templates mode="isp" select="/execution/log[1]/starttest"/>-->
      <xsl:call-template name="sommario"/>
    </div>
    <xsl:call-template name="dettagli"/>
  </xsl:template>
  <xsl:template name="sommario">
    <xsl:for-each select="/execution/log[1]">
      <xsl:call-template name="ispezione"/>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="ispezione">
    <xsl:if test="count(testcall) &gt; 0">
      <xsl:element name="ul">
        <xsl:for-each select="testcall">
          <xsl:variable name="sessione" select="@path"/>
          <li>
            <xsl:element name="a">
              <xsl:attribute name="href">
                <xsl:value-of select="concat('#',$sessione)"/>
              </xsl:attribute>
              <xsl:value-of select="/execution/log/starttest[@path=$sessione]/@local-name"/>
            </xsl:element>
            <xsl:call-template name="ricorsione"/>
          </li>
        </xsl:for-each>
      </xsl:element>
    </xsl:if>
  </xsl:template>
  <xsl:template name="ricorsione">
    <xsl:variable name="sessione2" select="@path"/>
    <xsl:comment>RESULT = <xsl:value-of
        select="/execution/log/starttest[@path=$sessione2]/parent::log/endtest/@result"/>
    </xsl:comment>
    <xsl:call-template name="testVerdictFromCode">
      <xsl:with-param name="resultCode"
        select="/execution/log/starttest[@path=$sessione2]/parent::log/endtest/@result"/>
    </xsl:call-template>
    <xsl:apply-templates mode="isp" select="/execution/log/starttest[@path=$sessione2]"/>
  </xsl:template>
  <xsl:template match="starttest" mode="isp">
    <xsl:for-each select="parent::*">
      <xsl:call-template name="ispezione"/>
    </xsl:for-each>
  </xsl:template>
  <!-- Contenuti -->
  <xsl:template name="dettagli">
    <xsl:for-each select="/execution/log">
      <div class="test">
        <xsl:apply-templates select="starttest" mode="call"/>
        <xsl:apply-templates select="message" mode="call"/>
        <xsl:apply-templates select="endtest" mode="call"/>
        <xsl:if test="count(testcall) &gt; 0">
          <p>
            <h4>Executed tests</h4> <ul>
              <xsl:apply-templates select="testcall" mode="call"/>
            </ul>
          </p>
        </xsl:if>
        <xsl:apply-templates select="formresults" mode="call"/>
        <xsl:apply-templates select="request" mode="call"/>
        <xsl:apply-templates select="response" mode="call"/>
      </div>
    </xsl:for-each>
  </xsl:template>
  <xsl:template match="starttest" mode="call">
    <h2>
      <xsl:element name="a">
        <xsl:attribute name="name">
          <xsl:value-of select="./@path"/>
        </xsl:attribute>test: <xsl:value-of select="concat(concat(./@prefix,':'),./@local-name)"/>
      </xsl:element>
    </h2>
    <p>
      <h4>Assertion</h4>
      <xsl:value-of select="./assertion"/>
    </p>
  </xsl:template>
  <xsl:template match="formresults" mode="call">
    <xsl:comment>FORM id= <xsl:value-of select="@id"/>
    </xsl:comment>
    <p>Form data:
      <pre>
        <xsl:if test="count(values/value) &gt; 0">
          <xsl:for-each select="values/value">
            <xsl:text/>
            <xsl:value-of select="current()/@key"/>=
            <xsl:value-of select="current()"/>
            <xsl:text/>
          </xsl:for-each>
        </xsl:if>
      </pre>
    </p>
  </xsl:template>
  <xsl:template match="testcall" mode="call">
    <xsl:variable name="sessione3" select="@path"/>
    <li>
      <xsl:element name="a">
        <xsl:attribute name="href">
          <xsl:value-of select="concat('#',$sessione3)"/>
        </xsl:attribute>
        <xsl:value-of
          select="concat(concat(/execution/log/starttest[@path=$sessione3]/@prefix,':'),/execution/log/starttest[@path=$sessione3]/@local-name)"
        />
      </xsl:element>
      <xsl:text> - </xsl:text>
      <xsl:call-template name="testVerdictFromCode">
        <xsl:with-param name="resultCode"
          select="/execution/log/starttest[@path=$sessione3]/parent::log/endtest/@result"/>
      </xsl:call-template>
    </li>
  </xsl:template>
  <xsl:template match="endtest" mode="call">
    <xsl:comment>RESULT number= <xsl:value-of select="@result"/>
    </xsl:comment>
    <p>
      <h4>Test result</h4>
      <xsl:call-template name="testVerdictFromCode">
        <xsl:with-param name="resultCode" select="@result"/>
      </xsl:call-template>
    </p>
  </xsl:template>
  <xsl:template match="message" mode="call">
    <p>
      <h4>Message</h4>
      <pre>
        <xsl:value-of select="current()"/>
      </pre>
    </p>
  </xsl:template>
  <xsl:template match="request" mode="call">
    <p><h4>Submitted request</h4>
      <pre>
        <b><em>Method</em></b>
        <xsl:text>&#10;</xsl:text>
        <xsl:value-of select="current()/ctl:request/ctl:method"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <b><em>URL</em></b>
        <xsl:text>&#10;</xsl:text>
        <xsl:value-of select="current()/ctl:request/ctl:url"/>
        <!--      <xsl:if test="count(current()/ctl:request/ctl:param) &lt; 1">NONE.</xsl:if> -->
        <xsl:if test="count(current()/ctl:request/ctl:param) &gt; 0">
          <xsl:for-each select="current()/ctl:request/ctl:param">
            <xsl:text/>
            <xsl:value-of select="current()/@name"/>=<xsl:value-of select="current()"/><xsl:text disable-output-escaping="yes"><![CDATA[&]]></xsl:text><br/>
          </xsl:for-each>
        </xsl:if>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>&#10;</xsl:text>
      </pre>
    </p>
    <pre>
      <xsl:apply-templates select="current()/ctl:request/ctl:body/*" mode="escape-xml"/>
    </pre>
  </xsl:template>
  <xsl:template match="response" mode="call">Response:
    <pre>
      <xsl:apply-templates select="content/*" mode="escape-xml"/>
    </pre>
  </xsl:template>
  <!-- escape-xml mode: serialize XML tree to text, with indent
    Based very loosely on templates by Wendell Piez -->
  <xsl:variable name="nl">
    <xsl:text>&#10;</xsl:text>
  </xsl:variable>
  <xsl:variable name="indent-increment" select="' '"/>
  <xsl:variable name="ns-decl-extra-indent" select="' '"/>
  <xsl:template match="*" mode="escape-xml">
    <xsl:param name="indent-string" select="$indent-increment"/>
    <xsl:param name="is-top" select="'true'"/>
    <!-- true if this is the top
                of the tree being serialized -->
    <xsl:param name="exclude-prefixes" select="''"/>
    <!-- ns-prefixes to avoid declaring -->
    <xsl:value-of select="$indent-string"/>
    <xsl:call-template name="write-starttag">
      <xsl:with-param name="is-top" select="$is-top"/>
      <xsl:with-param name="indent-string" select="$indent-string"/>
      <xsl:with-param name="exclude-prefixes" select="$exclude-prefixes"/>
    </xsl:call-template>
    <xsl:if test="*">
      <xsl:value-of select="$nl"/>
    </xsl:if>
    <xsl:apply-templates mode="escape-xml">
      <xsl:with-param name="indent-string" select="concat($indent-string, $indent-increment)"/>
      <xsl:with-param name="is-top" select="'false'"/>
    </xsl:apply-templates>
    <xsl:if test="*">
      <xsl:value-of select="$indent-string"/>
    </xsl:if>
    <xsl:if test="*|text()|comment()|processing-instruction()">
      <xsl:call-template name="write-endtag"/>
    </xsl:if>
    <xsl:value-of select="$nl"/>
  </xsl:template>
  <xsl:template name="write-starttag">
    <xsl:param name="is-top" select="'false'"/>
    <xsl:param name="exclude-prefixes" select="''"/>
    <!-- ns-prefixes to	  avoid declaring -->
    <xsl:param name="indent-string" select="''"/>
    <xsl:text>&lt;</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:for-each select="@*">
      <xsl:call-template name="write-attribute"/>
    </xsl:for-each>
    <xsl:call-template name="write-namespace-declarations">
      <xsl:with-param name="is-top" select="$is-top"/>
      <xsl:with-param name="exclude-prefixes" select="$exclude-prefixes"/>
      <xsl:with-param name="indent-string" select="$indent-string"/>
    </xsl:call-template>
    <xsl:if test="not(*|text()|comment()|processing-instruction())">/</xsl:if>
    <xsl:text>></xsl:text>
  </xsl:template>

  <xsl:template name="write-endtag">
    <xsl:text>&lt;/</xsl:text>
    <xsl:value-of select="name()"/>
    <xsl:text>></xsl:text>
  </xsl:template>

  <xsl:template name="write-attribute">
    <xsl:text/>
    <xsl:value-of select="name()"/>
    <xsl:text>="</xsl:text>
    <xsl:value-of select="."/>
    <xsl:text>"</xsl:text>
  </xsl:template>
  <!-- Output namespace declarations for the current element. -->
  <!-- Assumption: if an attribute in the source tree uses a
            particular namespace, its parent element will have a namespace node
            for that namespace (because the declaration for the namespace must
            be on the parent element or one of its ancestors). -->
  <xsl:template name="write-namespace-declarations">
    <xsl:param name="is-top" select="'false'"/>
    <xsl:param name="indent-string" select="''"/>
    <xsl:param name="exclude-prefixes" select="''"/>
    <xsl:variable name="current" select="."/>
    <xsl:variable name="parent-nss" select="../namespace::*"/>
    <xsl:for-each select="namespace::*">
      <xsl:variable name="ns-prefix" select="name()"/>
      <xsl:variable name="ns-uri" select="string(.)"/>
      <xsl:if
        test="not(contains(concat(' ', $exclude-prefixes, ' xml '), concat(' ', $ns-prefix, ''))) and ($is-top = 'true' or not($parent-nss[name() = $ns-prefix and string(.) = $ns-uri])) ">
        <!-- This namespace node doesn't exist on the parent, at least not
                        with that URI,
                        so we need to add a declaration. -->
        <!-- We could add the test and ($ns-prefix = '' or
                        ($current//.|$current//@*)[substring-before(name(), ':') =
                        $ns-prefix]) i.e. "and it's used by this element or some
                        descendant (or descendant-attribute) thereof:" Only problem
                        with the above test is that sometimes namespace declarations
                        are needed even though they're not used by a descendant
                        element or attribute: e.g. if the input is a stylesheet,
                        prefixes have to be declared if they're used in XPath
                        expressions [which are in attribute values]. We could have
                        problems in this area with regard to xsp-request.  -->
        <xsl:value-of select="concat($nl, $indent-string, $ns-decl-extra-indent)"/>
        <xsl:choose>
          <xsl:when test="$ns-prefix = ''">
            <xsl:value-of select="concat('xmlns=&quot;', $ns-uri, '&quot;')"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of
              select="concat('xmlns:', $ns-prefix, '=&quot;', $ns-uri, '&quot;')"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="testVerdictFromCode">
    <xsl:param name="resultCode" as="xs:string"/>
    <xsl:choose>
      <xsl:when test="number($resultCode) = 6">
        <b style="font-family: Verdana, sans-serif; color: #FF0000;"><xsl:text> Failed</xsl:text></b>
      </xsl:when>
      <xsl:when test="number($resultCode) = 5">
        <b style="font-family: Verdana, sans-serif; color: #FF0000;"><xsl:text> Failed (Inherited Failure)</xsl:text></b>
      </xsl:when>
      <xsl:when test="number($resultCode) = 4">
        <xsl:text>Warning</xsl:text>
      </xsl:when>
      <xsl:when test="number($resultCode) = 3">
        <xsl:text>Skipped</xsl:text>
      </xsl:when>
      <xsl:when test="number($resultCode) = 2">
        <xsl:text>Not Tested</xsl:text>
      </xsl:when>
      <xsl:when test="number($resultCode) = 1">
        <b style="font-family: Verdana, sans-serif; color: #006600;"><xsl:text> Passed</xsl:text></b>
      </xsl:when>
      <xsl:when test="number($resultCode) = 0">
        <xsl:text>Passed (Best Practice)</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>Continue (did not complete)</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>
