import os
import sys
from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cf,
    aws_cloudfront_origins as origins,
    aws_route53 as route53,
    aws_certificatemanager as cm,
    aws_route53_targets as targets,
    aws_s3_deployment as s3deploy
    # aws_sqs as sqs,
)
import aws_cdk as cdk

from constructs import Construct

class StaticWebsiteS3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        domain=os.environ.get('DOMAIN',None)
        if domain == None:
            sys.exit("You need to specify a domain name!")
        redirect_hostname= os.environ.get('REDIRECT',None)
        redirect = None
        if redirect_hostname:
            redirect=s3.RedirectTarget(host_name=redirect_hostname,protocol=s3.RedirectProtocol.HTTPS)
        domain_names = [domain,"www."+domain]

        bucket = s3.Bucket(self,domain,
            access_control=s3.BucketAccessControl.PRIVATE,
            removal_policy=cdk.RemovalPolicy.DESTROY,website_redirect=redirect)


        sources = None
        if os.path.exists("website/public") != False:
            sources = [s3deploy.Source.asset("website/public")]
            s3deploy.BucketDeployment(self,domain+"BucketDeployment",destination_bucket=bucket,sources=sources,retain_on_delete=False)

        origin_access_identity = cf.OriginAccessIdentity(self,domain+'OriginAccessIdentity')
        bucket.grant_read(origin_access_identity)

        hosted_zone = route53.HostedZone.from_lookup(
             self, domain+"HostedZone", domain_name=domain)

        cert = cm.DnsValidatedCertificate(
             self, domain+"Certificate",
             domain_name=domain,
             subject_alternative_names=domain_names,
             hosted_zone=hosted_zone,
             region="us-east-1")
        
        error_response = [cf.ErrorResponse(
            http_status=404,
            response_page_path="/404.html")]
        origin=origins.S3Origin(bucket,origin_access_identity=origin_access_identity)

        distribution = cf.Distribution(self,domain+'websitedistribution',       
            default_behavior=cf.behaviorOptions(origin=origin),domain_names=domain_names,price_class=cf.PriceClass.PRICE_CLASS_100,error_responses=error_response,certificate=cert, default_root_object="index.html",
            )
        distribution.add_behavior("*",origin,viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS)

        for record in domain_names:
            route53.ARecord(self, record+"Aalias",record_name=record,zone=hosted_zone,target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)))
            if record.startswith(domain):
                route53.AaaaRecord(self, record+"AAAAAalias",record_name=record,zone=hosted_zone,target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)))
