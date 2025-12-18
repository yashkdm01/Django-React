from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Department
from .serializers import DepartmentSerializer

# Create your views here.
class DepartmentViewSet(viewsets.ModelViewSet):
    """
    provides list, create, retrieve, update and soft-delete  actions for department
    """
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.filter(status=True)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)