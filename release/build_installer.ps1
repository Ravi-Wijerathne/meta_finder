# Build MetaFinder Installer Version
# PowerShell script to create installer release

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building MetaFinder Installer Version" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

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

# Run build script
Write-Host ""
Write-Host "Starting build process..." -ForegroundColor Green
python build_installer.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Build completed successfully!" -ForegroundColor Green
    Write-Host "📦 Check the 'dist' folder for output files" -ForegroundColor Green
    Write-Host ""
    Write-Host "If Inno Setup is not installed:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
    Write-Host "2. Open installer.iss in Inno Setup" -ForegroundColor Yellow
    Write-Host "3. Click 'Compile' to create the installer" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "❌ Build failed!" -ForegroundColor Red
    Write-Host "Please check the error messages above" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
