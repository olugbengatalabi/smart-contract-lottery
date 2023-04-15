# expecting
from brownie import Lottery, accounts, config, network
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3

def test_get_entrance_fee():
    # arrange
    lottery = deploy_lottery()
    #act
    # using 2000 usd/eth
    # entrance fee is $50 so 0.025eth
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    # assert
    assert expected_entrance_fee == entrance_fee
    