import os
import traceback
import logging
import json

from EndUserManagement.models import Case
from UNHCR_Backend.services import (
    PaginationService,
    TranslationService,
)
from EndUserManagement.serializers.inputValidators import CaseCreateValidator, CaseListValidator
from EndUserManagement.serializers.responseSerializers import CaseListResponseSerializer, CaseCreateResponseSerializer

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
def casesController(request, **kwargs):
    # loggedUser detected in UNHCR_Backend.middlewares.authMiddleware
    user = kwargs["loggedUser"]

    if request.method == "GET":
        """
        Lists all cases of the logged in user.
        @Endpoint: /cases
        @QueryParam: Description (String, OPTIONAL) (Part of the description of the description of the wanted case(s))
        @QueryParam: Status (String, OPTIONAL) (Status of the wanted case(s))
        @QueryParam: CreatedAtOrder (String ("asc" OR "desc"), OPTIONAL)
        @QueryParam: UpdatedAtOrder (String ("asc" OR "desc"), OPTIONAL)
        @QueryParam: page (Int, OPTIONAL) (For pagination. If given as '2', second page of the results is fetched) 
        """
        try:
            queryParams = request.GET.dict()
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

            cases = queryset.all()   
            responseSerializer = CaseListResponseSerializer
            pageNumber, pageCount, data = paginationService.fetchPaginatedResults(cases, request, responseSerializer,
                                                                                  int(os.environ.get('CASE_PAGINATION_COUNT', '25')))
            return Response({'success': True,
                             'current_page': pageNumber,
                             'page_count': pageCount,
                             'data': data},
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
             @Endpoint: /cases
             @BodyParam: Description (String, REQUIRED) (Part of the description of the description of the wanted case(s))
             """
        try:
            requestBody = json.loads(request.body)
            paramValidator = CaseCreateValidator(data=requestBody)
            isParamsValid = paramValidator.is_valid(raise_exception=False)
            # The case for body param(s) not being as they should be
            if not isParamsValid:
                return Response(
                    {"success": False, "message": str(paramValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = paramValidator.validated_data
            initialStatus = "OPEN"
            newCase = Case(User = user, Status = initialStatus, **validatedData)
            newCase.save()
            responseSerializer = CaseCreateResponseSerializer(newCase)
            return Response(
                {"success": True, "data": responseSerializer.data},
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
