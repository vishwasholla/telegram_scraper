## client get historical message scraping###
# testing historical data--client
import configparser
import json
import asyncio
import datetime
# from datetime import date, datetime
import pytz
import os
import time
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)
import pandas
from telethon import events
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputPeerChannel
from telethon.tl import functions, types
import re
import pandas as pd
from match_pattern import FindMatch
from config_channel import ConfigManage


def date_format(date):
    date=str(date).strip()
    try:
        date_obj = datetime.datetime.strptime(date, "%Y/%m/%d").date()
        return date_obj
    except:
        raise Exception('invalid date format, valid date format(yyyy/mm/dd)')
    finally:
        print(date)

    
    
def get_config():
    config_manager = ConfigManage()
    if not config_manager.solveException():
        credentials = config_manager.get_channel_credentials()
        if credentials:
            return credentials
        else:
            return None
        
def get_config_channel():
    config_manager = ConfigManage()
    credentials = config_manager.get_channel_list()
    if credentials:
        print(f'credentials::{credentials}')
        return credentials
    else:
        print('no')
        return None


def save_messages_to_excel(df,username):
    file_name = f'bot_{username}.xlsx'
    cwd = os.getcwd()
    file_path=os.path.join(cwd,'excel',file_name)
    # file_path = os.path.abspath(file_name)
    excel_dir = os.path.join(cwd, 'excel')
    if not os.path.exists(excel_dir):
        os.makedirs(excel_dir)
        
    if os.path.exists(file_path):
        os.remove(file_path)
    df.to_excel(file_path, index=False)
    print(f"Data saved to '{file_name}'")


class GetChatId():
    def get_channel():
        cwd = os.getcwd()
        channel_details_file = os.path.join(cwd,'channel_details.txt')
        file_path = channel_details_file

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                contents = file.read()
                print(contents)
        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        except IOError as e:
            print(f"An error occurred while reading the file: {str(e)}")


async def live_message(client,channel_list):
    @client.on(events.NewMessage())
    async def handle(event):
        entity = await client.get_entity(event.chat_id)
        channel_name = entity.title
        if channel_name == channel_list['channel_one']:
            try:
                grp_four_obj = FindMatch(message=event.message.message)
                matched_data = grp_four_obj.p1_match()
                print(matched_data)
            except Exception as e:
                print(e)
        if channel_name == channel_list['channel_two']:
            try:
                grp_four_obj = FindMatch(message=event.message.message)
                matched_data = grp_four_obj.p2_match() 
                print(matched_data)
            except Exception as e:
                print(e)
        if channel_name == channel_list['channel_three']:
            try:
                grp_four_obj = FindMatch(message=event.message.message)
                matched_data = grp_four_obj.p3_match() 
                print(matched_data)
            except Exception as e:
                print(e)
        if channel_name == channel_list['channel_four']:
            try:
                grp_four_obj = FindMatch(message=event.message.message)
                matched_data = grp_four_obj.p4_match() 
                print(matched_data)
            except Exception as e:
                print(e)
        if channel_name == channel_list['channel_five']:
            try:
                grp_four_obj = FindMatch(message=event.message.message)
                matched_data = grp_four_obj.p5_match() 
                print(matched_data)
            except Exception as e:
                print(e)
    await client.run_until_disconnected()

async def historical(channel,client,channel_name,start_date,end_date):
    dialogs = await client.get_dialogs()
    today = datetime.datetime.today().date()
    yesterday = today - datetime.timedelta(days=1)
    print(yesterday)
    for dialog in dialogs:
        if dialog.is_channel:
            username = channel_name + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            if channel == dialog.title:
                channel_entity = dialog.entity
                messages = await client.get_messages(channel_entity, limit=500)
                filtered_messages = [message for message in messages if start_date<=message.date.date()<=end_date]
                msgcoll=list()
                for message in filtered_messages:
                    data={}
                    if channel_name == 'channel_one':
                        try:
                            grp_four_obj = FindMatch(message=message.text)
                            matched_data = grp_four_obj.p1_match()
                        except Exception as e:
                            print(e)
                            continue
                    if channel_name == 'channel_two':
                        try:
                            grp_four_obj = FindMatch(message=message.text)
                            matched_data = grp_four_obj.p2_match() 
                        except Exception as e:
                            print(e)
                            continue
                    if channel_name == 'channel_three':
                        try:
                            grp_four_obj = FindMatch(message=message.text)
                            matched_data = grp_four_obj.p3_match() 
                        except Exception as e:
                            print(e)
                            continue
                    if channel_name == 'channel_four':
                        try:
                            grp_four_obj = FindMatch(message=message.text)
                            matched_data = grp_four_obj.p4_match() 
                        except Exception as e:
                            print(e)
                            continue
                    if channel_name == 'channel_five':
                        try:
                            grp_four_obj = FindMatch(message=message.text)
                            matched_data = grp_four_obj.p5_match() 
                        except Exception as e:
                            print(e)
                            continue
                    created_at = message.date.strftime('%Y-%m-%d %H:%M:%S')
                    matched_data['created_at'] = created_at
                    t_series_data = matched_data.get('t_series', {}) 
                    t_temp = t_series_data
                    del t_series_data
                    data['pair'] = matched_data.get('pair', '')
                    data['position'] = matched_data.get('position','')
                    data['entry'] = matched_data.get('entry','')
                    data['entryAverage'] = matched_data.get('entryAverage','')
                    data['t_series'] = t_temp.copy()
                    data['stopLoss'] = matched_data.get('stopLoss','')
                    data['created_at'] = created_at
                    del matched_data
                    msgcoll.append(data)
                    del grp_four_obj
                    del data
                df = pd.DataFrame(msgcoll)
                save_messages_to_excel(df,username)
                break


if __name__ == '__main__':
    import asyncio
    # try:
    config = get_config()
    config_channel = get_config_channel()
    channel = config['channel']
    is_historical = config['is_historical']
    channel_name=config['channel_name']
    api_id = config['api_id']
    api_hash = config['api_hash']
    cwd = os.getcwd()
    utc_plus_3 = pytz.timezone('Etc/GMT-3')
    session_file_location = os.path.join(cwd,'session_name_here.session')
    with TelegramClient(session_file_location, api_id, api_hash) as client:
        loop = asyncio.get_event_loop()
        if is_historical.lower() == 'true':
            if config:
                get_start_date=config['start_date']
                get_end_date=config['end_date']
                start_date = utc_plus_3.localize(datetime.datetime.strptime(get_start_date, "%Y/%m/%d")).date()
                end_date = utc_plus_3.localize(datetime.datetime.strptime(get_end_date, "%Y/%m/%d").replace(hour=23, minute=59, second=59)).date()
                loop.run_until_complete(historical(channel,client,channel_name,start_date,end_date))
            else:
                raise Exception('credentials not found')
        elif is_historical.lower() == 'false':
            if config_channel:
                print('excuting live messages')
                for channel in config_channel:
                    channel_list = config_channel
                loop.run_until_complete(live_message(client,channel_list))
            else:
                raise Exception('channel list not found')
        else:
            raise Exception('could not find valid start and end date')

