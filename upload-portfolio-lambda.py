import json
import boto3
from io import BytesIO
import zipfile
import mimetypes


def lambda_handler(event, context):
    # TODO implement

    # session = boto3.Session(profile_name='pythonAutomation')

    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:779436620566:deployPortfolioTopic')
    s3 = boto3.resource('s3')

    try:
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

        print("Job Done!")
        topic.publish(Subject="Portfolio is Updated and Deployed",
                      Message="Lucian's portfolio was deployed successfully!")
    except:
        topic.publish(Subject="Portfolio Deployment Failed",
                      Message="Lucian's portfolio was NOT deployed successfully!")

    return