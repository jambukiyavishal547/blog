from rest_framework import serializers
from .models import User, Blog
class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'},write_only=True)        
        #valitation of password
    def validate_email(self,value):
        print("email validate run")
        if value[-3:] ==  'com':
            raise serializers.ValidationError(".com domain is not allow")
        return value

    def validate(self, attrs, format=None):
        print("run this")
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password and password2 and password != password2:
            raise serializers.ValidationError("Password Not match")
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2'] 


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email', 'password']

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title','content','author']


class BlogEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title','content','author']