from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy

# User models.
class MyBaseUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("the Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, null=False)
    account_type = models.CharField(
        max_length=64,
        default="client",
        help_text=gettext_lazy(
            "Car Owner can use their car(s) for renting/Clients can rent car once a day."
        ),
    )

    is_staff = models.BooleanField(
        gettext_lazy("staff status"),
        default=False,
        help_text=gettext_lazy("Designates whether the user can log in this site"),
    )
    is_active = models.BooleanField(
        gettext_lazy("active"),
        default=True,
        help_text=gettext_lazy(
            "Designates whether this should be treated as active. unselect instead of deleting account."
        ),
    )

    USERNAME_FIELD = "email"
    objects = MyBaseUserManager()

    def __str__(self) -> str:
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


# Car Rent Models
class CarCategory(models.Model):
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "CarCategories"


class Car(models.Model):
    car_owner = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name="car_owner"
    )
    car_category = models.ForeignKey(
        CarCategory, on_delete=models.CASCADE, related_name="car_category"
    )
    car_name = models.CharField(max_length=264)
    car_detail = models.TextField(max_length=1024, verbose_name="car Description")
    car_rent_price = models.FloatField()
    car_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.car_name


class MyCustomerDetail(models.Model):
    address = models.TextField(blank=True)
    phone = models.CharField(blank=True, max_length=20)
    payment_type = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f"{self.address} {self.phone}"


class CarRent(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    car = models.OneToOneField(Car, on_delete=models.CASCADE, null=True)
    customer = models.OneToOneField(
        MyCustomerDetail, on_delete=models.CASCADE, null=True
    )
    rentDate = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} rented {self.car}"
