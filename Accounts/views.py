from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListCreateAPIView,UpdateAPIView,RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from .serializers import *
from .models import User,Job
from django.http import Http404


class AuthUserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)

    def put(self, request, id, format=None):
        user = self.get_object(id)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, formet=None):

        all_user = User.objects.all()
        serializer = self.serializer_class(all_user, many=True)
        return Response(serializer.data)


class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)
        
class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class JobCreateView(ListCreateAPIView):

    serializer_class = JobCreateSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Job.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def list(self, request):
        queryset = self.queryset.filter(owner=request.user)
        serializer = JobCreateSerializer(queryset, many=True)
        return Response(serializer.data)

class JobRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = JobCreateSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Job.objects.all()

class JobTypeView(ListCreateAPIView):

    serializer_class = JobTypeSerializers
    permission_classes = (IsAuthenticated, )
    queryset = JobType.objects.all()

class CompanyCreateView(ListCreateAPIView):

    serializer_class = CompanySerializers
    permission_classes = (IsAuthenticated, )
    queryset = Company.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def list(self, request):
        queryset = self.queryset.filter(owner=request.user)
        serializer = CompanySerializers(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        company = Company.objects.filter(owner=request.user)[0:]
        if company:
            return Response({"msg": "only one obj create!!"})
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            serializer.save(owner=request.user)
            return Response(serializer.data)

class CompanyRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    serializer_class = CompanySerializers
    permission_classes = (IsAuthenticated,)
    queryset = Company.objects.all()

class VehicleListCreateView(ListCreateAPIView):

    serializer_class = VehicleSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Vehicle.objects.all()

class DriverListCreateView(ListCreateAPIView):

    serializer_class = DriversSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Drivers.objects.all()









