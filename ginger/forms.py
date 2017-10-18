# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

class GingerKeyForm(forms.Form):
    # login = forms.ChoiceField(help_text="Choisir une asso.")
    login = forms.CharField(help_text="Choisir une asso.")
    description = forms.CharField(help_text="Justification courte de l'utilisation de la clé.", widget=forms.TextInput(attrs={'placeholder': "Justification courte de l\'utilisation de la cle"}))
    users_add = forms.BooleanField(help_text="TODO.", label="users_add", initial=False, required=False)
    users_delete = forms.BooleanField(help_text="TODO.", label="users_delete", initial=False, required=False)
    users_edit = forms.BooleanField(help_text="TODO.", label="users_edit", initial=False, required=False)
    users_badge = forms.BooleanField(help_text="TODO.", label="users_badge", initial=False, required=False)
    contributions_add = forms.BooleanField(help_text="TODO.", label="contributions_add", initial=False, required=False)
    contributions_delete = forms.BooleanField(help_text="TODO.", label="contributions_delete", initial=False, required=False)
    contributions_read = forms.BooleanField(help_text="TODO.", label="contributions_read", initial=False, required=False)
    stats_read = forms.BooleanField(help_text="TODO.", label="stats_read", initial=False, required=False)
    settings_read = forms.BooleanField(help_text="TODO.", label="settings_read", initial=False, required=False)
    keys_all = forms.BooleanField(help_text="TODO.", label="keys_al", initial=False, required=False)

    def clean_login(self):
        data = self.cleaned_data['login']

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

        #TODO: Check description length
        if len(data) > 100:
            raise ValidationError("La description est trop longue !")

        if len(data) == 0:
            raise ValidationError("Il faut fournir une description !")

        return data

    def clean_users_add(self):
        data = self.cleaned_data['users_add']

        return data

    def clean_users_delete(self):
        data = self.cleaned_data['users_delete']

        return data

    def clean_users_edit(self):
        data = self.cleaned_data['users_edit']

        return data

    def clean_users_badge(self):
        data = self.cleaned_data['users_badge']

        return data

    def clean_contributions_add(self):
        data = self.cleaned_data['contributions_add']

        return data

    def clean_contributions_delete(self):
        data = self.cleaned_data['contributions_delete']

        return data

    def clean_contributions_read(self):
        data = self.cleaned_data['contributions_read']

        return data

    def clean_stats_read(self):
        data = self.cleaned_data['stats_read']

        return data

    def clean_settings_read(self):
        data = self.cleaned_data['settings_read']

        return data

    def clean_keys_all(self):
        data = self.cleaned_data['keys_all']

        return data

    def as_materialize(self):
        formStr = ""
        for boundfield in self:
            if isinstance(boundfield.field, forms.BooleanField):
                formStr += "<p>\n"
            else:
                formStr += "<div class='row'>\n    <div class='input-field col s12'>\n"
            formStr += str(boundfield.errors) + "\n"
            formStr += str(boundfield) + "\n"
            formStr += "        %s\n" % boundfield.label_tag(label_suffix="")
            if isinstance(boundfield.field, forms.BooleanField):
                formStr += "</p>\n"
            else:
                formStr += "    </div>\n</div>\n"
        return formStr