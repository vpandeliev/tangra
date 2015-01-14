from django.forms import ModelForm, Textarea, Form, CharField, BooleanField
from models import Study, Note

class StudyForm(ModelForm):
	class Meta:
		model = Study
		fields = ['name', 'description', 'consent', 'instructions', 'eligibility', 'reward']
		widgets = {
            'name': Textarea(attrs={'cols': 80, 'rows': 1}),
            'description': Textarea(attrs={'cols': 80, 'rows': 5}),
            'consent': Textarea(attrs={'cols': 80, 'rows': 5}),
            'instructions': Textarea(attrs={'cols': 80, 'rows': 5}),
            'eligibility': Textarea(attrs={'cols': 80, 'rows': 5}),
            'reward': Textarea(attrs={'cols': 80, 'rows': 5}),
        }

        help_texts = {
            'name': ('Some useful help text.'),
        }

class NoteForm(ModelForm):
    class Meta:
		model = Note
		fields = ['datum', 'attachment', 'email']
		widgets = {
			'datum': Textarea(attrs={'rows': 4}),
    	}

class EmailForm(Form):
    subject = CharField(label='Subject', widget=Textarea(attrs={'cols': 80, 'rows': 1}))
    body = CharField(label='Email body', widget=Textarea(attrs={'cols': 80, 'rows': 8}))
