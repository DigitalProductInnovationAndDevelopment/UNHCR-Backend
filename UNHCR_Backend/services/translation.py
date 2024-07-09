class TranslationService:
    def __init__(self):
        self.translationMap = {
            "HTTP.method.invalid": {"en-us": "HTTP method is invalid."},
            "HTTP.not.authorized": {"en-us": "This operation is not authorized."},
            "case.create.successful": {"en-us": "The case has been successfully created."},
            "case.not.exist": {"en-us": "The case does not exist."},
            "case.update.successful": {"en-us": "The case has been successfully updated."},
            "case.delete.successful": {"en-us": "The case has been successfully deleted."},
            "user.create.successful": {"en-us": "The user has been successfully created."},
            "user.delete.successful": {"en-us": "The user has been successfully deleted."},
            "user.not.authenticated": {"en-us": "Authentication not successful. Check the email and password and try again."},
            "user.not.exist": {"en-us": "The user does not exist."},
            "user.update.successful": {"en-us": "The user has been successfully updated."},
            'user.not.authenticated': {"en-us": "Authentication not successful. Check the email and password and try again."},
            "message.not.exist": {"en-us": "The message does not exist."},
            "message.media.not.exist": {"en-us": "The message media does not exist."},
            "": {"en-us": ""},
        }

    def translate(self, translationKey, userLanguageISOCode="en-us"):
        if translationKey in self.translationMap:
            return self.translationMap[translationKey][userLanguageISOCode]
        else:
            raise Exception("Translation for the message is not found.")
