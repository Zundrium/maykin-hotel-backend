from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import City, Hotel, CustomUser

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'zone')
    list_filter = ('zone',)  # optioneel: laat city weg, want managers mogen alleen hun eigen stad zien
    search_fields = ('name', 'zone')

    def get_queryset(self, request):
        """Beperk de zichtbare hotels tot de stad van de ingelogde manager"""
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser:
            return qs
        return qs.filter(city=user.city)  # gebruik city van CustomUser

    def has_change_permission(self, request, obj=None):
        """Sta wijzigen alleen toe binnen eigen stad"""
        if obj is None:
            return True
        return request.user.is_superuser or obj.city == request.user.city

    def has_delete_permission(self, request, obj=None):
        """Sta verwijderen alleen toe binnen eigen stad"""
        if obj is None:
            return True
        return request.user.is_superuser or obj.city == request.user.city

    def save_model(self, request, obj, form, change):
        """Nieuwe hotels automatisch koppelen aan de stad van de manager"""
        if not change:
            obj.city = request.user.city
        super().save_model(request, obj, form, change)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('city',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('city',)}),
    )