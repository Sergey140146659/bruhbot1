import logging
import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import models
from telegram import Message

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def save(update, context):
    msg: Message = update.message

    models.User.get_or_create(
        tg_id=msg.from_user.id,
        defaults={
            "full_name": msg.from_user.full_name
        }
    )

    models.Message.create(message_id=msg.message_id,
                          chat_id=msg.chat_id,
                          text=msg.text,
                          tg_id=msg.from_user.id
                          )


def start(update, context):
    update.message.reply_text('Hi!')


def help(update, context):
    update.message.reply_text('Help!')


def last(update, context):
    last = 10
    if len(context.args) > 0:
        last = int(context.args[0])
    msg: telegram.Message = update.message
    for msg2 in models.Message.filter(chat_id=msg.chat_id).order_by(models.Message.id.desc()).limit(10):
        update.message.reply_text(msg2.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(config.TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("last", last))
    dp.add_handler(MessageHandler(Filters.text, save))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

    if config.HEROKU_APP_NAME is None:
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0",
                              port=config.PORT,
                              url_path=config.TOKEN)
        updater.bot.set_webhook(f"https://{config.HEROKU_APP_NAME}.herokuapp.com/{config.TOKEN}")

    updater.idle()

    if __name__ == '__main__':
        main()
