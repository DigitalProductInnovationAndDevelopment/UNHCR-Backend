class RequestService:
    def transformFormDataToDict(self, request):
        formData = request.POST
        dataDict = {}
        for key in formData.keys():
            values = formData.getlist(key)
            if len(values) == 1:
                dataDict[key] = values[0]
            else:
                dataDict[key] = values
        return dataDict