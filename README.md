# SAFE PME Express 2.0

Application ERP standalone pour PME tunisiennes.

## Démarrage rapide

1. Double-cliquer sur `Lancer_SAFE_PME_Express.cmd`
2. Ouvrir le navigateur sur http://localhost:8006
3. Se connecter avec `admin` / `admin`

## Comptes par défaut

| Utilisateur | Mot de passe | Rôle |
|-------------|-------------|------|
| admin | admin | Administrateur |
| admin | safe2024 | Administrateur |
| admin@safe.tn | safe2024 | Administrateur |
| demo | demo | Démo |
| comptable | comptable | Comptable |

## Modules

18 modules intégrés :
- Dashboard, Factures, Achats, Tiers, Articles, Stock
- Salariés, Paie (CNSS 9.68%, IRPP officiel)
- Comptabilité PCN, TVA, Fiscalité, Immobilisations
- Trésorerie, Déclarations, e-Fatoura
- Rapports, Réinitialisation, Paramètres

## Stack technique

- Backend : Python 3.x + FastAPI + SQLite
- Frontend : HTML5 + Bootstrap 5 + Chart.js
- Port : 8006 (standalone, sans Docker)

---
*SAFE Suite Tunisie — © 2026*
