from django.contrib import admin

# Register your models here.

from tweets.models import Post, Vote

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('date_posted',)

admin.site.register(Post, PostAdmin)
admin.site.register(Vote)
