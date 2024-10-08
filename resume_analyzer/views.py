from .models import Resume
from rest_framework import generics
from .serializers import ResumeSerializer

# Create your views here.

class ResumeView(generics.CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
