from srf.views import APIView
from srf.generics import GenericAPIView
from srf import mixins
from srf.constant import DEFAULT_METHOD_MAP

__all__ = ('ViewSetMixin', 'ViewSet', 'GenericViewSet', 'ModelViewSet')


class ViewSetMixin:

    @classmethod
    def as_view(cls, method_map=DEFAULT_METHOD_MAP, *class_args, **class_kwargs):

        # 返回的响应方法闭包
        def view(request, *args, **kwargs):
            self = view.base_class(*class_args, **class_kwargs)
            view_method_map = {}
            for method, action in method_map.items():
                handler = getattr(self, action, None)
                if handler:
                    setattr(self, method, handler)
                    view_method_map[method] = action

            self.method_map = view_method_map
            self.methods = list(view_method_map.keys())
            self.request = request
            self.args = args
            self.kwargs = kwargs
            self.app = request.app
            return self.dispatch(request, *args, **kwargs)

        view.base_class = cls
        view.methods = list(method_map.keys())
        view.API_DOC_CONFIG = class_kwargs.get('API_DOC_CONFIG')  # 未来的API文档配置属性+
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.__name__ = cls.__name__
        return view


class ViewSet(ViewSetMixin, APIView):
    """
    默认情况下，基本ViewSet类不提供任何操作。
    """
    pass


class GenericViewSet(ViewSetMixin, GenericAPIView):
    """
    GenericViewSet类默认不提供任何操作，但确实包含基本的通用视图行为集，
    例如 `get_object()` 和 `get_queryset()` 方法。
    """
    pass


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    `create()`, `retrieve()`, `update()`, `partial_update()`, `destroy()`, `list()` actions.
    """
    pass
