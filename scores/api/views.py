from django.http.response import JsonResponse
from django.core.paginator import Paginator
from .models import Score
from .utils import IsAuthenticatedWith, method_permission_classes, ANY
from .serializers import ScoreResponseSerializer

from rest_framework.views import APIView

# Create your views here.
class ScoreListView(APIView):
    
    @method_permission_classes((IsAuthenticatedWith(ANY),))
    def get(self, request):

        scores = Score.objects.all().order_by('-resolved_count')
        page = request.query_params.get('page', 1)
        pageSize = request.query_params.get('pageSize', 10)

        count = scores.count()
        paginator = Paginator(scores, pageSize)

        scores_serializer = ScoreResponseSerializer(
            paginator.page(page), many=True)
        return JsonResponse({'items': scores_serializer.data, 'count': count}, safe=False)

class ScoreDetailsListView(APIView):
    
    @method_permission_classes((IsAuthenticatedWith(ANY),))
    def get(self, request, pk):
        score = Score.objects.get(user_id=pk)
        serializer = ScoreResponseSerializer(score)
        return JsonResponse(serializer.data)