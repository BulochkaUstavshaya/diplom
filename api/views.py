from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.models import TokenUser # for get user id
from .models import User, Clothes, SetOfClothes
from .serializers import ClothesSerializer

from .utils import existClothes, invalidToken, existCloneSetOfClothes, countclothes, testResponse


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 9 шмоток
class SaveUserClothes(APIView): # замени на put
    def put(self, request):
        try:
            token = AccessToken(request.data[0]["access"])
            token.check_exp()

        except Exception as e:
            return Response(invalidToken)


        if not existClothes(request):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # if existCloneSetOfClothes(request):
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        # get user in token
        user_id = TokenUser(token).id
        user = User.objects.filter(id=user_id).first()


        # create a new set of clothes and associate with a user
        setOfClothes = SetOfClothes.objects.create(users=user, name_Set_Of_Clothes=request.data[1]["nameSetOfClothes"]) #bulk=False

        for i in range(2, len(request.data)):
            # print(str(request.data[i]))
            clothes = Clothes.objects.get_or_create(
                name_Clothes=request.data[i]["nameClothes"],
                type_Clothes=request.data[i]["typeClothes"],
                description=request.data[i]["description"],
                price=request.data[i]["price"],
                link_Image=request.data[i]["linkImage"],
                link_Source=request.data[i]["linkSource"]
            )
            id_clothes = Clothes.objects.get(link_Source=request.data[i]["linkSource"]).id
            setOfClothes.clothes_set.add(id_clothes)

        return Response({
                "nameSetOfClothes": setOfClothes.name_Set_Of_Clothes
            })

        # return Response({
        #     "setOfClothes": setOfClothes.id
        # })

# рабочая штука
# 9 шмоток
# class SaveUserClothes(APIView): # замени на put
#     def post(self, request):
#         try:
#             token = AccessToken(request.data[0]["access"])
#             token.check_exp()
#
#         except Exception as e:
#             return Response(invalidToken)
#
#
#         if not existClothes(request):
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         # if existCloneSetOfClothes(request):
#         #     return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         listClothes = request.data
#         listClothes.pop()
#
#         # get user in token
#         user_id = TokenUser(token).id
#         user = User.objects.filter(id=user_id).first()
#
#         # create a new set of clothes and associate with a user
#         setOfClothes = SetOfClothes.objects.create(users=user) #bulk=False
#
#         for i in range(1, len(request.data)):
#             clothes = Clothes.objects.get_or_create(
#                 name_Clothes=request.data[i]["nameClothes"],
#                 type_Clothes=request.data[i]["typeClothes"],
#                 description=request.data[i]["description"],
#                 price=request.data[i]["price"],
#                 link_Image=request.data[i]["linkImage"],
#                 link_Source=request.data[i]["linkSource"]
#             )
#             id_clothes = Clothes.objects.get(link_Source=request.data[i]["linkSource"]).id
#             setOfClothes.clothes_set.add(id_clothes)
#
#         return Response({
#             "setOfClothes": setOfClothes.id
#         })
###################

class DeleteUserClothes(APIView): # замени на delete
    def delete(self, request):
        try:
            token = AccessToken(request.data["access"])
            token.check_exp()

        except Exception as e:
            return Response(invalidToken)

        # get set of clothes
        setOfClothes = SetOfClothes.objects.filter(name_Set_Of_Clothes=request.data["nameSetOfClothes"]).first()

        if setOfClothes is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # user_id = TokenUser(token).id
        # user = User.objects.filter(id=user_id).first()

        SetOfClothes.objects.filter(name_Set_Of_Clothes=request.data["nameSetOfClothes"]).delete()

        # Допили удаление
        # return Response(status=status.HTTP_205_RESET_CONTENT)
        return Response({
            "status": "successful"
        })


# рабочее удаление
# class DeleteUserClothes(APIView): # замени на delete
#     def post(self, request):
#         try:
#             token = AccessToken(request.data["access"])
#             token.check_exp()
#
#         except Exception as e:
#             return Response(invalidToken)
#
#         # get set of clothes
#         setOfClothes = SetOfClothes.objects.filter(id=request.data["setOfClothes"]).first()
#
#         if setOfClothes is None:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         # user_id = TokenUser(token).id
#         # user = User.objects.filter(id=user_id).first()
#
#         SetOfClothes.objects.filter(id=request.data["setOfClothes"]).delete()
#
#         # Допили удаление
#         return Response(status=status.HTTP_205_RESET_CONTENT)
#################

class GetUserClothes(APIView):  # замени на гет
    def post(self, request):
        try:
            token = AccessToken(request.data["access"])
            token.check_exp()

        except Exception as e:
            return Response(invalidToken)

        user_id = TokenUser(token).id
        user = User.objects.filter(id=user_id).first()

        setOfClothes = SetOfClothes.objects.all().filter(users=user)

        if not setOfClothes:
            return Response({
                "response": "user have not set of clothes"
            })

        listClothes = []
        # print(setOfClothes)
        for i in setOfClothes:
            clothes = Clothes.objects.all().filter(set_Of_Clothes=i.id)

            serializer = ClothesSerializer(clothes, many=True)
            # listClothes.append({
            #     f'set {i.id}': serializer.data
            # })
            listClothes.append({
                f'{i.name_Set_Of_Clothes}': serializer.data
            })

        return Response(listClothes)

# class GetUserClothes(APIView):
#     def post(self, request):

