#!/usr/bin/env python

# Copyright (c) 2012, Darryl Pogue
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the
#       names of the contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import logging
import os.path
try:
    # These are for python3 support
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
    from urllib.parse import urlencode
    unistr = str
except ImportError:
    # Fallback to python2
    from urllib2 import urlopen, Request
    from urllib2 import HTTPError
    from urllib import urlencode
    unistr = unicode
try:
    import cPickle as pickle
except ImportError:
    import pickle


log = logging.getLogger(__name__)


class ClientLogin(object):
    """
    A Google ClientLogin session management class.

    It does not support a captcha verification, but it does work correctly with
    two-step authentication when it is provided with an application password
    rather than the Google account password.
    """

    # This is the URL used for ClientLogin authentication
    AUTH_URL = 'https://www.google.com/accounts/ClientLogin'

    def __init__(self, user=None, passwd=None, tokens=None, service="sj",
            acct_type='GOOGLE', source=None):
        """
        Create a new instance of the management class with the provided
        credentials.

        :param user:
        User's full email address.

        :param passwd:
        User's password. If the user is using two-factor authentication, this
        should be a password created specifically for this application.

        :param service:
        Name of the Google service you're requesting authorization for.

        :param acct_type:
        Type of account to request authorization for.
        Possible values are GOOGLE (default), HOSTED, or HOSTED_OR_GOOGLE.

        :param source: (optional)
        Short string identifying your application, for logging purposes.
        """
        if not tokens:  # Fetch tokens using user and password.
            if not user or not passwd:
                raise ValueError("You have to provide either tokens dict or"
                    " user/password pair")
            self.user = user
            self.passwd = passwd

            self.auth_token = None
            self.sid_token = None
            self.lsid_token = None
        else:  # Use previously acquired tokens.
            for name in ["auth", "sid", "lsid"]:
                if name not in tokens:
                    raise ValueError("Tokens dict has to provide '%s' token" %
                        name)
                else:
                    setattr(self, "%s_token" % name, tokens[name])

        self.service = service
        self.acct_type = acct_type
        self.source = source

    def get_tokens(self):
        "Returns a dict with obtained tokens."
        return {
            "auth": self.auth_token,
            "sid": self.sid_token,
            "lsid": self.lsid_token,
        }

    def _process_response(self, resp):
        ret = {}
        for line in resp.split('\n'):
            if '=' in line:
                var, val = line.split('=', 1)
                ret[var] = val
        return ret

    def _make_request(self, url, data, headers):
        if not data:
            data = None
        else:
            data = urlencode(data)
            data = data.encode('utf8')

        req = Request(url, data, headers)
        err = None

        try:
            resp_obj = urlopen(req)
        except HTTPError, e:
            err = e.code
            return err, e.read()
        resp = resp_obj.read()
        resp_obj.close()
        return None, unistr(resp, encoding='utf8')

    def _request_tokens(self):
        data = {
            'Email':        self.user,
            'Passwd':       self.passwd,
            'accountType':  self.acct_type,
            'service':      self.service
        }
        if self.source:
            data['source'] = self.source

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        err, resp = self._make_request(self.AUTH_URL, data, headers)
        if err is not None:
            raise RuntimeError("User/passsword verification failed: %s, %s" %
                (err, resp))

        ret = self._process_response(resp)
        if 'Auth' in ret:
            self.auth_token = ret['Auth']
        if 'SID' in ret:
            self.sid_token = ret['SID']
        if 'LSID' in ret:
            self.lsid_token = ret['LSID']

    def get_auth_token(self, request=False):
        """
        Returns an authentication token, creating one if needed.
        The first time this method is called, it will make a request for an
        authentication token. Subsequent calls to this method will return that
        same token, unless the request parameter is true.

        :param request: Force the request of a new authentication token.
        """
        if self.auth_token is None or request is True:
            self._request_tokens()
        return self.auth_token

    def get_sid_token(self, request=False):
        """
        Returns an SID cookie token, creating one if needed.
        The first time this method is called, it will make a request for an
        authentication token. Subsequent calls to this method will return that
        same token, unless the request parameter is true.

        :param request: Force the request of a new SID token.
        """

        if self.sid_token is None or request is True:
            self._request_tokens()
        return self.sid_token

    def get_lsid_token(self, request=False):
        """
        Returns an LSID cookie token, creating one if needed.
        The first time this method is called, it will make a request for an
        authentication token. Subsequent calls to this method will return that
        same token, unless the request parameter is true.

        :param request: Force the request of a new LSID token.
        """

        if self.lsid_token is None or request is True:
            self._request_tokens()
        return self.lsid_token

    def is_authenticated(self):
        """
        Returns whether this client login instance is authenticated.
        Returns True if there are valid tokens, False otherwise.
        """
        return  (
            self.auth_token is not None
            and self.sid_token  is not None
            and self.lsid_token is not None
        )
