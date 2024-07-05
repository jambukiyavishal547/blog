from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# Create your views here.
from .serializers import BlogSerializer,UserLoginSerializer,UserSerializer,BlogEditSerializer
from django.contrib.auth import authenticate
from .models import Blog,User

# Generate Token Manually
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':"user Added"}, status=201)
        return Response(serializer.errors, status=400)
    
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'msg':'login Completed',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Invalid credentials'}, status=400)
        return Response(serializer.errors, status=400)
            
class BlogListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admin users to add blogs.
    """
    def has_permission(self, request, view):
        # Allow read-only access to all users (GET, HEAD, OPTIONS requests)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if user is admin
        return request.user and request.user.is_staff



token_string = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2ODExMDYzLCJpYXQiOjE3MTY4MDkyNjMsImp0aSI6ImM4M2I1MjI1NThmMzQ5NzA4Y2QzOTE0M2Y3M2ZlZmFhIiwidXNlcl9pZCI6Mn0.HB81Q0m1aWIguVdS44Q-uxPKHR61iSJIo_KwuqJMx6M"
class BlogCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def decode_token(self, token_string):        
        try:
            decode_token = AccessToken(token_string)
            return decode_token.payload
        except Exception as e:
            print("Error decoding token:", e)
            return None
    def post(self, request):
        decode_payload = self.decode_token(token_string)
        if not decode_payload:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = decode_payload.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Add author field to request data
        request.data['author'] = user_id

        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogEditView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def decode_token(self, token_string):        
        try:
            decode_token = AccessToken(token_string)
            return decode_token.payload
        except Exception as e:
            print("Error decoding token:", e)
            return None
    def post(self, request):
        decode_payload = self.decode_token(token_string)
        print(decode_payload)
        if not decode_payload:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        email = decode_payload.get('email')
        print(email)
        try:
            user = User.objects.filter(id=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = BlogEditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)