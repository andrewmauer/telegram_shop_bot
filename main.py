import telebot
from telebot import types
from catalog import Catalog, itemslist, sizeslist, c_b, s_b, ct_b
from database import Query #connection

# VARIABLES

items = [] # List of items with parameters
user_info = [] #List of user information
bot = telebot.TeleBot('Your token') # Bot token
db = Query() # Database class
cat = Catalog() # Catalog class from catalog.py

# COMMAND HANDLER

@bot.message_handler(commands=['start']) #start actions

def start(message): # /start function
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    catalog = types.KeyboardButton('Catalog')
    make_order = types.KeyboardButton('Make an order')
    information = types.KeyboardButton('About us')
    instagram = types.KeyboardButton('Our Instagram')
    status = types.KeyboardButton('Order status')
    reply = types.KeyboardButton('Contact manager')
    if message.from_user.last_name: #if last name exists, we'll connect first name and last name
        mess = f'Hello, <b>{message.from_user.first_name} {message.from_user.last_name}</b>, welcome to SneakersForYou! Here you can find a good sneakers for your taste!'
    else: #if not, we'll show only first name
        mess = f'Hello, <b>{message.from_user.first_name}</b>, welcome to SneakersForYou! Here you can find a good sneakers for your taste!'
    markup.add(catalog, make_order, information, instagram, status, reply) # Main buttons
    bot.send_message(message.chat.id, mess, parse_mode='HTML')
    bot.send_message(message.chat.id, "Choose what you need by clicking on the buttons below.", reply_markup=markup)

# TEXT HANDLER

@bot.message_handler(content_types='text')

def message_reply(message): # Interaction with main buttons
    if message.text == 'Catalog': # Showing the catalog of items
        bot.send_media_group(message.chat.id, cat.get_catalog())
    elif message.text == 'Make an order': # Start making order
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) # Preferences for catalog buttons       
        # c1 = types.KeyboardButton('Moscow')
        # c2 = types.KeyboardButton('Saint-Petersburg')
        # c3 = types.KeyboardButton('Almaty')
        # c4 = types.KeyboardButton('Astana')
        # b = types.KeyboardButton('Back to menu')
        markup.add(ct_b[0], ct_b[1], ct_b[2], ct_b[3], ct_b[4]) # City buttons
        bot.send_message(message.chat.id, 'Please, choose your city.', reply_markup=markup)
        bot.register_next_step_handler(message, get_info)
    elif message.text == 'Our Instagram':
        bot.send_message(message.chat.id, 'Visit our Instagram and check for the updates!')
        bot.send_message(message.chat.id, 'https://www.instagram.com')
    elif message.text == 'About us': # Info about company
        bot.send_message(message.chat.id, 'We are young company, that opened in 2022. We can offer you a nice sneakers!')
    elif message.text == 'Order status': # Show all orders of client
        info_list = []
        client_id = str(message.from_user.id)
        info = db.fetch_query('SELECT os.order_id, item_name, size_name, amount, summ_order, order_status FROM orders os inner join buy_order bo on bo.order_id = os.order_id inner join items i on i.item_id = bo.item_id inner join sizes s on s.size_id = bo.size_id WHERE os.client_id = %s', (client_id,))
        orders_counter = db.fetch_query('SELECT COUNT(order_id) FROM orders WHERE client_id = %s', (client_id, ))[0][0]
        orders = db.fetch_query('SELECT order_id FROM orders WHERE client_id = %s', (client_id, ))
        city = db.fetch_query('SELECT city_name FROM client c inner join city ct on c.city_id = ct.city_id WHERE client_id = %s', (client_id, ))[0][0]
        if info: # If order(s) exists, it'll show info about all of them
            for i in range(orders_counter):
                info = db.fetch_query('SELECT os.order_id, item_name, size_name, amount, item_price, summ_order, order_status FROM orders os inner join buy_order bo on bo.order_id = os.order_id inner join items i on i.item_id = bo.item_id inner join sizes s on s.size_id = bo.size_id WHERE os.client_id = %s AND os.order_id = %s', (client_id, orders[i]))
                line_order = f'Order number: {info[0][0]}.'
                info_list.append(line_order)
                num = 0
                total = 0
                for row in info:
                    num += 1
                    line = f'№ {num}. Item: {row[1]} Size: {row[2]} Amount: {row[3]} * {row[4]}$ = {row[5]}$'
                    info_list.append('\n' + line)
                    total += float(row[5])
                addtotal = f'Total: {total}0 $.'
                status = f'Status: {row[6]}.'
                city_of_client = f'Shipping to: {city}.'
                info_list.append('\n' + addtotal)
                info_list.append('\n' + status)
                info_list.append('\n' + city_of_client)
                bot.send_message(message.chat.id, ''.join(info_list))
                info_list.clear()
        else: # If not exist
            bot.send_message(message.chat.id, "You've got no orders.")
    elif message.text == 'Contact manager': # Link to sale manager
        bot.send_message(message.chat.id, "If you have a question, please, contact our manager.")
        bot.send_message(message.chat.id, 'https://t.me/andrewmauer')
    else:
        bot.send_message(message.chat.id, 'Please use buttons below.')

