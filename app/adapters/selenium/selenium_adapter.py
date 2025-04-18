# app/adapters/selenium/selenium_adapter.py
"""
Adaptador para Selenium.
Implementa el puerto de salida SeleniumPort para gestionar sesiones de navegador.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.domain.entities.session import Session
from app.ports.out.selenium_port import SeleniumPort
from app.config.config import config
from app.shared.logger import logger
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional

class SeleniumAdapter(SeleniumPort):
    """
    Adaptador que conecta el dominio con Selenium para la gestión de sesiones.
    """
    def __init__(self):
        self.sessions = {}  # Almacenamiento temporal de sesiones

    def _init_driver(self) -> webdriver.Chrome:
        """
        Inicializa un nuevo driver de Chrome con las opciones configuradas.
        """
        options = Options()
        if config.SELENIUM_HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)

    def create_session(self, url: str, credentials: Dict[str, str]) -> Session:
        """
        Crea una nueva sesión de navegador y realiza el login.
        """
        try:
            driver = self._init_driver()
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(credentials["username"])
            driver.find_element(By.NAME, "password").send_keys(credentials["password"])
            driver.find_element(By.NAME, "login").click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard")))
            cookies = {cookie["name"]: cookie["value"] for cookie in driver.get_cookies()}
            session_id = str(uuid.uuid4())
            session = Session(
                session_id=session_id,
                cookies=cookies,
                created_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            self.sessions[session_id] = driver
            logger.info(f"Sesión creada: {session_id}")
            return session
        except Exception as e:
            logger.error(f"Error al crear sesión con Selenium: {e}")
            raise

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Recupera una sesión existente.
        """
        if session_id in self.sessions:
            return Session(
                session_id=session_id,
                cookies={},
                created_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
        return None

    def close_session(self, session_id: str) -> None:
        """
        Cierra una sesión de navegador.
        """
        if session_id in self.sessions:
            self.sessions[session_id].quit()
            del self.sessions[session_id]
            logger.info(f"Sesión cerrada: {session_id}")