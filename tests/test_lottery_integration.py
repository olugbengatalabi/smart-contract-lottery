from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link
from scripts.deploy_lottery import deploy_lottery
import pytest
import time



def test_can_pick_winner():
  if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    pytest.skip()
  lottery = deploy_lottery()
  account= get_account()
  lottery.startLottery({"from": account})
  lottery.enter_lottery({"from": account, "value": lottery.getEntranceFee() + 100})
  lottery.enter_lottery({"from": account, "value": lottery.getEntranceFee() + 100})
  fund_with_link(lottery)
  lottery.endLottery({"from": account})
  time.sleep(60)
  assert lottery.recentWinner() == account
  assert lottery.balance() == 0
  
  # only the admin account can stop the lottery