from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as  IAM,
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class StaticWebStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        bucket = s3.Bucket(self, "Hellobucket",
                           access_control=s3.BucketAccessControl.PUBLIC_READ,
                           website_index_document="helloworld.html"
                           )
        bucket.grant_public_access()
        
        distribution = cloudfront.CloudFrontWebDistribution(self, "MyDistribution",
          origin_configs=[cloudfront.SourceConfiguration(
            s3_origin_source=cloudfront.S3OriginConfig(
               s3_bucket_source=bucket
        ),
        behaviors=[cloudfront.Behavior(is_default_behavior=True)]
    )
    ]
)
        table = dynamodb.Table(self, "counttable",
        partition_key=dynamodb.Attribute(name="count", type=dynamodb.AttributeType.STRING)
)
    

        my_lambda = _lambda.Function(
            self, 'static',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='code.lambda_handler',
        )
        table.grant_read_data(my_lambda)
        table.grant_full_access(my_lambda)
    
        api = apigw.RestApi(self, 'cdkweb',
        rest_api_name="cdkweb",
        endpoint_types=[apigw.EndpointType.EDGE],
        default_cors_preflight_options= apigw.CorsOptions(
            allow_methods=['POST','GET', 'OPTIONS'],
            allow_origins=apigw.Cors.ALL_ORIGINS)
            )
        api.root.add_method("GET",
        apigw.LambdaIntegration(my_lambda, proxy=False,
        integration_responses=[apigw.IntegrationResponse(status_code="200",
        response_parameters={
            'method.response.header.Access-Control-Allow-Origin': "'*'"}
            )]
            ),
            method_responses=[apigw.MethodResponse(status_code="200",
            response_parameters={'method.response.header.Access-Control-Allow-Origin': True})
            ]
            )
        api.root.add_method("POST",
        apigw.LambdaIntegration(my_lambda, proxy=False,
        integration_responses=[apigw.IntegrationResponse(status_code="200",
        response_parameters={'method.response.header.Access-Control-Allow-Origin': "'*'"})]
        ),
        method_responses=[apigw.MethodResponse(status_code="200",
        response_parameters={'method.response.header.Access-Control-Allow-Origin': True})]
        )

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "StaticWebQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
