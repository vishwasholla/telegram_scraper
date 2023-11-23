import os
import configparser

class RaiseCustomExceptions(Exception):
    pass

class ConfigManage(RaiseCustomExceptions):
    def __init__(self):
        self.config_credential = configparser.ConfigParser()
        self.config_channel = configparser.ConfigParser()
        self.cwd = os.getcwd()
        self.config_path = os.path.join(self.cwd, 'telegram_automation.ini')
        self.config_credential.read(self.config_path)
        
        self.api_id = self.config_credential['telegram_automation']['api_id']
        self.api_hash = self.config_credential['telegram_automation']['api_hash']
        self.is_historical=self.config_credential['telegram_automation']['is_historical']
        self.start_date=self.config_credential['telegram_automation']['start_date']
        self.end_date=self.config_credential['telegram_automation']['end_date']
        
        self.credentials = {}
        self.channel = self.config_credential['telegram_automation']['channel']
        self.credentials['channel_name']=self.channel

        self.channel_list={}
    def solveException(self):
        allowed_keys = ['api_id', 'api_hash', 'channel','is_historical','start_date','end_date']
        for section in self.config_credential.sections():
            for key, value in self.config_credential.items(section):
                if key not in allowed_keys:
                    raise RaiseCustomExceptions(f'Kindly remove {key} from the telegram_automation.ini file')

    def get_channel_credentials(self):
        try:
            self.solveException()
            channel_details_file = os.path.join(self.cwd, 'channel_details.ini')
            with open(channel_details_file, 'r', encoding='utf-8') as file:
                self.config_channel.read_file(file)
                if self.channel in self.config_channel['channel']:
                    self.credentials['api_id']=self.api_id
                    self.credentials['api_hash']=self.api_hash
                    self.credentials['channel']=self.config_channel['channel'][self.channel]
                    self.credentials['is_historical']=self.is_historical
                    self.credentials['channel_name']=self.channel
                    self.credentials['start_date']=self.start_date
                    self.credentials['end_date']=self.end_date
                    
                    return self.credentials
                else:
                    raise EOFError(f'channel: {self.channel} not found in telegram_automation')
        except RaiseCustomExceptions as e:
            print(f"Exception occurred: {str(e)}")
    
    def get_channel_list(self):
        try:
            channel_details_file = os.path.join(self.cwd, 'channel_details.ini')
            with open(channel_details_file, 'r', encoding='utf-8') as file:
                self.config_channel.read_file(file)
                for key,value in self.config_channel['channel'].items():
                    self.channel_list[key]=value
            return self.channel_list
        except Exception as e:
            print(f'exception occured: {e}')