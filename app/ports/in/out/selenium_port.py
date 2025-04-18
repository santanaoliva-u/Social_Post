# app/ports/out/selenium_port.py
"""
Puerto de salida para la interacción con Selenium.
Define la interfaz para gestionar sesiones de navegador.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from app.domain.entities.session import Session

class SeleniumPort(ABC):
    """
    Interfaz para la gestión de sesiones con Selenium.
    """
    @abstractmethod
    def create_session(self, url: str, credentials: Dict[str, str]) -> Session:
        """
        Crea una nueva sesión de navegador.

        Args:
            url (str): URL inicial de la sesión.
            credentials (Dict[str, str]): Credenciales para el login.

        Returns:
            Session: Sesión creada.
        """
        pass

    @abstractmethod
    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Recupera una sesión existente.

        Args:
            session_id (str): ID de la sesión.

        Returns:
            Optional[Session]: Sesión si existe, None si no.
        """
        pass

    @abstractmethod
    def close_session(self, session_id: str) -> None:
        """
        Cierra una sesión de navegador.

        Args:
            session_id (str): ID de la sesión a cerrar.
        """
        pass