from django.contrib.contenttypes.models import ContentType
from .models import ResizedImage


def get_type_for_instance(instance):

    return ContentType.objects.get_for_model(instance.__class__)


def make_resized_image(source_instance,
                       source_field_name,
                       width,
                       height,
                       should_crop=False):

    instance, created = ResizedImage.objects.get_or_create(
        source_type = get_type_for_instance(source_instance),
        source_field_name = source_field_name,
        source_id = source_instance.id,
        width = width,
        height = height,
        should_crop = should_crop,
    )

    # TODO: Remove old data

    source_image = getattr(source_instance, source_field_name)
    source_image.open() # https://code.djangoproject.com/ticket/13750

    instance.make_image(source_image)
    return instance


def get_resized_image(source_instance,
                      source_field_name,
                      width,
                      height,
                      should_crop=False):
    try:
        return ResizedImage.objects.get(
            source_type = get_type_for_instance(source_instance),
            source_field_name = source_field_name,
            source_id = source_instance.id,
            width = width,
            height = height,
            should_crop = should_crop,
        )
    except ResizedImage.DoesNotExist:
        pass


def remove_resized_images(source_instance,
                          source_field_name):
    """
    Remove all ResizedImage instances for the specified object instance and
    field.
    """

    return ResizedImage.objects.filter(
        source_type = get_type_for_instance(source_instance),
        source_field_name = source_field_name,
        source_id = source_instance.id,
    ).delete()
