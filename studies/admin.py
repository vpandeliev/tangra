from django.contrib import admin
from suit.admin import SortableTabularInline
from django.forms import CheckboxSelectMultiple
from studies.models import *
from custom_auth.models import User

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
				'fields': ['name', 'api_name', 'description', 'consent',
				'instructions', 'eligibility', 'reward', 'start_date',
				'end_date', 'investigators',]
			}),
	]
	filter_horizontal = ('investigators',)
	list_display = ('name', 'description')
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

	def save_model(self, request, obj, form, change):
		for group_stage in GroupStage.objects.filter(group=obj):
			for participant in group_stage.group.users.all():
				UserStage.objects.create(user=participant, group_stage=group_stage)
		obj.save()

class UserStageAdmin(admin.ModelAdmin):
	list_display = ('user', 'group_stage', 'status')

admin.site.register(Study, StudyAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(UserStage, UserStageAdmin)
admin.site.register(Data)
