import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GIT_USUARIO = os.getenv("GIT_USUARIO", "")
GIT_TOKEN = os.getenv("GIT_TOKEN", "")
GIT_REPO_URL = os.getenv("GIT_REPO_URL", "")

def git_url_authenticada() -> str:
    if not GIT_REPO_URL:
        raise ValueError("URL de repositório Git não configurada")
    if GIT_USUARIO and GIT_TOKEN:
        return GIT_REPO_URL.replace("https://", f"https://{GIT_USUARIO}:{GIT_TOKEN}@")
    return GIT_REPO_URL

BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = BASE_DIR / "workspace"

MODULOS_VALIDOS = ["Atendimento", "Auth", "commons", "ejb", "jpa", "portal", "principal", "pabx-service"]

MAVEN_CMD = os.getenv("MAVEN_CMD", "mvn")

TOMCAT_HOST = os.getenv("TOMCAT_HOST", "")
TOMCAT_MANAGER_USER = os.getenv("TOMCAT_MANAGER_USER", "")
TOMCAT_MANAGER_PASS = os.getenv("TOMCAT_MANAGER_PASS", "")