def get_info(message): # Getting city and inserting it in database
    if message.text in ["Astana", "Almaty", "Moscow", "Saint-Petersburg"]:
        user_info.append(str(message.text)) # Adding city in our user list
        bot.send_media_group(message.chat.id, cat.get_sale_catalog()) # Sending catalog with photos
        mess = f"If you have chosen the wrong city, don't worry, just click on the button 'Back to city selection' and choose city again!"
        bot.send_message(message.chat.id, mess)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)       
        markup.add(c_b[0], c_b[1], c_b[2], c_b[3], c_b[4], c_b[5], c_b[6], c_b[7], c_b[8], c_b[9]) # Adding catalog buttons
        bot.send_message(message.chat.id, 'Please, choose a sneakers.', reply_markup=markup)
        bot.register_next_step_handler(message, order) # Move to order function
    elif message.text == 'Back to menu':
        start(message)
    else:
        bot.send_message(message.chat.id, "Please, use the buttons below to make your choice.")
        bot.register_next_step_handler(message, get_info)

def order(message): # Getting the item from user and putting it into the item_list
    if message.text == 'Cancel':
        message.text = 'No'
        order_repeat(message)
    elif message.text in itemslist:
        if message.from_user.last_name:
            name = message.from_user.first_name + ' ' + message.from_user.last_name
        else:
            name = message.from_user.first_name
        username = message.from_user.username
        client_id = message.from_user.id
        city = user_info[0]
        db.execute_query('INSERT INTO client (client_id, client_name, client_username, city_id) VALUES (%s, %s, %s, (select city_id from city where city_name = %s)) ON CONFLICT (client_id) DO UPDATE SET city_id = (select city_id from city where city_name = %s)', (client_id, name, username, city, city))
        items.append(str(message.text)) # Adding item into the database
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3) # Preferences for catalog buttons
        mess = f"If you make a mistake at any stage of the order, don't worry, just click on the button <b>'Back to item selection'</b> below, and make your choice again!"
        bot.send_message(message.chat.id, mess, parse_mode='HTML')
        markup.add(s_b[0], s_b[1], s_b[2], s_b[3], s_b[4], s_b[5], s_b[6], s_b[7], s_b[8], s_b[9])
        bot.send_message(message.chat.id, "Choose your size, please.", reply_markup=markup)
        bot.register_next_step_handler(message, get_size)
    elif message.text == 'Back to city selection': # Move to func message_reply with 'Make an order' button
        items.clear()
        message.text = 'Make an order'
        message_reply(message)
    else:
        bot.send_message(message.chat.id, 'Please, use the buttons below to make your choice.')
        bot.register_next_step_handler(message, order)

def get_size(message): # Getting the size of user and inserting it into the item_list
    if message.text in sizeslist:
        b = types.KeyboardButton('Back to item selection')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        items.append(str(message.text))
        markup.add(b)
        bot.send_message(message.chat.id, 'Please, type an amount from 1 to 20. More than 20 considered as a wholesale trade, so you need to contact our manager.', reply_markup=markup)
        bot.register_next_step_handler(message, get_amount)
    elif message.text == 'Back to item selection': # If user choosed a wrong item
        message.text = user_info[0]
        items.clear()
        get_info(message) # Return to get_info func with early selected city
    else:
        bot.send_message(message.chat.id, 'Please, use the buttons below to make your choice.')
        bot.register_next_step_handler(message, get_size)

def get_amount(message): # Getting the amount of item and inserting it into the item_list
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if message.text is None:
        bot.send_message(message.chat.id, 'Please type an correct amount in digits.')
        bot.register_next_step_handler(message, get_amount)
    elif message.text.isdigit() and int(message.text) < 20 and int(message.text) > 0:
        client_id = str(message.from_user.id)
        items.append(str(message.text))
        items.insert(0, client_id)
        items.append(int(message.text))
        items.append(items[1])
        db.execute_query('INSERT INTO buy_order(client_id, item_id, size_id, amount, summ_order) VALUES (%s,  (select item_id from items where item_name = %s), (select size_id from sizes where size_name = %s), %s, (SELECT item_price * %s FROM items WHERE item_name = %s))', tuple(items))
        items.clear() # Clear the list of items
        y = types.KeyboardButton('Yes')
        n = types.KeyboardButton('No')
        markup.add(y, n)
        bot.send_message(message.chat.id, 'Do you want to order something else?', reply_markup=markup)
        bot.register_next_step_handler(message, order_repeat)
    elif message.text == 'Back to item selection': #if user choosed a wrong size
        message.text = user_info[0]
        items.clear()
        get_info(message)
    elif message.text.isdigit() and int(message.text) > 20:
       bot.send_message(message.chat.id, 'This is a too big amount, contact our manager for wholesale trade.')
       start(message)
    else:
        bot.send_message(message.chat.id, 'Please type an correct amount in digits.')
        bot.register_next_step_handler(message, get_amount)

