from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username', 'email']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user and user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            return {'success':'User loggedin sucessfully..',
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
        raise serializers.ValidationError('Incorrect credentials')