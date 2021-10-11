import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

PUBLISH_KEY = 'pub-c-726e6c5a-6932-4fba-99ee-808888c74bf4'

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-3373170c-de33-11eb-be2b-a639cde32e15'
pnconfig.publish_key = 'pub-c-726e6c5a-6932-4fba-99ee-808888c74bf4'

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}


class Listener(SubscribeCallback):

    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message):
        print(f'\n-- Channel: {message.channel} | Message : {message.message}')

        if message.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print('\n -- Successfully replaced chain')
            except Exception as e:
                print(f"\n -- Did not replace chain: {e}")

        elif message.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n -- Set the new transaction in the transaction pool')


class PubSub():
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between the nodes of the blockchain network.
    """

    def __init__(self, blockchain, transaction_pool):
        self.pubnub = pubnub = PubNub(pnconfig)
        pubnub.subscribe().channels(CHANNELS.values()).execute()
        pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, data):
        """
        Publish the message object to the channel.
        """
        self.pubnub.publish().channel(
            channel).message(data).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block to all nodes.
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_transacion(self, transaction):
        """
        Broadcast transaction to all nodes.
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())


def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})


if __name__ == '__main__':
    main()
