from itertools import chain
from django.contrib import admin
from .models import User, Clothes, SetOfClothes

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'password', 'last_login', 'created_at')

admin.site.register(User, UserAdmin)


class SetOfClothesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_Set_Of_Clothes', 'users')

admin.site.register(SetOfClothes, SetOfClothesAdmin)


class ClothesAdmin(admin.ModelAdmin):
    def id_set_of_clothes(self, obj):
        a = obj.set_Of_Clothes.values_list('id')
        return list(chain.from_iterable(a))
    list_display = ('name_Clothes', 'type_Clothes', 'description', 'id_set_of_clothes')

admin.site.register(Clothes, ClothesAdmin)



# OLD WORKING VERSION

# from itertools import chain
# from django.contrib import admin
# from .models import User, UserClothes
#
#
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'is_active', 'password', 'last_login')
#
#
# admin.site.register(User, UserAdmin)
#
# class UserClothesAdmin(admin.ModelAdmin):
#     def users_names(self, obj):
#         a = obj.users.values_list('username')
#         return list(chain.from_iterable(a))
#     list_display = ('nameClothes', 'typeClothes', 'description', 'users_names')
#
# admin.site.register(UserClothes, UserClothesAdmin)
