import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from editor_publisher_feature_app.models import Blog
from editor_publisher_feature_app.serializers import BlogSerializer
from editor_publisher_feature_app.utils.handle_images import handle_images

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def blog_list_create(request):
    """
    Handles listing all blogs and creating a new blog.

    GET:
        Returns a list of all blogs, ordered by creation date.
    
    POST:
        Creates a new blog. Handles embedded images in the content by converting
        base64 images to URLs.

    Args:
        request (HttpRequest): The request object containing query parameters or data.

    Returns:
        Response: A Response object with serialized blog data or error messages.
    """
    if request.method == 'GET':
        blogs = Blog.objects.all().order_by('-created_at')
        serializer = BlogSerializer(blogs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        data = request.data.copy()
        content = data.get('content', '')

        # Handle embedded images
        data['content'] = handle_images(content)

        serializer = BlogSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            try:
                blog = serializer.save()

                if 'image_header' in request.FILES:
                    blog.image_header = request.FILES['image_header']
                    blog.save()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error saving blog: {e}")
                return Response({"detail": "An error occurred while saving the blog."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def blog_update(request, id):
    """
    Updates an existing blog.

    Args:
        request (HttpRequest): The request object containing data for updating the blog.
        id (int): The ID of the blog to update.

    Returns:
        Response: A Response object with serialized blog data or error messages.
    """
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    content = data.get('content', '')

    # Handle embedded images
    data['content'] = handle_images(content)
    
    serializer = BlogSerializer(blog, data=data, partial=True, context={'request': request})
    if serializer.is_valid():
        try:
            serializer.save()

            if 'image_header' in request.FILES:
                blog.image_header = request.FILES['image_header']
                blog.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error updating blog: {e}")
            return Response({"detail": "An error occurred while updating the blog."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def blog_delete(request, id):
    """
    Deletes an existing blog.

    Args:
        request (HttpRequest): The request object.
        id (int): The ID of the blog to delete.

    Returns:
        Response: A Response object indicating the status of the deletion.
    """
    try:
        blog = Blog.objects.get(id=id)
        blog.delete()
        return Response(status=status.HTTP_200_OK)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error deleting blog: {e}")
        return Response({"detail": "An error occurred while deleting the blog."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
