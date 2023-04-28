from aws_cdk import (aws_codecommit as codecommit,
 pipelines as pipelines,
 Stack)

from constructs import Construct
from .Stage_file import StageFile

class Pipeline(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        repo = codecommit.Repository(self, 'CodeCommitRepository',repository_name= "Static_Web")
        pipeline = pipelines.CodePipeline(
            self, 'pipelinetest1',
            cross_account_keys=True, 
            
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "master"),
                

            # Builds our source code outlined above into a could assembly artifact
                commands=[
                    'npm install -g aws-cdk', # Installs the cdk cli on Codebuild
                    #'cd cdk.out',
                    'pip install -r requirements.txt',
                    "npx cdk synth",
                    # Instructs codebuild to install required package
                ],
                
                primary_output_directory = './cdk.out' 
            ),
        )
      
        
        
        deploy = StageFile(self, "website")
        deploy_stage = pipeline.add_stage(deploy)
        