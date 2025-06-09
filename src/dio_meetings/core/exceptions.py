

class S3Error(Exception):
    pass


class UploadError(S3Error):
    pass


class DownloadError(S3Error):
    pass
