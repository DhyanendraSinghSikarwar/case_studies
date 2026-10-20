# Copies the AMPBA skills into .claude\skills so Claude Code can load them. Run once from this folder:
#   powershell -ExecutionPolicy Bypass -File .\install_skills.ps1
$src = Join-Path $PSScriptRoot "claude-skills"
$dst = Join-Path $PSScriptRoot ".claude\skills"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Path (Join-Path $src "*") -Destination $dst -Recurse -Force
Write-Host "Installed skills:"; Get-ChildItem $dst -Directory | ForEach-Object { " - " + $_.Name }
