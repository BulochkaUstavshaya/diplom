from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    LogoutView,
    SaveUserClothes,
    DeleteUserClothes,
    GetUserClothes,
    RequestToMicroservice
)


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('save/', SaveUserClothes.as_view(), name='save_clothes'),
    path('delete/', DeleteUserClothes.as_view(), name='delete_clothes'),
    path('get/', GetUserClothes.as_view(), name='get_clothes'),
    path('filters/', RequestToMicroservice.as_view(), name='filters_clothes'),
]
