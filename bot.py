import telebot
from bot_url import token
from data import *

bot = telebot.TeleBot(token)

# Test

is_in_test = dict()
quest_number = dict()
answer_sum = dict()

def start_test(message):
    print(str(message.from.username), " : start")
    is_in_test[message.chat.id] = True
    bot.send_message(message.chat.id, start_test_test)
    next_quest(message)

def stop_test(message):
    print(str(message.from.username), " : stop")
    is_in_test[message.chat.id] = False
    quest_number[message.chat.id] = 0
    answer_sum[message.chat.id] = 0

def write_results(message):
    print(str(message.from.username), " : write results")
    if answer_sum.get(message.chat.id, 0) >= quest_sure_level:
        bot.send_message(message.chat.id, should_stay, reply_markup=telebot.types.ReplyKeyboardHide())
    elif answer_sum.get(message.chat.id, 0) <= -quest_sure_level:
        bot.send_message(message.chat.id, should_change, reply_markup=telebot.types.ReplyKeyboardHide())
    else:
        bot.send_message(message.chat.id, should_not_sure, reply_markup=telebot.types.ReplyKeyboardHide())

def next_quest(message):
    print(str(message.from.username), " : next quest")
    if len(questions) == quest_number.get(message.chat.id, 0):
        write_results(message)
        stop_test(message)
    else:
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.row("/yes", "/not_sure", "/no")
        bot.send_message(message.chat.id, questions[quest_number.get(message.chat.id, 0)][0], reply_markup=markup)
        quest_number[message.chat.id] = quest_number.get(message.chat.id, 0) + 1

@bot.message_handler(commands=['test'])
def test(message):
    print(str(message.from.username), " : test")
    stop_test(message)
    start_test(message)

@bot.message_handler(commands=['yes'])
def yes(message):
    print(str(message.from.username), " : yes")

    print("Yes command: " + str(is_in_test))
    if not is_in_test.get(message.chat.id, False):
        return

    answer_sum[message.chat.id] = answer_sum.get(message.chat.id) + questions[quest_number.get(message.chat.id, 0) - 1][1]
    next_quest(message)

@bot.message_handler(commands=['no'])
def no(message):
    print(str(message.from.username), " : no")

    if not is_in_test.get(message.chat.id, False):
        return

    answer_sum[message.chat.id] = answer_sum.get(message.chat.id) - questions[quest_number.get(message.chat.id, 0) - 1][1]
    next_quest(message)

@bot.message_handler(commands=['not_sure'])
def not_sure(message):
    print(str(message.from.username), " : not sure")
    if not is_in_test.get(message.chat.id, False):
        return

    next_quest(message)

# Common

@bot.message_handler(commands=['start'])
def start(message):
    print(str(message.from.username), " : start")
    bot.send_message(message.chat.id, hello_message, reply_markup=telebot.types.ReplyKeyboardHide())

@bot.message_handler(commands=['info'])
def info(message):
    print(str(message.from.username), " : info")
    bot.send_message(message.chat.id, info_test, reply_markup=telebot.types.ReplyKeyboardHide())

bot.polling()
