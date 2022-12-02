# TLOPO Launcher for multi-distribution launching.
#
# python 3.7
import apirequests
import downloader
import startgame
import getpass
import argparse

# TODO: Replace main with a GUI
def get_response(token=False):
    parser = argparse.ArgumentParser(description='TLOPO Launcher')
    # add username and password arguments
    parser.add_argument('-u', '--username', help='Username', required=False)
    parser.add_argument('-p', '--password', help='Password', required=False)
    args = parser.parse_args()
    # Input username and password store in data dict
    if args.username is None:
        username = input("Username: ")
    else:
        username = args.username
    if args.password is None:
        password = getpass.getpass('Password: ')
    else:
        password = args.password
    
    
    
    # If token requested then get that as well
    if token:
        gtoken = input("2FA Code: ")
        data = {'username': username,
                'password': password,
                'gtoken': gtoken}
    else:
        data = {'username': username,
                'password': password}

    # Create APIRequest object
    requester = apirequests.APIRequester()
    # Get version (test, dev, live)
    if username.find('@') != -1:
        ver = username[username.find('@')+1:]
    else:
        ver = 'live'

    # Pass username/password dict to the APIRequest
    return requester.get_login_response(data), ver


### GET RESPONSE TO LOGIN
# Login success code = 7
while True:
    response, version = get_response()
    print(response.get('message'))
    if response.get('status') == 7:
        break
    # Status 3 = 2FA
    elif response.get('status') == 3:
        response, version = get_response(token=True)
        # Check to make sure login success
        if response.get('status') == 7:
            break
        else:
            continue
    # Status 11 - Arrmor location verification
    elif response.get('status') == 11:
        print('Please check your email for "Arrmor" Verification.')
        continue
    else:
        continue

### VERIFY FILES/DOWNLOAD
downlder = downloader.Downloader(version)
downlder.start_download()

### START GAME
startgame.start_game(response, version)
