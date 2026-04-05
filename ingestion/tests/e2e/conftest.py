import os
from typing import Generator, Any

import pytest
import boto3
from mypy_boto3_s3.client import S3Client
from moto import mock_aws


@pytest.fixture
def aws_credentials() -> None:
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture
def mocked_aws(aws_credentials: None) -> Generator[None, Any, None]:
    with mock_aws():
        yield


@pytest.fixture
def s3(mocked_aws) -> S3Client:
    return boto3.client("s3", region_name="us-east-1")


@pytest.fixture
def create_archive_bucket(s3) -> None:
    s3.create_bucket(Bucket="archive")
