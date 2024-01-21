from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import logging
from urllib.parse import urlencode, urljoin

ACCOUNT_NUMBER = "4455416043"
BANK_CODE = "0800"
PRICE_WITH_MS = 30
PRICE_WITHOUT_MS = 190

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
log = logging.getLogger(__name__)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Hi, I am alive!")
    log.info("123 check")
    return ConversationHandler.END


async def send_qr_with_ms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_photo(photo=build_qr_url(PRICE_WITH_MS, update.message.from_user))
    return ConversationHandler.END


async def send_qr_without_ms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_photo(photo=build_qr_url(PRICE_WITHOUT_MS, update.message.from_user))
    return ConversationHandler.END


def build_qr_url(amount, user):
    base_url = "https://api.paylibo.com/paylibo/generator/czech/image"
    params = {
        'accountNumber': ACCOUNT_NUMBER,
        'bankCode': BANK_CODE,
        'amount': str(amount),
        'currency': 'CZK',
        'vs': str(user.id),
        'message': user.first_name + " " + user.last_name + " " + user.username
    }
    return urljoin(base_url, '?' + urlencode(params))
