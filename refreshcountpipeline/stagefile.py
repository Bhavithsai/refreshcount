from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Stage
)
from .static_web_stack import StaticWebStack

class StageFile(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        
        
        service = StaticWebStack(self, 'StaticWebStack',env=cdk.Environment(account="403942067147", region="us-east-2"))
        
        
        
        
        