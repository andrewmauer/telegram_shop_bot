import telebot
from telebot import types

# Buttons

# Item buttons

nb1 = types.KeyboardButton('New Balance 57:40') 
nb2 = types.KeyboardButton('New Balance 327') 
nike1 = types.KeyboardButton('Nike AIR MAX GENOME')
nb3 = types.KeyboardButton('New Balance Fresh Foam X 1080v12')
ad1 = types.KeyboardButton('Adidas LITE RACER 3.0')
ad2 = types.KeyboardButton('Adidas PREDATOR EDGE.3 LL TF')
nike2 = types.KeyboardButton('Nike REACT MILLER') 
nike3 = types.KeyboardButton('Nike REVOLUTION 6 NN')
ad3 = types.KeyboardButton('Adidas SUPERNOVA M')
b = types.KeyboardButton('Back to city selection')
c_b = [nb1, nb2, nike1, nb3, ad1, ad2, nike2, nike3, ad3, b]

# Size buttons

s1 = types.KeyboardButton('6.5')
s2 = types.KeyboardButton('7')
s3 = types.KeyboardButton('7.5')
s4 = types.KeyboardButton('8')
s5 = types.KeyboardButton('8.5')
s6 = types.KeyboardButton('9')
s7 = types.KeyboardButton('9.5')
s8 = types.KeyboardButton('10')
s9 = types.KeyboardButton('10.5')
b = types.KeyboardButton('Back to item selection')
s_b = [s1, s2, s3, s4, s5, s6, s7, s8, s9, b]

# City buttons

c1 = types.KeyboardButton('Moscow')
c2 = types.KeyboardButton('Saint-Petersburg')
c3 = types.KeyboardButton('Almaty')
c4 = types.KeyboardButton('Astana')
b = types.KeyboardButton('Back to menu')
ct_b = [c1, c2, c3, c4, b]

# Lists with info about items

itemslist = ['New Balance 57:40', 'New Balance 327', 'Nike AIR MAX GENOME',
           'New Balance Fresh Foam X 1080v12', 'Adidas LITE RACER 3.0', 'Adidas PREDATOR EDGE.3 LL TF',
           'Nike REACT MILLER', 'Nike REVOLUTION 6 NN', 'Adidas SUPERNOVA M']
sizeslist = ['6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10', '10.5']

# Funcs that returns catalog photos with description

class Catalog():
    def get_catalog(self):
        with open('/Users/andrewmauer/Documents/venv/catalog.txt', 'r') as f: # Reading the description from file
                catalog = f.read()
        self.catalog_photos = [telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/57:40.jpg', 'rb'), catalog), telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/327.jpg', 'rb')), 
            telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/AIR MAX GENOME.jpg', 'rb')), telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/Fresh Foam X 1080v12.jpg', 'rb')),
            telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/LITE RACER 3.0.jpg', 'rb')), telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/PREDATOR EDGE.3 LL TF.jpg', 'rb')), 
            telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/REACT MILER.jpg', 'rb')), telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/REVOLUTION 6 NN.jpg', 'rb')), 
            telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/SUPERNOVA M.jpg', 'rb'))]
        return self.catalog_photos
    def get_sale_catalog(self):
        with open('/Users/andrewmauer/Documents/venv/description.txt', 'r') as f: # Reading the description from file
            text = f.read()
        self.catalog_photos_2 = [telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/57:40.jpg', 'rb'), text), telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/327.jpg', 'rb')), 
            telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/AIR MAX GENOME.jpg', 'rb')), telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/Fresh Foam X 1080v12.jpg', 'rb')),
            telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/LITE RACER 3.0.jpg', 'rb')), telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/PREDATOR EDGE.3 LL TF.jpg', 'rb')), 
            telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/REACT MILER.jpg', 'rb')), telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/REVOLUTION 6 NN.jpg', 'rb')), 
            telebot.types.InputMediaPhoto(open('/Users/andrewmauer/Documents/venv/Photos/SUPERNOVA M.jpg', 'rb'))]
        return self.catalog_photos_2