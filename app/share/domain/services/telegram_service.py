# app/domain/services/telegram_service.py
"""
Servicio de dominio para la gestión de comandos de Telegram.

Este servicio contiene la lógica de negocio para procesar comandos recibidos por el bot.
"""

from typing import Optional
from app.domain.entities.telegram_command import TelegramCommand, TelegramCommandError
from app.shared.logger import logger
from app.config.config import config

class TelegramService:
    """
    Servicio para procesar comandos de Telegram.

    Este servicio implementa la lógica de negocio para validar y ejecutar comandos
    recibidos por el bot, siguiendo la arquitectura hexagonal.
    """
    def validate_command(self, command: TelegramCommand) -> bool:
        """
        Valida si un comando es permitido y proviene de un administrador autorizado.

        Args:
            command (TelegramCommand): Comando a validar.

        Returns:
            bool: True si el comando es válido, False en caso contrario.

        Raises:
            TelegramCommandError: Si falla la validación del comando.
        """
        try:
            # Validar que el comando está soportado
            supported_commands = {"/status", "/logs", "/session", "/retry", "/health", "/reboot"}
            if command.command not in supported_commands:
                logger.warning(f"Comando no soportado: {command.command}")
                return False

            # Validar que el usuario es un administrador
            admin_ids = set(map(int, config.TELEGRAM_ADMIN_IDS.split(",")))
            if command.user_id not in admin_ids:
                logger.warning(f"Usuario no autorizado: {command.user_id}")
                return False

            logger.debug(f"Comando válido: {command.command} de {command.user_id}")
            return True
        except ValueError as e:
            logger.error(f"Error en el formato de TELEGRAM_ADMIN_IDS: {e}")
            raise TelegramCommandError(f"Error en la configuración de admin IDs: {e}") from e
        except Exception as e:
            logger.error(f"Error al validar el comando: {e}")
            raise TelegramCommandError(f"Error al validar el comando: {e}") from e

    def process_command(self, command: TelegramCommand) -> str:
        """
        Procesa un comando válido y devuelve una respuesta.

        Args:
            command (TelegramCommand): Comando a procesar.

        Returns:
            str: Respuesta del comando.

        Raises:
            TelegramCommandError: Si falla el procesamiento del comando.
        """
        try:
            if not self.validate_command(command):
                return "Comando no permitido o usuario no autorizado."

            # Lógica de procesamiento según el comando
            if command.command == "/status":
                return "Sistema operativo. Todos los servicios activos."
            elif command.command == "/logs":
                return "Logs disponibles. Usa /logs <filtro> para más detalles."
            elif command.command == "/session":
                return "Sesión activa. Usa /session <id> para detalles."
            elif command.command == "/retry":
                return "Reintentando operación solicitada."
            elif command.command == "/health":
                return "Health check: OK"
            elif command.command == "/reboot":
                return "Reinicio programado. Confirmar con /reboot confirm."

            logger.info(f"Comando procesado: {command.command} por {command.user_id}")
            return "Comando ejecutado con éxito."
        except Exception as e:
            logger.error(f"Error al procesar el comando: {e}")
            raise TelegramCommandError(f"Error al procesar el comando: {e}") from e