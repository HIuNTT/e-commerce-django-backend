from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['is_staff'] = user.is_staff
        # ...

        return token

    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #     serializer = UserInfoSerializer(self.user)
    #     data.update(serializer.data)
    #     return data