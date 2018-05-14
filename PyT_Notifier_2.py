import json
import time
import os
from urllib import request
from urllib import parse
from datetime import datetime
import itertools
import settings

#TO IMPELEMNT
# - push price change after sale if price drops below sale price -> how many profit have you missed?


#### CLASSES AND FUNCTIONS ####
class LogData(object):
    sales = {}
    pairs = {}
    dca   = {}

    def __init__(self, sales, pairs, dca, modtime):
        self.sales = sales
        self.pairs = pairs
        self.dca   = dca
        self.modtime = modtime
    def make_coinlist(self):
        coinlist = []
        for combination in itertools.zip_longest(self.pairs, self.dca):
            if (combination[0] is not None):
                if (combination[0]['market'] not in coinlist):
                    coinlist.append(combination[0]['market'])
            if (combination[1] is not None):
                if (combination[1]['market'] not in coinlist):
                    coinlist.append(combination[1]['market'])
        return coinlist
    def find_buy(self, coin):
        for combination in itertools.zip_longest(self.pairs, self.dca):
            if (combination[0] is not None):
                if (combination[0]['market'] == coin):
                    return combination[0], 'PAIR'
            if (combination[1] is not None):
                if (combination[1]['market'] == coin):
                    return combination[1], 'DCA'
        return False

def make_logdata(path):
    while True:
        try:
            with open(path, 'r') as myfile:
                    time = os.path.getmtime(path)
                    jsonData = myfile.read().replace('\n', '')
                    dataObject = json.loads(jsonData)
            data = LogData(dataObject['sellLogData'],dataObject['gainLogData'],dataObject['dcaLogData'], time)
            break
        except:
            continue
    return data

class TelegramBot(object):
    def __init__(self, token, chat_id, instance_name, path):
        self.token = token
        self.chat_id = chat_id
        self.name = instance_name
        self.path = path
    def sendmessage(self, text, **kwargs):
        try:
            parse_mode
        except:
            parse_mode = 'markdown'
        baseurl = "http://api.telegram.org/bot"
        url = baseurl + self.token + "/" + "sendMessage?"
        test = {"chat_id": self.chat_id, "text": text, "parse_mode": parse_mode}
        purl = parse.urlencode(test)
        furl = url + purl
        f = request.urlopen(furl)
def make_telegramBot(token, chat_id, name, path):
    bot = TelegramBot(token, chat_id, name, path)
    return bot

def compose_message(data, type, name):
    instance = name
    if (type == "sale"):
        coin = str(data['market'])
        amount = str(data['soldAmount'])
        dca = str(data['boughtTimes'])
        profit = str(data['profit'])
        strat = ''
        if (len(data['sellStrategies'])==1):
            strat = data['sellStrategies'][0]['name']
        else:
            for entry in data['sellStrategies']:
                strat = strat + entry['name']+ " "
        coinProfit = (data['averageCalculator']['avgCost'] * (1 + (data['profit'] / 100))) - data['averageCalculator']['avgCost']
        message = "\U0001F911"+instance+" *SOLD:*" + os.linesep + "`{0:<12}{1:>18}\n{2:<12}{3:>18}\n{4:<12}{5:>18}\n{6:<12}{7:>18}\n{8:<12}{9:>18}\n{10:<12}{11:>18}\n`".format("Coin:", coin, "Strategy:", strat, "DCA Levels:", dca, "Amount:", amount, "Profit:", profit, "Coin Profit:", str(format(float(coinProfit), '.8f')))
        return message
    elif (type == 'buy'):
        coin = str(data['market'])
        amount = str(data['totalAmount'])
        avgprice = str(data['averageCalculator']['avgPrice'])
        totalcost = str(data['averageCalculator']['totalCost'])
        message = "\U0001F4B8"+instance+" *BOUGHT:*" + os.linesep + "`{0:<12}{1:>20}\n{2:<12}{3:>20}\n{4:<12}{5:>20}\n{6:<12}{7:>20}\n`".format("Coin:", coin, "Amount:", amount, "Avg. Price:",str(format(float(avgprice), '.8f')), "Total Cost:",str(format(float(totalcost), '.4f')))
        return message
    elif (type == 'dca'):
        coin = str(data['market'])
        dca = str(data['boughtTimes'])
        amount = str(data['totalAmount'])
        curprice = str(data['currentPrice'])
        avgprice = str(data['averageCalculator']['avgPrice'])
        message = "\U0001F4B8\U0001F4B8 "+instance+"*BOUGHT DCA:*" + os.linesep + "`{0:<14}{1:>18}\n{2:<14}{3:>18}\n{4:<14}{5:>18}\n{6:<14}{7:>18}\n{8:<14}{9:>18}\n`".format("Coin:", coin, "Total amount:", amount, "Avg Price:",str(format(float(avgprice), '.8f')), "Current Price:",str(format(float(curprice), '.8f')), "DCA Level:", dca)
        return message



def tprint(*args):
    stamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(stamp + ' :PyTN: ', *args)

#### /CLASSES AND FUNCTIONS ####

#### BOTS INIT ####

Bots = []
for i in range(0,len(settings.bots)):
    Bots.append(make_telegramBot(settings.api_token, settings.chat_id, settings.bots[i]['name'], settings.bots[i]['path']))
Bots[0].sendmessage("Your "+str(len(settings.bots))+" PyTNBot(s) are up and running.")
tprint("Bot(s) initialized: "+str(len(settings.bots))+os.linesep)
#### /BOT INIT ####

#### INITIAL DATA PARSING ####
initial_data = []
for i in range(0,len(Bots)):
    initial_data.append(make_logdata(Bots[i].path))
    tprint("Data for "+Bots[i].name)
    tprint("Current Sales: ", len(initial_data[i].sales))
    tprint("Current Pairs: ", len(initial_data[i].pairs))
    tprint("Current DCA Entries: ", len(initial_data[i].dca), "\n")
    time.sleep(2)
alivecounter = 100
#### /INITIAL DATA PARSING ####

#### MAIN ####
while True:
    if alivecounter == 0:
        tprint("I am still alive and watching your trades, don't worry!")
        alivecounter = 50
    for i in range(0,len(Bots)):
        time.sleep(1)
        current_data = make_logdata(Bots[i].path)
        if (current_data.modtime != initial_data[i].modtime):
            if (current_data != initial_data[i]):
                # Sale
                if (current_data.sales != initial_data[i].sales):
                    tprint("Found a sale!")
                    diff = len(current_data.sales)-len(initial_data[i].sales)
                    for x in range(0,diff):
                        Bots[i].sendmessage(compose_message(current_data.sales[x], 'sale', Bots[i].name))
                        tprint("Telegram message sent.")
                    initial_data[i] = current_data
                # Pair and DCA
                elif (current_data.pairs != initial_data[i].pairs) or (current_data.dca != initial_data[i].dca):
                    coinlist_initial = set(initial_data[i].make_coinlist())
                    coinlist_current = set(current_data.make_coinlist())
                    new_coins    = coinlist_current-coinlist_initial
                    for e in new_coins:
                        resultdata, kind= current_data.find_buy(e)
                        if (kind == 'PAIRS'):
                            tprint("Found a buy!")
                            Bots[i].sendmessage(compose_message(resultdata, 'buy', Bots[i].name))
                            tprint("Telegram message sent.")
                        elif (kind == 'DCA'):
                            tprint("Found a DCA buy!")
                            Bots[i].sendmessage(compose_message(resultdata, 'dca', Bots[i].name))
                            tprint("Telegram message sent.")
                    initial_data[i] = current_data
        alivecounter -= 1

#### /MAIN ####
