$ErrorActionPreference = "Stop"

$Repo = "https://github.com/krystofham/F1_game"
$Dir = "F1_game"

if (-not (Test-Path $Dir)) {
  git clone $Repo
}

Set-Location $Dir

Write-Host "Installing Python dependencies..."
python -m pip install -r requirements.txt

Write-Host "Installing frontend dependencies..."
Set-Location frontend
npm install

Write-Host "Starting MMRAC1NG (development mode)..."
npm run desktop:dev
