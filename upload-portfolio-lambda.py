import boto3
from io import BytesIO
import zipfile
import mimetypes

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

portfolio_bucket = s3.Bucket('bio.lucian63ontheway.com')
build_bucket = s3.Bucket('portfoliobuild.lucian63ontheway.com')

portfolio_zip = BytesIO()
build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj, nm,
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
