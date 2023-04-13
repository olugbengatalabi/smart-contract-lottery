# expecting
from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    print(config["networks"][network.show_active()][0])
    lottery = Lottery.deploy(
        config["networks"][network.show_active()][0],
        {"from": account},
    )
 
    assert lottery.getEntranceFee() > Web3.toWei(0.018, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.022, "ether")