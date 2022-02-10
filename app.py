#!/usr/bin/env python3
import os

from aws_cdk import core

from static_website_s3.static_website_s3_stack import StaticWebsiteS3Stack

ACCOUNT=os.environ.get('AWS_ACCOUNT', '742344209721')
REGION=os.environ.get('AWS_REGION', 'eu-central-1')
DOMAIN=os.environ.get('DOMAIN','droptableuser.me')
env = core.Environment(account=ACCOUNT, region=REGION)
app = core.App()
StaticWebsiteS3Stack(app, "StaticWebsiteS3Stack",DOMAIN, env=env
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
