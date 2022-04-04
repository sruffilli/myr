#!/usr/bin/env python3
import os

from dotenv import load_dotenv
from googletrans import Translator
from telegram.constants import PARSEMODE_MARKDOWN
from telegram.ext import Filters, MessageHandler, Updater

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ERROR_UK = "Щось пішло не так, як я намагався перекласти :( Повторіть спробу"
ERROR_IT = "Qualcosa e' andato storto mentre provavo a tradurre :( Riprova"


def translate_message(txt):
  r = None
  try:
    translator = Translator()
    lang_to = None
    lang_from = translator.detect(txt).lang
    if lang_from == "uk":
      lang_to = "it"
    else:
      lang_to = "uk"

    r = translator.translate(txt, src=lang_from, dest=lang_to).text
  except:
    pass
  return r


def reaction(update, context):
  if update.message.chat.type == "private":
    return
  message = update.message.text
  translation = translate_message(message)
  if translation:
    ret = f'*{update.message.from_user.username} ({update.message.from_user.first_name} {update.message.from_user.last_name}) says:*'
    ret = ret + "\n" + translation
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ret,
        parse_mode=PARSEMODE_MARKDOWN,
    )
  else:
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=ERROR_IT + "\n" + ERROR_UK)
  return


def main():
  print("Myr starting...")
  updater = Updater(token=BOT_TOKEN)
  dispatcher = updater.dispatcher

  reaction_handler = MessageHandler(Filters.text & (~Filters.command), reaction)
  dispatcher.add_handler(reaction_handler)

  updater.start_polling()


if __name__ == '__main__':
  main()
