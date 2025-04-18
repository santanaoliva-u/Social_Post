# main.py
"""
Punto de entrada principal para la aplicación backend.

Este script inicializa la configuración, el logger, los servicios y adaptadores,
y arranca la aplicación de forma modular siguiendo los principios de la arquitectura hexagonal.
"""

import asyncio
from app.config.config import config, ConfigError
from app.shared.logger import logger, LoggerError
from app.domain.services.session_service import SessionService
from app.domain.services.telegram_service import TelegramService
from app.adapters.telegram.telegram_adapter import TelegramAdapter
from app.adapters.selenium.selenium_adapter import SeleniumAdapter
from app.adapters.storage.storage_adapter import InMemoryStorageAdapter

def main():
    """
    Función principal que arranca la aplicación.

    Raises:
        ConfigError: Si la configuración no se carga correctamente.
        LoggerError: Si falla la inicialización del logger.
        Exception: Para errores inesperados durante el arranque.
    """
    try:
        # Verificar que la configuración se ha cargado correctamente
        logger.info("Iniciando la aplicación...")
        logger.debug(f"Token de Telegram cargado: {config.TELEGRAM_BOT_TOKEN[:5]}... (truncado por seguridad)")
        logger.debug(f"IDs de administradores: {config.TELEGRAM_ADMIN_IDS}")

        # Instanciar servicios del dominio
        session_service = SessionService()
        telegram_service = TelegramService()

        # Instanciar adaptadores con inyección de dependencias
        storage_adapter = InMemoryStorageAdapter()
        selenium_adapter = SeleniumAdapter()
        telegram_adapter = TelegramAdapter(telegram_service)

        # Arrancar el bot de Telegram en un hilo separado
        logger.info("Arrancando el bot de Telegram...")
        asyncio.run(telegram_adapter.start_bot())

    except ConfigError as e:
        logger.error(f"Error en la configuración: {e}")
        raise
    except LoggerError as e:
        logger.error(f"Error en el logger: {e}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al iniciar la aplicación: {e}")
        raise

if __name__ == "__main__":
    main()