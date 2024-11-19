from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from notification.utils import create_notification

from .forms import SignupForm, ProfileForm
from .models import User
from .serializers import UserSerializer

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar()
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user = form.save()
        user.save()
    else:
        message = form.errors.as_json()
    
    print(message)

    return JsonResponse({'message': message}, safe=False)



@api_view(['POST'])
def editprofile(request):
    user = request.user
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'email already exists'})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
        
        serializer = UserSerializer(user)

        return JsonResponse({'message': 'information updated', 'user': serializer.data})
    

@api_view(['POST'])
def editpassword(request):
    user = request.user
    
    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)



