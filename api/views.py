from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.models import TokenUser # for get user id
from .models import User, UserClothes
from .serializers import UserClothesSerializer
from .utils import ExistClothes

class LogoutView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            # return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "exeption": str(e)
            })

# class SaveUserClothes(APIView):
#     def post(self, request):
#         try:
#             access_token = request.data["access"]
#             token = AccessToken(access_token)
#             # check access token
#             token.check_exp()
#         except Exception as e:
#             return Response({
#                 "detail": "Token is invalid or expired",
#                 "code": "token_not_valid"
#             })
#
#         if not ExistClothes(request):
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         clothes = UserClothes.objects.filter(linkSource=request.data["linkSource"]).first()
#         # if user have this clothes then BAN
#         if clothes is None:  # вынеси в отдельную переменную
#             # insert clothes in db
#             clothes.nameClothes = request.data["nameClothes"]
#             clothes.typeClothes = request.data["typeClothes"]
#             clothes.description = request.data["description"]
#             clothes.price = request.data["price"]
#             clothes.linkImage = request.data["linkImage"]
#             clothes.linkSource = request.data["linkSource"]
#             clothes.save()
#
#         user_id = TokenUser(token).id
#         user = User.objects.filter(id=user_id).first()
#         user.userclothes_set.add(clothes)
#
#         return Response(status=status.HTTP_201_CREATED)


class DeleteUserClothes(APIView):
    def post(self, request):
        try:
            access_token = request.data["access"]
            token = AccessToken(access_token)
            # check access token
            token.check_exp()
        except Exception as e:
            return Response({
                "detail": "Token is invalid or expired",
                "code": "token_not_valid"
            })

        # get clothes
        clothes = UserClothes.objects.filter(linkSource=request.data["linkSource"]).first()
        if clothes is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_id = TokenUser(token).id
        user = User.objects.filter(id=user_id).first()
        user.userclothes_set.remove(clothes)

        # Допили удаление
        return Response(status=status.HTTP_205_RESET_CONTENT)


class GetUserClothes(APIView):
    def post(self, request):
        try:
            access_token = request.data["access"]
            token = AccessToken(access_token)
            # check access token
            token.check_exp()
        except Exception as e:
            return Response({
                "detail": "Token is invalid or expired",
                "code": "token_not_valid"
            })

        user_id = TokenUser(token).id
        user = User.objects.filter(id=user_id).first()

        userclothes = UserClothes.objects.all().filter(users=user)

        serializer = UserClothesSerializer(userclothes, many=True)

        # return Response({"users": serializer.data})
        return Response(serializer.data)

class SaveUserClothes(APIView):
    def post(self, request):
        try:
            access_token = request.data["access"]
            token = AccessToken(access_token)
            # check access token
            token.check_exp()

            # if user have this clothes then BAN
            if UserClothes.objects.filter(linkSource=request.data["linkSource"]).first() is None: # вынеси в отдельную переменную
                # insert clothes in db
                userclothes = UserClothes()
                userclothes.nameClothes = request.data["nameClothes"]
                userclothes.typeClothes = request.data["typeClothes"]
                userclothes.description = request.data["description"]
                userclothes.price = request.data["price"]
                userclothes.linkImage = request.data["linkImage"]
                userclothes.linkSource = request.data["linkSource"]
                userclothes.save()
            else:
                userclothes = UserClothes.objects.filter(linkSource=request.data["linkSource"]).first()

            user_id = TokenUser(token).id
            user = User.objects.filter(id=user_id).first()
            user.userclothes_set.add(userclothes)

            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "detail": "Token is invalid or expired",
                "code": "token_not_valid"
            })

