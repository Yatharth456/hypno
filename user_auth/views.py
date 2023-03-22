from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, UserSerializer
from .models import User
from django.conf import settings
from django.core.mail import send_mail
from config import Config
from django.contrib.auth.hashers import make_password, check_password
from random_word import RandomWords
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import base64, ast
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser





class Register(APIView):
    def post(self, request):
        # Get the request data and create a random password and username
        data = request.data
        r = RandomWords()
        password = r.get_random_word()
        email = data['email']
        username = r.get_random_word()

        # Check if the email already exists in the User model
        if User.objects.filter(email=email).exists():
            return Response({'msg': 'This email already exists in the system.'}, status=status.HTTP_400_BAD_REQUEST)

        # Hash the password using Django's make_password function with the salt from the app config
        hashed_password = make_password(password, salt=Config.SALT)

        # Update the request data with the new username and hashed password
        data['username'] = username
        data['password'] = hashed_password

        # Create a dictionary of the user credentials for encoding
        cred = {'username': username, 'password': data['password'], 'email': email}

        # Encode the credentials dictionary using base64 encoding
        encode = str(cred).encode('UTF-8')
        encoded = base64.b64encode(encode)

        # Set up the email to be sent to the user with a verification link
        subject = 'Welcome to my site.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        context = {
            'email': email, 
            'verification_link': f'http://{Config.IP}/auth/confirm/?data={str(encoded, "UTF-8")}',
            'username': username, 
            'password': password
        }
        # Render the email template with the context variables
        html_content = render_to_string('auth/email.html', context=context)

        # Create and send the email using Django's EmailMultiAlternatives class
        msg = EmailMultiAlternatives(
            subject=subject,
            body="This is body",
            from_email=email_from,
            to=recipient_list
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # Return a response indicating that the user has been registered temporarily and needs to verify their email
        message = f'Click here for verify'
        return Response({"msg": "User register temporarily. Please check your email and click on link for verification."})





class UserVerification(APIView):
    def get(self, request):
        # Get encrypted user data from query parameter
        params = request.GET.get('data')
        if not params:
            return Response({"error": "Missing data parameter."}, status=status.HTTP_400_BAD_REQUEST)

        # Decode and deserialize user data
        try:
            decrypted_data = base64.b64decode(params).decode('UTF-8')
            dict_data = ast.literal_eval(decrypted_data)
        except (TypeError, ValueError, SyntaxError):
            return Response({"error": "Invalid data parameter."}, status=status.HTTP_400_BAD_REQUEST)

        # Create user and save to database
        serializer = RegisterUserSerializer(data=dict_data)
        if serializer.is_valid():
            user = serializer.save()

            # Create token for user and save to database
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user=user)

            return Response({"msg": "User data saved in database.", "token": token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from rest_framework import status

class Login(APIView):
    def post(self, request):
        # Get the data from the request object
        data = request.data
        # Check if the username and password are not None
        if data['username'] and data['password'] is not None:
            try:
                # Retrieve the user object for the given username
                user = User.objects.get(username=data['username'])
                # Check if the user is active
                if user.is_active:
                    # Check if the password is correct
                    checkpswd = check_password(data['password'], user.password)
                    # If the password is correct, create a token for the user and return the user information and token as response
                    if checkpswd:
                        token, created = Token.objects.get_or_create(user=user)
                        serializer = UserSerializer(user)
                        return Response({'user': serializer.data, 'token': token.key})
                    else:
                        # Return an error message if the user account is disabled
                        return Response({"msg":"please check your password"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    # Return an error message if the user account is disabled
                    return Response({"msg":"Your account is disabled."}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                # Return an error message if the user does not exist
                return Response({"msg": "Please provide valid username and password."}, status=status.HTTP_401_UNAUTHORIZED)
            except:
                # Return an error message for any other exception
                return Response({"msg": "Something went wrong. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Return an error message if the username and password are not provided
            return Response({"msg": "Please provide your username and password."}, status=status.HTTP_400_BAD_REQUEST)




class UpdatePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        user = request.user

        if not new_password:
            return Response({'message': 'New password is required.'}, status=400)

        if not current_password:
            return Response({'message': 'current_password is required.'}, status=400)

        if user.check_password(current_password):
            user.password = make_password(new_password)
            user.save()
            return Response({'message': 'Password updated successfully.'})
        else:
            return Response({'message': 'Current password is incorrect.'}, status=400)







class UserAdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        if not email:
            return Response({'email': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not username:
            return Response({'username': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'password': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        password = make_password(password)
        serializer = RegisterUserSerializer(data={'email': email, 'username': username, 'password': password})
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = RegisterUserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({"msg": "User deleted."}, status=status.HTTP_204_NO_CONTENT)
