from django.utils.translation import gettext_lazy as _


class SERVER_EXCEPTION:
    SERVER_ERROR = _("Server error")
    PERMISSION_ERROR = _("Permission error")


class ELIZA_BOT_EXCEPTION:
    ELIZA_BOT_NOT_EXIST = _("Eliza Chatbot Does not exist")
    PERMISSION_ERROR = _("Chosen Bot does not belong to this User")


class ELIZA_SERVICE_EXCEPTION:
    BOT_NOT_SET_ERROR = _("Bot not set, please set the bot before using ElizaService")
    INVALID_GOTO_KEY = _("Invalid goto key")
    INVALID_RESULT_INDEX = _("Invalid result index")


class FILE_EXCEPTION:
    INVALID_FILE_EXTENSION_TXT = _("Invalid File extension! Please use a .txt file")
    FILE_TOO_LARGE = _("File upload must be under 2MB")


class KEYWORD_EXCEPTION:
    KEYWORD_NOT_EXIST = _("Keyword does not exist")
