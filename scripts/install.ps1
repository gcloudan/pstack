param(
    [string]$SkillsRoot = '',
    [string]$AgentsRoot = '',
    [string]$WorkspaceRoot = '',
    [switch]$ReplaceExisting,
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$kitRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if ($WorkspaceRoot) {
    if ($SkillsRoot -or $AgentsRoot) { throw 'Use WorkspaceRoot or custom roots, not both.' }
    $workspace = [System.IO.Path]::GetFullPath($WorkspaceRoot)
    $SkillsRoot = Join-Path $workspace '.cursor/skills'
    $AgentsRoot = Join-Path $workspace '.cursor/agents'
} else {
    if (-not $SkillsRoot) { $SkillsRoot = Join-Path $HOME '.cursor/skills' }
    if (-not $AgentsRoot) { $AgentsRoot = Join-Path (Split-Path ([System.IO.Path]::GetFullPath($SkillsRoot)) -Parent) 'agents' }
}
$SkillsRoot = [System.IO.Path]::GetFullPath($SkillsRoot)
$AgentsRoot = [System.IO.Path]::GetFullPath($AgentsRoot)
if ((Split-Path $SkillsRoot -Leaf) -ne 'skills' -or $AgentsRoot -ne (Join-Path (Split-Path $SkillsRoot -Parent) 'agents')) {
    throw 'Use adjacent skills and agents directories: the investigator resolves ../skills. No files written.'
}
$backupRoot = Join-Path (Split-Path $SkillsRoot -Parent) ('pstack-harness-backups/' + [guid]::NewGuid().ToString('N'))
$packages = @()
foreach ($name in Get-Content -LiteralPath (Join-Path $kitRoot 'profiles/core.skills')) {
    if ($name -notmatch '^[a-z0-9]+(?:-[a-z0-9]+)*$') { throw "Invalid skill name: $name" }
    $sourceDirectory = Join-Path $kitRoot "skills/$name"
    if (-not (Test-Path -LiteralPath (Join-Path $sourceDirectory 'SKILL.md') -PathType Leaf)) { throw "Missing skill: $name" }
    $files = @(Get-ChildItem -LiteralPath $sourceDirectory -File -Recurse | ForEach-Object {
        $relative = $_.FullName.Substring($sourceDirectory.Length + 1)
        [pscustomobject]@{ Source = $_.FullName; Target = Join-Path (Join-Path $SkillsRoot $name) $relative; Backup = "skills/$name/$relative" }
    })
    $packages += [pscustomobject]@{ Name = "skill:$name"; Exists = (Test-Path -LiteralPath (Join-Path $SkillsRoot $name)); Files = $files }
}
foreach ($name in Get-Content -LiteralPath (Join-Path $kitRoot 'profiles/core.agents')) {
    if ($name -notmatch '^[a-z0-9]+(?:-[a-z0-9]+)*$') { throw "Invalid agent name: $name" }
    $sourceFile = Join-Path $kitRoot "agents/$name.md"
    if (-not (Test-Path -LiteralPath $sourceFile -PathType Leaf)) { throw "Missing agent: $name" }
    $targetFile = Join-Path $AgentsRoot "$name.md"
    $packages += [pscustomobject]@{ Name = "agent:$name"; Exists = (Test-Path -LiteralPath $targetFile); Files = @([pscustomobject]@{ Source = $sourceFile; Target = $targetFile; Backup = "agents/$name.md" }) }
}
if ($WorkspaceRoot) {
    $targetFile = Join-Path $workspace '.cursor/rules/pstack-harness.mdc'
    $packages += [pscustomobject]@{ Name = 'rule:pstack-harness'; Exists = (Test-Path -LiteralPath $targetFile); Files = @([pscustomobject]@{ Source = Join-Path $kitRoot 'rules/pstack-harness.mdc'; Target = $targetFile; Backup = 'rules/pstack-harness.mdc' }) }
}
$conflicts = @()
foreach ($package in $packages) {
    $different = @($package.Files | Where-Object {
        -not (Test-Path -LiteralPath $_.Target -PathType Leaf) -or
        (Get-FileHash -LiteralPath $_.Source).Hash -ne (Get-FileHash -LiteralPath $_.Target).Hash
    })
    if ($different.Count -eq 0) { Write-Output "Already current: $($package.Name)"; continue }
    if ($package.Exists -and -not $ReplaceExisting) {
        Write-Warning "Preserved differing $($package.Name); compare before replacement."
        $conflicts += $package.Name
        continue
    }
    if ($DryRun) { Write-Output "Would install: $($package.Name) ($($different.Count) files)"; continue }
    foreach ($file in $different) {
        if (Test-Path -LiteralPath $file.Target) {
            $backupFile = Join-Path $backupRoot $file.Backup
            New-Item -ItemType Directory -Path (Split-Path $backupFile -Parent) -Force | Out-Null
            Copy-Item -LiteralPath $file.Target -Destination $backupFile
            Write-Output "Backed up: $backupFile"
        }
        New-Item -ItemType Directory -Path (Split-Path $file.Target -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $file.Source -Destination $file.Target -Force
    }
    Write-Output "Installed: $($package.Name)"
}
if ($conflicts.Count) { Write-Output ('Preserved conflicts: ' + ($conflicts -join ', ')); exit 2 }
if ($DryRun) { Write-Output 'Preview complete; no files written.' }
elseif ($WorkspaceRoot) { Write-Output 'Core installed with a namespaced project rule. Existing harness files retained.' }
else { Write-Output 'Core skills/agent installed. User activation text is in docs/cursor-user-rule.txt.' }
