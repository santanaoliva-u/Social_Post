# app/domain/entities/telegram_command.py
"""
Entidad que representa un comando recibido por el bot de Telegram.
"""

from dataclasses import dataclass
from typing import Optional

# Excepción personalizada para errores relacionados con comandos
class TelegramCommandError(Exception):
    """Excepción lanzada cuando falla la creación o validación de un comando."""
    pass

@dataclass
class TelegramCommand:
    """
    Entidad que representa un comando de Telegram.

    Attributes:
        command (str): Nombre del comando (e.g., "/status").
        user_id (int): ID del usuario que envía el comando.
        args (Optional[str]): Argumentos adicionales del comando.
    """
    command: str
    user_id: int
    args: Optional[str] = None

    def __post_init__(self):
        """Valida los atributos del comando tras su inicialización."""
        try:
            if not self.command.startswith("/"):
                raise TelegramCommandError("El comando debe empezar con '/'.")
            if self.user_id <= 0:
                raise TelegramCommandError("El user_id debe ser un número positivo.")
        except Exception as e:
            raise TelegramCommandError(f"Error al inicializar el comando: {e}") from e