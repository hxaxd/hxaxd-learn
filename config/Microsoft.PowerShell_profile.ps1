# Ensure WinGet command links are available even when the terminal host
# inherited an older PATH before package changes were made.
$wingetLinks = Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Links'
if (Test-Path -LiteralPath $wingetLinks) {
  $sessionPathEntries = @($env:Path -split ';' | ForEach-Object { $_.Trim().TrimEnd('\') })
  if ($sessionPathEntries -notcontains $wingetLinks.TrimEnd('\')) {
    $env:Path = "$env:Path;$wingetLinks"
  }
}

# PowerToys CommandNotFound module
if (Get-Module -ListAvailable -Name Microsoft.WinGet.CommandNotFound) {
  Import-Module -Name Microsoft.WinGet.CommandNotFound -ErrorAction SilentlyContinue
}

if (Get-Module -ListAvailable -Name Terminal-Icons) {
  Import-Module -Name Terminal-Icons -ErrorAction SilentlyContinue
}

# Conda: load full Shell integration without automatically activating an environment.
# Conda must be available on PATH (its condabin directory is sufficient).
$condaCommand = Get-Command conda -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
if ($condaCommand) {
  $condaAutoActivate = $env:CONDA_AUTO_ACTIVATE_BASE
  try {
    $env:CONDA_AUTO_ACTIVATE_BASE = 'false'
    $condaHook = (& $condaCommand.Source shell.powershell hook 2>$null) | Out-String
    if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($condaHook)) {
      Invoke-Expression $condaHook
    }
  } finally {
    $env:CONDA_AUTO_ACTIVATE_BASE = $condaAutoActivate
    Remove-Variable condaAutoActivate, condaHook -ErrorAction SilentlyContinue
  }
}
Remove-Variable condaCommand -ErrorAction SilentlyContinue

$ompConfig = 'C:\Users\hxaxd\learn\hxaxd-learn\config\powerlevel10k_rainbow.omp.json'
if ((Get-Command oh-my-posh -ErrorAction SilentlyContinue) -and (Test-Path -LiteralPath $ompConfig)) {
  oh-my-posh init pwsh --config $ompConfig | Invoke-Expression
}

if (Get-Command fnm -ErrorAction SilentlyContinue) {
  fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression
}
