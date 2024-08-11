import os
import traceback
import logging
import json

from EndUserManagement.models import Case
from UNHCR_Backend.services import (
    PaginationService,
    TranslationService,
)
from AdminManagement.serializers.inputValidators import AdminCaseCreateValidator, AdminCaseListValidator
from AdminManagement.serializers.responseSerializers import AdminCaseListReponseSerializer, AdminCaseCreateReponseSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework import serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create instances of services
paginationService = PaginationService()
translationService = TranslationService()

# Create your views here.
@api_view(["GET", "POST"])
def adminCasesController(request, **kwargs):
    # loggedUser detected in UNHCR_Backend.middlewares.authMiddleware
    user = kwargs["loggedUser"]

    if request.method == "GET":
        """
        Lists all cases of the logged in user.
        @Endpoint: /cases
        @QueryParam: Description (String, OPTIONAL) (Part of the description of the description of the wanted case(s))
        @QueryParam: Status (String, OPTIONAL) (Status of the wanted case(s))
        @QueryParam: User (Int, OPTIONAL) (ID of the User whose cases will be listed)
        @QueryParam: CreatedAtOrder (String ("asc" OR "desc"), OPTIONAL)
        @QueryParam: UpdatedAtOrder (String ("asc" OR "desc"), OPTIONAL)
        @QueryParam: page (Int, OPTIONAL) (For pagination. If given as '2', second page of the results is fetched) 
        @QueryParam: VulnerabilityScore (String ("asc" OR "desc"), OPTIONAL)
       
        """
        try:
            queryParams = request.GET.dict()
            queryParamsValidator = AdminCaseListValidator(data = queryParams)
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
            if "User" in validatedData:
                queryset = queryset.filter(User = validatedData["User"])

            # Filter according to Description (Search if the given Description is a part of the Description field of any Case object)
            if "Description" in validatedData:
                queryset = queryset.filter(Description__icontains = validatedData["Description"])

            # Filter according to Status
            if "Status" in validatedData:
                queryset = queryset.filter(Status = validatedData["Status"])

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

                # Filter according to VulnerabilityScore
                if "VulnerabilityScore" in validatedData:
                    if validatedData["VulnerabilityScore"] == "asc":
                        queryset = queryset.order_by('VulnerabilityScore')
                    else:
                        queryset = queryset.order_by('-VulnerabilityScore')

            cases = queryset.all()
            
            responseSerializer = AdminCaseListReponseSerializer
            pageNumber, pageCount, data = paginationService.fetchPaginatedResults(cases, request, responseSerializer,
                                                                                  int(os.environ.get('ADMIN_CASE_PAGINATION_COUNT', '25')))
            return Response({'success': True,
                             'current_page': pageNumber,
                             'page_count': pageCount,
                             'data': data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": translationService.translate('general.exception.message')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    elif request.method == "POST":
        """
        Creates a case.
        @Endpoint: /cases
        @BodyParam: User (Int, REQUIRED) (ID of the user whom the case will belong to)
        @BodyParam: Description (String, REQUIRED) (Description of the case which will be created)
        @BodyParam: Status (String, REQUIRED) (Status of the case which will be created)
        """
        try:
            requestBody = json.loads(request.body)
            paramValidator = AdminCaseCreateValidator(data=requestBody)
            isParamsValid = paramValidator.is_valid(raise_exception=False)
            # The case for body param(s) not being as they should be
            if not isParamsValid:
                return Response(
                    {"success": False, "message": str(paramValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = paramValidator.validated_data
            newCase = Case(**validatedData)
            newCase.save()
            responseSerializer = AdminCaseCreateReponseSerializer(newCase)

            return Response(
                {"success": True, "data": responseSerializer.data},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response(
                {"success": False, "message": translationService.translate('general.exception.message')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    else:
        return Response(
            {"success": False, "message": translationService.translate("HTTP.method.invalid")},
            status=status.HTTP_400_BAD_REQUEST,
        )
