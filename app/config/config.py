# app/config/config.py
"""
Módulo de configuración para la aplicación.

Este módulo proporciona la clase Config que carga y valida las variables de entorno
necesarias para la aplicación utilizando pydantic.
"""

from pydantic import BaseSettings, Field, ValidationError
from dotenv import load_dotenv
import os

# Excepción personalizada para errores de configuración
class ConfigError(Exception):
    """Excepción lanzada cuando falla la carga o validación de la configuración."""
    pass

# Cargar el archivo .env desde la raíz del proyecto
load_dotenv()

class Config(BaseSettings):
    """
    Clase de configuración que carga y valida las variables de entorno.

    Attributes:
        TELEGRAM_BOT_TOKEN (str): Token del bot de Telegram.
        TELEGRAM_ADMIN_IDS (str): Lista de IDs de administradores separados por comas.
        SELENIUM_HEADLESS (bool): Bandera para ejecutar Selenium en modo headless.

    Raises:
        ConfigError: Si las variables de entorno no son válidas o están ausentes.
    """
    TELEGRAM_BOT_TOKEN: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    TELEGRAM_ADMIN_IDS: str = Field(..., env="TELEGRAM_ADMIN_IDS")
    SELENIUM_HEADLESS: bool = Field(True, env="SELENIUM_HEADLESS")

    class Config:
        """Configuración de pydantic para la carga de variables de entorno."""
        env_file = ".env"
        env_file_encoding = "utf-8"

try:
    # Instancia global de la configuración
    config = Config()
except ValidationError as e:
    raise ConfigError(f"Error al validar las variables de entorno: {e}") from e
except Exception as e:
    raise ConfigError(f"Error inesperado al cargar la configuración: {e}") from e