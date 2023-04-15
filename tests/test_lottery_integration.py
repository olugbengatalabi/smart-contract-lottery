from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS

def test_can_pick_winner():
  if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS