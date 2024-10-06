import parse

# Back4App credentials
APP_ID = "bYNyGAipvbuFrdu1jv3ucNYxjCDlzioPlHE3QiBN"
CLIENT_KEY = "CgBOi7Np3DT1elVimuJ642L4jLvyBffLtnYLt4wT"
MASTER_KEY = "q5QLq9jKAUPRbrswNmvZYfh875TBdjWlASntqoBV"

def initialize_back4app():
    # Initialize Parse
    parse.init(APP_ID, CLIENT_KEY, master_key=MASTER_KEY)
