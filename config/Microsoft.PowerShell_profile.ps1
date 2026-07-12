
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

$ompConfig = 'C:\Users\hxaxd\learn\hxlog\config\powerlevel10k_rainbow.omp.json'
if ((Get-Command oh-my-posh -ErrorAction SilentlyContinue) -and (Test-Path -LiteralPath $ompConfig)) {
  oh-my-posh init pwsh --config $ompConfig | Invoke-Expression
}

if (Get-Command fnm -ErrorAction SilentlyContinue) {
  fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression
}
