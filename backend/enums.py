from django.utils.translation import gettext_lazy as _


class SERVER_EXCEPTION:
    SERVER_ERROR = _('Server error')
    PERMISSION_ERROR = _('Permission error')


class FIREBASE_EXCEPTION:
    GET_USER_ERROR = _('Failed to get Firebase user')
    EMAIL_ALREADY_EXISTED = _('Email alredy existed')
    CREATE_USER_ERROR = _('Failed to create Firebase user')
    GET_USER_BY_EMAIL_ERROR = _('Failed to get Firebase user by email')


class ACCOUNT_EXCEPTION:
    ACCOUNT_NOT_EXIST = _('Account does not exist')
    EMAIL_ALREADY_EXISTED = _('Email alredy existed')
