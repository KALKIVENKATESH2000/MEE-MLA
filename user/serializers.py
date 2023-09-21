from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
User = get_user_model()
from django.contrib.auth.models import Permission
from .models import Profile, MLA, CustomUser
from api.models import PollingStation
from api.serializers import ConstituencySerializer, PollingStationSerializer


# admin register serializer
class SuperAdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'roles']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        superadmin = CustomUser(
            username=validated_data['email'],
            email=validated_data['email'],
            # roles=validated_data['roles'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        superadmin.set_password(validated_data['password'])
        superadmin.is_staff = True
        superadmin.is_superuser = True
        superadmin.roles = 'superadmin'

        superadmin.save()
        return superadmin
    
    
class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'email', 'password', 'roles', 'constituency']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        admin = CustomUser(
            username=validated_data['email'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            constituency=validated_data['constituency'],
            # polling_station=validated_data['polling_station'],
            roles=validated_data['roles'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        admin.set_password(validated_data['password'])
        admin.is_staff = True
        admin.roles = 'admin'

        admin.save()
        return admin


class AgentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    polling_station = serializers.CharField(write_only=True)
    phone = serializers.IntegerField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'email', 'password', 'roles', 'constituency', 'polling_station']

    def create(self, validated_data):
        
        polling_station = validated_data.pop('polling_station')
        print(polling_station)
        
        user = CustomUser.objects.create(
            username=validated_data['phone'],
            phone=validated_data['phone'],
            constituency=validated_data['constituency'],
            # polling_station=validated_data['polling_station'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            roles=validated_data['roles'],
        )
        user.set_password(validated_data['password'])
        polling_station = PollingStation.objects.get(id=polling_station)
        user.polling_station = polling_station
        user.save()
        

        polling_station.user.add(user)
        
        return user
    
class VoterRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.IntegerField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'email', 'password', 'roles', 'constituency']

    def create(self, validated_data):
        
        
        voter = CustomUser.objects.create(
            username=validated_data['phone'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            constituency=validated_data['constituency'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        voter.set_password(validated_data['password'])
        voter.roles = 'voter'
        voter.save()
                
        return voter

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = CustomUser.objects.filter(email=data['email']).first()
        if user and user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            return {'success':'User loggedin sucessfully..',
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'roles': user.roles,
                    'email': user.email,
                    'username': user.username,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
        raise serializers.ValidationError('Incorrect credentials')
    
class AgentLoginSerializer(serializers.Serializer):
    phone = serializers.IntegerField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = CustomUser.objects.filter(phone=data['phone']).first()
        if user and user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            return {'success':'User loggedin sucessfully..',
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'phone': user.phone,
                    'roles': user.roles,
                    'username': user.username,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
        raise serializers.ValidationError('Incorrect credentials')
  
    
class UserSerializer(serializers.ModelSerializer):
    constituency = ConstituencySerializer(read_only=True)
    polling_stations = PollingStationSerializer(read_only=True, many=True)
    class Meta:
        model = CustomUser
        fields = ['id','first_name', 'last_name', 'email', 'phone', 'roles', 'constituency', 'polling_stations']
        
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.CharField(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['user', 'email', 'full_name','phone', 'gender', 'constituency', 'image', 'fcm_token']
        
class MLASerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.CharField(read_only=True)
    
    class Meta:
        model = MLA
        fields = ['user', 'email', 'full_name','phone','constituency', 'image']
