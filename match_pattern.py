import re
class FindMatch():
    def __init__(self,message='',matches_split=[],pair='',position='',entry='',entryAverage='',t_series={},stopLoss='',created_at=0):
        self.message =message
        self.matches_split = matches_split
        self.pair = pair
        self.position= position
        self.entry=entry
        self.entryAverage=entryAverage
        self.t_series = t_series
        self.stopLoss=stopLoss
        self.created_at=created_at
    def contains_float(self,number):
        pattern = r'[-+]?\d*\.\d+|\d+\.\d*'  # Regex pattern for floating-point numbers

        if re.search(pattern, number):
            return True
        else:
            return False
    def p1_match(self):
        def check_ascii(matches_split):
            new_list=[]
            char = ''
            for item in matches_split:
                item = re.sub(':','',item)
                if not item.isascii():
                    ascii_text = re.sub(r'[^\x00-\x7F]+', '', item)
                    if ascii_text != '':
                        char = ascii_text
                    else:
                        continue
                else:
                    char = item
                if item not in ('loss','',' '):
                    new_list.append(char)
            return new_list
        matched_data={}
        self.matches_split = re.split(r'[\n\s]+',self.message)
        self.matches_split=list(map(lambda x:x.lower(),self.matches_split))
        self.matches_split=check_ascii(self.matches_split)
        #pair
        self.pair = self.matches_split[0].strip()
        #entry
        entry_pattern = re.compile(r'(\b\d+.\d*\s*-\s*\d+.\d*)')
        self.entry = entry_pattern.search(self.message).group()
        entries = re.findall(r'(\b\d+.\d+\b)\s*-\s*(\b\d+.\d+\b)', self.message)
        #entry average
        entry_start, entry_end = entries[0]  # Use the first matched entry if available
        self.entryAverage = "{:.5f}".format((float(entry_start) + float(entry_end)) / 2)
        #target
        if 'target' in self.matches_split:
            start_index = self.matches_split.index('target')
        elif 'targets' in self.matches_split:
            start_index = self.matches_split.index('targets')
        else:
            raise ValueError('target does not exist')
        start_index=start_index+1
        i=1
        for target in self.matches_split[start_index:]:
            if self.contains_float(target):
                self.t_series[f't{i}'] = target
                i=i+1
        self.position = 'LONG' if self.t_series.get('t1','')>entry_end else 'SHORT'
        try:
            loss_index = self.matches_split.index("stop")
            loss_index=loss_index+1
            self.stopLoss = self.matches_split[loss_index]
            print(f'stopLoss:{self.stopLoss}')
        except Exception as e:
            self.stopLoss = ''
            print(e)
        matched_data = {'matches_split':self.matches_split ,
        'pair':self.pair,
        'position':self.position,
        'entry':self.entry,
        'entryAverage':self.entryAverage,
        't_series':self.t_series,
        'stopLoss':self.stopLoss,
        'created_at':self.created_at}
        return matched_data
    
    def p2_match(self):
        def check_ascii(matches_split):
            new_list=[]
            char = ''
            for item in matches_split:
                item = re.sub(r'[:!@$%,]','',item)
                if not item.isascii():
                    ascii_text = re.sub(r'[^\x00-\x7F]+', '', item)
                    if ascii_text != '':
                        char = ascii_text
                    else:
                        continue
                else:
                    char = item
                if item not in ('loss','',' '):
                    new_list.append(char)
            return new_list
        
        def get_list():
            # print(self.message)
            matches_split = re.split(r'[\n\s-]+',self.message)
            matches_split=list(map(lambda x:x.strip().lower(),matches_split))
            self.matches_split = check_ascii(matches_split)

        def find_pattern():
            get_list()
            # print(f'matches::{self.matches_split}')
            for item in self.matches_split:
                if item.startswith('#'):
                    # print('startswith')
                    self.pair = item.replace('#','')
                    break
            else:
                #use regex
                pair_pattern = re.compile(r'(\w+ / \w+)')
                self.pair = pair_pattern.search(self.message).group()
            # print(f'pair::{self.pair}')
            #entry
            if 'entry' in self.matches_split:
                entry_index = self.matches_split.index('entry')
                entry_start=self.matches_split[entry_index+1]
                entry_end=self.matches_split[entry_index+2]
                self.entry = entry_start+'-'+entry_end
                # print(f'entry::{self.entry}')
            elif 'buy' in self.matches_split:
                entry_index = self.matches_split.index('buy')
                entry_start=self.matches_split[entry_index+1]
                entry_end=self.matches_split[entry_index+2]
                self.entry = entry_start+'-'+entry_end
                # print(f'buy::{self.entry}')
            else:
                raise ValueError("entry is not present in the message")
            #entry average
            self.entryAverage = "{:.5f}".format((float(entry_start)+float(entry_end))/2)
