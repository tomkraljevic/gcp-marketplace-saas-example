import json
import os
import pprint
import sys

from google.cloud import pubsub_v1

PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT']

PUBSUB_SUBSCRIPTION = os.environ['H2O_PUBLIC_SUBSCRIPTION_ID']


g_message_sequence_num = 0


def main(argv):
    """Main entrypoint to the integration with the Procurement Service."""

    # Get the subscription object in order to perform actions on it.
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID,
                                                     PUBSUB_SUBSCRIPTION)

    def callback(message):
        """Callback for handling Cloud Pub/Sub messages."""
        global g_message_sequence_num
        g_message_sequence_num += 1
        message_sequence_num = g_message_sequence_num

        payload = json.loads(message.data)

        print('Received message:  Sequence number {}'.format(message_sequence_num))
        pprint.pprint(payload)
        print()

        print("TOM: Attempting to NACK sequence number {}".format(message_sequence_num))
        message.nack()
        print("TOM: NACK sequence number {}".format(message_sequence_num))

    subscription = subscriber.subscribe(subscription_path, callback=callback)

    print('Listening for messages on {}'.format(subscription_path))
    print('Exit with Ctrl-\\')

    while True:
        try:
            subscription.result()
        except Exception as exception:
            print('Listening for messages on {} threw an Exception: {}.'.format(
                subscription_path, exception))


if __name__ == '__main__':
    main(sys.argv)
