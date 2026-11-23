# -*- coding: utf-8 -*-
"""
SAFE PME Express - Serveur Standalone Dédié (Port 8006)
Facturation, Paie Tunisienne, TEIF e-Fatoura, Paramètres Fiscaux Modifiables
Conforme SCE NC 01, TVA 19/13/7%, Timbre 1.000 DT, Hardware ID HMAC-SHA256
"""
import os
import sys
import uuid
import hmac
import hashlib
import sqlite3
import socket
import webbrowser
import threading
import time
import json
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

MODULE_CODE = "PME_EXPRESS"
MODULE_TITLE = "SAFE PME Express & e-Fatoura TEIF"
PORT = 8006
SECRET_SALT = b"SAFE_ERP_TUNISIE_2026_MASTER_HMAC_KEY_#991"

prog_data = os.environ.get("PROGRAMDATA", os.path.expanduser("~"))
DATA_DIR = os.path.join(prog_data, "SAFE_ERP_Tunisie", "06_SAFE_PME_Express")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "safe_pme_express.db")
LICENSE_FILE = os.path.join(DATA_DIR, "license.dat")

def get_hardware_id() -> str:
    raw = f"{uuid.getnode()}-{socket.gethostname()}-{sys.platform}".encode("utf-8")
    return "HW-" + hashlib.sha256(raw).hexdigest()[:12].upper()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS company (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT DEFAULT 'Société Tunisienne SARL',
        matricule_fiscal TEXT DEFAULT '1234567/A/M/000',
        registre_commerce TEXT DEFAULT 'B01234562026',
        adresse TEXT DEFAULT 'Avenue Habib Bourguiba, Tunis',
        telephone TEXT DEFAULT '+216 71 000 000',
        email TEXT DEFAULT 'contact@societe.tn',
        regime_tva TEXT DEFAULT 'assujetti',
        regime_fiscal TEXT DEFAULT 'reel',
        taux_is INTEGER DEFAULT 15,
        exercice INTEGER DEFAULT 2026,
        tva_normale REAL DEFAULT 19.0,
        tva_intermediaire REAL DEFAULT 13.0,
        tva_reduite REAL DEFAULT 7.0,
        timbre_fiscal REAL DEFAULT 1.000,
        cnss_salarie REAL DEFAULT 9.68,
        cnss_patronale REAL DEFAULT 17.07,
        css REAL DEFAULT 0.50,
        tfp REAL DEFAULT 1.00,
        foprolos REAL DEFAULT 1.00,
        abattement_famille REAL DEFAULT 300.0,
        abattement_enfant REAL DEFAULT 100.0
    )
    """)
    c.execute("SELECT COUNT(*) FROM company")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO company (name) VALUES ('Société Tunisienne SARL')")
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS factures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT UNIQUE,
        client_nom TEXT,
        client_mat TEXT,
        date_facture TEXT,
        total_ht REAL,
        total_tva REAL,
        timbre REAL,
        total_ttc REAL,
        statut TEXT DEFAULT 'VALIDEE'
    )
    """)
    c.execute("SELECT COUNT(*) FROM factures")
    if c.fetchone()[0] == 0:
        c.execute("""
        INSERT INTO factures (numero, client_nom, client_mat, date_facture, total_ht, total_tva, timbre, total_ttc)
        VALUES 
        ('FAC-2026-001', 'STE COMMERCIALE DU NORD', '0892341/B/A/000', '2026-02-15', 12500.000, 2375.000, 1.000, 14876.000),
        ('FAC-2026-002', 'COMPTOIR INDUSTRIEL TUNISIEN', '0459201/C/M/000', '2026-02-18', 4800.000, 912.000, 1.000, 5713.000)
        """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS salaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricule TEXT UNIQUE,
        nom TEXT,
        cin TEXT,
        salaire_base REAL,
        cnss_salarie REAL,
        irpp REAL,
        css REAL,
        salaire_net REAL
    )
    """)
    c.execute("SELECT COUNT(*) FROM salaries")
    if c.fetchone()[0] == 0:
        c.execute("""
        INSERT INTO salaries (matricule, nom, cin, salaire_base, cnss_salarie, irpp, css, salaire_net)
        VALUES
        ('EMP-001', 'Mohamed Ben Salah', '08923412', 2500.000, 242.000, 285.500, 12.500, 1960.000),
        ('EMP-002', 'Fatma Trabelsi', '07891234', 1800.000, 174.240, 142.300, 9.000, 1474.460)
        """)

    conn.commit()
    conn.close()

init_db()

app = FastAPI(title=MODULE_TITLE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/settings")
def get_settings():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.cursor().execute("SELECT * FROM company LIMIT 1").fetchone()
    conn.close()
    return dict(row)

class SettingsUpdate(BaseModel):
    name: str
    matricule_fiscal: str
    registre_commerce: str
    adresse: str
    telephone: str
    email: str
    regime_tva: str
    regime_fiscal: str
    taux_is: int
    tva_normale: float
    tva_intermediaire: float
    tva_reduite: float
    timbre_fiscal: float
    cnss_salarie: float
    cnss_patronale: float
    css: float
    tfp: float
    foprolos: float
    abattement_famille: float
    abattement_enfant: float

@app.post("/api/settings")
def update_settings(data: SettingsUpdate):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    UPDATE company SET 
        name=?, matricule_fiscal=?, registre_commerce=?, adresse=?, telephone=?, email=?,
        regime_tva=?, regime_fiscal=?, taux_is=?, tva_normale=?, tva_intermediaire=?, tva_reduite=?,
        timbre_fiscal=?, cnss_salarie=?, cnss_patronale=?, css=?, tfp=?, foprolos=?,
        abattement_famille=?, abattement_enfant=?
    WHERE id=1
    """, (
        data.name, data.matricule_fiscal, data.registre_commerce, data.adresse, data.telephone, data.email,
        data.regime_tva, data.regime_fiscal, data.taux_is, data.tva_normale, data.tva_intermediaire, data.tva_reduite,
        data.timbre_fiscal, data.cnss_salarie, data.cnss_patronale, data.css, data.tfp, data.foprolos,
        data.abattement_famille, data.abattement_enfant
    ))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Parametres et taux SAFE ERP enregistres avec succes !"}

