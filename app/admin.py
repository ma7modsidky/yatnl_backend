from django.contrib import admin
from .models import Leader
# Register your models here.


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ['main_account', 'leader_type',
                    'parent', 'children_count', 'is_eligible', 'created']
    class Meta:
        model = Leader
        
        fields = '__all__'
