from srf.generics import GenericAPIView
from srf import mixins

__all__ = ('GenericViewSet', 'ModelViewSet')


class GenericViewSet(GenericAPIView):
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
