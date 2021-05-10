import telepot

def SendTelegramMessage(msg):
    try:
        #Telegram bot api token for connection to telegram
        bot = telepot.Bot('1239071011:AAHB2AIUdoGaYAxrYF6WmNaC8gD2SMNt32o')
        #Left parameter, chat ID that represent the Telegram channel. 
        bot.sendMessage("-1001270898070", msg)
        return True
    except:
        return False




