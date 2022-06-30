from django.contrib import admin
from .models import CarRent, MyUser, MyCustomerDetail, CarCategory, Car

# Register your models here.
admin.site.register(MyUser)
admin.site.register(MyCustomerDetail)
admin.site.register(Car)
admin.site.register(CarCategory)
admin.site.register(CarRent)
