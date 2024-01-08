from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *
from .models import *
# Create your views here.


class User_Login_And_SignUp_Viewset(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def list(self, request):
        return Response({'status': 400, 'message': "error"}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request):
        return Response({'status': 400, 'message': "error"}, status=status.HTTP_400_BAD_REQUEST)
    
    def retreive(self, request):
        return Response({'status': 400, 'message': "error"}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request):
        return Response({'status': 400, 'message': "error"}, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request):
        return Response({'status': 400, 'message': "error"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        return Response({'status': 400, 'message': "error"}, status=status.HTTP_400_BAD_REQUEST)
    
    

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny], authentication_classes=[])
    def login(self, request):
        try:
            if str(request.user != 'AnonymousUser' or request.auth is not None):
                return Response({
                    'status': 400,
                    'error': "user already logged in"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            username_and_password = request.data

            serialize = LoginSerializer(data=username_and_password)

            if serialize.is_valid():
                user = authenticate(request=request, username=serialize.validated_data.get('user_username'), 
                                    password=serialize.validated_data.get('user_password'))
                
                if not user or user is None:
                    return Response({
                        'status': 401,
                        'error': "Invalid credentials entered",
                    }, status=status.HTTP_401_UNAUTHORIZED)
                
                user_refresh_token = RefreshToken.for_user(user=user)

                return Response({
                    'status': 200,
                    'message': "User logged in successfully",
                    'refresh token': str(user_refresh_token),
                    'access token': str(user_refresh_token.access_token)
                }, status=status.HTTP_200_OK)
            
            return Response({
                'status': 400,
                'error': "Invalid data",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
        
        return Response({
            'status': 400,
            'error': "Something Went Wrong",
        }, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny], authentication_classes=[])
    def signup(self, request):
        try:
            print("i am in signup func")
            data = request.data
            print(data)

            serialize = SignUpSerializer(data=data)

            if serialize.is_valid():
                user_obj = serialize.save()

                token = RefreshToken.for_user(user = user_obj)

                return Response({
                    'status': 201,
                    'message': "User Signup Successful",
                    'user details': serialize.data,
                    'Refresh token': str(token),
                    'Access token': str(token.access_token)
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'status': 400,
                'message': "User sign up failed",
                'error': serialize.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
        
        return Response({
            'status': 400,
            'message': "Something Went Wrong",
        }, status=status.HTTP_400_BAD_REQUEST)



class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def list(self, request):
        try:
            queryset = Notes.objects.filter(user=request.user.id)
            serialze = NotesSerializer(queryset, many=True)

            if serialze.is_valid():
                return Response({
                    'status': 200,
                    'message': "Notes fetched",
                    'data': serialze.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'status': 400,
                'error': "error in fetching data"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(e)
        
        return Response({
            'status': 400,
            'error': "something went wrong"
        }, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request):
        try:
            super().retrieve(request=request, **request.data)

        except Exception as e:
            print(e)

        return Response({
            'status': 400,
            'error': "something went wrong"
        }, status=status.HTTP_400_BAD_REQUEST)
    

    def create(self, request):
        try:
            user_id = request.user.id
            data = request.data

            data['user'] = user_id

            serialize = NotesSerializer(data=data)

            if serialize.is_valid():                
                serialize.save()

                return Response({
                    'status': 201,
                    'message': "New Note is Created Successfully",
                    'data': serialize.data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'status': 400,
                'error': "Error occured",
                'data': serialize.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
        
        return Response({
            'status': 400,
            'message': "something went wrong"
        }, status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, id):
        try:
            data = request.data
            instance = Notes.objects.filter(id = str(id), user = request.user.id)

            if instance.count() == 0:
                return Response({
                    'status': 400,
                    'message': "No such notes found"
                }, status=status.HTTP_400_BAD_REQUEST)
            

            serialize = NotesSerializer(instance=instance, data=data)

            if serialize.is_valid():
                serialize.save()

                return Response({
                    'status': 200,
                    'message': "Notes updated successfully"
                }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
        
        return Response({
            'status': 400,
            'message': "Something went wrong",
        }, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, id):
        try:
            note_obj = Notes.objects.filter(id = str(id), user = request.user.id)

            if note_obj.count() == 0:
                return Response({
                    'status': 404,
                    'message': "No Notes found"
                }, status=status.HTTP_404_NOT_FOUND)
            
            note_obj.delete()

            return Response({
                'status': 200,
                'message': "Note deleted successfully"
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
        
        return Response({
            'status': 400,
            'message': "Something went wrong"
        }, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=False, methods=['GET'])
    def search(self, request):
        try:
            search_query = str(request.query_params.get('q'))

            if len(search_query) > 50:
                return Response({
                    'status': 404,
                    'message': "Searched note not found"
                }, status=status.HTTP_404_NOT_FOUND)
            
            Notes.objects.filter(notes_title=search_query, notes_desc=search_query)
            

        except Exception as e:
            print(e)
        
        return Response({
            'status': 400,
            'message': "Something went wrong"
        }, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=True, methods=['POST'])
    def share(self, request, id):
        try:
            user = request.user.id
            id = id

            data = request.data

            whoom_to_share = data.get('share_to')

            Notes_Shared.objects.create(notes_id = str(id), share_to = whoom_to_share, share_from = user)

            return Response({
                'status': 200,
                'message': "Note shared to user",
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
        
        return Response({
            'status': 400,
            'error': "Something went wrong"
        }, status=status.HTTP_400_BAD_REQUEST)
    
