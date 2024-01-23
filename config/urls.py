
from django.contrib import admin
from django.urls import path
from follow.views import *
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView,SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('signup-user/', UserRegister.as_view()),
    path('user-check-code-after-register/', UserCodeView.as_view()),
    
    path('api/', SpectacularAPIView.as_view(), name="schema"),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),    
    path('user-login/', TokenObtainPairView.as_view()),
    path('user-refresh-token/', TokenRefreshView.as_view()),

    path('user-send-code/', UserSendCodeView.as_view()),
    path('user-check-code/', CheckCodeView.as_view()),
    path('user-chage-password/', UserRessetPasswordView.as_view())

    
]
