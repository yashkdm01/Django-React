from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from departments.views import DepartmentViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
    path('', RedirectView.as_view(url = '/api/departments/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
