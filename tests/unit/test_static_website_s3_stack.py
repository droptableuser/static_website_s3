import aws_cdk as core
import aws_cdk.assertions as assertions

from static_website_s3.static_website_s3_stack import StaticWebsiteS3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in static_website_s3/static_website_s3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = StaticWebsiteS3Stack(app, "static-website-s3")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
