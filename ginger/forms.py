# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

class GingerKeyForm(forms.Form):
    # Possible organizations, tuple of pairs (login, human_readable_name)
    organizations = ()

    login = forms.ChoiceField(label='Sélectionner une asso')
    description = forms.CharField(help_text="Justification courte de l'utilisation de la clé.", widget=forms.TextInput(attrs={'placeholder': "Justification courte de l\'utilisation de la cle"}))
    users_add = forms.BooleanField(label="users_add", initial=False, required=False)
    users_delete = forms.BooleanField(label="users_delete", initial=False, required=False)
    users_edit = forms.BooleanField(label="users_edit", initial=False, required=False)
    users_badge = forms.BooleanField(label="users_badge", initial=False, required=False)
    contributions_add = forms.BooleanField(label="contributions_add", initial=False, required=False)
    contributions_delete = forms.BooleanField(label="contributions_delete", initial=False, required=False)
    contributions_read = forms.BooleanField(label="contributions_read", initial=False, required=False)
    stats_read = forms.BooleanField(label="stats_read", initial=False, required=False)
    settings_read = forms.BooleanField(label="settings_read", initial=False, required=False)
    keys_all = forms.BooleanField(label="keys_all", initial=False, required=False)

    def __init__(self, organizations, *args, **kwargs):
            super(forms.Form, self).__init__(*args, **kwargs)
            self.organizations = organizations
            help_text = self.fields['login'].help_text
            # print(self.organizations)
            self.fields['login'].choices = self.organizations

    def clean_login(self):
        data = self.cleaned_data['login']

        # Get only organizations logins
        organizations_login = [item[0] for item in self.organizations]

        if data not in organizations_login:
            raise ValidationError("Tu dois avoir les droits sur cette asso !")

        return data

    def clean_description(self):
        data = self.cleaned_data['description']

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
                formStr += unicode(boundfield.errors) + "\n"
                formStr += unicode(boundfield) + "\n"
                formStr += "        %s\n" % boundfield.label_tag(label_suffix="")
                formStr += "</p>\n"
            elif isinstance(boundfield.field, forms.ChoiceField):
                formStr += "<div class='row'>\n    <div class='input-field col s12'>\n"
                formStr += "        %s\n" % boundfield.label_tag(label_suffix="")
                formStr += unicode(boundfield) + "\n"
                formStr += unicode(boundfield.errors) + "\n"
                formStr += "    </div>\n</div>\n"
            else:
                formStr += "<div class='row'>\n    <div class='input-field col s12'>\n"
                formStr += unicode(boundfield.errors) + "\n"
                formStr += unicode(boundfield) + "\n"
                formStr += "        %s\n" % boundfield.label_tag(label_suffix="")
                formStr += "    </div>\n</div>\n"
        return formStr

    