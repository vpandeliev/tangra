from django.contrib import admin
from suit.admin import SortableTabularInline
from django.forms import CheckboxSelectMultiple
from studies.models import *

class GroupStageInline(SortableTabularInline):
	model = GroupStage
	extra = 1
	sortable = 'order'
	suit_classes = 'suit-tab suit-tab-stages'

class StageInline(admin.StackedInline):
	model = Stage
	extra = 1
	suit_classes = 'suit-tab suit-tab-stages'

class StudyAdmin(admin.ModelAdmin):
	inlines = [StageInline]
	fieldsets = [
		(None, {
				'classes': ('suit-tab suit-tab-general',),
				'fields': ['name', 'description', 'consent', 
				'instructions', 'eligibility', 'reward', 'start_date', 
				'end_date', 'started', 'investigators',]
			}),
	]
	filter_horizontal = ('investigators',)
	list_display = ('name', 'description', 'started')
	suit_form_tabs = (('general', 'General'), ('stages', 'Stages'))

class GroupAdmin(admin.ModelAdmin):
	inlines = [GroupStageInline]
	fieldsets = [
		(None, {
				'classes': ('suit-tab suit-tab-general',),
				'fields': ['study', 'name', 'users',]
			}),
	]
	filter_horizontal = ("users",)
	list_display = ('name', 'study')
	suit_form_tabs = (('general', 'Manage Users'), ('stages', 'Stages'))

class UserStageAdmin(admin.ModelAdmin):
	list_display = ('user', 'group_stage', 'status')

admin.site.register(Study, StudyAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(UserStage, UserStageAdmin)
admin.site.register(Data)