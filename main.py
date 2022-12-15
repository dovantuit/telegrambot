# pip install python-telegram-bot
import types
from telegram.ext import *
# thu vien lay gia crypto
import json
import requests
import keys

print('Starting up bot...')

# Lets us use the /start command
def start_command(update, context):
    makeKeyboard()
    update.message.reply_text('Hello there! I\'m a bot. What\'s up?')

stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}
crossIcon = u"\u274C"

def makeKeyboard():
    markup = types.InlineKeyboardMarkup()

    for key, value in stringList.items():
        markup.add(types.InlineKeyboardButton(text=value,
                                              callback_data="['value', '" + value + "', '" + key + "']"),
        types.InlineKeyboardButton(text=crossIcon,
                                   callback_data="['key', '" + key + "']"))

    return markup

# Lets us use the /help command
def help_command(update, context):
    update.message.reply_text("""
    hello -> xin chào
    jack79 -> xin chào tới chó điên, chào mừng bạn đã đến với con bot này
    còn lại -> cần lập trình thêm
    """)


# Lets us use the /custom command
def custom_command(update, context):
    update.message.reply_text('This is a custom command, you can add whatever text you want here.')
#log
def log_command(update, context):
    print(f'\n\nUpdate: {update}\ncontext: {context}\n\n')
    update.message.reply_text('log done')

# make funcion write log to logBot.log file
def writeLog(update, textFromUser):
    # create time for log
    import datetime
    now = datetime.datetime.now()
    logFile = open("logBot.log", "a")
    logFile.write(f"{now}: {update.message.from_user.username}-{update.message.chat.id} --> {textFromUser} \n")

def handle_response(text) -> str:
    text = str(text).lower()
    # Create your own response logic
    if 'hello' in text:
        return 'Hey there!'
    elif 'jack79' in text:
        return 'Xin chào tới chó điên, chào mừng bạn đã đến với con bot này'
    elif 'how are you' in text:
        return 'I\'m good!'
    elif 'hehe' in text or 'hihi' in text or 'haha' in text or 'kk' in text:
        return 'cười cc'
    elif 'check giá' in text or 'giá' in text or 'btc' in text or 'bitcoin' in text:
        tenCoin = 'BTC'
        if 'btc' in text or 'bitcoin' in text or 'bit' in text:
            tenCoin = 'BTC'
        if 'eth' in text:
            tenCoin = 'ETH'
        if 'xrp' in text:
            tenCoin = 'XRP'
        key = f"https://api.binance.com/api/v3/ticker/price?symbol={tenCoin}USDT"
        response = requests.get(key)
        data = json.loads(response.text)
        return f'Giá {tenCoin} hiện tại là: ' + data['price']
    elif 'bot ngu quá' in text or 'bot lol' in text or 'bot ngu' in text:
        return 'Tao ngu vì tao là bot, tao chỉ làm theo lệnh của người lập trình thôi'
    elif 'ai đẹp trai nhất' in text or 'ai đẹp trai' in text or 'ai đẹp trai nhất thế giới' in text:
        return 'Tất nhiên là anh Tom rồi hihi'
    elif 'mày đâu rồi' in text or 'mày đâu' in text or 'đâu' in text:
        return 'Dạ em nghe đại ca ơi'
    elif 'tên gì' in text or 'tên là gì' in text or 'tên là' in text:
        return 'Tao là ông nội'
    # create a string to store the response
    response = 'bot không hiểu\n'
    return response

def handle_message(update, context):
    user_name = context.bot.get_chat(update.message.chat_id).first_name
    # Get basic info of the incoming message
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ''    
    # Print a log for debugging
    print(f'userID ({update.message.chat.id}) says: "{text}" in: {message_type}')
    writeLog(update, text)
    if 'bot' in text:
        response = handle_response(text)
        # Reply normal if the message is in private
        update.message.reply_text(response)
    else:
        return
   


# Log errors
def error(update, context):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    updater = Updater(keys.token, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('custom', custom_command))
    dp.add_handler(CommandHandler('log', log_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling()
    updater.idle()