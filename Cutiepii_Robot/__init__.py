import logging
import os
import platform
import sys
import time
import asyncio
import telegram.ext as tg
import random

from pyrogram import Client, errors
from pyrogram.enums import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.sessions import StringSession
from motor import motor_asyncio
from odmantic import AIOEngine
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from redis import StrictRedis
from Python_ARQ import ARQ
from aiohttp import ClientSession
from telegraph import Telegraph
from telegram import Chat
from httpx import AsyncClient, Timeout
from ptbcontrib.postgres_persistence import PostgresPersistence


from telegram.ext import Application
from telegram.error import BadRequest, Forbidden
from telegram import __bot_api_version__, __version__ as ptb_version
from dotenv import load_dotenv

load_dotenv()
StartTime = time.time()

# enable logging
FORMAT = "[CUTIEPII ROBOT] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("LOGGER.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

# if version < 3.9, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 9:
    LOGGER.error(
        "You MUST have a python version of at least 3.9! Multiple features depend on this. Bot quitting.",
    )
    quit(1)

ENV = bool(os.environ.get("ENV", False))
BOT_VERSION = "2.3"
PTB_VERSION = ptb_version
BOT_API_VERSION = __bot_api_version__
PYTHON_VERSION = platform.python_version()

if ENV:
    TOKEN = os.environ.get("TOKEN", None)

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get("INFOPIC", False))
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get("API_ID", None)
    API_HASH = os.environ.get("API_HASH", None)
    DONATION_LINK = os.environ.get("DONATION_LINK")
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation rss cleaner connection math").split()
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))
    WORKERS = int(os.environ.get("WORKERS", 8))
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAACAgUAAxkBAAEDRNJhjolhBDkOeJLs2cPuhskKthnoQwACFwIAAs4DwFWTjimU8iDvqiIE")
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    AI_API_KEY = os.environ.get("AI_API_KEY", None)
    WALL_API = os.environ.get("WALL_API", None)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)

    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    DB_URI = os.environ.get("DATABASE_URL")

    if DB_URI.startswith("postgres://"):
        DB_URI = DB_URI.replace("postgres://", "postgresql://")
    
    TEMP_DOWNLOAD_LOC = os.environ.get("TEMP_DOWNLOAD_LOC", None)


    try:
        BL_CHATS = set(int(x) for x in os.environ.get("BL_CHATS", "").split())
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

else:
    from Cutiepii_Robot.config import Development as Config
    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME
    ALLOW_CHATS = Config.ALLOW_CHATS
    try:
        DRAGONS = set(int(x) for x in Config.DRAGONS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    EVENT_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    TIME_API_KEY = Config.TIME_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    INFOPIC = Config.INFOPIC
    TEMP_DOWNLOAD_LOC = Config.TEMP_DOWNLOAD_LOC
    DB_URI = Config.DB_URI

    if DB_URI.startswith("postgres://"):
        DB_URI = DB_URI.replace("postgres://", "postgresql://")

    try:
        BL_CHATS = set(int(x) for x in Config.BL_CHATS or [])
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")
        
DEV_USERS.add(OWNER_ID)
ALIVE_TEXT = [
    "Hey developer's I'm online now.",
    "Hey fellas how ya doing",
    "Woah this day going to be so good!",
    "Wait guys I'm not dead yet, so count me in",
    "Sending alive message became my hobby, here goes another one",
    "What a worst day! Hey guys, How ya doing",
    "Somebody help, this server is killing me"
]

LOGGER.debug("[CUTIEPII]: Telegraph Installing")
telegraph = Telegraph()
LOGGER.debug("[CUTIEPII]: Telegraph Account Creating")
telegraph.create_account(short_name="Cutiepii")

telethn = TelegramClient(MemorySession(), API_ID, API_HASH)
PyroGram = TOKEN.split(":")[0]
pgram = Client(
    name=PyroGram,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    workers=min(32, os.cpu_count() + 4),
    parse_mode=ParseMode.DEFAULT,
    workdir=DOWNLOAD_DIRECTORY,
    sleep_threshold=60,
    in_memory=True,
)

LOGGER.debug("[CUTIEPII]: Connecting To Y??ki ??? Data Center ??? Mumbai ??? MongoDB Database")
mongodb = MongoClient(MONGO_DB_URL, 27017)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
db = motor[MONGO_DB]
engine = AIOEngine(motor, MONGO_DB)
LOGGER.debug("[INFO]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
# ARQ Client
LOGGER.debug("[INFO]: INITIALIZING ARQ CLIENT")
arq = ARQ("arq.hamker.dev", "ERUOGT-KHSTDT-RUYZKQ-FZNSHO-ARQ", aiohttpsession)
LOGGER.debug("[CUTIEPII]: Connecting To Y??ki ??? Data Center ??? Mumbai ??? PostgreSQL Database")
ubot = TelegramClient(StringSession(STRING_SESSION), APP_ID, APP_HASH)
LOGGER.debug("[CUTIEPII]: Connecting To Y??ki ??? Cutiepii Userbot (https://telegram.dog/Awesome_Cutiepii)")
timeout = Timeout(40)
http = AsyncClient(http2=True, timeout=timeout)

async def post_init(application: Application):
    try:
        await application.bot.sendMessage(-1001151980503, random.choice(ALIVE_TEXT))
    except Forbidden:
        LOGGER.warning(
            "Bot isn't able to send message to support_chat, go and check!",
        )
    except BadRequest as e:
        LOGGER.warning(e.message)

application = Application.builder().token(TOKEN).post_init(post_init).build()
asyncio.get_event_loop().run_until_complete(application.bot.initialize())

DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)


# Load at end to ensure all prev variables have been set
from Cutiepii_Robot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
)

# make sure the regex handler can take extra kwargs
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
