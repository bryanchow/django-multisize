import os
from cStringIO import StringIO
from PIL import Image, ImageOps
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.dispatch import receiver
from . import resources


class ResizedImage(models.Model):

    source_type = models.ForeignKey(ContentType)
    source_field_name = models.CharField(max_length=80)
    source_id = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    actual_width = models.IntegerField(blank=True, null=True)
    actual_height = models.IntegerField(blank=True, null=True)
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
                if self.should_crop:
                    p = ImageOps.fit(
                        image = p,
                        size = (self.width, self.height),
                        method = Image.ANTIALIAS,
                        centering = (0.5, 0.5),
                    )
                else:
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
        self.actual_width = p.size[0]
        self.actual_height = p.size[1]
        self.save()


@receiver(models.signals.post_delete, sender=ResizedImage)
def deleted_image_file(sender, instance, **kwargs):

    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
