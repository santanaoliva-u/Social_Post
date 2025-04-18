# app/domain/entities/session.py
"""
Entidad que representa una sesión de navegador en la aplicación.

Esta entidad encapsula los datos relacionados con una sesión activa, como cookies y estado.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

# Excepción personalizada para errores relacionados con sesiones
class SessionError(Exception):
    """Excepción lanzada cuando falla la creación o manejo de una sesión."""
    pass

@dataclass
class Session:
    """
    Entidad que representa una sesión de navegador.

    Attributes:
        session_id (str): Identificador único de la sesión.
        cookies (Dict[str, str]): Cookies asociadas a la sesión.
        created_at (datetime): Fecha de creación de la sesión.
        expires_at (datetime): Fecha de expiración de la sesión.
        is_active (bool): Indica si la sesión está activa.
    """
    session_id: str
    cookies: Dict[str, str]
    created_at: datetime
    expires_at: datetime
    is_active: bool = True

    def __post_init__(self):
        """Valida los atributos de la sesión tras su inicialización."""
        try:
            if not self.session_id:
                raise SessionError("El session_id no puede estar vacío.")
            if self.created_at >= self.expires_at:
                raise SessionError("La fecha de expiración debe ser posterior a la de creación.")
        except Exception as e:
            raise SessionError(f"Error al inicializar la sesión: {e}") from e

    def deactivate(self) -> None:
        """
        Desactiva la sesión.

        Raises:
            SessionError: Si la sesión ya está desactivada.
        """
        if not self.is_active:
            raise SessionError("La sesión ya está desactivada.")
        self.is_active = False