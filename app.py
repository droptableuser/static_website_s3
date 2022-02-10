#!/usr/bin/env python3
import os

from aws_cdk import core

from static_website_s3.static_website_s3_stack import StaticWebsiteS3Stack

ACCOUNT=os.environ.get('AWS_ACCOUNT', '742344209721')
REGION=os.environ.get('AWS_REGION', 'eu-central-1')
env = core.Environment(account=ACCOUNT, region=REGION)
app = core.App()
StaticWebsiteS3Stack(app, "StaticWebsiteS3Stack", env=env)

app.synth()
