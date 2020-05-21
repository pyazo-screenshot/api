import logging

from PIL import Image

log = logging.getLogger(__name__)


class CreateThumbnailAction:
    def __call__(self, filepath: str, thumbnail_size: int):
        try:
            im = Image.open(filepath)
            im.thumbnail((thumbnail_size, thumbnail_size), Image.ANTIALIAS)
            im.save('asdf.webp', "WEBP")
        except IOError as e:
            log.error(e)
