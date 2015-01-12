from cStringIO import StringIO
from PIL import Image
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from . import resources


class ResizedImage(models.Model):

    source_type = models.ForeignKey(ContentType)
    source_field_name = models.CharField(max_length=80)
    source_id = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    format = models.IntegerField(
        choices = resources.FORMAT_CHOICES,
        default = resources.DEFAULT_FORMAT,
    )
    quality = models.IntegerField(blank=True, null=True)
    should_crop = models.BooleanField(default=False)

    image = models.FileField(
        upload_to = "resized/",
        blank = True,
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified']

    def make_image(self, source_image):
        try:
            source_image.seek(0)
            p = Image.open(source_image)
        except Exception, e: # TEMP
            raise e
        # Don't process or upscale if source size is smaller than target size
        if self.width >= p.size[0] and self.height >= p.size[1]:
            self.image.save(source_image.name, source_image)
        else:
            try:
                f = StringIO()
                p.thumbnail((self.width, self.height), Image.ANTIALIAS)
                p.save(
                    f,
                    format=resources.get_format(self.format),
                    quality=self.quality or resources.DEFAULT_JPEG_QUALITY,
                )
                s = f.getvalue()
                self.image.save(source_image.name, ContentFile(s))
            except Exception, e: # TEMP
                raise e
            finally:
                f.close()
        self.save()