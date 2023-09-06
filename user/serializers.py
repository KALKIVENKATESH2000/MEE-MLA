from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
User = get_user_model()
from django.contrib.auth.models import Permission
from .models import Profile, MLA, CustomUser


# admin register serializer
class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'fcm_token', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        superadmin = CustomUser(
            username=validated_data['email'],
            email=validated_data['email'],
            fcm_token=validated_data['fcm_token'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        superadmin.set_password(validated_data['password'])
        superadmin.is_staff = True
        # superadmin.is_superuser = True
        # add_permission = Permission.objects.get(name='Can add question')
        # view_permission = Permission.objects.get(name='Can view question')
        # change_permission = Permission.objects.get(name='Can change question')
        # delete_permission = Permission.objects.get(name='Can delete question')
        # view_answer = Permission.objects.get(name='Can view answer')

        superadmin.save()
        # superadmin.user_permissions.add(
        #     add_permission,
        #     view_permission,
        #     change_permission,
        #     delete_permission,
        #     view_answer
        # )
        return superadmin


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    # fcm_token = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'fcm_token']

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            fcm_token=validated_data['fcm_token'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = CustomUser.objects.filter(email=data['email']).first()
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
  
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','first_name', 'last_name', 'email', 'mla']
        
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.CharField(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['user', 'email', 'full_name','phone', 'gender','constituency', 'image']
        
class MLASerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.CharField(read_only=True)
    
    class Meta:
        model = MLA
        fields = ['user', 'email', 'full_name','phone','constituency', 'image']
