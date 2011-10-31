from django.core.files.storage import FileSystemStorage
from django.conf import settings


class StaticFileSystemStorage(FileSystemStorage):
    """Overrides the default file system storage to
    be in a different location outside the project"""
    def __init__(self, location=None, base_url=None):
        super(StaticFileSystemStorage,
              self).__init__(settings.STATIC_ROOT,
                             settings.STATIC_URL)
