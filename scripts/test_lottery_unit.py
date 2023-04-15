# expecting
from brownie import Lottery, accounts, config, network
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link, get_contract
from web3 import Web3
import pytest

def test_get_entrance_fee():
    # arrange
    lottery = deploy_lottery()
    #act
    # using 2000 usd/eth
    # entrance fee is $50 so 0.025eth
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    print(expected_entrance_fee)
    print(entrance_fee)
    # assert
    assert expected_entrance_fee == entrance_fee
    
    # ? current problem is that expected_entrance fee u
    # ? exp_entrance_fee = 25000000000000000 while
    # ? ____entrance_fee = 250000000000000000

def test_can_pick_winner_correctly():
    # arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from": account, "value":lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value":lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value":lottery.getEntranceFee()})
    fund_with_link(lottery)
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STARTING_RND = 777
    get_contract("vrf_coordinator").callBackWithRandomness(request_id, STARTING_RND, lottery.address, {"from":account} )
    
    starting_balance_of_account = account.balance()
    print(f"initial account balance of the winner is {starting_balance_of_account}")
    balance_of_lottery = lottery.balance()
    print(
        f"initial account balance of the lottery is {lottery.balance()}")
    # 777 % 3
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery 
    
    
    
def main():
    test_can_pick_winner_correctly()
    
    