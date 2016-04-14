# -*- coding: utf-8 -*-
#
# This file is part of EUDAT B2Share.
# Copyright (C) 2015, 2016, University of Tuebingen, CERN.
#
# B2Share is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# B2Share is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with B2Share; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""EUDAT B2ACCESS OAuth configuration."""


# def decorate_http_request(remote):
#     """ Decorate the OAuth call to access token endpoint to inject the Authorization header"""
#     old_http_request = remote.http_request
#     def new_http_request(uri, headers=None, data=None, method=None):
#         if not headers:
#             headers = {}
#         if not headers.get("Authorization"):
#             from urlparse import parse_qs
#             from base64 import b64encode
#             args = parse_qs(data)
#             client_id_list = args.get('client_id')
#             client_id = None if len(client_id_list) == 0 else client_id_list[0]
#             client_secret_list = args.get('client_secret')
#             client_secret = None if len(client_secret_list) == 0 else client_secret_list[0]
#             userpass = b64encode("%s:%s" % (client_id, client_secret)).decode("ascii")
#             headers.update({ 'Authorization' : 'Basic %s' %  (userpass,) })
#         return old_http_request(uri, headers=headers, data=data, method=method)
#     remote.http_request = new_http_request

REMOTE_APP = dict(
    title='B2Access',
    description='EUDAT B2Access authentication.',
    icon='',
    # setup=decorate_http_request,
    authorized_handler="invenio_oauthclient.handlers:authorized_signup_handler",
    disconnect_handler="invenio_oauthclient.handlers:disconnect_handler",
    signup_handler=dict(
        info="b2share.oauth.b2access:account_info",
        setup="b2share.oauth.b2access:account_setup",
        view="invenio_oauthclient.handlers:signup_handler",
    ),
    params=dict(
        request_token_params={'scope': 'USER_PROFILE GENERATE_USER_CERTIFICATE'},
        base_url='https://b2access.eudat.eu:8443/',
        request_token_url=None,
        access_token_url= "https://b2access.eudat.eu:8443/oauth2/token",
        access_token_method='POST',
        authorize_url="https://b2access.eudat.eu:8443/oauth2-as/oauth2-authz",
        app_key="B2ACCESS_APP_CREDENTIALS",
    ),
    tokeninfo_url = "https://b2access.eudat.eu:8443/oauth2/tokeninfo",
    userinfo_url = "https://b2access.eudat.eu:8443/oauth2/userinfo",
)


def account_info(remote, resp):
    """Retrieve remote account information used to find local user. """
    from flask import current_app
    import json
    try:
        import urllib2 as http
    except ImportError:
        from urllib import request as http

    url = REMOTE_APP.get('userinfo_url')
    headers = { 'Authorization' : 'Bearer %s' %  (resp.get('access_token'),) }
    req = http.Request(url, headers=headers)
    response, content = None, None
    try:
        response = http.urlopen(req)
        content = response.read()
        response.close()
        dict_content = json.loads(content)
        if dict_content.get('cn') is None:
            return dict(email=dict_content.get('email'), nickname=dict_content.get('userName'))
        else:
            return dict(email=dict_content.get('email'), nickname=dict_content.get('cn'))
    except http.HTTPError as response:
        content = response.read()
        response.close()
        current_app.logger.warning("Failed to get user info from Unity", exc_info=True)

    return dict(email=None, nickname=None)


def account_setup(remote, token):
    """ Perform additional setup after user have been logged in. """
    pass
