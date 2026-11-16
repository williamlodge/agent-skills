[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Name,

    [Parameter(Position = 1)]
    [ValidateSet("shared-agents", "claude", "kimi", "")]
    [string]$Platform = "",

    [Parameter(Position = 2)]
    [string]$Destination = ".\skills"
)

$ErrorActionPreference = "Stop"
$ManifestUrl = "https://raw.githubusercontent.com/williamlodge/agent-skills/main/manifest.json"
$RepoUrl = "https://github.com/williamlodge/agent-skills.git"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is required. Install it from https://git-scm.com/download/win and reopen PowerShell."
}

$Manifest = Invoke-RestMethod -Uri $ManifestUrl -TimeoutSec 30
$Skill = $Manifest.skills | Where-Object { $_.name -eq $Name } | Select-Object -First 1
if ($null -eq $Skill) {
    throw "Skill not found: $Name. Search the repository catalog for the exact name."
}

if ($Platform) {
    $Copy = $Skill.copies | Where-Object { $_.platform -eq $Platform } | Select-Object -First 1
    if ($null -eq $Copy) {
        $Available = $Skill.platforms -join ", "
        throw "$Name is not available for $Platform. Available: $Available"
    }
} else {
    $Copy = $Skill.copies | Where-Object { $_.platform -eq "shared-agents" } | Select-Object -First 1
    if ($null -eq $Copy) {
        $Copy = $Skill.copies | Where-Object { $_.path -eq $Skill.primary_path } | Select-Object -First 1
    }
}

$Target = Join-Path $Destination $Name
if (Test-Path $Target) {
    throw "Destination already exists; refusing to overwrite: $Target"
}

$Temp = Join-Path ([System.IO.Path]::GetTempPath()) ("agent-skills-" + [System.Guid]::NewGuid().ToString("N"))
$Clone = Join-Path $Temp "repository"
New-Item -ItemType Directory -Path $Temp | Out-Null

try {
    git clone --quiet --depth 1 --filter=blob:none --sparse $RepoUrl $Clone
    if ($LASTEXITCODE -ne 0) { throw "Git clone failed." }
    git -C $Clone sparse-checkout set "all-skills/$($Copy.path)"
    if ($LASTEXITCODE -ne 0) { throw "Git sparse checkout failed." }

    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    Copy-Item -Path (Join-Path $Clone "all-skills/$($Copy.path)") -Destination $Target -Recurse
    Write-Host "Installed $Name to $Target"
} finally {
    if (Test-Path $Temp) {
        Remove-Item -Path $Temp -Recurse -Force
    }
}
