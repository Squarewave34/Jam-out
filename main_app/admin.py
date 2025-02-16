from django.contrib import admin
from .models import Game_jam, Role, Dev_log, Thread, Comment, Participant

admin.site.register(Game_jam)
admin.site.register(Role)
admin.site.register(Dev_log)
admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(Participant)