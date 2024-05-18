class TranslationService:
    def __init__(self):
        self.translationMap = {
            "HTTP.method.invalid": {"en-us": "HTTP method is invalid."},
            "": {"en-us": ""},
        }

    def translate(self, translationKey, userLanguageISOCode="en-us"):
        if translationKey in self.translationMap:
            return self.translationMap[translationKey][userLanguageISOCode]
        else:
            raise Exception("Translation for the message is not found.")
