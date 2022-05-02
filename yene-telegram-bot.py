import os, telebot, csv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

#API_KEY = '5376008511:AAF0PUs25QGnIfmf0cFcU53O3tnS3e1lgPk'
API_KEY = '5114435234:AAGyFATaFCUXyonmRV8kB68WGTBP-s2oDOc'

bot = telebot.TeleBot(API_KEY)
#bot.set_webhook()

tg_std_ids = {616540060: '0102/13', 1085350448: '0406/13', 1457760659: '4748/13', 716072962: '0547/13', 1852599241: '0571/13', 790361728: '0727/13', 946954073: '0793/13', 5275555010: '0857/13', 1749942403: '0987/13', 5124247505: '1092/13', 1326369761: '1178/13', 642540516: '1198/13', 1650564210: '1247/13', 659006861: '1380/13', 1607004128: '1485/13', 5243708594: '1496/13', 835007431: '1501/13', 1869220319: '1542/13', 687140116: '1630/13', 1671602737: '1651/13', 1352447923: '1653/13', 781655041: '1970/13', 1429824442: '1974/13', 788617323: '2006/13', 1601244847: '2050/13', 1935617579: '2063/13', 196262476: '2082/13', 1122447230: '2134/13', 1165764727: '2357/13', 5058453464: '2494/13', 705112575: '2505/13', 476765725: '2521/13', 1486466727: '2525/13', 1067019910: '2550/13', 1288185971: '2723/13', 1910231449: '2726/13', 1788848778: '2799/13', 1651407207: '2878/13', 1822882222: '2956/13'}

def get_tg_id(student_id):
  for tg_id, std_id in tg_std_ids.items():
    if student_id == std_id:
      return tg_id



def send_result():
  ResultsFile = "./Assets/DLD-Results.csv"
  with open(ResultsFile, "r", encoding="utf-8")as RFile:
    Results = csv.DictReader(RFile)
    header = Results.fieldnames

    for Result in Results:
      msg = "✨✨DLD-Results✨✨\n--------------------------------------\n"
      std_id = Result[header[0]]
      tg_id = get_tg_id(std_id)
      for x in range(0,len(header)-1):
        msg += "   "+header[x] + " : " + Result[header[x]] + "\n"
      try:
        markup = InlineKeyboardMarkup()
        markup.width = 2
        markup.add(
          InlineKeyboardButton("✅", callback_data = str(tg_id)+"yes"),
          InlineKeyboardButton("❎", callback_data = str(tg_id)+"no!")
        )

        bot.send_message(tg_id, msg, reply_markup = markup)
      except:
        print(std_id, tg_id)

#send_result()
@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
  if call.data[-3:] == "yes":
    bot.send_message(int(call.data[:-3]), "Thanks for the Reply.")
    bot.send_message(5058453464, tg_std_ids[int(call.data[:-3])]+"\nYes!")
  if call.data[-3:-1] == "no":
    sent_msg = bot.send_message(int(call.data[:-3]), "What went wrong?")
    bot.register_next_step_handler_by_chat_id(int(call.data[:-3]), reply_handler)
def reply_handler(message):
  reply = message.text
  bot.send_message(5058453464, tg_std_ids[message.chat.id]+"\n"+reply)
  bot.send_message(message.chat.id, "Thanks for the feedback")

bot.polling()
