from django.contrib import admin
from iradioapp import models

# Register your models here.
admin.site.register(models.Song)
admin.site.register(models.Group)
admin.site.register(models.User)
