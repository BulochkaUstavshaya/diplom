from itertools import chain
from django.contrib import admin
from .models import User, UserClothes


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'password', 'last_login')


admin.site.register(User, UserAdmin)

class UserClothesAdmin(admin.ModelAdmin):
    def users_names(self, obj):
        a = obj.users.values_list('username')
        return list(chain.from_iterable(a))
    list_display = ('nameClothes', 'typeClothes', 'description', 'users_names')

admin.site.register(UserClothes, UserClothesAdmin)
