import telebot
from bot_url import token
from data import *

bot = telebot.TeleBot(token)

# Test

is_in_test = False
quest_number = 0
answer_sum = 0

def start_test(message):
    global is_in_test
    is_in_test = True
    bot.send_message(message.chat.id, start_test_test)
    next_quest(message)

def stop_test():
    global is_in_test
    global quest_number
    global answer_sum
    print("stop test")
    is_in_test = False
    quest_number = 0
    answer_sum = 0

def write_results(message):
    if answer_sum >= quest_sure_level:
        bot.send_message(message.chat.id, should_stay, reply_markup=telebot.types.ReplyKeyboardHide())
    elif answer_sum <= -quest_sure_level:
        bot.send_message(message.chat.id, should_change, reply_markup=telebot.types.ReplyKeyboardHide())
    else:
        bot.send_message(message.chat.id, should_not_sure, reply_markup=telebot.types.ReplyKeyboardHide())

def next_quest(message):
    global quest_number
    if len(questions) == quest_number:
        write_results(message)
        stop_test()
    else:
        markup = telebot.types.ReplyKeyboardMarkup()
        markup.row("/yes", "/not_sure", "/no")
        bot.send_message(message.chat.id, questions[quest_number][0], reply_markup=markup)
        quest_number += 1

@bot.message_handler(commands=['test'])
def test(message):
    stop_test()
    start_test(message)

@bot.message_handler(commands=['yes'])
def yes(message):
    global answer_sum

    print("Yes command: " + str(is_in_test))
    if not is_in_test:
        return

    answer_sum += questions[quest_number - 1][1]
    next_quest(message)

@bot.message_handler(commands=['no'])
def no(message):
    global answer_sum

    if not is_in_test:
        return

    answer_sum -= 1
    next_quest(message)

@bot.message_handler(commands=['not_sure'])
def not_sure(message):
    if not is_in_test:
        return

    next_quest(message)

# Common

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, hello_message)

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, info_test)

bot.polling()
