from brownie import network, accounts, config, MockV3Aggregator, VRFCoordinatorMock, LinkToken, Contract, interface
from web3 import Web3


FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "maiinnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    'development', "ganache-local", "ganache-locale"]


def get_account(index = None, id=None):
  print("get account called")
  if index:
    return accounts[index]
  if id:
    return accounts.load(id)
  
  if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
    print("network in local blockchain enviroment")
    return accounts[0] 
  return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {
  "eth_usd_price_feed": MockV3Aggregator,
  "vrf_coordinator": VRFCoordinatorMock,
  "link_token": LinkToken,
  
  
  }
def get_contract(contract_name):
  """
    this function will grab the contract addresses from the brownie config, if defined otherwise it will deploy a mock version of that contract, and return that mock contract
    
    Args: contract_namem (string)
    
    returns:
      brownie.network.contract.ProjectContract: The most recently deployed version of this contract.
    """
  print("get contract called")
  contract_type = contract_to_mock[contract_name]
  if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    if len(contract_type) <= 0:
      # mockV3aggregator. lenght
      deploy_mocks()
      # you need to deploy mock when using local environments like ganache-local 
    contract = contract_type[-1]
    # more likw movkV3Aggregator[-1]
  else:
    # when deploying to a testnet/ we are on a real network
    contract_address = config["networks"][network.show_action()][contract_name]
    #address and abi needed
    contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    # basically MockV3Aggregator.abi
  print("contract returned")
  return contract
  
     
DECIMALS = 8
INITIAL_VALUE =  200000000000

def deploy_mocks(decimals = DECIMALS, initial_value = INITIAL_VALUE):
  print("deploy mocks called")
  account = get_account()
  mock_price_feed = MockV3Aggregator.deploy(decimals, initial_value, {"from":account})
  link_token = LinkToken.deploy({"from":account})
  VRFCoordinatorMock.deploy(link_token.address, {"from":account})
  print("deployed")
  
  
def fund_with_link(contract_address, account = None, link_token = None, amount = 100000000000000000):
  account = account if account else get_account()
  link_token = link_token if link_token else get_contract("link_token")
  tx = link_token.transfer(contract_address, amount, {"from":account})
  # link_token_contract= interface.LinkTokenInterFace(link_token.address)
  # tx =link_token_contract.transfer(contract_address, amount, {"from":account})
  tx.wait(1)
  print("fund contract")
  return tx