#!/usr/bin/env python3
import imp
import os

import aws_cdk as cdk

from static_website_s3.static_website_s3_stack import StaticWebsiteS3Stack

ACCOUNT=os.environ.get('AWS_ACCOUNT', '742344209721')
REGION=os.environ.get('AWS_REGION', 'eu-central-1')
env = cdk.Environment(account=ACCOUNT, region=REGION)
app = cdk.App()
domain=os.environ.get("DOMAIN",None)
StaticWebsiteS3Stack(app, domain+"StaticWebsiteS3Stack", env=env)

app.synth()
