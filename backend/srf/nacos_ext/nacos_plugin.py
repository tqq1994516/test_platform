import json
from typing import Union
import requests
from requests.adapters import HTTPAdapter
from sanic.log import logger

from settings import NACOS_HOST, NACOS_PORT, NACOS_SSL


class NacosClient:
    CONFIG_BASE_URL = '''/nacos/v1/cs/configs'''
    INSTANCE_BASE_URL = '''/nacos/v1/ns/instance'''
    SERVICE_BASE_URL = '''/nacos/v1/ns/service'''
    NAMESPACE_BASE_URL = '''/nacos/v1/console/namespaces'''

    def __init__(self, ssl=NACOS_SSL):
        self.request = requests.session()
        self.request.mount("http://", HTTPAdapter(max_retries=3))
        self.request.mount("https://", HTTPAdapter(max_retries=3))
        self.base_host = f"{'http://' if not ssl else 'https://'}{NACOS_HOST}:{NACOS_PORT}"
        self.log = logger

    def __responseHa(self, res):
        self.log.info(f"响应信息：{res.text}")
        try:
            ret = json.loads(res.text)
            time = res.elapsed.total_seconds()
        except Exception as e:
            ret = res.text
            time = -1
        return ret, time

    def call_api(self, data, session=None, timeout=30):
        self.log.info("call_api接受的参数data是： %s" % data)

        if not session:
            sessionrun = self.request
        else:
            sessionrun = session
        try:
            data["timeout"] = timeout
            response = sessionrun.request(**data)
        except Exception as e:
            self.log.info("调用接口发生异常 ： %s" % e)
            return False, -1
        else:
            self.log.info("接口返回的消息体是： %s" % response.content)
            return self.__responseHa(res=response)

    def get_config(
        self,
        dataId: str,
        group: str,
        tenant: str = None
    ) -> tuple:
        """
        获取配置
        :param dataId: 配置的唯一标识
        :param group: 配置的分组
        :param tenant: 租户
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"获取配置的参数是： id:{dataId},group:{group}"
            f"{',tenant:' + tenant if tenant else ''}"
        )
        data = {
            "params": {
                "dataId": dataId,
                "group": group
            },
            "method": "GET",
            "url": self.base_host + self.CONFIG_BASE_URL
        }
        if tenant:
            data["params"]["tenant"] = tenant
        return self.call_api(data=data)

    def listener_config(
        self,
        dataId: str,
        group: str,
        contentMD5: str,
        timeout: int = 30000,
        tenant: str = None
    ) -> tuple:
        """
        获取配置
        :param dataId: 配置的唯一标识
        :param group: 配置的分组
        :param contentMD5: 配置的md5值
        :param tenant: 租户
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"获取配置的参数是： id:{dataId},group:{group}"
            f"contentMD5:{contentMD5},timeout:{timeout}"
            f"{',tenant:' + tenant if tenant else ''}"
        )
        data = {
            "data": {
                "Listening-Configs":
                    f"{dataId}^2{group}^2{contentMD5}"
                    f"{'^2' + tenant + '^1' if tenant else '^1'}"
            },
            "headers": {"Long-Pulling-Timeout": timeout},
            "method": "POST",
            "url": self.base_host + self.CONFIG_BASE_URL + '/listener'
        }
        return self.call_api(data=data)

    def publish_config(
        self,
        dataId: str,
        group: str,
        content: Union[str, dict],
        tenant: str = None,
        type: str = "json",
    ) -> tuple:
        """
        发布配置
        :param dataId: 配置的唯一标识
        :param group: 配置的分组
        :param content: 配置的内容
        :param tenant: 租户
        :param type: 配置的类型
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"发布配置的参数是： id:{dataId},group:{group},content:{content}"
            f"{',tenant:' + tenant if tenant else ''}"
        )
        data = {
            "data": {
                "dataId": dataId,
                "group": group,
                "content": content if isinstance(content, str) else json.dumps(content)
            },
            "method": "POST",
            "url": self.base_host + self.CONFIG_BASE_URL
        }
        if tenant:
            data["data"]["tenant"] = tenant
        if not isinstance(content, str):
            data["data"]['type'] = type
        return self.call_api(data=data)

    def delete_config(
        self,
        dataId: str,
        group: str,
        tenant: str = None
    ) -> tuple:
        """
        删除配置
        :param dataId: 配置的唯一标识
        :param group: 配置的分组
        :param tenant: 租户
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"删除配置的参数是： id:{dataId},group:{group}"
            f"{',tenant:' + tenant if tenant else ''}"
        )
        data = {
            "params": {
                "dataId": dataId,
                "group": group
            },
            "method": "DELETE",
            "url": self.base_host + self.CONFIG_BASE_URL
        }
        if tenant:
            data["params"]["tenant"] = tenant
        return self.call_api(data=data)

    def register_instance(
        self,
        ip: str,
        port: int,
        serviceName: str,
        namespaceId: str = None,
        weight: float = None,
        enabled: bool = None,
        healthy: bool = None,
        metadata: str = None,
        clusterName: str = None,
        groupName: str = None,
        ephemeral: bool = False,
    ) -> tuple:
        """
        注册实例
        :param appId: 应用id
        :param ip: 实例ip
        :param port: 实例端口
        :param serviceName: 实例名称
        :param namespaceId: 命名空间id
        :param weight: 实例权重
        :param enabled: 实例是否可用
        :param healthy: 实例是否健康
        :param metadata: 实例的元数据
        :param clusterName: 实例所属集群名称
        :param groupName: 实例所属分组名称
        :param ephemeral: 是否临时实例
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"注册实例的参数是： serviceName:{serviceName},ip:{ip},port:{port}"
            f"',ephemeral:{ephemeral}"
            f"{',namespaceId:' + namespaceId if namespaceId else ''}"
            f"{',weight:' + str(weight) if weight else ''}"
            f"{',enabled:' + str(enabled) if enabled else ''}"
            f"{',healthy:' + str(healthy) if healthy else ''}"
            f"{',metadata:' + metadata if metadata else ''}"
            f"{',clusterName:' + clusterName if clusterName else ''}"
            f"{',groupName:' + groupName if groupName else ''}"

        )
        data = {
            "data": {
                "ip": ip,
                "port": port,
                "serviceName": serviceName,
                "ephemeral": ephemeral
            },
            "method": "POST",
            "url": self.base_host + self.INSTANCE_BASE_URL
        }
        if namespaceId:
            data["data"]["namespaceId"] = namespaceId
        if weight:
            data["data"]["weight"] = weight
        if enabled:
            data["data"]["enabled"] = enabled
        if healthy:
            data["data"]["healthy"] = healthy
        if metadata:
            data["data"]["metadata"] = metadata
        if clusterName:
            data["data"]["clusterName"] = clusterName
        if groupName:
            data["data"]["groupName"] = groupName
        return self.call_api(data=data)

    def cancellation_instance(
        self,
        serviceName: str,
        ip: str,
        port: int,
        namespaceId: str = None,
        groupName: str = None,
        clusterName: str = None,
        ephemeral: bool = None,
    ) -> tuple:
        """
        取消注册实例
        :param serviceName: 应用名称
        :param ip: 实例ip
        :param port: 实例端口
        :param namespaceId: 命名空间id
        :param groupName: 实例所属分组名称
        :param clusterName: 实例所属集群名称
        :param ephemeral: 是否临时实例
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"取消注册实例的参数是： serviceName:{serviceName},ip:{ip},port:{port}"
            f"{',namespaceId:' + namespaceId if namespaceId else ''}"
            f"{',groupName:' + groupName if groupName else ''}"
            f"{',clusterName:' + clusterName if clusterName else ''}"
            f"{',ephemeral:' + str(ephemeral) if ephemeral else ''}"
        )
        data = {
            "params": {
                "serviceName": serviceName,
                "ip": ip,
                "port": port
            },
            "method": "DELETE",
            "url": self.base_host + self.INSTANCE_BASE_URL
        }
        if namespaceId:
            data["params"]["namespaceId"] = namespaceId
        if groupName:
            data["params"]["groupName"] = groupName
        if clusterName:
            data["params"]["clusterName"] = clusterName
        if ephemeral:
            data["params"]["ephemeral"] = ephemeral
        return self.call_api(data=data)

    def update_instance(
        self,
        serviceName: str,
        ip: str,
        port: int,
        namespaceId: str = None,
        weight: float = None,
        enabled: bool = None,
        metadata: str = None,
        clusterName: str = None,
        groupName: str = None,
        ephemeral: bool = None,
    ) -> tuple:
        """
        更新实例
        :param serviceName: 应用名称
        :param ip: 实例ip
        :param port: 实例端口
        :param namespaceId: 命名空间id
        :param weight: 实例权重
        :param enabled: 实例是否可用
        :param metadata: 实例的元数据
        :param clusterName: 实例所属集群名称
        :param groupName: 实例所属分组名称
        :param ephemeral: 是否临时实例
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"更新实例的参数是： serviceName:{serviceName},ip:{ip},port:{port}"
            f"{',namespaceId:' + namespaceId if namespaceId else ''}"
            f"{',weight:' + str(weight) if weight else ''}"
            f"{',enabled:' + str(enabled) if enabled else ''}"
            f"{',metadata:' + metadata if metadata else ''}"
            f"{',clusterName:' + clusterName if clusterName else ''}"
            f"{',groupName:' + groupName if groupName else ''}"
            f"{',ephemeral:' + str(ephemeral) if ephemeral else ''}"
        )
        data = {
            "params": {
                "serviceName": serviceName,
                "ip": ip,
                "port": port
            },
            "method": "PUT",
            "url": self.base_host + self.INSTANCE_BASE_URL
        }
        if namespaceId:
            data["params"]["namespaceId"] = namespaceId
        if groupName:
            data["params"]["groupName"] = groupName
        if clusterName:
            data["params"]["clusterName"] = clusterName
        if ephemeral:
            data["params"]["ephemeral"] = ephemeral
        if weight:
            data["params"]["weight"] = weight
        if enabled:
            data["params"]["enabled"] = enabled
        if metadata:
            data["params"]["metadata"] = metadata
        return self.call_api(data=data)

    def get_instance(
        self,
        serviceName: str,
        namespaceId: str = None,
        clusters: str = None,
        groupName: str = None,
        healthyOnly: bool = False,
    ) -> tuple:
        """
        获取实例
        :param serviceName: 应用名称
        :param namespaceId: 命名空间id
        :param clusters: 实例所属集群名称，多个集群用逗号分隔
        :param groupName: 实例所属分组名称
        :param healthyOnly: 是否只返回健康的实例
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"获取实例的参数是： serviceName:{serviceName}"
            f"{',namespaceId:' + namespaceId if namespaceId else ''}"
            f"{',clusters:' + clusters if clusters else ''}"
            f"{',groupName:' + groupName if groupName else ''}"
            f"{',healthyOnly:' + str(healthyOnly) if healthyOnly else ''}"
        )
        data = {
            "params": {
                "serviceName": serviceName,
            },
            "method": "GET",
            "url": self.base_host + self.INSTANCE_BASE_URL + '/list'
        }
        if namespaceId:
            data["params"]["namespaceId"] = namespaceId
        if clusters:
            data["params"]["clusters"] = clusters
        if groupName:
            data["params"]["groupName"] = groupName
        if healthyOnly:
            data["params"]["healthyOnly"] = healthyOnly
        return self.call_api(data=data)

    def detail_instance(
        self,
        serviceName: str,
        ip: str,
        port: int,
        namespaceId: str = None,
        clusterName: str = None,
        groupName: str = None,
        healthyOnly: bool = False,
        ephemeral: bool = None,
    ) -> tuple:
        """
        获取实例详情
        :param serviceName: 应用名称
        :param ip: 实例ip
        :param port: 实例端口
        :param namespaceId: 命名空间id
        :param clusterName: 实例所属集群名称
        :param groupName: 实例所属分组名称
        :param healthyOnly: 是否只返回健康的实例
        :param ephemeral: 是否临时实例
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"获取实例详情的参数是： serviceName:{serviceName},ip:{ip},port:{port}"
            f"{',namespaceId:' + namespaceId if namespaceId else ''}"
            f"{',clusterName:' + clusterName if clusterName else ''}"
            f"{',groupName:' + groupName if groupName else ''}"
            f"{',healthyOnly:' + str(healthyOnly) if healthyOnly else ''}"
            f"{',ephemeral:' + str(ephemeral) if ephemeral else ''}"
        )
        data = {
            "params": {
                "serviceName": serviceName,
                "ip": ip,
                "port": port
            },
            "method": "GET",
            "url": self.base_host + self.INSTANCE_BASE_URL
        }
        if namespaceId:
            data["params"]["namespaceId"] = namespaceId
        if clusterName:
            data["params"]["clusterName"] = clusterName
        if groupName:
            data["params"]["groupName"] = groupName
        if healthyOnly:
            data["params"]["healthyOnly"] = healthyOnly
        if ephemeral:
            data["params"]["ephemeral"] = ephemeral
        return self.call_api(data=data)

    def send_beat(
        self,
        serviceName: str,
        beat: dict,
        groupName: str = None,
        ephemeral: bool = False
    ) -> tuple:
        """
        发送心跳
        :param serviceName: 应用名称
        :param beat: 心跳信息
        :param groupName: 实例所属分组名称
        :param ephemeral: 是否临时实例
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"发送心跳的参数是： serviceName:{serviceName}"
            f",ephemeral:{ephemeral}"
            f"{',groupName:' + groupName if groupName else ''}"
        )
        data = {
            "params": {
                "serviceName": serviceName,
                "beat": json.dumps(beat),
                "ephemeral": ephemeral
            },
            "method": "PUT",
            "url": self.base_host + self.INSTANCE_BASE_URL + '/beat'
        }
        if groupName:
            data["params"]["groupName"] = groupName
        return self.call_api(data=data)

    def create_service(
        self,
        serviceName: str,
        namespaceId: str = None,
        protectThreshold: float = None,
        groupName: str = None,
        metadata: str = None,
        selector: dict = None
    ) -> tuple:
        """
        创建服务
        :param serviceName: 服务名称
        :param namespaceId: 命名空间id
        :param protectThreshold: 保护阈值
        :param groupName: 分组名称
        :param metadata: 元数据
        :param selector: 访问策略
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"创建服务的参数是： serviceName:{serviceName}"
            f"{',namespaceId:' + namespaceId if namespaceId else ''}"
            f"{',protectThreshold:' + str(protectThreshold) if protectThreshold else ''}"
            f"{',groupName:' + groupName if groupName else ''}"
            f"{',metadata:' + metadata if metadata else ''}"
            f"{',selector:' + json.dumps(selector) if selector else ''}"
        )
        data = {
            "data": {
                "serviceName": serviceName,
            },
            "method": "POST",
            "url": self.base_host + self.SERVICE_BASE_URL
        }
        if namespaceId:
            data["data"]["namespaceId"] = namespaceId
        if protectThreshold:
            data["data"]["protectThreshold"] = protectThreshold
        if groupName:
            data["data"]["groupName"] = groupName
        if metadata:
            data["data"]["metadata"] = metadata
        if selector:
            data["data"]["selector"] = json.dumps(selector)
        return self.call_api(data=data)

    def delete_service(
        self,
        serviceName: str,
        namespaceId: str = None,
        groupName: str = None,
    ) -> tuple:
        """
        删除服务
        :param serviceName: 服务名称
        :param namespaceId: 命名空间id
        :param groupName: 分组名称
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"删除服务的参数是： serviceName:{serviceName}"
            f"{',namespaceId:' + namespaceId if namespaceId else ''}"
            f"{',groupName:' + groupName if groupName else ''}"
        )
        data = {
            "params": {
                "serviceName": serviceName,
            },
            "method": "DELETE",
            "url": self.base_host + self.SERVICE_BASE_URL
        }
        if namespaceId:
            data["params"]["namespaceId"] = namespaceId
        if groupName:
            data["params"]["groupName"] = groupName
        return self.call_api(data=data)

    def update_service(
        self,
        serviceName: str,
        namespaceId: str = None,
        protectThreshold: float = None,
        groupName: str = None,
        metadata: str = None,
        selector: dict = None
    ) -> tuple:
        """
        更新服务
        :param serviceName: 服务名称
        :param namespaceId: 命名空间id
        :param protectThreshold: 保护阈值
        :param groupName: 分组名称
        :param metadata: 元数据
        :param selector: 访问策略
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"更新服务的参数是： serviceName:{serviceName}"
            f"{',namespaceId:' + namespaceId if namespaceId else ''}"
            f"{',protectThreshold:' + str(protectThreshold) if protectThreshold else ''}"
            f"{',groupName:' + groupName if groupName else ''}"
            f"{',metadata:' + metadata if metadata else ''}"
            f"{',selector:' + json.dumps(selector) if selector else ''}"
        )
        data = {
            "params": {
                "serviceName": serviceName,
            },
            "method": "PUT",
            "url": self.base_host + self.SERVICE_BASE_URL
        }
        if namespaceId:
            data["params"]["namespaceId"] = namespaceId
        if protectThreshold:
            data["params"]["protectThreshold"] = protectThreshold
        if groupName:
            data["params"]["groupName"] = groupName
        if metadata:
            data["params"]["metadata"] = metadata
        if selector:
            data["params"]["selector"] = json.dumps(selector)
        return self.call_api(data=data)

    def get_service(
        self,
        serviceName: str,
        namespaceId: str = None,
        groupName: str = None,
    ) -> tuple:
        """
        查询服务
        :param serviceName: 服务名称
        :param namespaceId: 命名空间id
        :param groupName: 分组名称
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"查询服务的参数是： serviceName:{serviceName}"
            f"{',namespaceId:' + namespaceId if namespaceId else ''}"
            f"{',groupName:' + groupName if groupName else ''}"
        )
        data = {
            "params": {
                "serviceName": serviceName,
            },
            "method": "GET",
            "url": self.base_host + self.SERVICE_BASE_URL
        }
        if namespaceId:
            data["params"]["namespaceId"] = namespaceId
        if groupName:
            data["params"]["groupName"] = groupName
        return self.call_api(data=data)

    def get_service_list(
        self,
        pageNo: int = 1,
        pageSize: int = 20,
        namespaceId: str = None,
        groupName: str = None,
    ) -> tuple:
        """
        查询服务列表
        :param pageNo: 页码
        :param pageSize: 每页数量
        :param namespaceId: 命名空间id
        :param groupName: 分组名称
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"查询服务列表的参数是： pageNo:{pageNo},pageSize:{pageSize}"
            f"{',namespaceId:' + namespaceId if namespaceId else ''}"
            f"{',groupName:' + groupName if groupName else ''}"
        )
        data = {
            "params": {
                "pageNo": pageNo,
                "pageSize": pageSize,
            },
            "method": "GET",
            "url": self.base_host + self.SERVICE_BASE_URL + '/list'
        }
        if namespaceId:
            data["params"]["namespaceId"] = namespaceId
        if groupName:
            data["params"]["groupName"] = groupName
        return self.call_api(data=data)

    def update_instance_health(
        self,
        serviceName: str,
        ip: str,
        port: int,
        healthy: bool,
        namespaceId: str = None,
        groupName: str = None,
        clusterName: str = None
    ) -> tuple:
        """
        更新实例健康状态
        :param serviceName: 服务名称
        :param ip: 实例ip
        :param port: 实例端口
        :param healthy: 健康状态
        :param namespaceId: 命名空间id
        :param groupName: 分组名称
        :param clusterName: 集群名称
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"更新实例健康状态的参数是： serviceName:{serviceName},ip:{ip},port:{port},healthy:{healthy}"
            f"{',namespaceId:' + namespaceId if namespaceId else ''}"
            f"{',groupName:' + groupName if groupName else ''}"
            f"{',clusterName:' + clusterName if clusterName else ''}"
        )
        data = {
            "params": {
                "serviceName": serviceName,
                "ip": ip,
                "port": port,
                "healthy": healthy,
            },
            "method": "PUT",
            "url": self.base_host + '/nacos/v1/ns/health/instance'
        }
        if namespaceId:
            data["params"]["namespaceId"] = namespaceId
        if groupName:
            data["params"]["groupName"] = groupName
        if clusterName:
            data["params"]["clusterName"] = clusterName
        return self.call_api(data=data)

    def get_namespace(self) -> tuple:
        """
        查询命名空间
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        data = {
            "method": "GET",
            "url": self.base_host + self.NAMESPACE_BASE_URL
        }
        return self.call_api(data=data)

    def create_namespace(
        self,
        namespaceName: str,
        customNamespaceId: str,
        namespaceDesc: str = None
    ) -> tuple:
        """
        创建命名空间
        :param namespaceName: 命名空间名称
        :param customNamespaceId: 自定义命名空间id
        :param namespaceDesc: 命名空间描述
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"创建命名空间的参数是： namespaceName:{namespaceName}"
            f",customNamespaceId:{customNamespaceId}"
            f"{',namespaceDesc:' + namespaceDesc if namespaceDesc else ''}"
        )
        data = {
            "data": {
                "namespaceName": namespaceName,
                "customNamespaceId": customNamespaceId,
            },
            "method": "POST",
            "url": self.base_host + self.NAMESPACE_BASE_URL
        }
        if namespaceDesc:
            data["data"]["namespaceDesc"] = namespaceDesc
        return self.call_api(data=data)

    def update_namespace(
        self,
        namespaceName: str,
        customNamespaceId: str,
        namespaceDesc: str
    ) -> tuple:
        """
        更新命名空间
        :param namespaceName: 命名空间名称
        :param customNamespaceId: 自定义命名空间id
        :param namespaceDesc: 命名空间描述
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(
            f"更新命名空间的参数是： namespaceName:{namespaceName}"
            f",customNamespaceId:{customNamespaceId}"
            f",namespaceDesc:{namespaceDesc}"
        )
        data = {
            "data": {
                "namespaceName": namespaceName,
                "customNamespaceId": customNamespaceId,
            },
            "method": "PUT",
            "url": self.base_host + self.NAMESPACE_BASE_URL
        }
        if namespaceDesc:
            data["params"]["namespaceDesc"] = namespaceDesc
        return self.call_api(data=data)

    def delete_namespace(self, namespaceId: str) -> tuple:
        """
        删除命名空间
        :param namespaceId: 命名空间id
        :return: 配置值

        err code:
        400	Bad Request	客户端请求中的语法错误
        403	Forbidden	没有权限
        404	Not Found	无法找到资源
        500	Internal Server Error	服务器内部错误
        200	OK	正常
        """
        self.log.info(f"删除命名空间的参数是： namespaceId:{namespaceId}")
        data = {
            "data": {
                "namespaceId": namespaceId,
            },
            "method": "DELETE",
            "url": self.base_host + self.NAMESPACE_BASE_URL
        }
        return self.call_api(data=data)


nacos_client = NacosClient()
