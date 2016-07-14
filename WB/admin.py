from django.contrib import admin
from WB.models import *
# Register your models here.
class IndicatorAdmin(admin.ModelAdmin):
	list_display = ['id', 'Description', 'Quality', 'DataSets_Availables', 'PBSB', 'Source', 'ID_WB_Category', 'ID_Indicator_Type', 'ID_Indicator_Country', 'created', 'modified']
	search_fields = ['id', 'created', 'modified', 'Quality', 'PBSB', 'Source', 'ID_WB_Category', 'ID_Indicator_Type', 'ID_Indicator_Country']
admin.site.register(Indicator, IndicatorAdmin)

class WB_CategoryAdmin(admin.ModelAdmin):
	list_display = ['Theme']
	search_fields = ['Theme']
admin.site.register(WB_Category, WB_CategoryAdmin)

class Indicator_TypeAdmin(admin.ModelAdmin):
	list_display = ['Type']
	search_fields = ['Type']
admin.site.register(Indicator_Type, Indicator_TypeAdmin)

class Indicator_CountryAdmin(admin.ModelAdmin):
	list_display = ['Country']
	search_fields = ['Country']
admin.site.register(Indicator_Country, Indicator_CountryAdmin)

class Indicator_CommentsAdmin(admin.ModelAdmin):
	list_display = ['id', 'Comment', 'ID_Indicator']
	search_fields = ['Comment']
admin.site.register(Indicator_Comments, Indicator_CommentsAdmin)

class Indicator_NotesAdmin(admin.ModelAdmin):
	list_display = ['id', 'Note', 'ID_Indicator']
	search_fields = ['Note']
admin.site.register(Indicator_Notes, Indicator_NotesAdmin)