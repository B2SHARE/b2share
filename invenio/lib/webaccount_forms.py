# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2012 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""WebAccount Forms"""

from invenio.webinterface_handler_flask_utils import _
from invenio.wtforms_utils import InvenioBaseForm
from flask.ext.wtf import (Form, SubmitField, BooleanField, TextField,
                           PasswordField, Required, HiddenField, validators)
from invenio.websession_model import User
from invenio.webuser import email_valid_p, nickname_valid_p
from sqlalchemy.exc import SQLAlchemyError
from websession_webinterface import wash_login_method


def validate_nickname_or_email(form, field):
    try:
        User.query.filter(User.nickname == field.data).one()
    except SQLAlchemyError:
        try:
            User.query.filter(User.email == field.data).one()
        except SQLAlchemyError:
            raise validators.ValidationError(
                _('Not valid nickname or email: %s') % (field.data, ))


class LoginForm(Form):
    nickname = TextField(
        _("User Name"),
        validators=[Required(message=_("Nickname not provided")), validate_nickname_or_email])
    password = PasswordField(_("Password"))
    remember = BooleanField(_("Remember Me"))
    referer = HiddenField()
    login_method = HiddenField()
    submit = SubmitField(_("Sign in"))

    def validate_login_method(self, field):
        field.data = wash_login_method(field.data)


class ChangeUserEmailSettingsForm(InvenioBaseForm):
    email = TextField(_("New email"))


class RegisterForm(Form):
    """
    User registration form
    """
    email = TextField(
        _("Email address"),
        validators=[Required(message=_("Email not provided"))],
        description=_("Example") + ": john.doe@example.com")
    nickname = TextField(
        _("User Name"),
        validators=[Required(message=_("User name not provided"))],
        description=_("Example") + ": johnd")
    password = PasswordField(
        _("Password"),
        description=_("The password phrase may contain punctuation, spaces, etc."),
        validators=[Required(message=_("Please enter a password")),
                    validators.Length(
                        min=6,
                        message=_('Password must be at least 6 characters long'))])
    password2 = PasswordField(_("Confirm password"),)
    referer = HiddenField()
    action = HiddenField(default='login')
    submit = SubmitField(_("Register"))

    def validate_nickname(self, field):
        if nickname_valid_p(field.data) != 1:
            raise validators.ValidationError(
                _("Desired user name %s is invalid.") % field.data
            )

        # is nickname already taken?
        try:
            User.query.filter(User.nickname == field.data).one()
            raise validators.ValidationError(
                _("Desired user name %s already exists in the database.") % field.data
            )
        except SQLAlchemyError:
            pass

    def validate_email(self, field):
        field.data = field.data.lower()
        if email_valid_p(field.data.lower()) != 1:
            raise validators.ValidationError(
                _("Supplied email address %s is invalid.") % field.data
            )

        # is email already taken?
        try:
            User.query.filter(User.email == field.data).one()
            raise validators.ValidationError(
                _("Supplied email address %s already exists in the database.") % field.data
            )
        except SQLAlchemyError:
            pass

    def validate_password2(self, field):
        if field.data != self.password.data:
            raise validators.ValidationError(_("Both passwords must match."))
