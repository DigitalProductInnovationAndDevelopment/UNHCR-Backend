from django.core.paginator import Paginator

class PaginationService:
    def fetchPaginatedResults(self, queryset, request, serializer, paginationCount):
        paginator = Paginator(queryset, paginationCount)

        pageNumber = request.GET.get("page") if request.GET.get("page") else 1
        pageObj = paginator.get_page(pageNumber)

        configuredSerializer = serializer(pageObj, many=True)
        return pageNumber, paginator.num_pages, configuredSerializer.data