def order_repeat(message): # If user want to add some extra items, this func will send user to order function again without asking a city
    if message.text == 'Yes': # Repeat the get_info func
        message.text = user_info[0]
        get_info_repeat(message) # Extra func get_info without button 'Back to city selection'
    elif message.text == 'No':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) #preferences for catalog buttons
        y = types.KeyboardButton('Yes')
        n = types.KeyboardButton('No')
        markup.add(y, n)
        client_id = str(message.from_user.id)
        result = db.fetch_query('SELECT item_name, size_name, item_price, amount, summ_order from buy_order inner join items on buy_order.item_id = items.item_id inner join sizes on buy_order.size_id = sizes.size_id inner join client on buy_order.client_id = client.client_id where buy_order.client_id = %s and buy_order.order_id IS NULL', (client_id,))
        number = 0
        order_list = []
        items_list = 'List of your items:'
        order_list.append(items_list + '\n')
        total = 0
        for row in result:
            number += 1
            line = f'{number}: Item: {row[0]}, Size: {row[1]}, Price: {row[2]} $, Amount: {row[3]}, Cost: {row[4]} $.'
            order_list.append('\n' + line)
            total += float(row[4])
        add_total = f'Total: {total}0 $.'
        city = db.fetch_query('SELECT city_name FROM client c inner join city ct on c.city_id = ct.city_id WHERE client_id = %s', (client_id, ))[0][0]
        add_city = f'Shipping to: <b>{city}</b>.'
        order_list.append('\n' + add_total)
        order_list.append('\n' + add_city)
        bot.send_message(message.chat.id, ''.join(order_list), parse_mode='HTML')
        bot.send_message(message.chat.id, 'Is all correct?', reply_markup=markup)
        bot.register_next_step_handler(message, finish)
    else:
        bot.send_message(message.chat.id, 'Please, use the buttons below.')
        bot.register_next_step_handler(message, order_repeat)

def get_info_repeat(message): # Getting city and inserting it in database
    if message.text in ["Astana", "Almaty", "Moscow", "Saint-Petersburg"]:
        user_info.append(str(message.text)) # Addint city in our user list
        bot.send_media_group(message.chat.id, cat.get_sale_catalog()) # Sending catalog with photos
        mess = f"If you don't want to get extra items, just click on the <b>'Cancel'</b> button below and finish the order."
        bot.send_message(message.chat.id, mess, parse_mode='HTML')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)      
        markup.add(c_b[0], c_b[1], c_b[2], c_b[3], c_b[4], c_b[5], c_b[6], c_b[7], c_b[8], c_b[9])
        bot.send_message(message.chat.id, 'Please, choose a sneakers.', reply_markup=markup) 
        bot.register_next_step_handler(message, order) # Move to order function
    else:
        bot.send_message(message.chat.id, "Please, use the buttons below to make your choice.")
        bot.register_next_step_handler(message, get_info)

def finish(message): # Finishing the order
    client_id = str(message.from_user.id)
    if message.text == 'Yes':
        user_info.clear() 
        db.execute_query('INSERT INTO orders (client_id) VALUES (%s)', (client_id,))
        db.execute_query('UPDATE buy_order SET order_id = (SELECT MAX(order_id) FROM orders WHERE client_id = %s) where client_id = %s and order_id IS NULL', (client_id, client_id))
        days = db.fetch_one('select days_delivery from city inner join client on client.city_id = city.city_id where client_id = %s', (client_id,))
        ord_num = db.fetch_query('SELECT MAX(order_id) FROM orders WHERE client_id = %s', (client_id, ))[0][0]
        city = db.fetch_query('SELECT city_name FROM client c inner join city ct on c.city_id = ct.city_id WHERE client_id = %s', (client_id, ))[0][0]
        bot.send_message(message.chat.id, f'Great! Your order number is: {ord_num}. Deliver to {city} will take {days[0]} days. Check your order status by touching the button in menu!')
        start(message)
    elif message.text == 'No':
        bot.send_message(message.chat.id, 'Please, make a new order from begin.')
        user_info.clear()
        db.execute_query('DELETE FROM buy_order WHERE client_id = %s', (client_id,))
        start(message)
    else:
        bot.send_message(message.chat.id, "Please, touch on the buttons below.", parse_mode='HTML')

bot.polling(none_stop=True)