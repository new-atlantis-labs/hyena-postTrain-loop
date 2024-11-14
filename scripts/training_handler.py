from sagemaker.pytorch import PyTorch
from sagemaker.experiments.run import Run
from sagemaker.debugger import TensorBoardOutputConfig
from sagemaker.inputs import TrainingInput


class TrainingHandler:
    def __init__(self, session_info):
        self.role = session_info['role']
        self.region_name = session_info['region_name']
        self.sagemaker_session = session_info['sagemaker_session']
        self.bucket = session_info['bucket']

    def setup_tensorboard_config(self, base_job_name):
        """Setup TensorBoard configuration"""
        output_path = f"s3://{self.bucket}/sagemaker-output/training/{base_job_name}"
        return TensorBoardOutputConfig(
            s3_output_path=f"{output_path}/tensorboard",
            container_local_output_path="/opt/ml/output/tensorboard"
        )

    def setup_training(self, experiment_name, base_job_name, hyperparameters, metric_definitions):
        """Configure training job"""
        self.experiment_name = experiment_name
        self.base_job_name = base_job_name

        # Setup tensorboard config
        tensorboard_config = self.setup_tensorboard_config(base_job_name)

        # Create estimator
        self.estimator = PyTorch(
            base_job_name=base_job_name,
            entry_point="train_hf_accelerate.py",
            source_dir="scripts/",
            instance_type="ml.g5.12xlarge",
            instance_count=1,
            image_uri=f"763104351884.dkr.ecr.{self.region_name}.amazonaws.com/pytorch-training:2.2.0-gpu-py310-cu121-ubuntu20.04-sagemaker",
            role=self.role,
            hyperparameters=hyperparameters,
            metric_definitions=metric_definitions,
            sagemaker_session=self.sagemaker_session,
            distribution={"torch_distributed": {"enabled": True}},
            tags=[{"Key": "project", "Value": "genomics-model-pretraining"}],
            keep_alive_period_in_seconds=1800,
            tensorboard_output_config=tensorboard_config,
        )

    def train(self, data_uri):
        """Run training job"""
        with Run(experiment_name=self.experiment_name, 
                sagemaker_session=self.sagemaker_session) as run:
            self.estimator.fit(
                {"data": TrainingInput(s3_data=data_uri, input_mode="File")},
                wait=True
            )
        return self.estimator.latest_training_job.name
