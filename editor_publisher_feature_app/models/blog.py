import os
import re
from django.db import models
from django.conf import settings

class Blog(models.Model):
    """
    Model to represent a blog.

    Attributes:
        title (str): Title of the blog.
        content (str): Blog content in HTML format.
        image_header (ImageField): Header image of the blog.
        created_at (datetime): Creation date of the blog.
        updated_at (datetime): Last update date of the blog.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    image_header = models.ImageField(upload_to='blog_headers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        """
        Deletes the blog instance and associated images.

        Overrides the delete method to remove the header image and 
        embedded images in the content before deleting the blog.
        """
        self._delete_image(self.image_header)
        self._delete_embedded_images(self.content)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Saves the blog instance and manages associated images.

        Overrides the save method to delete the old header image and 
        embedded images if they have been modified before saving.
        """
        if self.pk:
            original = Blog.objects.get(pk=self.pk)
            self._handle_image_header_change(original)
            self._handle_content_change(original)

        super().save(*args, **kwargs)

    def _delete_image(self, image_field):
        """
        Deletes the image file associated with the image field.

        Args:
            image_field (ImageField): Image field to delete the associated file.
        """
        if image_field and os.path.isfile(image_field.path):
            try:
                os.remove(image_field.path)
            except OSError as e:
                # Log the error if needed
                print(f"Error deleting file {image_field.path}: {e}")

    def _delete_embedded_images(self, content):
        """
        Deletes the embedded images in the blog content.

        Args:
            content (str): Blog content in HTML format.
        """
        image_paths = re.findall(r'<img src="([^"]+)"', content)
        for path in image_paths:
            relative_path = path.replace(f'{settings.SITE_URL}/media/', '')
            image_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            self._delete_image_path(image_path)

    def _delete_image_path(self, image_path):
        """
        Deletes the image file at the specified path.

        Args:
            image_path (str): Path to the image file to delete.
        """
        if os.path.isfile(image_path):
            try:
                os.remove(image_path)
            except OSError as e:
                # Log the error if needed
                print(f"Error deleting file {image_path}: {e}")

    def _handle_image_header_change(self, original):
        """
        Manages the change of the blog header image.

        Args:
            original (Blog): Original blog instance before changes.
        """
        if original.image_header and original.image_header != self.image_header:
            self._delete_image(original.image_header)

    def _handle_content_change(self, original):
        """
        Manages the change of the blog content.

        Args:
            original (Blog): Original blog instance before changes.
        """
        if original.content != self.content:
            self._delete_embedded_images(original.content)
