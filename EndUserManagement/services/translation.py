class TranslationService:
    def __init__(self):
        self.translationMap = {
            "HTTP.method.invalid": {"en-us": "HTTP method is invalid."},
            "HTTP.not.authorized": {"en-us": "This operation is not authorized."},
            "case.not.exist": {"en-us": "The case does not exist."},
            "case.update.successful": {"en-us": "The case has been successfully updated."},
            "user.create.successful": {"en-us": "The user has been successfully created."},
            "user.delete.successful": {"en-us": "The user has been successfully deleted."},
            'user.not.authenticated': {"en-us": "Authentication not successful. Check the email and password and try again."},
            "": {"en-us": ""},
        }

    def translate(self, translationKey, userLanguageISOCode="en-us"):
        if translationKey in self.translationMap:
            return self.translationMap[translationKey][userLanguageISOCode]
        else:
            raise Exception("Translation for the message is not found.")
