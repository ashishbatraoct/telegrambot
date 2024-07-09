import os
import re
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from telegram.error import BadRequest

# Load environment variables from .env file
load_dotenv()

# Your bot token from the .env file
TOKEN = os.getenv('BOT_TOKEN')

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the set of words to filter
FILTER_WORDS = {
   
    'join', 'follow', 'click here', 'buy now',  # Added words
    # Sample list of vulgar words (this is just an example, you might want to use a more comprehensive list)
    'sex'
}

# Create variations for common words
VARIATIONS = {
    'join': r'j\s*o\s*i\s*n|joim',
    'follow': r'f\s*o\s*l\s*l\s*o\s*w',
    'click here': r'c\s*l\s*i\s*c\s*k\s*h\s*e\s*r\s*e',
    'buy now': r'b\s*u\s*y\s*n\s*o\s*w',
}

# Include the variations in the filter words
for word, variation in VARIATIONS.items():
    FILTER_WORDS.add(variation)

# Construct a regular expression pattern that matches links or any of the filter words
pattern = re.compile(
    r'\b(?:' + '|'.join(re.escape(word) for word in FILTER_WORDS) +  r')\b|http[s]?://|^//|@|^!|('  + '|'.join(VARIATIONS.values()) + ')',
    re.IGNORECASE
)


async def delete_links(update: Update, context: CallbackContext) -> None:
    try:
        message = update.message
        logger.info(f"Received message: {message.text}")
        
        # Check if the user is an admin
        chat_id = message.chat.id
        user_id = message.from_user.id

        try:
            member = await context.bot.get_chat_member(chat_id, user_id)
            if member.status in ['administrator', 'creator']:
                logger.info(f"Message from admin: {message.text}")
                return
        except BadRequest as e:
            logger.error(f"Error checking admin status: {e}")

        if pattern.search(message.text):
            await context.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            logger.info(f"Deleted message: {message.text}")
    except Exception as e:
        logger.error(f"Error in delete_links: {e}")

def main() -> None:
    try:
        app = Application.builder().token(TOKEN).build()
        link_handler = MessageHandler(filters.TEXT & filters.Regex(pattern), delete_links)
        app.add_handler(link_handler)
        app.run_polling()
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == '__main__':
    main()
