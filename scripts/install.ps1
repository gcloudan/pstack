param(
    [string]$SkillsRoot = (Join-Path $HOME '.cursor/skills'),
    [switch]$ReplaceExisting
)
$ErrorActionPreference = 'Stop'
$sourceRoot = (Resolve-Path (Join-Path $PSScriptRoot '../skills')).Path
$destinationRoot = [System.IO.Path]::GetFullPath($SkillsRoot)
$backupRoot = Join-Path ([System.IO.Directory]::GetParent($destinationRoot).FullName) ('work-style-backups/' + [guid]::NewGuid().ToString('N'))
$conflicts = @()
foreach ($skillName in @('automate-me', 'work-mode', 'repo-onboarding')) {
    $sourceFile = Join-Path $sourceRoot "$skillName/SKILL.md"
    $destinationFile = Join-Path $destinationRoot "$skillName/SKILL.md"
    if (-not (Test-Path -LiteralPath $sourceFile -PathType Leaf)) { throw "Missing kit file: $sourceFile" }
    if (Test-Path -LiteralPath $destinationFile) {
        if ((Get-FileHash -LiteralPath $sourceFile).Hash -eq (Get-FileHash -LiteralPath $destinationFile).Hash) {
            Write-Output "Already current: $skillName"
            continue
        }
        if (-not $ReplaceExisting) {
            Write-Warning "Preserved existing $skillName. Compare it before using -ReplaceExisting."
            $conflicts += $skillName
            continue
        }
        $backupDirectory = Join-Path $backupRoot $skillName
        New-Item -ItemType Directory -Path $backupDirectory -Force | Out-Null
        Copy-Item -LiteralPath $destinationFile -Destination (Join-Path $backupDirectory 'SKILL.md')
        Write-Output "Backed up: $skillName to $backupDirectory"
    }
    New-Item -ItemType Directory -Path (Split-Path $destinationFile -Parent) -Force | Out-Null
    Copy-Item -LiteralPath $sourceFile -Destination $destinationFile -Force
    Write-Output "Installed: $skillName to $destinationFile"
}
if ($conflicts.Count -gt 0) {
    Write-Output ('Preserved differing skills: ' + ($conflicts -join ', '))
    exit 2
}
Write-Output 'Skills installed. Activate work-mode separately using docs/cursor-user-rule.txt.'
