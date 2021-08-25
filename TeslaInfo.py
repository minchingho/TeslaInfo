
import argparse
import getpass
from teslapy import Product, Tesla, Vehicle

def main():
    parser = argparse.ArgumentParser(description='Tesla Info CLI')
    parser.add_argument('-u', dest='email', help='login email', required=True)
    parser.add_argument('-p', dest='password', help='login password')

    args = parser.parse_args()

    if args.password == None:
        password = getpass.getpass('Password: ')
    else:
        password = args.password

    with Tesla(args.email, password) as tesla:
        tesla.fetch_token()
        selected = tesla.vehicle_list()

        for i, product in enumerate(selected):
            print('product %d:', i)
            print(product)

if __name__ == "__main__":
    main()