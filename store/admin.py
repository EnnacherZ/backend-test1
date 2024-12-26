from django.contrib import admin
from store.models import *
from django.utils.html import mark_safe
# Register your models here.

admin.site.register(ShoeDetail)
admin.site.register(Sandal)
admin.site.register(SandalDetail)
admin.site.register(Shirt)
admin.site.register(ShirtDetail)
admin.site.register(Pant)
admin.site.register(PantDetail)
admin.site.register(Client)
admin.site.register(ProductOrdered)
class ShoeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_thumbnail')  # Affiche le nom, prix et une miniature de l'image
    search_fields = ('name',)  # Recherche par nom
    list_filter = ('price',)  # Filtrage par prix

    def image_thumbnail(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')  # Génère une miniature
        return None
    image_thumbnail.short_description = 'Image'

admin.site.register(Shoe, ShoeAdmin)