#             stoploss
            try:
                if 'stoploss' in self.matches_split:
                    end_index = self.matches_split.index('stoploss')
                elif 'stop' in self.matches_split:
                    end_index = self.matches_split.index('stop')
                else:
                    end_index = None
                self.stopLoss=self.matches_split[end_index+1] if end_index else None
            except:
                self.stopLoss=''
            pattern_one = re.compile(r'[Tt]+[Aa]+[Rr]+[Gg]+[Ee]+[Tt]+[Ss]?.*?\d?:\s*(\b\d*.\d*\b)')
            pattern_two=re.compile(r'[Tt]+[Aa]+[Rr]+[Gg]+[Ee]+[Tt]+[Ss]?:\s*((?:\d+\.\d+\s*-\s*)+\d+\.\d+)')
            target_match_one = pattern_one.findall(self.message)
            target_match_two = pattern_two.findall(self.message)
            if target_match_two:
                if '-' in target_match_two[0]:
                    numbers = [float(number) for number in re.split(r'\s*-\s*', target_match_two[0])]
                    # print(f'numbers::{numbers}')
                    for i, num in enumerate(numbers):
                        self.t_series[f't{i+1}'] = num
                    for tuple_ in self.t_series.items():
                        print(f't_series in p2_match::{tuple_}')
                        
            else:
                for i, num in enumerate(target_match_one):
                    if self.contains_float(num):
                        self.t_series[f't{i+1}'] = num
            try:
                self.position = 'LONG' if 'long' in self.matches_split else 'SHORT'
            except:
                self.position=''
            matched_data = {'pair':self.pair,
            'position':self.position,
            'entry':self.entry,
            'entryAverage':self.entryAverage,
            't_series':self.t_series,
            'stopLoss':self.stopLoss,
            'created_at':self.created_at}
            return matched_data
        matched_data = find_pattern() 
        return matched_data

    def p3_match(self):
        def check_ascii(matches_split):
            new_list=[]
            char = ''
            for item in matches_split:
                item = re.sub(':','',item)
                if not item.isascii():
                    ascii_text = re.sub(r'[^\x00-\x7F]+', '', item)
                    if ascii_text != '':
                        char = ascii_text
                    else:
                        continue
                else:
                    char = item
                if char not in ('zone','range','',' '):
                    new_list.append(char)
            return new_list
        def get_list():
            matches_split = re.split(r'[\n\s-]+',self.message)
            matches_split=list(map(lambda x:x.strip().lower(),matches_split))
            self.matches_split = check_ascii(matches_split)
        matched_data={}
        get_list()
        if 'invalidations' in self.matches_split:
            get_match_index = self.matches_split.index('invalidations')
            self.matches_split=self.matches_split[:get_match_index]
        for item in self.matches_split:
            if item.startswith('$'):
                self.pair = item.replace('$','')
                break
        else:
            self.pair = self.matches_split[0]
        #entry
        # try:
        start_entry = [index for index, item in enumerate(self.matches_split) if 'entry' in item][0]
        entry_point = self.matches_split[start_entry+1]
        exit_point = self.matches_split[start_entry+2]
        if exit_point == 'sl':
            self.stopLoss = self.matches_split[start_entry+3]
            self.entry = self.matches_split[start_entry+1]
            self.entryAverage = self.entry
        else:
            self.entry = entry_point+'-'+exit_point
            self.entryAverage = "{:.5f}".format((float(entry_point)+float(exit_point))/2)
        # except:
        #     self.entry=self.entryAverage=''
         
        #target
        # try:
        # t_series = {}
        i=-1
        pattern = re.compile(r'(tp\d?)\s*(\b\d*.\d*\b)')
        matches = pattern.findall(' '.join(self.matches_split))
        for i,target in enumerate(matches):
            if self.contains_float(target[1]):
                self.t_series[f't{i}'] = target[1]
        # except:
        #     self.t_series={}
        #position
        try:
            self.position = 'LONG' if 'long' in self.matches_split else 'SHORT'
        except:
            self.position = ''
        #stop loss
        if self.stopLoss == '':
            pattern = r'([Hh]?[aA]?[rR]?[dD]?\s*SL[:\s:]*)(\b\d+\.\d+\b)'
            stop_loss = re.search(pattern,self.message)
            self.stopLoss = stop_loss.group(2)
        matched_data = {'pair':self.pair,
        'position':self.position,
        'entry':self.entry,
        'entryAverage':self.entryAverage,
        't_series':self.t_series,
        'stopLoss':self.stopLoss,
        'created_at':self.created_at}
        return matched_data
    
    
    def p4_match(self):
        def check_ascii(matches_split):
            new_list=[]
            char = ''
            for item in matches_split:
                item = re.sub('[:;@!$]+','',item)
                if not item.isascii():
                    ascii_text = re.sub(r'[^\x00-\x7F]+', '', item)
                    if ascii_text != '':
                        char = ascii_text
                    else:
                        continue
                else:
                    char = item
                if item not in ('',' '):
                    new_list.append(char)
            return new_list
        matched_data={}
        matches_split = re.split(r'[\n\s]+',self.message)
        matches_split=list(map(lambda x:x.lower(),matches_split))
        self.matches_split = check_ascii(matches_split)
        #pair
        for item in self.matches_split:
            if item.startswith('#'):
                self.pair = item.replace('#','')
                break
        else:
            self.pair = self.matches_split[0].strip()
        #entry
        if 'entries' in self.matches_split:
            start_entry = self.matches_split.index('entries')
        else:
            start_entry = self.matches_split.index('entry')
        entry = self.matches_split[start_entry+1]
        if self.contains_float(entry):
            self.entry = entry
        else:
            raise Exception('Entry not found')
        #average entry
        self.entryAverage = self.entry
        #target
        find_regex=re.compile(r'([Tt]+[Aa]+[Rr]+[Gg]+[Ee]+[Tt]+[Ss]*\w*\s*\d*\s*)(\b\d*\.\d*\b)')
        target_match = find_regex.findall(self.message)
        i=-1
        for target in target_match:
            i=i+1
            if self.contains_float(target[1]):
                self.t_series[f't{i}'] = target[1]
        #position
        self.position = 'LONG' if 'long' in self.matches_split else 'SHORT'
        #stop loss
        if 'sl' in self.matches_split:
            start_sl = self.matches_split.index('sl') 
        elif 'stoploss' in self.matches_split:
            start_sl=self.matches_split.index('stoploss')
        elif 'stop' in self.matches_split:
            start_sl=self.matches_split.index('stop')
        else:
            start_sl=None
        self.stopLoss = self.matches_split[start_sl+1]
        matched_data = {'pair':self.pair,
        'position':self.position,
        'entry':self.entry,
        'entryAverage':self.entryAverage,
        't_series':self.t_series,
        'stopLoss':self.stopLoss,
        'created_at':self.created_at}
        return matched_data
    
    def p5_match(self):
        def check_ascii(matches_split):
            new_list=[]
            char = ''
            for item in matches_split:
                item = re.sub(r'[:;@!$]+','',item)
                item = re.sub(r'\d\)','',item)
                if not item.isascii():
                    ascii_text = re.sub(r'[^\x00-\x7F]+', '', item)
                    if ascii_text != '':
                        char = ascii_text
                    else:
                        continue
                else:
                    char = item
                if item not in ('','zone','loss') :
                    new_list.append(char)
            return new_list
        
        def get_list():
            matches_split = re.split(r'[\n\s\-\_]+',self.message)
            matches_split=list(map(lambda x:x.strip().lower(),matches_split))
            self.matches_split = check_ascii(matches_split)

        def find_pattern():
            get_list()
            # print(self.matches_split)
            for item in self.matches_split:
                if item.startswith('#'):
                    self.pair = item.replace('#','')
                    print(f'pair inside match::{self.pair}')
                    break
            else:
                self.pair = self.matches_split[0]
            #entry
            try:
                entry_index = self.matches_split.index('entry')
                entry_start=self.matches_split[entry_index+1]
                entry_end=self.matches_split[entry_index+2]
                self.entry = entry_start+'-'+entry_end
                self.entryAverage = "{:.5f}".format((float(entry_start)+float(entry_end))/2)
            except:
                entry_pattern = re.compile(r'[Ee]+[Nn]+[Tt]+[Rr]+[Yy]+.*?:\s*(\b\d+.\d*\b)')
                self.entry = entry_pattern.search(self.message).group(1)
                print(f'entry::{self.entry}')
                self.entryAverage = self.entry
            
