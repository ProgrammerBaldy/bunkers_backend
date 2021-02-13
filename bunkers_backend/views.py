from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class TestConn(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = True

    def get(self, request, *args, **kwargs):
        return Response(data={'message':True})