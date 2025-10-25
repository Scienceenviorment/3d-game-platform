# Ancient Bharat - Advanced Permission Setup (PowerShell)
# Run as Administrator for full permissions

Write-Host "🏛️  ANCIENT BHARAT - ADVANCED PERMISSIONS SETUP  🏛️" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Yellow
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "⚠️  This script should be run as Administrator for full permissions" -ForegroundColor Red
    Write-Host "   Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Red
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit
    }
}

# Get current directory
$projectDir = Get-Location

Write-Host "📁 Setting directory permissions..." -ForegroundColor Green

try {
    # Give full control to current user
    $acl = Get-Acl $projectDir
    $username = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule($username, "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
    $acl.SetAccessRule($accessRule)
    Set-Acl -Path $projectDir -AclObject $acl
    
    Write-Host "✅ Full permissions granted to $username" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not set directory permissions: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔥 Configuring Windows Firewall..." -ForegroundColor Green

try {
    # Get Python executable path
    $pythonPath = (Get-Command python).Source
    
    # Add firewall rules
    New-NetFirewallRule -DisplayName "Ancient Bharat Game Server (Inbound)" -Direction Inbound -Program $pythonPath -Action Allow -Protocol TCP -LocalPort 8000 -ErrorAction SilentlyContinue
    New-NetFirewallRule -DisplayName "Ancient Bharat Game Server (Outbound)" -Direction Outbound -Program $pythonPath -Action Allow -Protocol TCP -LocalPort 8000 -ErrorAction SilentlyContinue
    
    Write-Host "✅ Windows Firewall rules added" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not add firewall rules: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "   You may need to manually allow Python through Windows Firewall" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🐍 Setting PowerShell execution policy..." -ForegroundColor Green

try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "✅ PowerShell execution policy set to RemoteSigned" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not set execution policy: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📂 Creating required directories..." -ForegroundColor Green

$requiredDirs = @("game_data", "config", "logs", "temp", "client", "server")

foreach ($dir in $requiredDirs) {
    try {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Created: $dir\" -ForegroundColor Green
    } catch {
        Write-Host "❌ Could not create $dir\: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📦 Installing Python packages..." -ForegroundColor Green

$packages = @("fastapi", "uvicorn[standard]", "websockets")

foreach ($package in $packages) {
    Write-Host "   Installing $package..." -ForegroundColor Cyan
    try {
        & python -m pip install $package --user --quiet
        Write-Host "✅ $package installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Could not install $package" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📝 Creating launch scripts..." -ForegroundColor Green

# Create batch file launcher
$batchContent = @"
@echo off
title Ancient Bharat Game Server
echo Starting Ancient Bharat Game Server...
cd /d "%~dp0"
python simple_game_server.py
echo.
echo Server stopped. Press any key to exit...
pause >nul
"@

try {
    $batchContent | Out-File -FilePath "start_game.bat" -Encoding ASCII
    Write-Host "✅ Created start_game.bat" -ForegroundColor Green
} catch {
    Write-Host "❌ Could not create batch file" -ForegroundColor Red
}

# Create PowerShell launcher
$psContent = @"
# Ancient Bharat Game Launcher
Write-Host "🏛️  Starting Ancient Bharat Game Server..." -ForegroundColor Yellow
Set-Location (Split-Path -Parent `$MyInvocation.MyCommand.Path)
& python simple_game_server.py
Write-Host ""
Write-Host "Server stopped. Press any key to exit..." -ForegroundColor Yellow
`$null = `$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
"@

try {
    $psContent | Out-File -FilePath "start_game.ps1" -Encoding UTF8
    Write-Host "✅ Created start_game.ps1" -ForegroundColor Green
} catch {
    Write-Host "❌ Could not create PowerShell script" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯" + "=" * 58 + "🎯" -ForegroundColor Yellow
Write-Host "   SETUP COMPLETE - ANCIENT BHARAT READY!" -ForegroundColor Yellow
Write-Host "🎯" + "=" * 58 + "🎯" -ForegroundColor Yellow
Write-Host ""

Write-Host "🚀 How to Start the Game:" -ForegroundColor Cyan
Write-Host "   Option 1: Double-click start_game.bat" -ForegroundColor White
Write-Host "   Option 2: python simple_setup.py" -ForegroundColor White
Write-Host "   Option 3: python simple_game_server.py" -ForegroundColor White
Write-Host ""

Write-Host "🌐 Game URLs (after starting server):" -ForegroundColor Cyan
Write-Host "   Game Client: http://localhost:8000/client" -ForegroundColor White
Write-Host "   Server Status: http://localhost:8000/status" -ForegroundColor White
Write-Host ""

Write-Host "🔐 Permissions Set:" -ForegroundColor Cyan
Write-Host "   ✅ Directory read/write access" -ForegroundColor Green
Write-Host "   ✅ Windows Firewall rules" -ForegroundColor Green
Write-Host "   ✅ PowerShell execution policy" -ForegroundColor Green
Write-Host "   ✅ Python package installation" -ForegroundColor Green
Write-Host ""

Write-Host "🎮 Ready to explore Ancient Bharat!" -ForegroundColor Yellow
Write-Host ""

$startNow = Read-Host "Start the game now? (Y/n)"
if ($startNow -eq "" -or $startNow -eq "y" -or $startNow -eq "Y") {
    Write-Host ""
    Write-Host "🚀 Launching Ancient Bharat..." -ForegroundColor Yellow
    & python simple_setup.py
}