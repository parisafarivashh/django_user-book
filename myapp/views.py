from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Book
from .serializer import BookSerializer
from .permission import IsOwnOrReadOnly

class book_viewset(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

