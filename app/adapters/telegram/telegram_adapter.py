# app/adapters/telegram/telegram_adapter.py
"""
Adaptador para el bot de Telegram.
Implementa el puerto de entrada TelegramPort para procesar comandos.
"""

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app.domain.entities.telegram_command import TelegramCommand
from app.domain.services.telegram_service import TelegramService
from app.ports.in.telegram_port import TelegramPort
from app.config.config import config
from app.shared.logger import logger

class TelegramAdapter(TelegramPort):
    """
    Adaptador que conecta el bot de Telegram con el dominio.
    """
    def __init__(self, telegram_service: TelegramService):
        self.telegram_service = telegram_service
        self.application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    async def _handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Maneja los comandos recibidos por el bot.
        """
        try:
            command_text = update.message.text.split()[0]
            user_id = update.message.from_user.id
            args = " ".join(update.message.text.split()[1:]) if len(update.message.text.split()) > 1 else None
            command = TelegramCommand(command=command_text, user_id=user_id, args=args)
            response = self.telegram_service.process_command(command)
            await update.message.reply_text(response)
        except Exception as e:
            logger.error(f"Error al procesar comando de Telegram: {e}")
            await update.message.reply_text("Error al procesar el comando.")

    def start_bot(self) -> None:
        """
        Inicia el bot de Telegram y registra los manejadores de comandos.
        """
        try:
            supported_commands = ["status", "logs", "session", "retry", "health", "reboot"]
            for cmd in supported_commands:
                self.application.add_handler(CommandHandler(cmd, self._handle_command))
            self.application.run_polling()
        except Exception as e:
            logger.error(f"Error al iniciar el bot de Telegram: {e}")
            raise

    def process_command(self, command: TelegramCommand) -> str:
        """
        Implementación del método del puerto para procesar comandos.
        """
        return self.telegram_service.process_command(command)