#             stoploss
            if 'stoploss' in self.matches_split:
                end_index = self.matches_split.index('stoploss')
            elif 'stop' in self.matches_split:
                end_index = self.matches_split.index('stop')
            elif 'sl' in self.matches_split:
                end_index = self.matches_split.index('sl')
            else:
                end_index = None
            self.stopLoss=self.matches_split[end_index+1] if end_index else None
            #target
            numbers=[]
            start_index =int(entry_index)+3
            if self.matches_split[start_index].strip('tp') =='' or self.matches_split[start_index].strip('targets')=='':
                numbers = self.matches_split[start_index+1:end_index]
            else:
                numbers = self.matches_split[start_index:end_index]
            numbers = [re.sub(r'[a-zA-Z]*','',num) for num in numbers]


            for i, num in enumerate(numbers):
                if self.contains_float(num):
                    self.t_series[f't{i+1}'] = num
            #position
            if self.contains_float(self.entry):
                print('contains float')
                self.position = 'LONG' if self.t_series.get('t1','')>self.entry else 'SHORT'
            else:
                self.position = 'LONG' if 'long' in self.matches_split else 'SHORT'
       
            matched_data = {'pair':self.pair,
            'position':self.position,
            'entry':self.entry,
            'entryAverage':self.entryAverage,
            't_series':self.t_series,
            'stopLoss':self.stopLoss,
            'created_at':self.created_at}
            return matched_data
        matched_data = find_pattern()  # Assign matched_data from find_pattern()
        return matched_data
# if __name__=='__main__':
    
#     obj = FindMatch(message=p5_text)
#     obj.p5_match()