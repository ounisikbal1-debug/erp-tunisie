@echo off
chcp 65001 >nul
title SAFE PME Express - Facturation, Paie & e-Fatoura TEIF (Port 8006)
cls
echo ===============================================================================
echo   SAFE PME Express & e-Fatoura TEIF (Tunisie)
echo   Facturation rapide, Paie SCE, Comptabilite TND & E-Facture Officielle
echo   Version 1.0.0 ^| Port Dédié : 8006 ^| Conforme Législation Tunisienne
echo ===============================================================================
echo.
cd /d "%~dp0"

echo [1/2] Verification de l'environnement Python...
python -m pip install --quiet fastapi uvicorn pydantic >nul 2>&1

echo [2/2] Demarrage du serveur autonome SAFE PME Express (Port 8006)...
python standalone_pme_server.py
if errorlevel 1 (
    echo.
    echo [ERREUR] Impossible de lancer le serveur autonome SAFE PME Express.
    pause
)
