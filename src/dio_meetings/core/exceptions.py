

class S3Error(Exception):
    pass


class UploadError(S3Error):
    pass


class DownloadError(S3Error):
    pass


class RepositoryError(Exception):
    pass


class ReadDataError(RepositoryError):
    pass


class CreateDataError(RepositoryError):
    pass


class UpdateDataError(RepositoryError):
    pass


class DeleteDataError(RepositoryError):
    pass
