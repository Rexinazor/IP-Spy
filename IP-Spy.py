import requests
import json
import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN 
#edit config.py for self host
from functools import partial
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

command = partial(filters.command, prefixes=["!", "/"])

start_text = f"Hey, Thanks for selecting me, I can help you in getting details of an IP\n**Syntax:** `/ip [ip]`\n\nA bot by @Hazard_Bots"

app = Client("IP-Spy", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(command("start"))
async def start(_, message):
    keyboard = InlineKeyboardMarkup(
        [ 
            [
                InlineKeyboardButton(
                    text="Support", url="https://t.me/HazardBot_Support"
                ),
                InlineKeyboardButton(
                    text="Creator", url="https://t.me/ZenoByte"
                )
            ]
        ]
    )
    await message.reply_text(start_text, reply_markup=keyboard)
    
@app.on_message(command("help"))
async def help(_, message):
    await message.reply_text("Use the Following Syntax\n/ip [ip], Commands starts with either / or !. Report Errors in @HazardBot_Support")
    

@app.on_message(command("ip"))
async def ip(_, message): 
    searchip = message.text.split(" ", 1)
    if len(searchip) == 1:
        await message.reply_text("**Usage:**\n/ip [ip]")
        return
    else:
        searchip = searchip[1]
        m = await message.reply_text("Searching...")
    try:
        url = requests.get(f"http://ip-api.com/json/{searchip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query")
        response = json.loads(url.text)
        text = f"""
**IP Address:** `{response['query']}`
**Status:** `{response['status']}`
**Continent Code:** `{response['continentCode']}`
**Country:** `{response['country']}`
**Country Code :** `{response['countryCode']}`
**Region:** `{response['region']}`
**Region Name :** `{response['regionName']}`
**City:** `{response['city']}`
**District:** `{response['district']}`
**ZIP:** `{response['zip']}`
**Latitude:** `{response['lat']}`
**Longitude:** `{response['lon']}`
**Time Zone:** `{response['timezone']}`
**Offset:** `{response['offset']}`
**Currency:** `{response['currency']}`
**ISP:** `{response['isp']}`
**Org:** `{response['org']}`
**As:** `{response['as']}`
**Asname:** `{response['asname']}`
**Reverse:** `{response['reverse']}`
**User is on Mobile:** `{response['mobile']}`
**Proxy:** `{response['proxy']}`
**Hosting:** `{response['hosting']}`"""
        await m.edit_text(text, parse_mode="markdown")
    except:
        await m.edit_text("Unable To Find Info!")


app.run()
