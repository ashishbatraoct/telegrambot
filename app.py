import os
import re
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Load environment variables from a .env file
load_dotenv()

# Initialize logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the command handler
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logger.info(f"Received message: {user_message}")
    
    # Example: simple response
    await update.message.reply_text(f"You said: {user_message}")

# Main function to set up the bot
def main() -> None:
    # Get the token from the environment variable
    token = os.getenv("TELEGRAM_TOKEN")
    
    if not token:
        logger.error("No TELEGRAM_TOKEN found in environment variables")
        return

    # Create the Application and pass it your bot's token
    application = Application.builder().token(token).build()

    # Add a message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    application.run_polling()

if __name__ == '__main__':
    main()