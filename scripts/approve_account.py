import os
import sys

from googleapiclient.discovery import build

PROJECT_ID = os.environ['GOOGLE_CLOUD_PROJECT']

PROCUREMENT_API = 'cloudcommerceprocurement'


def _get_account_name(account_id):
    return 'providers/{}/accounts/{}'.format(PROJECT_ID, account_id)


def main(argv):
    """Main entrypoint to the Account approve tool."""

    if len(argv) != 2:
        print('Usage: python3 approve_account.py <account_id>')
        return

    account_id = argv[1]

    procurement = build(PROCUREMENT_API, 'v1', cache_discovery=False)
    account_name = _get_account_name(account_id)
    approve_request = procurement.providers().accounts().approve(
        name=account_name, body={'approvalName': 'signup'})
    approve_request.execute()


if __name__ == '__main__':
    main(sys.argv)
