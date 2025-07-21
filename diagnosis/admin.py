from django.contrib import admin
from .models import DiagnosisHistory

@admin.register(DiagnosisHistory)
class DiagnosisHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'symptoms', 'prediction', 'created_at')
    search_fields = ('user__email', 'symptoms', 'prediction')
    list_filter = ('created_at',)
