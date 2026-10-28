# Windows Codex global setup (one time)

This setup configures the **local Windows Codex user** to consult the two repositories automatically for website tasks. It does not run remotely from ChatGPT or modify the PC until you execute the script there.

## Install

1. Download `tools/install-codex-global.ps1` from the GitHub repository to your Windows Downloads folder.
2. Open PowerShell in that folder and run:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\install-codex-global.ps1
   ```

3. Look for **Global rules installed and verified**. For best results also check that both checkouts say **VERIFIED**. Restart local Windows Codex.

The script creates/updates `$env:CODEX_HOME\AGENTS.md` if CODEX_HOME is set, otherwise `$HOME\.codex\AGENTS.md`. It preserves any existing instructions, makes a timestamped backup on change, and safely appends/replaces only its own marked section. It checks out repositories in `standards\` under the same Codex home.

## Private research repo

`chenmu2024/gefei-seo` is private. If it displays **UNAVAILABLE**, check that your Git for Windows credential login has access to it, then run the same script again. The engineering repository is public, but also needs Git and network access to clone. The script never prompts for or stores credentials itself.

## Verify

In a **new local Windows Codex session**, ask: 

> 请报告你实际读取到的全局 AGENTS.md 路径，分别读取 Website-Starter-Standard 和 gefei-seo 本地仓库的 AGENTS.md，列出读到的具体文件。如果任何文件未访问成功，请明确标为未加载。

The global file instructs Codex to read relevant documents; it cannot guarantee a runtime has network access, Git authentication or permission to read local files. **Codex Cloud/WSL use separate environments** and need their own configuration.

## Security and scope

- No admin privileges, paid APIs, background services or changes to any existing website.
- No destructive Git cleanup or force updates; checkout must be on clean `main` for auto-fast-forward.
- No auto-deployment; publication requires explicit authorization.
- Re-running the installer is safe and doesn't duplicate rules.
- To remove the integration, delete just the managed block between the two HTML comment markers inside your global `AGENTS.md`; backups are retained.

To test the installer without downloading repos or changing real user settings: `powershell -NoProfile -ExecutionPolicy Bypass -File .\tests\test-codex-global-installer.ps1` from the repository root.
