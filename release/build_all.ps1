# Build All Release Versions
# PowerShell script to create both portable and installer versions

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building All MetaFinder Releases" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Clean previous builds (except dist folder which will hold final outputs)
if (Test-Path "build") {
    Write-Host "Cleaning previous build artifacts..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "build" -ErrorAction SilentlyContinue
}

# Remove temporary folders from dist if they exist
if (Test-Path "dist\portable_temp") {
    Remove-Item -Recurse -Force "dist\portable_temp" -ErrorAction SilentlyContinue
}
if (Test-Path "dist\installer_temp") {
    Remove-Item -Recurse -Force "dist\installer_temp" -ErrorAction SilentlyContinue
}

# Activate virtual environment if it exists
if (Test-Path "..\.venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "..\.venv\Scripts\Activate.ps1"
}

# Check if PyInstaller is installed
Write-Host "Checking for PyInstaller..." -ForegroundColor Yellow
$pyinstallerCheck = python -c "import PyInstaller" 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Build portable version
Write-Host ""
Write-Host "Step 1: Building Portable Version..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
python build_portable.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Portable build failed!" -ForegroundColor Red
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Build installer version
Write-Host ""
Write-Host "Step 2: Building Installer Version..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
python build_installer.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ All builds completed successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📦 Release files created:" -ForegroundColor Cyan
    Write-Host "   - Portable: dist\MetaFinder-Portable-v*.zip" -ForegroundColor White
    Write-Host "   - Installer: dist\MetaFinder-Setup-v*.exe (if Inno Setup installed)" -ForegroundColor White
    Write-Host ""
    Write-Host "Ready for GitHub release upload! 🚀" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "⚠️ Installer build had issues" -ForegroundColor Yellow
    Write-Host "Portable version is ready, but installer may need manual compilation" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
