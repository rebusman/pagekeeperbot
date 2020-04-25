import telebot
import configparser
import requests
import os
import re
import pdfkit
import uuid

config = configparser.ConfigParser()
config.read("config.ini")
if config.has_option("DEFAULT","Filepath"):
    filepath = config["DEFAULT"]["Filepath"]
else:
    filepath = "temp"
# Download page
def savePage(self):
    try:
        pdfdoc = str("%s/%s.pdf" % (filepath,str(uuid.uuid4())))
        pdfkit.from_url(self, pdfdoc)
        return {"message":"page coverted", "file":pdfdoc}
    except Exception as e:
        print(e)
        if os.path.exists(pdfdoc):
            os.remove(pdfdoc)
        return {"message":"page convert failed"}
# Link validation
def checkUrl(self):
    regex = re.compile(
            r'^(?:http)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, self):
        r = requests.get(self).status_code
        if r == 200:
            return savePage(self)
        else:
            msg = {"message":("Bad request: %s" % r)}
            print(msg["message"])
            return msg
    else:
        msg = {"message":("Bad url: %s " % self)}
        print(msg["message"])
        return msg

def main():
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    if config.has_option("DEFAULT","Proxy"):
        print("Use proxy %s" % config["DEFAULT"]["Proxy"] )
        telebot.apihelper.proxy = {'https': config["DEFAULT"]["Proxy"]}
    bot = telebot.TeleBot(config["DEFAULT"]["Token"])
    # Handle '/start' and '/help'
    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        bot.reply_to(message, """\
    Этот бот умеет конвертировать ссылки в pdf файл\
    Чтобы этим воспользоваться, просто отправь ссылку и получи в ответ pdf файл\
    """)
    # Message handle
    @bot.message_handler(func=lambda message: True)
    def echo_message(message):
        result = checkUrl(message.text)
        bot.reply_to(message,result["message"])
        if "file" in result:
            with open(result["file"],"rb") as f:
                bot.send_document(message.chat.id,f) # Send pdf
            os.remove(result["file"])

    bot.polling()

if __name__ == "__main__":
    main()