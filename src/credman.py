from getpass import getpass
import argparse

from passman import Passman
from storage import Storage

CRED_SALT = b'ed\xd9\xf1+\x07\xa7K|\n)6YgUy'
CRED_FILENAME = "~/creds.db"
storage = Storage(CRED_FILENAME)
passman_instance: Passman


def get(key: str) -> str:
    pwd = passman_instance.get_password(key)
    return pwd


def add(key: str, password: str):
    passman_instance.set_password(key, password)
    passman_instance.save()


def delete(key: str):
    passman_instance.delete_password(key)
    passman_instance.save()


def update(key: str, password: str):
    passman_instance.set_password(key, password)
    passman_instance.save()


def update_master(old_pwd: str, new_pwd: str):
    passman_instance.load(old_pwd)
    passman_instance.save(new_pwd)


def main():
    parser = argparse.ArgumentParser(description="Password manager for command line")
    parser.add_argument('operation',
                        help='Operation',
                        type=str.lower,
                        choices=['get', 'add', 'delete', 'update', 'update-master'])
    parser.add_argument('application',
                        help='Application key for password',
                        type=str.lower)
    parser.add_argument('--password',
                        help='Password value',
                        dest='password',
                        type=str,
                        default='not_set',
                        required=False)

    args = parser.parse_args()

    master_pass = getpass("Master password:")

    global passman_instance
    passman_instance = Passman(storage, CRED_SALT, master_pass)

    if args.operation == 'get':
        print(get(args.application))
    elif args.operation == 'add':
        if args.password == 'not_set':
            print('Password is required')
            exit(1)
        else:
            add(args.application, args.password)
    elif args.operation == 'delete':
        delete(args.application)
    elif args.operation == 'update':
        if args.password == 'not_set':
            print('Password is required')
            exit(1)
        else:
            update(args.application, args.password)
    elif args.operation == 'update-master':
        password = getpass("New master password:")
        update_master(master_pass, password)


if __name__ == '__main__':
    main()
