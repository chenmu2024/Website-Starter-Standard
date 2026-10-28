#requires -Version 5.1
<#
.SYNOPSIS
  One-time installation of Codex global website rules for Windows.
.DESCRIPTION
  Backs up and preserves the existing AGENTS.md, replacing only a marked section.
  Optionally clones/fast-forward-syncs the two GitHub repositories.
  Does not change website source code, deploy anything, or store GitHub tokens.
.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File .\install-codex-global.ps1
#>
[CmdletBinding()]
param([switch]$SkipRepositorySync)

$ErrorActionPreference = 'Stop'
function Log([string]$Message) { Write-Host "[Codex setup] $Message" }
function Warn([string]$Message) { Write-Warning "[Codex setup] $Message" }
function CanonicalRemote([string]$Url) {
    return (($Url.Trim() -replace '\.git$', '').TrimEnd('/') -replace '^git@github\.com:', 'https://github.com/')
}
function GitRun([string[]]$Arguments) {
    # Git often emits progress on stderr; PS 5.1 should not treat it as a terminating error.
    $previous = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & git @Arguments 2>&1 | Out-Host
        return $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $previous
    }
}
function SyncRepo([string]$Remote, [string]$Local) {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Warn 'Git for Windows is not available; repository cache not installed.'
        return $false
    }
    $gitDir = Join-Path $Local '.git'
    if (Test-Path -LiteralPath $Local) {
        if (-not (Test-Path -LiteralPath $gitDir)) {
            Warn "Path exists but is not a Git checkout: $Local. Preserving it."
            return $false
        }
        $origin = (& git -C $Local remote get-url origin 2>$null)
        if ($LASTEXITCODE -ne 0 -or (CanonicalRemote ([string]$origin)) -ne (CanonicalRemote $Remote)) {
            Warn "Origin mismatch: $Local; no update was attempted."
            return $false
        }
        $current = [string](& git -C $Local branch --show-current 2>$null)
        if ($LASTEXITCODE -ne 0 -or $current.Trim() -ne 'main') {
            Warn "Not on main: $Local; preserving local branch."
            return $false
        }
        $dirty = & git -C $Local status --porcelain 2>$null
        if ($LASTEXITCODE -ne 0 -or $dirty) {
            Warn "Uncommitted changes: $Local; preserving local files."
            return $false
        }
        Log "Fast-forwarding: $Remote"
        if ((GitRun @('-C', $Local, 'pull', '--ff-only', 'origin', 'main')) -ne 0) {
            Warn "Unable to update $Local; previous clone preserved."
            return $false
        }
    } else {
        Log "Cloning: $Remote"
        if ((GitRun @('clone', '--quiet', '--branch', 'main', '--single-branch', $Remote, $Local)) -ne 0) {
            Warn "Unable to clone $Remote. Check GitHub authentication and network."
            return $false
        }
    }
    if (-not (Test-Path -LiteralPath (Join-Path $Local 'AGENTS.md'))) {
        Warn "Repository checkout has no AGENTS.md: $Local"
        return $false
    }
    Log "Verified local rules: $Local"
    return $true
}

$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$codexHome = [System.IO.Path]::GetFullPath($codexHome)
$standards = Join-Path $codexHome 'standards'
$build = Join-Path $standards 'Website-Starter-Standard'
$research = Join-Path $standards 'gefei-seo'
$global = Join-Path $codexHome 'AGENTS.md'
New-Item -ItemType Directory -Path $standards -Force | Out-Null

$buildOK = $false
$researchOK = $false
if ($SkipRepositorySync) {
    $buildOK = Test-Path -LiteralPath (Join-Path $build 'AGENTS.md')
    $researchOK = Test-Path -LiteralPath (Join-Path $research 'AGENTS.md')
    Log 'Skipping repository download/update; global rules will still be installed.'
} else {
    $buildOK = SyncRepo 'https://github.com/chenmu2024/Website-Starter-Standard.git' $build
    $researchOK = SyncRepo 'https://github.com/chenmu2024/gefei-seo.git' $research
}

$start = '<!-- BEGIN MANAGED WEBSITE STANDARD RULES -->'
$end = '<!-- END MANAGED WEBSITE STANDARD RULES -->'
$block = @'
<!-- BEGIN MANAGED WEBSITE STANDARD RULES -->
# Website-specific global Codex routing

Apply these rules to building new websites, editing existing websites, adding tool pages, technical SEO, UI, accessibility, performance, testing, and releases. Do not impose this workflow on unrelated tasks.

ENGINEERING SOURCE (how to build): {{BUILD_PATH}}
Upstream: https://github.com/chenmu2024/Website-Starter-Standard
At the beginning of website implementation tasks, ACTUALLY READ the engineering repository's AGENTS.md, README.md, and relevant DESIGN.md, BUILD-INTAKE-CONTRACT.md, SEO-GEO-QUALITY-GATE.md, TECHNICAL-SEO-IMPLEMENTATION.md, TASTE-UI-PROTOCOL.md, IMPECCABLE-UI-QUALITY-GATE.md, QA-CHECKLIST.md and release evidence rules. Select relevant sections based on task scope. These documents govern architecture, UI, site quality, technical SEO implementation, performance, mobile design and validation.

