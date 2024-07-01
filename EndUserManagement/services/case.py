from EndUserManagement.models import CaseType, PsnType

class CaseService:
    def __init__(self):
        pass

    def canUserCreateCase(self, user):
        unchrId = user.UnhcrIndividualId
        countryOfAsylumRegistrationNumber = user.CountryOfAsylumRegistrationNumber
        if not unchrId and not countryOfAsylumRegistrationNumber:
            return False, 'UnhcrIndividualId,CountryOfAsylumRegistrationNumber'
        provinceOfResidence = user.ProvinceOfResidence
        if not provinceOfResidence:
            return False, 'ProvinceOfResidence'
        phoneNumber = user.PhoneNumber
        if not phoneNumber:
            return False, 'PhoneNumber'
        return True, None
    
    def getAllCaseTypes(self):
        allCaseTypes = CaseType.objects.all()
        caseTypesDict = {}
        for caseType in allCaseTypes:
            caseTypesDict[caseType.name] = caseType.ID
        return caseTypesDict

    def getAllPsnTypes(self):
        allPsnTypes = PsnType.objects.all()
        psnTypesDict = {}
        for psnType in allPsnTypes:
            psnTypesDict[psnType.name] = psnType.ID
        return psnTypesDict