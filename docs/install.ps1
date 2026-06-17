# Mission Canvas — Windows Install (PowerShell)
# Usage: irm https://missioncanvas.ai/install.ps1 | iex
# Or:    .\install.ps1

Write-Host ""
Write-Host "  ╔══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║     Mission Canvas — Install (Windows)   ║" -ForegroundColor Cyan
Write-Host "  ║     Governed AI for Professional Judgment ║" -ForegroundColor Cyan
Write-Host "  ╚══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# --- Check Python ---
Write-Host "Checking prerequisites..."
try {
    $pyver = python --version 2>&1
    if ($pyver -match "3\.(1[1-9]|[2-9]\d)") {
        Write-Host "  Python: $pyver ✓" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: Python 3.11+ required (found $pyver)" -ForegroundColor Red
        Write-Host "  Install from: https://python.org" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "  ERROR: Python not found. Install from https://python.org" -ForegroundColor Red
    exit 1
}

# --- Check Git ---
try {
    git --version | Out-Null
    Write-Host "  Git: ✓" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Git required. Install from https://git-scm.com" -ForegroundColor Red
    exit 1
}

# --- Clone ---
if (-not (Test-Path "MANIFEST.yaml")) {
    Write-Host ""
    Write-Host "Cloning Mission Canvas..."
    git clone https://github.com/pretendhome/mission-canvas.git
    Set-Location mission-canvas
}

# --- Install Python deps ---
Write-Host ""
Write-Host "Installing Python dependencies..."
pip install -e ".[dev]" 2>$null
if ($LASTEXITCODE -ne 0) {
    pip install pyyaml redis fastapi uvicorn websockets pytest
}

# --- Node (optional) ---
try {
    $nodever = node --version 2>&1
    Write-Host "  Node.js: $nodever ✓" -ForegroundColor Green
    if (Test-Path "runtime/package.json") {
        Set-Location runtime
        npm install --silent 2>$null
        Set-Location ..
    }
} catch {
    Write-Host "  Node.js: not found (optional)" -ForegroundColor Yellow
}

# --- Verify ---
Write-Host ""
Write-Host "Running verification..."
python src/mc_cli.py status

Write-Host ""
Write-Host "  ╔══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║     Installation complete                ║" -ForegroundColor Cyan
Write-Host "  ╠══════════════════════════════════════════╣" -ForegroundColor Cyan
Write-Host "  ║                                          ║" -ForegroundColor Cyan
Write-Host "  ║  Start:  python mc research `"query`"     ║" -ForegroundColor Cyan
Write-Host "  ║  Status: python src/mc_cli.py status     ║" -ForegroundColor Cyan
Write-Host "  ║  Web UI: http://localhost:7891            ║" -ForegroundColor Cyan
Write-Host "  ║                                          ║" -ForegroundColor Cyan
Write-Host "  ╚══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