RESEARCH SOURCE (what to build and why): {{RESEARCH_PATH}}
Upstream (private): https://github.com/chenmu2024/gefei-seo
For new business opportunities, target keywords, non-brand SEO demand, SERP competition, traffic opportunity or independent page expansion, ACTUALLY READ the research repository's AGENTS.md, SKILL.md, and relevant research documents, including contracts/RESEARCH-TO-BUILD.md. Only owner-approved research decisions and exact keywords pass into the engineering BUILD-INTAKE-CONTRACT.md. Do not guess KD, Volume, CPC, competitor traffic, payment evidence or indexed rankings.

LATEST VERSION: When Git and network access permit, safely fast-forward local checkouts with git pull --ff-only origin main before substantial work. Never reset, force, clean or overwrite modified local checkouts. If updates fail, mark the repository version as potentially stale.

ACCESS: These rules do not fetch repositories by themselves. If local checkout is absent or unreadable, use authorized connected GitHub access if supported and explicitly report any unavailable sources. The private research repository may require login. Do not claim to have read a document without actually loading it. On an existing approved website, safe bug/SEO/UI repairs need not restart commercial research.

SAFETY AND QA: Preserve existing approved URLs, titles, canonical/robots/hreflang, working calculations, navigation, analytics, keywords, branding, and traffic-sensitive pages. Prefer browser-local tools, low ongoing costs and no paid API/AI/server/database without approval. Run real checks (build, functionality, mobile, offline HTML/technical SEO when possible) and report PASS/FAIL/NOT RUN truthfully. Never equate offline audit with Google indexing/ranking. Do not deploy/publish or buy services without explicit authorization. Project-specific approved requirements still apply.
<!-- END MANAGED WEBSITE STANDARD RULES -->
'@
$block = $block.Replace('{{BUILD_PATH}}', $build).Replace('{{RESEARCH_PATH}}', $research)
$utf8 = New-Object System.Text.UTF8Encoding($false)
$old = if (Test-Path -LiteralPath $global) { [System.IO.File]::ReadAllText($global, [System.Text.Encoding]::UTF8) } else { '' }
$atStart = $old.IndexOf($start, [System.StringComparison]::Ordinal)
$atEnd = $old.IndexOf($end, [System.StringComparison]::Ordinal)
if (($atStart -ge 0) -xor ($atEnd -ge 0)) {
    throw "Only one managed marker was found. Refusing to alter: $global"
}
if ($atStart -ge 0) {
    if ($atEnd -le $atStart) { throw "Invalid managed marker order: $global" }
    $new = $old.Substring(0, $atStart) + $block.TrimEnd() + $old.Substring($atEnd + $end.Length)
} else {
    $joiner = if ([string]::IsNullOrWhiteSpace($old)) { '' } else { [Environment]::NewLine + [Environment]::NewLine }
    $new = $old + $joiner + $block.TrimEnd() + [Environment]::NewLine
}
if ($new -ne $old) {
    if (Test-Path -LiteralPath $global) {
        $backup = "$global.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')-$(Get-Random)"
        Copy-Item -LiteralPath $global -Destination $backup -ErrorAction Stop
        Log "Existing global rules backed up: $backup"
    }
    [System.IO.File]::WriteAllText($global, $new, $utf8)
} else {
    Log 'Global rules are already up to date (no duplicate block).'
}
$verify = [System.IO.File]::ReadAllText($global, [System.Text.Encoding]::UTF8)
if (-not ($verify.Contains($start) -and $verify.Contains($end) -and $verify.Contains($build))) {
    throw "Global configuration verification failed: $global"
}
Log "Global rules installed and verified: $global"
Log ("Engineering local checkout: " + $(if ($buildOK) { 'VERIFIED' } else { 'UNAVAILABLE' }))
Log ("Research private checkout: " + $(if ($researchOK) { 'VERIFIED' } else { 'UNAVAILABLE' }))
if (-not $buildOK) { Warn 'Engineering standard was NOT cached locally; re-run with working Git and network.' }
if (-not $researchOK) { Warn 'gefei-seo was NOT cached locally. Ensure your connected Git credentials can read its private repo, then re-run.' }
if (Test-Path -LiteralPath (Join-Path $codexHome 'AGENTS.override.md')) {
    Warn 'Global AGENTS.override.md also exists and may supersede AGENTS.md. Check for conflicting instructions.'
}
if ((Get-Item -LiteralPath $global).Length -gt 32768) {
    Warn 'Global AGENTS.md exceeds 32 KiB; Codex may truncate instruction files based on configured size limits.'
}
Log 'Restart LOCAL Windows Codex to load the new global instructions. WSL and Codex Cloud can use different environments.'
