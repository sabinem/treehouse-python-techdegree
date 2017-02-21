"""
must not be the same as the current password
"""
import string
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class IncludesNumericCharacterValidator(object):
    """
    minimum password length of 14 characters.
    """
    def validate(self, password, user=None):
        """
        must include of one or more numerical digits
        """
        numeric_letters = [l for l in list(password) if l.isdigit() == True]
        if len(numeric_letters) < 1:
            raise ValidationError(
                _("The password includes no numerical digits"),
                code='password_no_numeric_digits',
            )

    def get_help_text(self):
        return _(
            "include of one or more numerical digits."
        )


class UpperAndLowerCaseValidator(object):
    """
    must use of both uppercase and lowercase letters
    """
    def validate(self, password, user=None):
        uppercase_letters = [l for l in list(password) if l.isupper() == True]
        lowercase_letters = [l for l in list(password) if l.islower() == True]
        if len(lowercase_letters) < 1 and len(uppercase_letters) < 1:
            raise ValidationError(
                _("The password includes no uppercase and no lowercase letter"),
                code='password_lower_case_letters',
            )
        if len(lowercase_letters) < 1:
            raise ValidationError(
                _("The password includes no lowercase letter"),
                code='password_lower_case_letters',
            )
        if len(uppercase_letters) < 1:
            raise ValidationError(
                _("The password includes no uppercase letter"),
                code='password_lower_case_letters',
            )


    def get_help_text(self):
        return _(
            "use both uppercase and lowercase letters."
        )


class IncludeSpecialCharacterValidator(object):
    """
    must use of both uppercase and lowercase letters
    """
    def validate(self, password, user=None):
        special_chars = set(string.punctuation.replace("_", ""))
        special_char_letters = [l for l in list(password) if l in special_chars]
        if len(special_char_letters) < 1:
            raise ValidationError(
                _("The password includes no special characters"),
                code='password_special_chars',
            )

    def get_help_text(self):
        return _(
            "include of special characters, such as @, #, $."
        )


class ContainsUserAttributeValidator:
    """
    cannot contain the user name or parts of the user’s full name, such as his first name
    """
    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in ['username', 'first_name', 'last_name']:
            uservalue = getattr(user, attribute_name, None)
            if not uservalue:
                continue
            uservalue_parts = re.split(" ", uservalue)
            for part in uservalue_parts:
                if re.match(part.lower(), password.lower()):
                    raise ValidationError(
                        _("The password cannot contain the {}".format(attribute_name)
                          .format(attribute_name)),
                        code='password_too_similar_to_userattruîbute',
                    )

    def get_help_text(self):
        return _("cannot contain the username first or last name.")


class DifferentPasswordValidator:
    """
    cannot contain the user name or parts of the user’s full name, such as his first name
    """
    def validate(self, password, user=None):
        if not user:
            return
        if user.check_password(password):
            raise ValidationError(
                _("The new password must differ from the old password"),
                code='password_must_differ',
            )

    def get_help_text(self):
        return _("The new password must differ from the old password.")
