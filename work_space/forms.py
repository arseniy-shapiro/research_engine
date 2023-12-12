from django import forms
from .models import WorkSpace
from user_management.models import User


CONFIRMATION = (("Yes", "Yes"), ("No", "No"),)

SOURCES_RECEIVING_OPTIONS = (("copy", "Create New Work Space"), ("download", "Download sources"),)


class NewSpaceForm(forms.Form):
    title = forms.CharField(max_length=50)

    def save_work_space(self, user: User):
        """Sace new WorkSpace object"""
        new_work_space = WorkSpace(owner=user, title=self.cleaned_data["title"])
        new_work_space.save()
        return new_work_space


class RenameSpaceForm(forms.Form):
    new_title = forms.CharField(max_length=50)

    def set_initial(self, space: WorkSpace):
        self.fields["new_title"].initial = space.title
        return self
    

    def save_new_title(self, space: WorkSpace):
        space.title = self.cleaned_data["new_title"]
        return space.save(update_fields=("title",))
    

class DeleteSpaceForm(forms.Form):
    confirm = forms.ChoiceField(choices=CONFIRMATION)


class ReceiveCodeForm(forms.Form):
    code = forms.CharField(max_length=15)


class ReceiveSourcesForm(forms.Form):
    code = forms.CharField(max_length=15)
    option = forms.ChoiceField(choices=SOURCES_RECEIVING_OPTIONS)
