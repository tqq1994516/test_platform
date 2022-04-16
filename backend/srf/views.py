"""
@Author: WangYuXiang
@E-mile: Hill@3io.cc
@CreateTime: 2021/1/19 15:44
@DependencyLibrary:
@MainFunction：
@FileDoc:
    login.py
    基础视图文件
    BaseView    只实现路由分发的基础视图
    GeneralView 通用视图，可以基于其实现增删改查，提供权限套件
    ViewSetView 视图集视图，可以配合Mixin实现复杂的视图集，
                数据来源基于模型查询集,可以配合Route组件实现便捷的路由管理



"""
from sanic.response import json, HTTPResponse
from sanic_jwt import protected, Authentication
from ujson import dumps
from sanic.views import HTTPMethodView

from srf.exceptions import APIException, ValidationException
from srf.permissions import BasePermission, ViewMapPermission
from srf.status import RuleStatus, HttpStatus

__all__ = 'APIView'


class APIView(HTTPMethodView):
    """通用视图，可以基于其实现增删改查，提供权限套件"""
    authentication_classes = ()
    permission_classes = ()
    decorators = [protected()]
    is_transaction = True

    def handle_exception(self, exc: APIException):
        return self.json_response(**exc.response_data())

    def json_response(self, data=None, msg="OK", status=RuleStatus.STATUS_1_SUCCESS,
                      http_status=HttpStatus.HTTP_200_OK):
        """
        Json 相应体
        :param data: 返回的数据主题
        :param msg: 前台提示字符串
        :param status: 前台约定状态，供前台判断是否成功
        :param http_status: Http响应数据
        :return:
        """
        if data is None:
            data = {}
        response_body = {
            'result': data,
            'message': msg,
            'status': status
        }
        return json(body=response_body, status=http_status, dumps=dumps)

    def success_json_response(self, data=None, msg="Success", **kwargs):
        """
        快捷的成功的json响应体
        :param data: 返回的数据主题
        :param msg: 前台提示字符串
        :return: json
        """
        status = kwargs.pop('status', RuleStatus.STATUS_1_SUCCESS)
        http_status = kwargs.pop('http_status', HttpStatus.HTTP_200_OK)
        return self.json_response(data=data, msg=msg, status=status, http_status=http_status)

    def error_json_response(self, data=None, msg="Fail", **kwargs):
        """
        快捷的失败的json响应体
        :param data: 返回的数据主题
        :param msg: 前台提示字符串
        :return: json
        """
        status = kwargs.pop('status', RuleStatus.STATUS_0_FAIL)
        http_status = kwargs.pop('http_status', HttpStatus.HTTP_400_BAD_REQUEST)
        return self.json_response(data=data, msg=msg, status=status, http_status=http_status)

    def get_authenticators(self):
        """
        实例化并返回此视图可以使用的身份验证器列表
        """
        authentications = []
        for auth in self.authentication_classes:
            if isinstance(auth, Authentication):
                authentications.append(auth)
            else:
                authentications.append(auth)
        return authentications

    async def check_authentication(self, request):
        """
        检查权限 查看是否拥有权限，并在此处为Request.User 赋值
        :param request: 请求
        :return:
        """
        for authenticators in self.get_authenticators():
            await authenticators.authenticate(request, self)

    def get_permissions(self):
        """
        实例化并返回此视图所需的权限列表
        """
        permissions = []
        for permission in self.permission_classes:
            if isinstance(permission, BasePermission):
                permissions.append(permission)
            else:
                permissions.append(permissions)
        return permissions

    async def check_permissions(self, request):
        """
        检查是否应允许该请求，如果不允许该请求，
        则在 has_permission 中引发一个适当的异常。
        :param request: 当前请求
        :return:
        """
        for permission in self.get_permissions():
            await permission.has_permission(request, self)

    async def check_object_permissions(self, request, obj):
        """
        检查是否应允许给定对象的请求, 如果不允许该请求，
        则在 has_object_permission 中引发一个适当的异常。
            常用于 get_object() 方法
        :param request: 当前请求
        :param obj: 需要鉴权的模型对象
        :return:
        """
        for permission in self.get_permissions():
            await permission.has_object_permission(request, self, obj)

    async def check_throttles(self, request):
        """
        检查范围频率。
        则引发一个 APIException 异常。
        :param request:
        :return:
        """
        pass

    async def initial(self, request, *args, **kwargs):
        """
        在请求分发之前执行初始化操作，用于检查权限及检查基础内容
        """
        # jwt protected装饰器已取代authentication类
        # await self.check_authentication(request)
        await self.check_permissions(request)
        await self.check_throttles(request)