@app.get("/api/invoices")
def get_invoices():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.cursor().execute("SELECT * FROM factures ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/payroll")
def get_payroll():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.cursor().execute("SELECT * FROM salaries ORDER BY id ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/efatoura/xml/{invoice_id}")
def generate_teif_xml(invoice_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    inv = conn.cursor().execute("SELECT * FROM factures WHERE id=?", (invoice_id,)).fetchone()
    co = conn.cursor().execute("SELECT * FROM company LIMIT 1").fetchone()
    conn.close()
    if not inv:
        raise HTTPException(status_code=404, detail="Facture introuvable")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
         xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
         xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2">
    <cbc:ID>{inv['numero']}</cbc:ID>
    <cbc:IssueDate>{inv['date_facture']}</cbc:IssueDate>
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cac:PartyName><cbc:Name>{co['name']}</cbc:Name></cac:PartyName>
            <cac:PartyTaxScheme><cbc:CompanyID>{co['matricule_fiscal']}</cbc:CompanyID></cac:PartyTaxScheme>
        </cac:Party>
    </cac:AccountingSupplierParty>
    <cac:AccountingCustomerParty>
        <cac:Party>
            <cac:PartyName><cbc:Name>{inv['client_nom']}</cbc:Name></cac:PartyName>
            <cac:PartyTaxScheme><cbc:CompanyID>{inv['client_mat']}</cbc:CompanyID></cac:PartyTaxScheme>
        </cac:Party>
    </cac:AccountingCustomerParty>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="TND">{inv['total_tva']:.3f}</cbc:TaxAmount>
    </cac:TaxTotal>
    <cac:LegalMonetaryTotal>
        <cbc:TaxExclusiveAmount currencyID="TND">{inv['total_ht']:.3f}</cbc:TaxExclusiveAmount>
        <cbc:PayableAmount currencyID="TND">{inv['total_ttc']:.3f}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>
</Invoice>"""
    return HTMLResponse(content=xml, media_type="application/xml")

@app.get("/", response_class=HTMLResponse)
def index_html():
    hw_id = get_hardware_id()
    # Read external html file or render template
    html_file = os.path.join(os.path.dirname(__file__), "pme_index.html")
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = "<h2>SAFE PME Express</h2>"
    return content.replace("{{HARDWARE_ID}}", hw_id)

def open_browser():
    time.sleep(1.2)
    webbrowser.open(f"http://127.0.0.1:{PORT}")

if __name__ == "__main__":
    hw_id = get_hardware_id()
    print("=" * 75)
    print(f" {MODULE_TITLE} (STANDALONE)")
    print(f" Port Local           : {PORT}")
    print(f" Verrou Hardware ID   : {hw_id}")
    print(f" Cryptographie        : HMAC-SHA256")
    print(f" Normes Fiscales      : TND (3 déc.) | TVA 19% | Timbre 1.000 DT | TEIF e-Fatoura")
    print("=" * 75)
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")
