"""
@Author：WangYuXiang
@E-mile：Hill@3io.cc
@CreateTime：2021/3/26 14:43
@DependencyLibrary：无
@MainFunction：无
@FileDoc： 
    mixins.py
    文件说明
@ChangeHistory:
    datetime action why
    example:
    2021/3/26 14:43 change 'Fix bug'
        
"""
from srf.paginations import ORMPagination
from srf.status import HttpStatus

__all__ = (
    'ListModelMixin', 'CreateModelMixin', 'RetrieveModelMixin', 'UpdateModelMixin', 'DestroyModelMixin'
)


class ListModelMixin:
    """
    适用于输出列表类型数据
    """
    pagination_class = ORMPagination

    async def list(self, request, *args, **kwargs):
        queryset = await self.get_queryset(request, *args, **kwargs)

        page = await self.paginate_queryset(queryset, request, *args, **kwargs)
        if page is not None:
            self._paginator.set_count(await self.get_paginator_count(queryset))
            serializer = self.get_serializer(request, page, many=True, *args, **kwargs)
            data = self.get_paginated_response(await serializer.data)
            return self.success_json_response(msg="查询成功！", data=data)

        serializer = self.get_serializer(queryset, many=True)
        return self.success_json_response(msg="查询成功！", data=await serializer.data)


class CreateModelMixin:
    """
    适用于快速创建内容
    占用 post 方法
    """

    async def post(self, request, *args, **kwargs):
        request.data['owner'] = await request.app.ctx.auth.extract_user_id(request)
        return await self.create(request, *args, **kwargs)

    async def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        await serializer.is_valid(raise_exception=True)
        await self.perform_create(serializer)
        return self.success_json_response(msg="创建成功！", data=await serializer.data, http_status=HttpStatus.HTTP_201_CREATED)

    async def perform_create(self, serializer):
        await serializer.save()


class RetrieveModelMixin:
    """
    适用于查询指定PK的内容
    """

    async def get(self, request, *args, **kwargs):
        if '' != kwargs[self.lookup_field]:
            return await self.retrieve(request, *args, **kwargs)
        else:
            kwargs.pop(self.lookup_field)
            return await self.list(request, *args, **kwargs)
    async def retrieve(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.request = request
        instance = await self.get_object()
        serializer = self.get_serializer(request, instance)
        return self.success_json_response(msg="查询成功！", data=await serializer.data)


class UpdateModelMixin:
    """
    适用于快速创建更新操作
    """

    async def put(self, request, *args, **kwargs):
        return await self.update(request, *args, **kwargs)

    async def patch(self, request, *args, **kwargs):
        return await self.partial_update(request, *args, **kwargs)

    async def update(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.request = request
        partial = kwargs.pop('partial', False)
        instance = await self.get_object()
        serializer = self.get_serializer(request, instance, data=request.data, partial=partial)
        await serializer.is_valid(raise_exception=True)
        await self.perform_update(serializer)
        return self.success_json_response(msg="更新成功！", data=await serializer.data)

    async def perform_update(self, serializer):
        await serializer.save()

    async def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return await self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    用于快速删除
    """

    async def delete(self, request, *args, **kwargs):
        return await self.destroy(request, *args, **kwargs)

    async def destroy(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.request = request
        instance = await self.get_object()
        await self.perform_destroy(instance)
        return self.success_json_response(msg="删除成功！", http_status=HttpStatus.HTTP_200_OK)

    async def perform_destroy(self, instance):
        await instance.delete()
