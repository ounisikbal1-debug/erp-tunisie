@echo off
chcp 65001 >nul
title SAFE PME Express et Facturation Rapide - SAFE Suite Tunisie
cls
echo ===============================================================================
echo   SAFE PME Express et Facturation Rapide
echo   Facturation clients, achats, paie SCE, comptabilite TND millimes & e-Fatoura TEIF
echo   Version 1.0.0 ^| Conforme Legislation Tunisienne
echo ===============================================================================
echo.
echo Initialisation du service en local...

set "CORE_DIR=%~dp0..\..\SAFE_ERP_DRAFT 3"
if not exist "%CORE_DIR%\LANCER_SAFE_ERP_LOCAL.ps1" (
    set "CORE_DIR=%~dp0..\SAFE_ERP_DRAFT 3"
)
if not exist "%CORE_DIR%\LANCER_SAFE_ERP_LOCAL.ps1" (
    set "CORE_DIR=C:\Users\USER\OneDrive\Desktop\SAFE_ERP_DRAFT 4\SAFE_ERP_DRAFT 3"
)

if not exist "%CORE_DIR%\LANCER_SAFE_ERP_LOCAL.ps1" (
    echo [ERREUR] Le noyau SAFE ERP est introuvable dans : %CORE_DIR%
    pause
    exit /b 1
)

cd /d "%CORE_DIR%"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\LANCER_SAFE_ERP_LOCAL.ps1" -App "pme_express"
if errorlevel 1 (
    echo.
    echo [ERREUR] Erreur lors du demarrage du prologiciel.
    pause
)
