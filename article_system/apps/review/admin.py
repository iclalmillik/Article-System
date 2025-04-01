from django.contrib import admin
from .models import Referee ,Review 

admin.site.register(Referee)  



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('article', 'referee', 'review_status', 'reviewed_at')
    list_filter = ('review_status',)
    search_fields = ('article__title', 'referee__username')
