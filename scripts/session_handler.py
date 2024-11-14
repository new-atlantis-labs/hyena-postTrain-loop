import boto3
import sagemaker
import json


class SessionHandler:
    def __init__(self, region_name=None):
        self.boto_session = boto3.session.Session(region_name=region_name)
        self.sagemaker_session = sagemaker.session.Session(self.boto_session)
        self.region_name = self.sagemaker_session.boto_region_name
        self.bucket = self.sagemaker_session.default_bucket()
        self.role = sagemaker.get_execution_role(self.sagemaker_session)

    @property
    def get_session_info(self):
        return {
            'region_name': self.region_name,
            'bucket': self.bucket,
            'role': self.role,
            'boto_session': self.boto_session,
            'sagemaker_session': self.sagemaker_session
        }

    def setup_tensorboard(self, training_job_name, user_profile):
        """Get URL for TensorBoard dashboard"""
        from sagemaker.interactive_apps.tensorboard import TensorBoardApp

        # Get domain ID from metadata
        with open("/opt/ml/metadata/resource-metadata.json", "r") as f:
            app_metadata = json.loads(f.read())
            domain_id = app_metadata["DomainId"]

        tb_app = TensorBoardApp(self.region_name)
        return tb_app.get_app_url(
            training_job_name=training_job_name,
            create_presigned_domain_url=True,
            domain_id=domain_id,
            user_profile_name=user_profile,
            open_in_default_web_browser=False
        )
