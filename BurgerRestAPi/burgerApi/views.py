from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import MyUser, CarRent, Car
from .serializers import MyUserSerializer, MyOrderSerializer, MyCarSerializer


class MyUserViewSet(ModelViewSet):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()


class CarsViewSet(ModelViewSet):
    serializer_class = MyCarSerializer
    queryset = Car.objects.all()


class MyRentViewSet(ModelViewSet):
    serializer_class = MyOrderSerializer
    # queryset = MyOrder.objects.all()
    permission_classes = [
        # IsAuthenticated,
    ]

    def get_queryset(self):
        queryset = CarRent.objects.all()
        id = self.request.query_params.get("id", None)

        if id is not None:
            queryset = queryset.filter(user__id=id)
        return queryset
