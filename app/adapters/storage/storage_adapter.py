# app/adapters/storage/storage_adapter.py
"""
Adaptador para almacenamiento persistente.
Implementa el puerto de salida StoragePort para guardar y recuperar sesiones.
"""

from typing import Optional
from app.domain.entities.session import Session
from app.ports.out.storage_port import StoragePort
from app.shared.logger import logger

class InMemoryStorageAdapter(StoragePort):
    """
    Adaptador de almacenamiento en memoria para sesiones.
    """
    def __init__(self):
        self.sessions = {}

    def save_session(self, session: Session) -> None:
        """
        Guarda una sesión en el almacenamiento.
        """
        self.sessions[session.session_id] = session
        logger.info(f"Sesión guardada en memoria: {session.session_id}")

    def load_session(self, session_id: str) -> Optional[Session]:
        """
        Carga una sesión desde el almacenamiento.
        """
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str) -> None:
        """
        Elimina una sesión del almacenamiento.
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Sesión eliminada de memoria: {session_id}")