<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>
<%def name="js()" filter="trim">
    ${utils.js_link("lobbypy.js")}
</%def>

<%def name="main_content()" filter="trim">
<div id="app-container"></div>
</%def>
