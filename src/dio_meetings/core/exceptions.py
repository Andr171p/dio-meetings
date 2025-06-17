

class FileStoreError(Exception):
    pass


class UploadingError(FileStoreError):
    pass


class DownloadingError(FileStoreError):
    pass


class RepositoryError(Exception):
    pass


class CreationError(RepositoryError):
    pass


class ReadingError(RepositoryError):
    pass


class UpdatingError(RepositoryError):
    pass


class DeletingError(RepositoryError):
    pass
