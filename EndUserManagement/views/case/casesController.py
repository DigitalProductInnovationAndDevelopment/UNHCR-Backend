import os
import traceback
import logging

from EndUserManagement.models import Case
from EndUserManagement.services import (
    PaginationService,
    TranslationService,
)
from EndUserManagement.serializers.responseSerializers import createCaseListResponseEndUserSerializer
from EndUserManagement.serializers.inputValidators import createCaseListValidator

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create instances of services
paginationService = PaginationService()
translationService = TranslationService()

# Create your views here.
@api_view(["GET", "POST"])
def casesController(request, **kwargs):

    if request.method == "GET":
        """
        Lists all cases.
        @Endpoint: /cases
        @QueryParam: User (Int, REQUIRED (For the end user), OPTIONAL (For admins))
        (ID of the user whose cases will be fetched)
        @QueryParam: Description (String, OPTIONAL) (Part of the description of the description of the wanted case(s))
        @QueryParam: Status (String, OPTIONAL) (Status of the wanted case(s))
        @QueryParam: CreatedAtOrder (String ("asc" OR "desc"), OPTIONAL)
        @QueryParam: UpdatedAtOrder (String ("asc" OR "desc"), OPTIONAL)
        @QueryParam: page (Int, OPTIONAL) (For pagination. If given as '2', second page of the results is fetched) 
        """
        try:
            queryParamsValidatorPtr = createCaseListValidator()
            queryParams = request.GET.dict()
            queryParamsValidator = queryParamsValidatorPtr(data = queryParams)
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
            if validatedData["User"] is not None:
                queryset = queryset.filter(User = validatedData["User"])

            # Filter according to Description (Search if the given Description is a part of the Description field of any Case object)
            if validatedData["Description"] is not None:
                queryset = queryset.filter(Description__icontains = validatedData["Description"])

            # Filter according to Status
            if validatedData["Status"] is not None:
                queryset = queryset.filter(Status = validatedData["Status"])

            # Filter according to CreatedAtOrder
            if validatedData["CreatedAtOrder"] is not None:
                if validatedData["CreatedAtOrder"] == "asc":
                    queryset = queryset.order_by('CreatedAt')
                else:
                    queryset = queryset.order_by('-CreatedAt')

            # Filter according to UpdatedAtOrder
            if validatedData["UpdatedAtOrder"] is not None:
                if validatedData["UpdatedAtOrder"] == "asc":
                    queryset = queryset.order_by('UpdatedAt')
                else:
                    queryset = queryset.order_by('-UpdatedAt')

            cases = queryset.all()
            
            responseSerializer = createCaseListResponseEndUserSerializer()
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
        """
        try:
            return Response(
                {"success": True, "message": "CASE CREATE HIT!"},
                status=status.HTTP_200_OK,
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
