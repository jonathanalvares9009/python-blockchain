from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA


def test_blockchain_instance():
    # It ensures that blockchain works as expected

    blockchain = Blockchain()

    assert blockchain.chain[0].hash == GENESIS_DATA['hash']


def test_add_block():
    # It checks if the add_block method works as expected

    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data
