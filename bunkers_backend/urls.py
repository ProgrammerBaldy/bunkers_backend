from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from . views import TestConn

urlpatterns = [
    path('api-token/', TokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    path('admin/', admin.site.urls),
    path('testconn/', TestConn.as_view(), name="testconn_view"),
    path('',include('supplies_control.urls'))
]
