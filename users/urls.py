from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views


router = DefaultRouter()
router.register('list',views.UsersViewSet)

urlpatterns = [
   path('',include(router.urls)),
   path('register/',views.UserRegistrationAPIView.as_view(),name='register'),
   path('active/<uid64>/<token>/', views.activate, name='activate'),
   path('login/',views.UserLoginView.as_view(), name='login'),
   path('logout/',views.UserLogoutView.as_view(), name='logout'),
   path('changepassword/',views.ChangePasswordView.as_view(), name='changepassword')
]
