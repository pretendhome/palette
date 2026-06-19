# Mission Canvas — Windows Install (PowerShell)
# Usage: irm https://missioncanvas.ai/install.ps1 | iex
# Downloads pre-built binary. No Python. No Git. No dependencies.
$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "  ╔══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║   Mission Canvas Installer (Windows)     ║" -ForegroundColor Cyan
Write-Host "  ║   Governed AI for professionals          ║" -ForegroundColor Cyan
Write-Host "  ╚══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Detect architecture
$arch = if ([Environment]::Is64BitOperatingSystem) { "x86_64" } else { "x86" }
Write-Host "  ✓ Detected: windows-$arch" -ForegroundColor Green

# Get latest release
$release = try {
    (Invoke-RestMethod "https://api.github.com/repos/pretendhome/mission-canvas/releases/latest" -ErrorAction Stop).tag_name
} catch { "v1.2.0" }
Write-Host "  ✓ Version: $release" -ForegroundColor Green

# Download binary
$binary = "mc-windows-${arch}.exe"
$url = "https://github.com/pretendhome/mission-canvas/releases/download/$release/$binary"
$installDir = "$env:LOCALAPPDATA\MissionCanvas"
$mcPath = "$installDir\mc.exe"

Write-Host "  → Downloading Mission Canvas..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $installDir | Out-Null

try {
    Invoke-WebRequest -Uri $url -OutFile $mcPath -UseBasicParsing
    Write-Host "  ✓ Downloaded to $mcPath" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Download failed: $url" -ForegroundColor Red
    Write-Host "  Try: https://github.com/pretendhome/mission-canvas/releases" -ForegroundColor Yellow
    exit 1
}

# Add to PATH if not already there
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*MissionCanvas*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$installDir", "User")
    $env:Path = "$env:Path;$installDir"
    Write-Host "  ✓ Added to PATH" -ForegroundColor Green
}

# Set UTF-8 permanently
[Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User")

# Verify
Write-Host ""
& $mcPath status 2>$null

Write-Host ""
Write-Host "  ╔══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║   Installation complete!                 ║" -ForegroundColor Cyan
Write-Host "  ╠══════════════════════════════════════════╣" -ForegroundColor Cyan
Write-Host "  ║                                          ║" -ForegroundColor Cyan
Write-Host "  ║   Start:    mc shell                     ║" -ForegroundColor Cyan
Write-Host "  ║   Web UI:   mc start                     ║" -ForegroundColor Cyan
Write-Host "  ║   Status:   mc status                    ║" -ForegroundColor Cyan
Write-Host "  ║                                          ║" -ForegroundColor Cyan
Write-Host "  ║   Requires: Ollama (ollama.com/download) ║" -ForegroundColor Cyan
Write-Host "  ║   Then:     ollama pull qwen2.5:7b       ║" -ForegroundColor Cyan
Write-Host "  ║                                          ║" -ForegroundColor Cyan
Write-Host "  ╚══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Open a NEW PowerShell window, then type: mc shell" -ForegroundColor Yellow
Write-Host ""
