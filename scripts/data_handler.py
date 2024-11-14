import boto3


class HealthOmicsHandler:
    def __init__(self, region_name=None):
        self.omics = boto3.client("omics", region_name=region_name)

    def get_store_access(self, store_id, store_type="sequence"):
        """
        Get access info for either sequence or reference store

        Args:
            store_id (str): The ID of the store
            store_type (str): Either "sequence" or "reference"

        Returns:
            dict: Access information including URIs and ARNs
        """
        if store_type.lower() not in ["sequence", "reference"]:
            raise ValueError("store_type must be either 'sequence' or 'reference'")

        access_info = {}

        # Get store info based on type
        if store_type.lower() == "sequence":
            store_info = self.omics.get_sequence_store(id=store_id)
            data_suffix = "readSet/"

            access_info = {
                "store_type": store_type,
                "s3_uri": store_info["s3Access"]["s3Uri"],
                "s3_arn": store_info["s3Access"]["s3AccessPointArn"],
                "key_arn": store_info["sseConfig"]["keyArn"]
            }
        elif store_type.lower() == "reference":

            store_info = self.omics.get_reference_store(id=store_id)
            data_suffix = "reference/"

            """
            Get StreamingBody payload from s3 buckets using get_reference()
            Work in progress
            """


        # Add appropriate data URI based on store type
        access_info["data_uri"] = f"{access_info['s3_uri']}{data_suffix}"

        return access_info

    def get_iam_policy(self, s3_arn, key_arn):
        """
        Generate required IAM policy for store access

        Args:
            s3_arn (str): S3 access point ARN
            key_arn (str): KMS key ARN

        Returns:
            dict: IAM policy document
        """
        return {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "S3DirectAccess",
                    "Effect": "Allow",
                    "Action": ["s3:GetObject", "s3:ListBucket"],
                    "Resource": "*",
                    "Condition": {
                        "StringEquals": {
                            "s3:DataAccessPointArn": s3_arn
                        }
                    }
                },
                {
                    "Sid": "DefaultSequenceStoreKMSDecrypt",
                    "Effect": "Allow",
                    "Action": "kms:Decrypt",
                    "Resource": key_arn
                }
            ]
        }