
from users.models import NewUser
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Leader
from .serializers import LeaderSerializer , LeaderRetrieveSerializer
from rest_framework.views import APIView
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class LeaderViewSet(viewsets.ModelViewSet):
    queryset = Leader.objects.all()
    permission_classes = [AllowAny]
    serializer_class = LeaderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('uuid', 'main_account', 'leader_type', 'parent')
    
    def create(self, request, *args, **kwargs):
        # print(request.data.get('parent'), 'getttttt')
        serializer = LeaderSerializer(data=request.data)
        parent_id = request.data.get('parent')
        if parent_id:
            parent = Leader.objects.get(id=parent_id)
            if parent and not parent.is_eligible:
                raise ValueError(
                    "Parent is not eligible - (Maximum children 4)")
        if serializer.is_valid():
            leader = serializer.save()
            if leader:
                # parent = leader.parent
                # print(parent, 'in the create view')
                # if parent:
                #     print('the parent is', parent)
                #     parent.children_count += 1
                #     parent.save()
                #     print('from the saave method')
                # else:
                #     print('no parent :((')    
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
