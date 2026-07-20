# Thin wrapper: talk to the LOCAL Hermes 3 model via Ollama (tier "local").
# Equivalent to: python scripts/llm.py --tier local "<prompt>"
# Usage:
#   .\scripts\hermes.ps1 "Say ready if you can hear me"
#   Get-Content notes.txt | .\scripts\hermes.ps1 -Stdin
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Prompt,
    [switch]$Stdin
)

$ErrorActionPreference = "Stop"
$llmPy = Join-Path $PSScriptRoot "llm.py"

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) { $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $pythonCmd) {
    Write-Error "No python/python3 found on PATH. Install Python 3 to use the Hermes sidecar."
    exit 1
}

if ($Stdin) {
    $input | & $pythonCmd.Source $llmPy --tier local --stdin
} elseif ($Prompt -and $Prompt.Count -gt 0) {
    & $pythonCmd.Source $llmPy --tier local ($Prompt -join " ")
} else {
    Write-Error 'Usage: .\scripts\hermes.ps1 "<prompt>"   (or pipe text in with -Stdin)'
    exit 1
}
exit $LASTEXITCODE
