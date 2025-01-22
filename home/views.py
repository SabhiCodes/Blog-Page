from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .serializers import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

# Create your views here.

class PublicBlog(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'home/blog_list.html'  # Add this line

    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('?')

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))

            page_number = request.GET.get('page', 1)
            paginator = Paginator(blogs, 5)
            page_obj = paginator.get_page(page_number)

            serializer = BlogSerializer(page_obj, many=True)
            
            if request.accepted_renderer.format == 'html':
                return Response({
                    'data': serializer.data,
                    'page_obj': page_obj,
                    'message': "Blogs fetched successfully"
                })
            
            return Response({
                'data': serializer.data,
                'message': "Blogs fetched successfully"
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong or invalid page'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request):
        try:
            blogs = Blog.objects.filter(user = request.user)
            serializer = BlogSerializer(blogs, many = True)

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))

            return Response({
                'data': serializer.data,
                'message': "blog created sccessfully"
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({
                'data':{},
                'message': 'something went wrong'
            }, status= status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return Response({
                    'data' : {},
                    'message' : 'invalid blog uid'
                }, status = status.HTTP_400_BAD_REQUEST)
            if request.user != blog[0].user:
                return Response({
                        'data' : {},
                        'message' : "You are not authorized to do this"
                    }, status= status.HTTP_400_BAD_REQUEST)
            
            serializer = BlogSerializer(blog[0], data = data, partial = True)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong'
                }, status= status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': "blog updated sccessfully"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'data':{},
                'message': 'something went wrong'
            }, status= status.HTTP_400_BAD_REQUEST)

    # There are some issues to be resolved with the following part

    def post(self, request):
        try:
            print(f"Authorization Header: {request.headers.get('Authorization')}")      #for debugging
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data = data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong'
                }, status= status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': "blog created sccessfully"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data':{},
                'message': 'something went wrong'
            }, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return Response({
                    'data' : {},
                    'message' : 'invalid blog uid'
                }, status = status.HTTP_400_BAD_REQUEST)
            if request.user != blog[0].user:
                return Response({
                        'data' : {},
                        'message' : "You are not authorized to do this"
                    }, status= status.HTTP_400_BAD_REQUEST)
            
            blog[0].delete()

            return Response({
                'data':  {},
                'message': "blog deleted sccessfully"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'data':{},
                'message': 'something went wrong'
            }, status= status.HTTP_400_BAD_REQUEST)