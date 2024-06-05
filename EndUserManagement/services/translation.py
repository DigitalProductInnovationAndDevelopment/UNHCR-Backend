class TranslationService:
    def __init__(self):
        self.translationMap = {
            "HTTP.method.invalid": {"en-us": "HTTP method is invalid."},
            "case.not.exist": {"en-us": "The case does not exist."},
            "case.update.successful": {"en-us": "The case has been successfully updated."},
            "user.create.successful": {"en-us": "The user has been successfully created."},
            "user.update.successful": {"en-us": "The user has been successfully updated."},
            "user.not.found": {"en-us": "User not found."},
            "": {"en-us": ""},
        }

    def translate(self, translationKey, userLanguageISOCode="en-us"):
        if translationKey in self.translationMap:
            return self.translationMap[translationKey][userLanguageISOCode]
        else:
            raise Exception("Translation for the message is not found.")
