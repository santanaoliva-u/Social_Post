# app/domain/services/session_service.py
"""
Servicio de dominio para la gestión de sesiones de navegador.

Este servicio contiene la lógica de negocio para crear, validar y desactivar sesiones.
"""

from datetime import datetime, timedelta
from typing import Dict
from app.domain.entities.session import Session, SessionError
from app.shared.logger import logger

class SessionService:
    """
    Servicio para gestionar sesiones de navegador.

    Este servicio implementa la lógica de negocio para la creación, validación y
    desactivación de sesiones, siguiendo la arquitectura hexagonal.
    """
    def create_session(self, session_id: str, cookies: Dict[str, str], ttl_hours: int = 24) -> Session:
        """
        Crea una nueva sesión con los datos proporcionados.

        Args:
            session_id (str): Identificador único de la sesión.
            cookies (Dict[str, str]): Cookies asociadas a la sesión.
            ttl_hours (int): Tiempo de vida de la sesión en horas (por defecto 24).

        Returns:
            Session: Entidad de sesión creada.

        Raises:
            SessionError: Si falla la creación de la sesión.
        """
        try:
            created_at = datetime.utcnow()
            expires_at = created_at + timedelta(hours=ttl_hours)
            session = Session(
                session_id=session_id,
                cookies=cookies,
                created_at=created_at,
                expires_at=expires_at
            )
            logger.info(f"Sesión creada: {session_id}")
            return session
        except SessionError as e:
            logger.error(f"Error al crear la sesión: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al crear la sesión: {e}")
            raise SessionError(f"Error inesperado: {e}") from e

    def validate_session(self, session: Session) -> bool:
        """
        Valida si una sesión es activa y no ha expirado.

        Args:
            session (Session): Sesión a validar.

        Returns:
            bool: True si la sesión es válida, False en caso contrario.

        Raises:
            SessionError: Si la sesión no es válida o está mal formada.
        """
        try:
            if not session.is_active:
                logger.warning(f"Sesión desactivada: {session.session_id}")
                return False
            if datetime.utcnow() > session.expires_at:
                logger.warning(f"Sesión expirada: {session.session_id}")
                return False
            logger.debug(f"Sesión válida: {session.session_id}")
            return True
        except Exception as e:
            logger.error(f"Error al validar la sesión: {e}")
            raise SessionError(f"Error al validar la sesión: {e}") from e

    def deactivate_session(self, session: Session) -> None:
        """
        Desactiva una sesión existente.

        Args:
            session (Session): Sesión a desactivar.

        Raises:
            SessionError: Si falla la desactivación de la sesión.
        """
        try:
            session.deactivate()
            logger.info(f"Sesión desactivada: {session.session_id}")
        except SessionError as e:
            logger.error(f"Error al desactivar la sesión: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al desactivar la sesión: {e}")
            raise SessionError(f"Error inesperado: {e}") from e