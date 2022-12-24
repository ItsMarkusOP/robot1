import json
import os


def get_user_list(Config, key):
    with open('{}/zerotwobot/{}'.format(os.getcwd(), Config),
              'r') as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    TOKEN = "5210518952:AAH2AebGwebPOdiaHUdDbs7KckNREVJIYEo"
    OWNER_ID = int(2131857711) 
    JOIN_LOGGER = -1001151980503
    OWNER_USERNAME = "Awesome_RJ"
    ALLOW_CHATS = True
    DRAGONS = get_user_list('elevated_users.json', 'sudos')
    DEV_USERS = get_user_list('elevated_users.json', 'devs')
    EVENT_LOGS = -1001151980503
    WEBHOOK = False
    URL = None
    PORT = 5000
    CERT_PATH = None 
    API_ID = 991649
    API_HASH = "3c929d4c9c4ecb54d70bb425647fceaf"
    DONATION_LINK = "t.me/awesome_RJ"
    LOAD = []
    NO_LOAD = ['rss', 'cleaner', 'connection', 'math']
    DEL_CMDS = True
    STRICT_GBAN = True
    WORKERS = 8
    BAN_STICKER = "CAACAgQAAx0CU_rCTAABAczQXyBOv1TsVK4EfwnkCUT1H0GCkPQAAtwAAwEgTQaYsMtAltpEwhoE"
    ALLOW_EXCL = True
    TIME_API_KEY = "-HW6LQCYX43HS"
    WALL_API = "2795f44dad7746122baaa83d01db8541"
    SUPPORT_CHAT = "Black_Knights_Union_Support"
    INFOPIC = True
    TEMP_DOWNLOAD_LOC = "./" 
    DB_URI = "postgresql://betaur:DfFiJChWTPYN@75.119.132.150/betanm"
    BL_CHATS = []

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
