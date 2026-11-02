# 🔌 Entwicklung eines Model Context Protocol (MCP) Servers zur direkten Claude-Obsidian-Integration

Ein sicherer, performanter Python-Server auf Basis des **Model Context Protocol (MCP)**, der Claude Desktop direkten, strukturierten Lese- und Schreibzugriff auf ein lokales Obsidian-Knowledge-Management-System (PKM) gewährt.

---

## 🚀 Executive Summary & Projektziel

Um die Interaktion zwischen modernsten LLMs (wie Claude) und lokalen Arbeitsumgebungen nahtlos zu gestalten, wurde in diesem Projekt ein eigener MCP-Server implementiert. Der Server stellt standardisierte Tools bereit, mit denen Claude eigenständig Notizen auflisten, analysieren, erstellen und aktualisieren kann. Im Fokus standen dabei maximale Entwicklungsgeschwindigkeit, intuitive Tool-Definitionen über `FastMCP` sowie ein kompromissloses Sicherheitskonzept.

> **Transparenzhinweis & Entwicklungsansatz:** Dieses System wurde nach dem „AI-First-Builder“-Prinzip konzipiert und umgesetzt. Als Architekt der Schnittstelle lag der Fokus auf der Definition der Tool-Signaturen, der Datenvalidierung und der sicheren Sandbox-Architektur. Der Einsatz moderner KI-Assistenten diente dabei als hocheffizienter Entwicklungshebel für die Boilerplate-Implementierung und Dokumentation – ein klares Statement für pragmatisches, zukunftsorientiertes AI Engineering.

---

## 🛠️ Tech Stack & Architektur

* **Programmiersprache:** Python 3.10+
* **Protokoll & Framework:** Model Context Protocol (MCP) via `mcp.server.fastmcp`
* **Datenformat & Serialisierung:** YAML (`pyyaml`) für frontmatter-kompatibles Wissensmanagement
* **Dateisystem-Interaktion:** Native Python Pathlib (`pathlib.Path`)

---

## ⚙️ Bereitgestellte MCP-Tools

Der Server registriert vier essenzielle Werkzeuge, die Claude dynamisch aufrufen kann:

1. **`list_vault_notes()`**: Scannt den konfigurierten Obsidian-Vault rekursiv und liefert eine Liste aller relativen Markdown-Dateipfade.
2. **`read_note(note_path)`**: Liest den exakten Inhalt einer spezifischen Notiz aus.
3. **`create_note(note_path, content, frontmatter)`**: Erstellt neue Notizen inklusive automatisierter YAML-Frontmatter-Generierung und automatischer Verzeichnis-Erstellung.
4. **`update_note(note_path, content, mode)`**: Erlaubt das modifizierte Aktualisieren bestehender Dokumente wahlweise im `append`-Modus (anhängen) oder `replace`-Modus (überschreiben).

---

## 🔒 Security & Sandboxing

Um unbefugten Dateizugriff oder Systemkompromittierungen durch das LLM auszuschließen, ist in jedem Tool eine strikte **Path-Traversal-Validierung** integriert:

```python
if not full_path.resolve().is_relative_to(VAULT_PATH.resolve()):
    return "Fehler: Ungültiger Pfad (Sicherheitsverletzung)."
```
Dadurch wird sichergestellt, dass Claude sich physisch niemals außerhalb des definierten Obsidian-Vault-Verzeichnisses bewegen kann.

📥 Integration in Claude Desktop
Um den Server lokal in Claude Desktop einzubinden, wird die Konfigurationsdatei (claude_desktop_config.json) um folgenden Eintrag ergänzt:

{
  "mcpServers": {
    "obsidian-vault-manager": {
      "command": "python",
      "args": [
        "C:/Dein/Pfad/zu/mcp-obsidian-manager/Scripts/server.py"
      ]
    }
  }
}

## 💡 Key Learnings & Fazit
Standardisierung durch MCP: MCP löst das Schnittstellen-Chaos zwischen LLMs und lokalen Tools auf elegante, standardisierte Weise.

Sicherheit an erster Stelle: Auch bei lokalen KI-Integrationen sind Sandbox-Prüfungen (is_relative_to) unerlässlich, um unbeabsichtigte Dateimodifikationen zu verhindern.

Effizienz von FastMCP: Das Framework reduziert den Implementierungsaufwand für komplexe Protokoll-Server auf ein absolutes Minimum.

## 📁 Repository-Struktur
'''text
├── Scripts/
│   └── server.py           # MCP-Server mit FastMCP & Sicherheitsvalidierung
├── requirements.txt        # Python-Abhängigkeiten (mcp, pyyaml)
└── README.md               # Projektdokumentation
