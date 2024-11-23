
from .serializers import MyUserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import MyUser


class RegisterUserViewset(viewsets.ModelViewSet):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    
    def get_queryset(self):
        return MyUser.objects.none()
    
    
    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail": "Vous êtes déjà connecté."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Crée l'utilisateur en utilisant les données validées
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    