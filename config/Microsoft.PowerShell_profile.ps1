
#f45873b3-b655-43a6-b217-97c00aa0db58 PowerToys CommandNotFound module

if (Get-Module -ListAvailable -Name Microsoft.WinGet.CommandNotFound) {
    Import-Module -Name Microsoft.WinGet.CommandNotFound
}
#f45873b3-b655-43a6-b217-97c00aa0db58
if (Get-Module -ListAvailable -Name Terminal-Icons) {
    Import-Module -Name Terminal-Icons
}

$themePath = "C:\Users\hxaxd\learn\hxlog\config\powerlevel10k_rainbow.omp.json"
if ((Get-Command oh-my-posh -ErrorAction SilentlyContinue) -and (Test-Path -LiteralPath $themePath)) {
    oh-my-posh init pwsh --config $themePath | Invoke-Expression
}

if (Get-Command fnm -ErrorAction SilentlyContinue) {
    fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression
}
