import os
from typing import Generator

import pytest
import boto3
from mypy_boto3_s3.client import S3Client
from moto import mock_aws

from tests.e2e.constants import ARCHIVE_BUCKET_NAME


@pytest.fixture
def aws_region() -> str:
    return "us-east-1"


@pytest.fixture
def aws_credentials(aws_region: str) -> None:
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = aws_region


@pytest.fixture
def mocked_aws(aws_credentials: None) -> Generator[None]:
    with mock_aws():
        yield


@pytest.fixture
def s3_client(mocked_aws: None, aws_region: str) -> S3Client:
    return boto3.client("s3", region_name=aws_region)


@pytest.fixture
def create_archive_bucket(s3_client: S3Client) -> None:
    s3_client.create_bucket(Bucket=ARCHIVE_BUCKET_NAME)