#
#         user_id = TokenUser(token).id
#         user = User.objects.filter(id=user_id).first()
#
#         userclothes = UserClothes.objects.all().filter(users=user)
#
#         serializer = UserClothesSerializer(userclothes, many=True)
#
#         # return Response({"users": serializer.data})
#         return Response(serializer.data)


# class DeleteUserClothes(APIView):
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
#         # get clothes
#         clothes = UserClothes.objects.filter(linkSource=request.data["linkSource"]).first()
#         if clothes is None:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         user_id = TokenUser(token).id
#         user = User.objects.filter(id=user_id).first()
#         user.userclothes_set.remove(clothes)
#
#         # Допили удаление
#         return Response(status=status.HTTP_205_RESET_CONTENT)
#
#
# class GetUserClothes(APIView):
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
#         user_id = TokenUser(token).id
#         user = User.objects.filter(id=user_id).first()
#
#         userclothes = UserClothes.objects.all().filter(users=user)
#
#         serializer = UserClothesSerializer(userclothes, many=True)
#
#         # return Response({"users": serializer.data})
#         return Response(serializer.data)
#
#
# # БЫЛО ИЗНАЧАЛАЛЬНО
# # class SaveUserClothes(APIView):
# #     def post(self, request):
# #         try:
# #             access_token = request.data["access"]
# #             token = AccessToken(access_token)
# #             # check access token
# #             token.check_exp()
# #
# #             # if user have this clothes then BAN
# #             if UserClothes.objects.filter(linkSource=request.data["linkSource"]).first() is None: # вынеси в отдельную переменную
# #                 # insert clothes in db
# #                 # userclothes = UserClothes()
# #                 # userclothes.nameClothes = request.data["nameClothes"]
# #                 # userclothes.typeClothes = request.data["typeClothes"]
# #                 # userclothes.description = request.data["description"]
# #                 # userclothes.price = request.data["price"]
# #                 # userclothes.linkImage = request.data["linkImage"]
# #                 # userclothes.linkSource = request.data["linkSource"]
# #                 # userclothes.save()
# #                 userclothes = UserClothes.objects.create(nameClothes=request.data["nameClothes"],
# #                                                          typeClothes=request.data["typeClothes"],
# #                                                          description=request.data["description"],
# #                                                          price=request.data["price"],
# #                                                          linkImage=request.data["linkImage"],
# #                                                          linkSource=request.data["linkSource"]
# #                                                          )
# #             else:
# #                 userclothes = UserClothes.objects.filter(linkSource=request.data["linkSource"]).first()
# #
# #             user_id = TokenUser(token).id
# #             user = User.objects.filter(id=user_id).first()
# #             user.userclothes_set.add(userclothes)
# #
# #             return Response(status=status.HTTP_201_CREATED)
# #
# #         except Exception as e:
# #             # return Response({
# #             #     "detail": "Token is invalid or expired",
# #             #     "code": "token_not_valid"
# #             # })
# #             return Response({
# #                 "exeption": str(e)
# #             })
#
# class SaveUserClothes(APIView):
#     def post(self, request):
#         try:
#             access_token = request.data["access"]
#             token = AccessToken(access_token)
#             # check access token
#             token.check_exp()
#         except Exception as e:
#             return Response({
#                 "exeption_token": str(e)
#             })
#
#         try:
#             # if user have this clothes then BAN
#             userclothes = UserClothes.objects.filter(linkSource=request.data["linkSource"]).first()
#         except Exception as e:
#             return Response({
#                 "exeption_get_clothes": str(e)
#             })
#
#         try:
#             if userclothes is None: # вынеси в отдельную переменную
#                 try:
#                     userclothes = UserClothes.objects.get_or_create(nameClothes=request.data["nameClothes"],
#                                                                     typeClothes=request.data["typeClothes"],
#                                                                     description=request.data["description"],
#                                                                     price=request.data["price"],
#                                                                     linkImage=request.data["linkImage"],
#                                                                     linkSource=request.data["linkSource"]
#                                                                     )
#                 #     userclothes = UserClothes()
#                 #     userclothes.nameClothes = request.data["nameClothes"]
#                 #     userclothes.typeClothes = request.data["typeClothes"]
#                 #     userclothes.description = request.data["description"]
#                 #     userclothes.price = request.data["price"]
#                 #     userclothes.linkImage = request.data["linkImage"]
#                 #     userclothes.linkSource = request.data["linkSource"]
#                 except Exception as e:
#
#                     return Response({
#                         "exeption_to_create_clothes": repr(e)
#                     })
#
#                 # try:
#                 #     userclothes.save()
#                 # except Exception as e:
#                 #     return Response({
#                 #         "exeption_to_save_clothes": str(e)
#                 #     })
#             else:
#                 userclothes = UserClothes.objects.filter(linkSource=request.data["linkSource"]).first()
#
#             userclothes = UserClothes.objects.filter(linkSource=request.data["linkSource"]).first()
#
#         except Exception as e:
#             return Response({
#                 "exeption_create_clothes": str(e)[0:240]
#             })
#
#         try:
#             user_id = TokenUser(token).id
#             user = User.objects.filter(id=user_id).first()
#         except Exception as e:
#             return Response({
#                 "exeption_filter_user": str(e)
#             })
#
#         try:
#             user.userclothes_set.add(userclothes)
#             return Response(status=status.HTTP_201_CREATED)
#
#         except Exception as e:
#             return Response({
#                 "exeption_add_clothes_for_user": str(e)
#             })

class RequestToMicroservice(APIView):
    def post(self, request):
        return Response(testResponse)
