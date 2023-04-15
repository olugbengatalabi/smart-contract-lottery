from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time



def deploy_lottery():
  print("started")
  account = get_account()
  print("account gotten")
  print(f"{account} is the account")
  fees = config["networks"][network.show_active()]["fee"]
  keys = config["networks"][network.show_active()]["keyhash"]
  print(f"type of  {fees} is {type(fees)}")
  print(f"type of  {keys} is {type(keys)}")
  
  """
  you were getting error cannot convert str type e to wei..
  in site packages, normalize.py, it takes the different inputs and try to get their type.
  
  the fee should be an integer for it to be convertible to wei
  
  
  """
  lottery = Lottery.deploy(
    get_contract("eth_usd_price_feed").address,
    get_contract("vrf_coordinator").address,
    get_contract("link_token").address,
    config["networks"][network.show_active()]["fee"],
    config["networks"][network.show_active()]["keyhash"],
    {"from": account}, 
    publish_source= False,
    # meaning get the verify key, if not specified default to falso
  )
  
  print("deployed lottery!")
  return lottery

def start_lottery():
  account = get_account()
  lottery = Lottery[-1]
  starting_tx = lottery.startLottery({"from": account})
  
  starting_tx.wait(1)
  print("lottery started")
  
def enter_lottery():
  account = get_account()
  lottery = Lottery[-1]
  value = lottery.getEntranceFee() + 10000000
  tx = lottery.enter({"from":account, "value": value})
  tx.wait(1)
  print("you entered the lottery")
  
def end_lottery():
  account = get_account()
  lottery = Lottery[-1]
  tx = fund_with_link((lottery.address))
  tx.wait(1)
  ending_tx = lottery.endLottery({"from":account})
  ending_tx.wait()
  time.sleep()
  print(f"{lottery.recentWinner()} is the new winner!" )

def main():
  deploy_lottery()
  start_lottery()
  enter_lottery()