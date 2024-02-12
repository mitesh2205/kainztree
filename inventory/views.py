from django.core.cache import cache
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from .models import Item
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .serializers import ItemSerializer, UserLoginSerializer, UserSignupSerializer

class ItemList(generics.ListAPIView):
    serializer_class = ItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 15, key_prefix='item_list_cache_user_{user_id}'))   # Cache for 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = Item.objects.all()

        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            queryset = queryset.filter(date_added__range=[start_date, end_date])

        # Filter by stock status
        stock_status = self.request.query_params.get('stock_status', None)
        if stock_status:
            queryset = queryset.filter(stock_status=stock_status)

        return queryset

class UserSignup(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving with make_password
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Fetch user by username from the database
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the provided password matches the stored password
        if user.check_password(password):
            # If password is correct, create or retrieve the token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserLogout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the token to logout the user
        request.auth.delete()

        # Invalidate the cache by changing the cache key based on the user's ID
        user_id = request.user.id
        cache_key = f'item_list_cache_user_{user_id}'
        cache.delete(cache_key)

        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)