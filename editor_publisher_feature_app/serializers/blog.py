from rest_framework import serializers
from editor_publisher_feature_app.models import Blog

class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for the Blog model.

    This serializer converts Blog model instances to JSON representations 
    and vice versa. Additionally, it provides an absolute URL for the header image.
    """
    image_header = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'image_header', 'created_at', 'updated_at']

    def get_image_header(self, obj):
        """
        Gets the absolute URL of the header image.

        Args:
            obj (Blog): Instance of the Blog model.

        Returns:
            str: Absolute URL of the header image or None if it doesn't exist.
        """
        request = self.context.get('request')
        try:
            if obj.image_header and request is not None:
                return request.build_absolute_uri(obj.image_header.url)
        except Exception as e:
            # Log the error if needed
            print(f"Error getting image header URL: {e}")
        return None
