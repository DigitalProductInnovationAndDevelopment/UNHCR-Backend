import os
import traceback
import logging
import json

from EndUserManagement.models import Case
from UNHCR_Backend.services import (
    PaginationService,
    TranslationService,
)
from EndUserManagement.services import CaseService, MediaService
from EndUserManagement.serializers.inputValidators import CaseCreateValidator, CaseListValidator
from EndUserManagement.serializers.responseSerializers import CaseListResponseSerializer, CaseCreateResponseSerializer
from UNHCR_Backend.services import RequestService

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create instances of services
paginationService = PaginationService()
translationService = TranslationService()
caseService = CaseService()
mediaService = MediaService()
requestService = RequestService()

# Create your views here.
@api_view(["GET", "POST"])
def casesController(request, **kwargs):
    # loggedUser detected in UNHCR_Backend.middlewares.authMiddleware
    user = kwargs["loggedUser"]

    if request.method == "GET":
        """
        Lists all cases of the logged in user.
        @Endpoint: /cases
        @QueryParam: Coverage (String ("INDIVIDUAL" OR "HOUSEHOLD"), OPTIONAL) (Coverage of the wanted case(s))
        @QueryParam: Description (String, OPTIONAL) (Part of the description of the description of the wanted case(s))
        @QueryParam: Status (String, OPTIONAL) (Status of the wanted case(s))
        @QueryParam: CaseTypes (String, OPTIONAL, MULTIPLE) (IDs of the case types of the wanted case(s). This param can be submitted more than once)
        @QueryParam: PsnTypes (String, OPTIONAL, MULTIPLE) (IDs of the case types of the wanted case(s). This param can be submitted more than once)
        @QueryParam: CreatedAtOrder (String ("asc" OR "desc"), OPTIONAL)
        @QueryParam: UpdatedAtOrder (String ("asc" OR "desc"), OPTIONAL)
        @QueryParam: page (Int, OPTIONAL) (For pagination. If given as '2', second page of the results is fetched) 
        """
        try:
            # request.GET.dict() method discards query params if there are more than one query param with the same key
            queryParams = dict(request.GET)
            queryParamsValidator = CaseListValidator(data = queryParams)
            isQueryParamsValid = queryParamsValidator.is_valid(raise_exception = False)
            # The case for query param(s) not being as they should be
            if not isQueryParamsValid:
                return Response(
                    {"success": False, "message": str(queryParamsValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            validatedData = queryParamsValidator.validated_data
            queryset = Case.objects
            # Filter according to User ID
            queryset = queryset.filter(User = user)
            # Filter according to Coverage
            if "Coverage" in validatedData:
                queryset = queryset.filter(Coverage = validatedData["Coverage"])
            # Filter according to Description (Search if the given Description is a part of the Description field of any Case object)
            if "Description" in validatedData:
                queryset = queryset.filter(Description__icontains = validatedData["Description"])
            # Filter according to Status
            if "Status" in validatedData:
                queryset = queryset.filter(Status = validatedData["Status"])
            # Filter according to CaseTypes
            if "CaseTypes" in validatedData:
                caseTypeIds = [caseType.ID for caseType in validatedData["CaseTypes"]] 
                queryset = queryset.filter(CaseTypes__in = caseTypeIds)
            # Filter according to PsnTypes
            if "PsnTypes" in validatedData:
                psnTypeIds = [psnType.ID for psnType in validatedData["PsnTypes"]] 
                queryset = queryset.filter(PsnTypes__in = psnTypeIds)
            # Filter according to CreatedAtOrder
            if "CreatedAtOrder" in validatedData:
                if validatedData["CreatedAtOrder"] == "asc":
                    queryset = queryset.order_by('CreatedAt')
                else:
                    queryset = queryset.order_by('-CreatedAt')
            # Filter according to UpdatedAtOrder
            if "UpdatedAtOrder" in validatedData:
                if validatedData["UpdatedAtOrder"] == "asc":
                    queryset = queryset.order_by('UpdatedAt')
                else:
                    queryset = queryset.order_by('-UpdatedAt')
                    
            cases = queryset.distinct().all()   
            responseSerializer = CaseListResponseSerializer
            pageNumber, pageCount, data = paginationService.fetchPaginatedResults(cases, request, responseSerializer,
                                                                                  int(os.environ.get('CASE_PAGINATION_COUNT', '25')))
            canUserCreateCase, missingField = caseService.canUserCreateCase(user)
            allCaseTypes = caseService.getAllCaseTypes()
            allPsnTypes = caseService.getAllPsnTypes()
            return Response({'success': True,
                             'current_page': pageNumber,
                             'page_count': pageCount,
                             'data': data,
                             'case_create': {
                                'eligibility': canUserCreateCase,
                                'missing_field': missingField,
                                'case_types': allCaseTypes,
                                'psn_types': allPsnTypes
                             }},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "POST":
        """
        Creates a case.
        This request's body should be the type form-data.
        @Endpoint: /cases
        @BodyParam: Coverage (String ("INDIVIDUAL" OR "HOUSEHOLD"), REQUIRED) (Coverage for the new case)
        @BodyParam: Description (String, REQUIRED) (Text description for the new case)
        @BodyParam: CaseTypes (String, REQUIRED, MULTIPLE) (IDs of the case types.)
        @BodyParam: PsnTypes (String, OPTIONAL, MULTIPLE) (IDs of the case types.)
        @BodyParam: File (File, OPTIONAL, MULTIPLE) (Files related to the case.)
        @BodyParam: VoiceRecording (File, OPTIONAL) (The voice recording attached to the message)
        """
        try:
            # Transforming form data request body to dictionary
            requestBody = requestService.transformFormDataToDict(request)
            requestBody.update({
                "File": request.FILES.getlist('File'),
                "VoiceRecording": request.FILES.getlist('VoiceRecording')
            })
            paramValidator = CaseCreateValidator(data = requestBody)
            isParamsValid = paramValidator.is_valid(raise_exception=False)
            # The case for body param(s) not being as they should be
            if not isParamsValid:
                return Response(
                    {"success": False, "message": str(paramValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = paramValidator.validated_data
            caseCreateDict = validatedData.copy()
            for key in ['CaseTypes', 'PsnTypes', 'File', 'VoiceRecording']: 
                caseCreateDict.pop(key, None)
            initialStatus = "OPEN"
            newCase = Case(User = user, Status = initialStatus, **caseCreateDict)
            newCase.save()
            if "CaseTypes" in validatedData:
                newCase.CaseTypes.set(validatedData["CaseTypes"])
            if "PsnTypes" in validatedData:
                newCase.PsnTypes.set(validatedData["PsnTypes"])
            # Returns empty list if there are no files submitted under the key 'File'
            filesList = validatedData["File"]
            voiceRecordingsList = validatedData["VoiceRecording"]
            savedFileIds = []
            savedVoiceRecordingIds = []
            if filesList:
                for file in filesList:
                    fileId = mediaService.saveCaseMedia(file, newCase)
                    savedFileIds.append(fileId)
            if voiceRecordingsList:
                for voiceRecording in voiceRecordingsList:
                    voiceRecordingId = mediaService.saveCaseMedia(voiceRecording, newCase)
                    translationService.translateCaseVoiceRecording(voiceRecording, newCase)
                    savedVoiceRecordingIds.append(voiceRecordingId)  
            responseSerializer = CaseCreateResponseSerializer(newCase)
            responseDict = responseSerializer.data.copy()
            responseDict["Files"] = savedFileIds
            responseDict['VoiceRecordings'] = savedVoiceRecordingIds

            return Response(
                {"success": True, "data": responseDict},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    else:
        return Response(
            {"success": False, "message": translationService.translate("HTTP.method.invalid")},
            status=status.HTTP_400_BAD_REQUEST,
        )
