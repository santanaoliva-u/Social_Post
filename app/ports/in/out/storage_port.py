# app/ports/out/storage_port.py
"""
Puerto de salida para la interacción con almacenamiento persistente.
Define la interfaz para guardar y recuperar datos.
"""

from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.session import Session

class StoragePort(ABC):
    """
    Interfaz para gestionar almacenamiento persistente.
    """
    @abstractmethod
    def save_session(self, session: Session) -> None:
        """
        Guarda una sesión en el almacenamiento.

        Args:
            session (Session): Sesión a guardar.
        """
        pass

    @abstractmethod
    def load_session(self, session_id: str) -> Optional[Session]:
        """
        Carga una sesión desde el almacenamiento.

        Args:
            session_id (str): ID de la sesión.

        Returns:
            Optional[Session]: Sesión si existe, None si no.
        """
        pass

    @abstractmethod
    def delete_session(self, session_id: str) -> None:
        """
        Elimina una sesión del almacenamiento.

        Args:
            session_id (str): ID de la sesión a eliminar.
        """
        pass