# main.py
"""
Punto de entrada principal para la aplicación backend.

Este script inicializa la configuración, el logger y arranca la aplicación de forma modular
siguiendo los principios de la arquitectura hexagonal.
"""

from app.config.config import config, ConfigError
from app.shared.logger import logger, LoggerError

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

        # Lógica de arranque (desacoplada, preparada para inyectar dependencias)
        logger.info("Aplicación iniciada correctamente.")
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