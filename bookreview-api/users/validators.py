from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class MustContainBValidator:
    def validate(self, password, user=None):
        if "B" not in password:
            raise ValidationError(
                _("This password must contain the letter 'B'."),
                code="password_no_b",
            )

    def get_help_text(self):
        return _("Your password must contain the letter 'B'.")
