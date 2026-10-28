#requires -Version 5.1
$ErrorActionPreference = 'Stop'
$script = Join-Path (Split-Path $PSScriptRoot -Parent) 'tools\install-codex-global.ps1'
$temp = Join-Path ([System.IO.Path]::GetTempPath()) ('codex-standard-test-' + [Guid]::NewGuid().ToString('N'))
$previous = $env:CODEX_HOME
try {
    $env:CODEX_HOME = Join-Path $temp '.codex'
    New-Item -ItemType Directory -Force -Path $env:CODEX_HOME | Out-Null
    $target = Join-Path $env:CODEX_HOME 'AGENTS.md'
    [System.IO.File]::WriteAllText($target, '# Keep existing project preferences' + [Environment]::NewLine)
    & $script -SkipRepositorySync
    $one = [System.IO.File]::ReadAllText($target)
    if ($one -notlike '*# Keep existing project preferences*') { throw 'Installer overwrote existing instructions.' }
    if ($one -notlike '*Website-Starter-Standard*') { throw 'Engineering source absent.' }
    if ($one -notlike '*gefei-seo*') { throw 'Research source absent.' }
    if (@([regex]::Matches($one, '<!-- BEGIN MANAGED WEBSITE STANDARD RULES -->')).Count -ne 1) {
        throw 'Managed block missing or duplicated.'
    }
    & $script -SkipRepositorySync
    $two = [System.IO.File]::ReadAllText($target)
    if ($one -cne $two) { throw 'Reinstall should be idempotent.' }
    $backups = @(Get-ChildItem -Path $env:CODEX_HOME -Filter 'AGENTS.md.backup-*')
    if ($backups.Count -ne 1) { throw "Expected one backup, got $($backups.Count)." }
    Write-Host 'PASS: preserved existing text, one managed block, idempotence, and backup.'
} finally {
    $env:CODEX_HOME = $previous
    if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Recurse -Force }
}
