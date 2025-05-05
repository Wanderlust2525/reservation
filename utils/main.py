import base64

from django.core.files.base import ContentFile


def base64_to_image_file(base64_string, filename='image'):
    """
    Converts a base64 string to a Django ContentFile suitable for ImageField or FileField.

    :param base64_string: The base64-encoded string of the image
    :param filename: The name to assign to the file
    :return: A ContentFile object that can be saved to a Django model
    """
    # Strip the data prefix if it exists (e.g., 'data:image/jpeg;base64,')

    _format = 'jpg'

    if 'data:' in base64_string:
        _format = base64_string.split(';')[0].split(':')[1].split('/')[1]

    if 'base64,' in base64_string:
        base64_string = base64_string.split('base64,')[1]

    # Decode the base64 string
    decoded_file = base64.b64decode(base64_string)

    # Create a ContentFile
    image_file = ContentFile(decoded_file, name=f'{filename}.{_format}')

    return image_file