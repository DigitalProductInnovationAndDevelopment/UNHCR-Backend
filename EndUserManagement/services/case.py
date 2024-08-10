from EndUserManagement.models import CaseType, PsnType

class CaseService:
    def __init__(self):
        self.childrenAgeVulnerabilityScore = 0
        self.adultAgeVulnerabilityScore = 10
        self.defaultAgeVulnerabilityScore = 7
        self.caseTypesVulnerabilityScores = {
            "Health": 7,
            "Education": 6,
            "Food Assistance": 6,
            "Cash Assistance": 6,
            "Legal Support": 6,
            "NFI Support": 5,
            "Protection From Violence": 10,
            "MHPSS": 7,
            "Child Protection": 10,
            "Detention/Deportation": 10,
            "Other": 2,
        }
        self.psnTypesVulnerabilityScores = {
            "Pregnant": 8,
            "Elderly": 7,
            "Unaccompanied And/Or Seperated Children": 9,
            "Chronic Disease": 4,
            "Disability": 9,
        }
        self.highRiskScoreBorder = 30
        self.moderateRiskScoreBorder = 30
    
    def calcCaseVulnerabilityScore(self, case):
        # Calculating the score which is coming from the user's age
        userAge = case.User.calculateAge()
        ageValue = self.defaultAgeVulnerabilityScore
        if userAge <= 18:
            ageValue = self.childrenAgeVulnerabilityScore
        elif userAge <= 59:
            ageValue = self.adultAgeVulnerabilityScore
        else:
            pass
        # Calculating the score which is coming from the case types of the case
        caseTypeValue = 0
        for caseType in case.CaseTypes.all():
            caseTypeName = caseType.name
            if caseTypeName in self.caseTypesVulnerabilityScores:
                caseTypeValue = caseTypeValue + self.caseTypesVulnerabilityScores[caseTypeName]
        # Capping the score coming from case types to 16
        if caseTypeValue > 16:
            caseTypeValue = 16
        # Calculating the score which is coming from the psn types of the case
        psnTypeValue = 0
        for psnType in case.PsnTypes.all():
            psnTypeName = psnType.name
            if psnTypeName in self.psnTypesVulnerabilityScores:
                psnTypeValue = psnTypeValue + self.psnTypesVulnerabilityScores[psnTypeName]
        # Capping the score coming from case types to 16
        if psnTypeValue > 16:
            psnTypeValue = 16
        # Calculating the score which is coming from the registration (Unregistered if no CoA or UNHCR id exists)
        registerationValue = 10
        unchrId = case.User.UnhcrIndividualId
        countryOfAsylumRegistrationNumber = case.User.CountryOfAsylumRegistrationNumber
        # If the user is registered to UNHCR, he/she is better legally protected. So less vulnerable
        if unchrId or countryOfAsylumRegistrationNumber:
            registerationValue = 0
        totalScore = ageValue + caseTypeValue + psnTypeValue + registerationValue
        vulnerabilityCategory = None
        if totalScore >= self.highRiskScoreBorder:
            vulnerabilityCategory = "HIGH RISK"
        elif totalScore >= self.moderateRiskScoreBorder:
            vulnerabilityCategory = "MODERATE RISK"
        else:
            vulnerabilityCategory = "LOW RISK"
        return totalScore, vulnerabilityCategory

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