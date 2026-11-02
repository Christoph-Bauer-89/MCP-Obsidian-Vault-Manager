from mcp.server.fastmcp import FastMCP
import os
from pathlib import Path
import yaml

# Initialisiere den MCP-Server
mcp = FastMCP("Obsidian Vault Manager")

# WICHTIG: Passe diesen Pfad exakt an den Ordner deines Obsidian-Vaults an!
VAULT_PATH = Path(r"C:/Dein/Pfad/zu/deinem/Vault")

@mcp.tool()
def list_vault_notes() -> list[str]:
    """Listet alle Markdown-Notizen im Obsidian-Vault auf."""
    if not VAULT_PATH.exists():
        return [f"Fehler: Vault-Pfad {VAULT_PATH} existiert nicht."]
    
    md_files = [str(p.relative_to(VAULT_PATH)) for p in VAULT_PATH.glob("**/*.md")]
    return md_files

@mcp.tool()
def read_note(note_path: str) -> str:
    """Liest den Inhalt einer spezifischen Obsidian-Notiz.
    
    Args:
        note_path: Der relative Pfad zur Notiz (z.B. 'Ordner/Notiz.md').
    """
    full_path = VAULT_PATH / note_path
    
    if not full_path.resolve().is_relative_to(VAULT_PATH.resolve()):
        return "Fehler: Ungültiger Pfad (Sicherheitsverletzung)."
        
    if not full_path.exists():
        return f"Fehler: Notiz '{note_path}' wurde nicht gefunden."
        
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def create_note(note_path: str, content: str, frontmatter: dict = None) -> str:
    """Erstellt eine neue Markdown-Notiz inklusive optionalem YAML-Frontmatter.
    
    Args:
        note_path: Relativer Pfad zur neuen Datei (z. B. 'AI-Lab/MCP-Kapitel.md').
        content: Der eigentliche Textinhalt der Notiz.
        frontmatter: Schlüssel-Wert-Paare für YAML-Frontmatter (z. B. {"tags": ["mcp", "ai"], "status": "draft"}).
    """
    full_path = VAULT_PATH / note_path
    
    if not full_path.resolve().is_relative_to(VAULT_PATH.resolve()):
        return "Fehler: Ungültiger Pfad (Sicherheitsverletzung)."
        
    if full_path.exists():
        return f"Fehler: Notiz '{note_path}' existiert bereits. Nutze 'update_note' zum Bearbeiten."
        
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_content = ""
    if frontmatter:
        yaml_block = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
        file_content += f"---\n{yaml_block}---\n\n"
        
    file_content += content
    
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(file_content)
        
    return f"Erfolg: Notiz '{note_path}' wurde erfolgreich erstellt."

@mcp.tool()
def update_note(note_path: str, content: str, mode: str = "append") -> str:
    """Aktualisiert eine bestehende Obsidian-Notiz.
    
    Args:
        note_path: Relativer Pfad zur Datei.
        content: Der Inhalt, der hinzugefügt oder überschrieben werden soll.
        mode: 'append' (unten anhängen) oder 'replace' (ganze Datei überschreiben).
    """
    full_path = VAULT_PATH / note_path
    
    if not full_path.resolve().is_relative_to(VAULT_PATH.resolve()):
        return "Fehler: Ungültiger Pfad (Sicherheitsverletzung)."
        
    if not full_path.exists():
        return f"Fehler: Notiz '{note_path}' existiert nicht. Nutze 'create_note' zum Erstellen."
        
    if mode == "append":
        with open(full_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n{content}")
        return f"Erfolg: Notiz '{note_path}' wurde ergänzt (append)."
    elif mode == "replace":
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Erfolg: Notiz '{note_path}' wurde überschrieben (replace)."
    else:
        return "Fehler: Ungültiger Modus. Erlaubt sind 'append' oder 'replace'."

if __name__ == "__main__":
    mcp.run(transport='stdio')
