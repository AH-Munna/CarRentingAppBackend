from django.urls import path
from rest_framework import routers
from .views import MyUserViewSet, MyRentViewSet, CarsViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

myRouter = routers.DefaultRouter()
myRouter.register("user", MyUserViewSet)
myRouter.register("cars", CarsViewSet, basename="cars")
myRouter.register("rent", MyRentViewSet, basename="rent")

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + myRouter.urls
