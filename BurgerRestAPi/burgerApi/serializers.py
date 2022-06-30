from rest_framework import serializers
from .models import MyUser, MyCustomerDetail, CarRent, Car


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            "id",
            "email",
            "account_type",
            "password",
        ]

        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def create(self, validated_data):
        return MyUser.objects.create_user(
            email=validated_data["email"],
            account_type=validated_data["account_type"],
            password=validated_data["password"],
        )


class MyCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class MyCustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCustomerDetail
        exclude = [
            "id",
        ]


class MyOrderSerializer(serializers.ModelSerializer):
    customer = MyCustomerDetailSerializer()

    class Meta:
        model = CarRent
        fields = "__all__"

    def create(self, validated_data):
        customer_data = validated_data.pop("customer")
        customer = MyCustomerDetailSerializer.create(
            MyCustomerDetailSerializer(), validated_data=customer_data
        )
        order, created = CarRent.objects.update_or_create(
            car=validated_data.pop("car"),
            customer=customer,
            user=validated_data.pop("user"),
        )
        return order
