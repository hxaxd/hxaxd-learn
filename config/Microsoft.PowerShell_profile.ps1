
#f45873b3-b655-43a6-b217-97c00aa0db58 PowerToys CommandNotFound module

Import-Module -Name Microsoft.WinGet.CommandNotFound
#f45873b3-b655-43a6-b217-97c00aa0db58
Import-Module -Name Terminal-Icons

oh-my-posh init pwsh --config "C:\Users\hxaxd\learn\hxlog\config\powerlevel10k_rainbow.omp.json" | Invoke-Expression

fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression
