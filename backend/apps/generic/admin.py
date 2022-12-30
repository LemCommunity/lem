from django.contrib import admin

from apps.generic.models import Like


class LikeAdmin(admin.ModelAdmin):
    readonly_fields = ("content_object",)


admin.site.register(Like, LikeAdmin)
