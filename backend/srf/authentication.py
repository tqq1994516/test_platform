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
from sanic import json
from sanic_babel import lazy_gettext as _
from sanic_jwt import BaseEndpoint
from tortoise.expressions import Q
from ujson import dumps

from settings import CACHE_REFRESH_PREFIX
from srf import ModelSerializer
from srf.encryption_algorithm import genearteMD5
from srf.helpers import get_user_models
from srf.redis_tool import del_json_key
from srf.request import SRFRequest
from srf.status import HttpStatus


class LoginSerializer(ModelSerializer):
    class Meta:
        model = get_user_models()
        fields = ('username', 'password')


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = get_user_models()
        read_only_fields = 'id'
        exclude = ('password', 'is_online')


async def authenticate(request: SRFRequest, *args, **kwargs):
    model_class = get_user_models()
    request.data['password'] = genearteMD5(request.data['password'])
    serializer = LoginSerializer(data=request.data)
    if await serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        u = await model_class.filter(Q(username=data['username']) & Q(password=data['password'])).first()
        if u:
            u.is_online = True
            await model_class.save(u)
            return u


class Logout(BaseEndpoint):
    async def get(self, request, *args, **kwargs):
        jwt = request.app.ctx.auth
        user_id = jwt.extract_user_id(request)
        model_class = get_user_models()
        u = await model_class.filter(id=user_id).first()
        if u:
            u.is_online = False
            await model_class.save(u)
            with request.app.ctx.redis as redis:
                await del_json_key(redis, f'{CACHE_REFRESH_PREFIX}{user_id}')
            return json(body={"msg": _("Logout success!")}, status=HttpStatus.HTTP_200_OK, dumps=dumps)
        else:
            return json(body={"msg": _("Token error!")}, status=HttpStatus.HTTP_400_BAD_REQUEST, dumps=dumps)


class Register(BaseEndpoint):
    async def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(request.data)
        await serializer.is_valid(raise_exception=True)
        try:
            await serializer.save()
            return json(body={"msg": _("Register success!")},
                        data=await serializer.data,
                        http_status=HttpStatus.HTTP_201_CREATED)
        except:
            return json(body={"msg": _("Register fail!")},
                        status=HttpStatus.HTTP_401_UNAUTHORIZED)


logout_register = (('/logout', Logout), ('/register', Register))
