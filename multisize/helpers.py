from django.contrib.contenttypes.models import ContentType
from .models import ResizedImage


def get_type_for_instance(instance):

    return ContentType.objects.get_for_model(instance.__class__)


def make_resized_image(source_instance,
                       source_field_name,
                       width,
                       height):

    instance, created = ResizedImage.objects.get_or_create(
        source_type = get_type_for_instance(source_instance),
        source_field_name = source_field_name,
        source_id = source_instance.id,
        width = width,
        height = height,
    )

    # TODO: Remove old data
    instance.make_image(getattr(source_instance, source_field_name))
    return instance


def get_resized_image(source_instance,
                      source_field_name,
                      width,
                      height):
    try:
        return ResizedImage.objects.get(
            source_type = get_type_for_instance(source_instance),
            source_field_name = source_field_name,
            source_id = source_instance.id,
            width = width,
            height = height,
        )
    except ResizedImage.DoesNotExist:
        pass
