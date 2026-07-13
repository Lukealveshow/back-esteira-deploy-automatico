import subprocess
from pathlib import Path
from dataclasses import dataclass, field

from app import config

@dataclass
class ResultadoBuild:
    sucesso: bool
    log: str
    caminho_war: Path | None = None
    comandos_executados: list[str] = field(default_factory=list)

def _executar_comando(comando: list[str], cwd: Path)-> tuple[bool, str]:
    processo = subprocess.run(
        comando,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    saida = processo.stdout + processo.stderr
    return processo.returncode == 0, saida

def preparar_workspace(branch: str) -> tuple[bool, str]:
    config.WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    repo_dir = config.WORKSPACE_DIR / "ebop"
    log_completo = ""

    if not (repo_dir / ".git").exists():
        ok, saida = _executar_comando(
                        ["git", "clone", config.git_url_authenticada(), str(repo_dir)],
            cwd=config.WORKSPACE_DIR,
        )

        log_completo += f"$ git clone <repo>\n{saida}\n"
        if not ok:
            return False, log_completo
    else:
        ok, saida = _executar_comando(["git", "fetch", "origin"], cwd=repo_dir)
        log_completo += f"$ git fetch origin\n{saida}\n"
        if not ok:
            return False, log_completo
 
    ok, saida = _executar_comando(["git", "checkout", branch], cwd=repo_dir)
    log_completo += f"$ git checkout {branch}\n{saida}\n"
    if not ok:
        return False, log_completo
 
    ok, saida = _executar_comando(["git", "pull", "origin", branch], cwd=repo_dir)
    log_completo += f"$ git pull origin {branch}\n{saida}\n"
    if not ok:
        return False, log_completo
 
    return True, log_completo
 
def buildar_modulo(modulo: str, branch: str = "main")-> ResultadoBuild:
    if modulo not in config.MODULOS_VALIDOS:
        return ResultadoBuild(
            sucesso=False,
            log=f"Módulo '{modulo}' inválido. Válidos: {config.MODULOS_VALIDOS}",
        )
    log_total = ""
    ok, log_git = preparar_workspace(branch)
    log_total+=log_git
    if not ok:
        return ResultadoBuild(sucesso=False, log=log_total)
    repo_dir = config.WORKSPACE_DIR / "ebop"
    modulo_dir = repo_dir / modulo

    if not modulo_dir.exists():
        log_total += f"\nPasta do módulo não encontrada: {modulo_dir}\n"
        return ResultadoBuild(sucesso=False, log=log_total)

    ok, log_maven = _executar_comando(
        [config.MAVEN_CMD, "clean", "package"],
        cwd=modulo_dir,
    )
    log_total += f"$ mvn clean package -pl {modulo} -am\n{log_maven}\n"

    if not ok:
        return ResultadoBuild(sucesso=False, log=log_total)
    
    target_dir = repo_dir / modulo / "target"
    wars = list(target_dir.glob("*.war")) if target_dir.exists() else []

    if not wars:
        log_total += f"\nBuild passou, mas nenhum .war encontrado em {target_dir}\n"
        return ResultadoBuild(sucesso=False, log=log_total)
    
    return ResultadoBuild(sucesso=True, log=log_total, caminho_war=wars[0])