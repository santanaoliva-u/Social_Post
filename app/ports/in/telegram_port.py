# app/ports/in/telegram_port.py
"""
Puerto de entrada para la interacción con el bot de Telegram.
Define la interfaz que los adaptadores deben implementar para procesar comandos.
"""

from abc import ABC, abstractmethod
from app.domain.entities.telegram_command import TelegramCommand

class TelegramPort(ABC):
    """
    Interfaz para gestionar comandos de Telegram.
    """
    @abstractmethod
    def process_command(self, command: TelegramCommand) -> str:
        """
        Procesa un comando de Telegram y devuelve una respuesta.

        Args:
            command (TelegramCommand): Comando recibido del bot.

        Returns:
            str: Respuesta generada para el usuario.
        """
        pass