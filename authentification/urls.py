from django.urls import path,include
from . import views
from .views import  *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'recon.*',ReconViewSet,basename='recon')
router.register(r'user.*',UserData,basename='user')
router.register(r"vuln.*",VulnScanViewSet,basename='vuln')
urlpatterns = [
     path('home/', views.HomeView.as_view(), name ='home'),
     path('logout/', views.LogoutView.as_view(), name ='logout'),
     path('user/create/', CustomUserCreate.as_view(), name="create_user"),
     path('',include(router.urls))
]

