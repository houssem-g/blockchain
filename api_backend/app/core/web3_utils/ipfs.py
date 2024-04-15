import os
from dataclasses import dataclass
from typing import Any, Dict, Union
from warnings import warn

import ipfshttpclient  # type: ignore
import yaml
from ipfshttpclient.client.base import ResponseBase  # type: ignore


@dataclass
class IpfsConfig:
    server_address: str
    host_address: str
    project_id: Union[str, None] = None
    secret: Union[str, None] = None

    @classmethod
    def load_yaml(cls, yaml_path: str):
        with open(yaml_path, "r") as file:
            config: Dict[str, str] = yaml.safe_load(file)

        return cls(**config)

    def get_auth(self):
        if self.project_id is not None and self.secret is not None:
            return (self.project_id, self.secret)
        return None


def get_ipfs_config() -> IpfsConfig:
    ipfs_config_dict: Dict[str, Any] = {
        "server_address": os.environ.get("IPFS_SERVER_ADDRESS"),
        "host_address": os.environ.get("IPFS_HOST_ADDRESS"),
        "project_id": os.environ.get("IPFS_PROJECT_ID", None),
        "secret": os.environ.get("IPFS_SECRET", None),

    }
    return IpfsConfig(**ipfs_config_dict)


def upload_binary(binary: bytes, ipfs_config: IpfsConfig):
    """
    returns hash_key, file_name, file_size
    """
    file_name, file_size = "", 0

    client = ipfshttpclient.connect(ipfs_config.server_address, auth=ipfs_config.get_auth())
    hash_key: str = client.add_bytes(binary)
    client.close()
    file_size = len(binary)

    return hash_key, file_name, file_size


def upload_file(file_path: str, ipfs_config: IpfsConfig):
    """
    returns hash_key, file_name, file_size
    """
    hash_key, file_name, file_size = "", "", 0

    if os.path.isfile(file_path):
        client = ipfshttpclient.connect(ipfs_config.server_address, auth=ipfs_config.get_auth())
        response = client.add(file_path)
        client.close()

        if isinstance(response, ResponseBase):
            hash_key, file_name, file_size = parse_base_response(response)
        elif isinstance(response, list):
            warn("this function handles only one file at a time..")

        else:
            warn(f"unrecognized response: {response}")
    else:
        warn(f"file path {file_path} does not exist..")

    return hash_key, file_name, file_size


def upload_dict(dict_to_send: Dict[str, str], ipfs_config: IpfsConfig):
    hash_key: str = ""

    assert isinstance(dict_to_send, dict), "can only send dict data.."

    client = ipfshttpclient.connect(ipfs_config.server_address, auth=ipfs_config.get_auth())
    hash_key = client.add_json(dict_to_send)
    client.close()

    return hash_key


def parse_base_response(response: ResponseBase):
    if isinstance(response, ResponseBase):
        file_name = str(response.get("Name"))
        hash_key = str(response.get("Hash"))
        file_size = int(str(response.get("Size")))
        return hash_key, file_name, file_size
