import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

bot = telebot.TeleBot("5093808717:AAHCHWQH-_-uzagPBzTORy2P41jNRvN6sX4")


def add_db(message):
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS my_data (id INTEGER UNIQUE, sphere STRING, name STRING, age INTEGER, phone_number STRING)')

	try:
		cursor.execute("""INSERT INTO my_data(id) VALUES (?)""", (message,))
		conn.commit()
	except:
		pass

@bot.message_handler(commands=['rassilka'])
def before(message):
	try:
		f=bot.send_message(message.chat.id, "Jo'natmoqchi bo'lgan habaringizni yuboring(text, rasm, video...)")
		bot.register_next_step_handler(f, rassilka)
	except:
		pass

@bot.message_handler(commands=['database'])
def send_db(message):
	file = open("database.db", 'rb')
	bot.send_document(message.chat.id,file)

@bot.message_handler(commands=['start'])
def welcome(message):
	add_db(message.chat.id)
	xabar = "Assalomu aleykum. Oxlab IT o'quv markazimizga xush kelibsiz.\nQuyidagi yo'nalishlardan qaysi birida o'qimoqchisiz?"
	markup = InlineKeyboardMarkup()
	markup.row_width = 3
	btn1 = InlineKeyboardButton("Back-End", callback_data="Back-End")
	btn2 = InlineKeyboardButton("Front-End", callback_data="Front-end")
	btn3 = InlineKeyboardButton("Mobile Dev", callback_data="Mobile Dev")
	markup.add(btn1, btn2, btn3)
	bot.send_message(message.chat.id, xabar, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()
	
	try:
		cursor.execute("""UPDATE my_data SET sphere=? WHERE id=?""", (call.data, call.from_user.id, ))
		conn.commit()
	except:
		pass


	bot.edit_message_reply_markup(call.from_user.id, call.message.message_id ,reply_markup=None)
	bot.edit_message_text(f"{call.data}✅", call.from_user.id, call.message.message_id)
	msg = bot.send_message(call.from_user.id, "Yaxshi, iltimos ism-familyangizni kiriting👇🏻")
	bot.register_next_step_handler(msg, get_name)

def get_name(message):
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()

	if message.text.isnumeric():
		msg2 = bot.send_message(message.chat.id, "Iltimos, ism-sharifingizni to'g'ri kiriting👇🏻")
		bot.register_next_step_handler(msg2, get_name)
	else:				
		try:
			cursor.execute("""UPDATE my_data SET name=? WHERE id=?""", (message.text, message.chat.id, ))
			conn.commit()
		except:
			pass
		
		msg2 = bot.send_message(message.chat.id, "Yoshingizni kiriting👇🏻")
		bot.register_next_step_handler(msg2, get_age)	
		
def get_age(message):
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()

	if message.text.isnumeric():
		try:
			cursor.execute("""UPDATE my_data SET age=? WHERE id=?""", (int(message.text), message.chat.id, ))
			conn.commit()
		except:
			pass
		msg3 = bot.send_message(message.chat.id, "Telefon raqamingizni kiriting👇🏻\nFormat: 9X-XXX-XX-XX")
		bot.register_next_step_handler(msg3, get_number)
	else:
		msg2 = bot.send_message(message.chat.id, "Iltimos, yoshingizni to'g'ri kiriting👇🏻")
		bot.register_next_step_handler(msg2, get_age)

def has_numbers(inputString):
	return any(char.isdigit() for char in inputString)

def get_number(message):
	conn = sqlite3.connect("database.db")
	cursor = conn.cursor()

	if has_numbers(message.text):		
		try:
			cursor.execute("""UPDATE my_data SET phone_number=? WHERE id=?""", (message.text, message.chat.id, ))
			conn.commit()
		except:
			pass
		bot.send_message(message.chat.id, "Rahmat!\nTez orada menejirimiz siz bilan bog'lanadi")
	else:
		msg2 = bot.send_message(message.chat.id, "Iltimos, telefon raqamingizni to'g'ri kiriting👇🏻\nFormat: 9X-XXX-XX-XX")
		bot.register_next_step_handler(msg2, get_number)	

def rassilka(message):
	try:
		if message.text!="cancel" and message.text!="Cancel" and message.text!="ortga":
			conn = sqlite3.connect("database.db") # или :memory: чтобы сохранить в RAM
			cursor = conn.cursor()
			cursor.execute("SELECT id FROM my_data")
			Lusers = cursor.fetchall()
			users=[]
			for i in Lusers:
				users.append(list(i)[0])

			for i in users:
				try:
					if message.content_type == "text":
					#text
						tex = message.html_text
						bot.send_message(i, tex, parse_mode='html')
					elif message.content_type == "photo":
					#photo
						capt = message.html_caption
						photo = message.photo[-1].file_id
						bot.send_photo(i, photo, caption=capt, parse_mode='html')
					elif message.content_type == "video":
					#video
						capt = message.html_caption
						photo = message.video.file_id
						bot.send_video(i, photo, caption=capt, parse_mode='html')
					elif message.content_type == "audio":
					#audio
						capt = message.html_caption
						photo = message.audio.file_id
						bot.send_audio(i, photo, caption=capt, parse_mode='html')
					elif message.content_type == "voice":
					#voice
						capt = message.html_caption
						photo = message.voice.file_id
						bot.send_voice(i, photo, caption=capt, parse_mode='html')
					elif message.content_type == "animation":
					#animation
						capt = message.html_caption
						photo = message.animation.file_id
						bot.send_animation(i, photo, caption=capt, parse_mode='html')
					elif message.content_type == "document":
					#document
						capt = message.html_caption
						photo = message.document.file_id
						bot.send_document(i, photo, caption=capt, parse_mode='html')
				except Exception as e:
					re=10
					pass        
	except:
		pass



bot.polling(none_stop=True)