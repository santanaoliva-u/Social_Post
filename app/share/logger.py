# app/shared/logger.py
"""
Módulo de logging para la aplicación.

Este módulo configura y proporciona un logger global para la aplicación utilizando la
biblioteca estándar de logging.
"""

import logging
import sys

# Excepción personalizada para errores del logger
class LoggerError(Exception):
    """Excepción lanzada cuando falla la configuración o uso del logger."""
    pass

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Configura y devuelve un logger con el nombre y nivel especificados.

    Args:
        name (str): Nombre del logger.
        level (int): Nivel de logging (por defecto INFO).

    Returns:
        logging.Logger: Instancia del logger configurado.

    Raises:
        LoggerError: Si falla la configuración del logger.
    """
    try:
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Evitar duplicación de handlers
        if not logger.handlers:
            # Handler para la consola
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)

            # Formato de los logs
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger
    except Exception as e:
        raise LoggerError(f"Error al configurar el logger: {e}") from e

# Logger global para la aplicación
logger = setup_logger("app")