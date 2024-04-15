import json

import pytest
import requests
from app.core.web3_utils.account import generate_random_string_from_clock
from app.core.web3_utils.ipfs import (get_ipfs_config, upload_binary,
                                      upload_dict, upload_file)
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3


def get_provider():
    return Web3(Web3.HTTPProvider(("http://127.0.0.1:8545/")))


@pytest.mark.skip(reason="we don't test web3 for now")
def test_tester_provider():
    w3 = get_provider()
    assert w3.isConnected()


@pytest.mark.skip(reason="we don't test web3 for now")
def test_balance():
    w3 = get_provider()
    address_0 = w3.eth.accounts[0]
    balance_0 = Web3.fromWei(w3.eth.get_balance(address_0), "ether")
    assert balance_0 < 10000, "balance does not match"


@pytest.mark.skip(reason="we don't test web3 for now")
def test_create_new_account():
    random_key = generate_random_string_from_clock()
    new_account: LocalAccount = Account.create(random_key)
    w3 = get_provider()
    assert w3.eth.get_balance(new_account.address) == 0, "new account is not empty"


def test_upload_and_fetch_image_ipfs():
    ipfs_config = get_ipfs_config()

    sample_image_file_path = "tests/samples/sample_1.jpg"
    hash_key, _, file_size = upload_file(sample_image_file_path, ipfs_config)
    assert hash_key, "hash key returned was empty.."
    assert file_size > 0, "file size returned is 0.."

    ipfs_url = f"{ipfs_config.host_address}{hash_key}"

    ipfs_data = requests.get(ipfs_url).content

    with open(sample_image_file_path, mode="rb") as file:
        file_data = file.read()

    assert ipfs_data == file_data, "uploaded file does not match local file"


def test_upload_and_fetch_json_ipfs():
    ipfs_config = get_ipfs_config()

    sent_dict = {"hello": "it's me"}
    hash_key = upload_dict(sent_dict, ipfs_config)
    assert hash_key, "hash key returned was empty.."

    ipfs_url = f"{ipfs_config.host_address}{hash_key}"

    ipfs_data = requests.get(ipfs_url).content

    retreived_dict = json.loads(ipfs_data.decode())

    assert retreived_dict == sent_dict, "retreived dict does not match initial dict"


def test_upload_binary_ipfs():
    ipfs_config = get_ipfs_config()

    sample_image_file_path = "tests/samples/sample_1.jpg"
    with open(sample_image_file_path, mode="rb") as file:
        file_data = file.read()

    hash_key, _, file_size = upload_binary(file_data, ipfs_config)
    assert hash_key, "hash key returned was empty.."
    assert file_size > 0, "file size returned is 0.."

    ipfs_url = f"{ipfs_config.host_address}{hash_key}"

    ipfs_data = requests.get(ipfs_url).content

    assert ipfs_data == file_data, "uploaded file does not match local file"


@pytest.mark.skip(reason="we don't test web3 for now")
def test_interact_with_contract():
    w3 = get_provider()
    on_limited_token_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
    minter_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    with open("contracts/ONLimitedNFT.sol/ONLimitedNFT.json", "r") as file:
        abi = json.load(file)["abi"]

    on_limited_token_contract = w3.eth.contract(address=on_limited_token_address, abi=abi)
    assert on_limited_token_contract.functions.balanceOf(minter_address).call() > 100000000000000000000000000


def test_create_nft():
    pass
