import logging

from PIL import Image

log = logging.getLogger(__name__)


class CreateThumbnailAction:
    def __call__(self, filepath: str):
        try:
            im = Image.open(filepath)
            im.thumbnail((128, 128), Image.ANTIALIAS)
            im.save('asdf', "WEBP")
        except IOError as e:
            log.error(e)
