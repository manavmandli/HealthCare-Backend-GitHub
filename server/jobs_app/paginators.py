from utils.pagination_setup import PaginationWithPageCount

class JobListPagination(PaginationWithPageCount):
      page_query_param = 'page'
      