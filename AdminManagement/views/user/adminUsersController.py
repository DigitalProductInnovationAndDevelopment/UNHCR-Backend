import os
import traceback
import logging
import json

from EndUserManagement.models import User
from UNHCR_Backend.services import (
    PaginationService,
    TranslationService,
)
from AdminManagement.serializers.responseSerializers import AdminUserListReponseSerializer, AdminUserCreateResponseSerializer
from AdminManagement.serializers.inputValidators import AdminUserCreateValidator

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
def adminUsersController(request, **kwargs):

    if request.method == "GET":
        """
        Lists all users.
        @Endpoint: /users
        """
        try:
            users = User.objects.all()
            responseSerializer = AdminUserListReponseSerializer
            pageNumber, pageCount, data = paginationService.fetchPaginatedResults(users, request, responseSerializer,
                                                                                    int(os.environ.get('ADMIN_USER_PAGINATION_COUNT', '25')))
                
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
        Creates a user.
        @Endpoint: /users
        @BodyParam: Name (String, REQUIRED)
        @BodyParam: Surname (String, REQUIRED)
        @BodyParam: DateOfBirth (String (YYYY-MM-DD), OPTIONAL)
        @BodyParam: PhoneNumber (String, OPTIONAL)
        @BodyParam: EmailAddress (String, REQUIRED)
        @BodyParam: Address (String, OPTIONAL)
        """
        try:
            requestBody = json.loads(request.body)
            paramValidator = AdminUserCreateValidator(data = requestBody)
            isParamsValid = paramValidator.is_valid(raise_exception = False)
            # The case for body param(s) not being as they should be
            if not isParamsValid:
                return Response(
                    {"success": False, "message": str(paramValidator.errors)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            validatedData = paramValidator.validated_data
            newUser = User(**validatedData)
            newUser.save()
            responseSerializer = AdminUserCreateResponseSerializer
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
