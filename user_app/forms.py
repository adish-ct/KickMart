from typing import Any, Optional
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import PasswordChangeForm


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].widget.attrs = {'class': 'form-control'}