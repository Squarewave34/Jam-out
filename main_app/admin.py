from django.contrib import admin
from .models import Game_jam, Roles, Dev_logs, Thread, Comments

admin.site.register(Game_jam)
admin.site.register(Roles)
admin.site.register(Dev_logs)
admin.site.register(Thread)
admin.site.register(Comments)
