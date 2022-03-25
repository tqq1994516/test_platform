# -*- coding: utf-8 -*-
# @Time : 2022/3/9 15:48
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : authentication.py
# @Project : backend
# @Description : ...
"""
Provides various authentication policies.
"""
from sanic_babel import lazy_gettext as _

from srf.exceptions import AuthenticationDenied
from srf.redis_tool import get_value
from srf.request import SRFRequest


class BaseAuthentication:
    """
    All authentication classes should extend BaseAuthentication.
    """

    def authenticateauthenticate(self, request: SRFRequest, view, **kwargs):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        raise NotImplementedError(".authenticate() must be overridden.")

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass


class JWTAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'X-Token'

    async def authenticate(self, request: SRFRequest, view, **kwargs):
        token = request.headers.get(self.keyword)
        if token is None:
            raise AuthenticationDenied(_('Authentication error:request headers "{}" nonentity').format(self.keyword))
        return self.authenticate_credentials(request, token)

    async def authenticate_credentials(self, request: SRFRequest, key):
        with request.app.ctx.redis as redis:
            val = get_value(redis, key)
        if val:
            return ('test', 'success')
        else:
            raise AuthenticationDenied(_('User not logged in.'))

    async def authenticate_header(self, request):
        return self.keyword
