from rest_framework import generics,status
from .models import Property, Unit, Tenant
from .serializers import PropertySerializer, UnitSerializer, TenantSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminOrReadOnly
from django.db.models import Q

class LoginView(APIView):
    def post(self, request):
        superuser_email = request.data.get('email', '')
        superuser_password = request.data.get('password', '')

        # Authenticate the superuser using email
        user = authenticate(request, email=superuser_email, password=superuser_password)

        if user is not None:
            # If authentication is successful, generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({'access_token': access_token, 'refresh_token': refresh_token})

        else:
            return Response({'error': 'Failed to authenticate superuser'}, status=401)


class PropertyListCreateView(generics.ListCreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminOrReadOnly]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminOrReadOnly]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    def perform_destroy(self, instance):
        # Delete associated units
        units = Unit.objects.filter(property=instance)
        units.delete()
        # Delete the property
        instance.delete()

class UnitListCreateView(generics.ListCreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminOrReadOnly]
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class UnitDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminOrReadOnly]
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class TenantListCreateView(generics.ListCreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,IsAdminUser]
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class TenantDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,IsAdminUser]
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class PropertySearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q')

        if query:
            properties = Property.objects.filter(
                Q(name__icontains=query) |
                Q(address__icontains=query) 
            ).distinct()

            units = Unit.objects.filter(
                Q(rent_cost__icontains=query) |
                Q(bedroom_type__icontains=query) |
                Q(property__name__icontains=query) |
                Q(property__address__icontains=query)
            ).distinct()

            property_serializer = PropertySerializer(properties, many=True)
            unit_serializer = UnitSerializer(units, many=True)

            return Response({'properties': property_serializer.data, 'units': unit_serializer.data})

        else:
            properties = Property.objects.all()
            units = Unit.objects.all()

            property_serializer = PropertySerializer(properties, many=True)
            unit_serializer = UnitSerializer(units, many=True)

            return Response({'properties': property_serializer.data, 'units': unit_serializer.data})

