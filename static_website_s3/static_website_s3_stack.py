from os import access
import uuid
from aws_cdk import (
    # Duration,
    core,
    aws_s3 as s3,
    aws_cloudfront as cf,
    aws_cloudfront_origins as origins,
    aws_route53 as route53,
    aws_certificatemanager as cm,
    aws_route53_targets as targets,
    # aws_sqs as sqs,
)
from constructs import Construct

class StaticWebsiteS3Stack(core.Stack):

    def __init__(self, scope: Construct, construct_id: str, Domain, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        domain = Domain
        domain_names = [domain,"www."+domain]

        bucket = s3.Bucket(self,domain+str(uuid.uuid4()),access_control=s3.BucketAccessControl.PRIVATE)

        origin_access_identity = cf.OriginAccessIdentity(self,domain+'OriginAccessIdentity')
        bucket.grant_read(origin_access_identity)

        hosted_zone = route53.HostedZone.from_lookup(
             self, domain+"HostedZone", domain_name=domain)

        cert = cm.Certificate(
             self, domain+"Certificate",
             domain_name=domain,
             subject_alternative_names=domain_names,
             validation=cm.CertificateValidation.from_dns(hosted_zone))
        
        error_response = [cf.ErrorResponse(
            http_status=404,
            response_page_path="/404.html")]


        distribution = cf.Distribution(self,domain+'websitedistribution',       
            default_behavior=cf.BehaviorOptions(origin=origins.S3Origin(bucket,origin_access_identity=origin_access_identity)),domain_names=domain_names,certificate=cert,price_class=cf.PriceClass.PRICE_CLASS_100,error_responses=error_response)
        for record in domain_names:
            route53.ARecord(self, record+"Aalias",record_name=record,zone=hosted_zone,target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)))
            route53.AaaaRecord(self, record+"AAAAAalias",record_name=record,zone=hosted_zone,target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)))
