import sys
import uuid

from database import JsonDatabase


def _generate_internal_account_id():
    # TODO: Replace with whatever ID generation code already exists.
    return str(uuid.uuid4())


def main(argv):
    """Main entrypoint to the integration with the Procurement Service."""

    if len(argv) != 2:
        print('Usage: python3 reset_account.py <account_id>')
        return

    account_id = argv[1]
    internal_id = _generate_internal_account_id()

    customer = {
        'procurement_account_id': account_id,
        'internal_account_id': internal_id,
        'products': {}
    }

    database = JsonDatabase()

    database.write(account_id, customer)


if __name__ == '__main__':
    main(sys.argv)
