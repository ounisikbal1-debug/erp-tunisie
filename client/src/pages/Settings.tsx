import { trpc } from "@/_core/trpc";
import { PageHeader, Panel, Table } from "@/components/primitives";
import {
  CNSS_EMPLOYEE_RATE,
  CNSS_EMPLOYER_RATE,
  CSS_RATE,
  IRPP_BRACKETS,
  IRPP_DEPENDENT_DEDUCTION,
  IRPP_HEAD_OF_FAMILY_DEDUCTION,
  IS_RATES,
  STAMP_DUTY,
  TCL_RATES_BP,
  WITHHOLDING_RATES,
  fmtTND,
} from "../../../shared/fiscal";

export default function Settings() {
  const company = trpc.company.get.useQuery();
  const c = company.data;

  const rows: [string, string][] = c
    ? [
        ["Raison sociale", c.name],
        ["Matricule fiscal", c.matriculeFiscal],
        ["Registre de commerce", c.registreCommerce],
        ["Adresse", c.address],
        ["Téléphone", c.phone],
        ["E-mail", c.email],
        ["Régime TVA", c.vatRegime === "assujetti" ? "Assujetti" : c.vatRegime === "exportateur" ? "Exportateur" : "Non assujetti"],
        ["Régime fiscal", c.taxRegime === "reel" ? "Réel" : "Forfaitaire"],
        ["Taux IS", `${c.isRate} %`],
        ["Exercice comptable", String(c.fiscalYear)],
        ["Taux TCL", `${(c.tclRateBp / 10).toFixed(1)} %`],
      ]
    : [];

  return (
    <>
      <PageHeader
        title="Paramètres"
        subtitle="Identité de la société, taux fiscaux et barème IRPP appliqués"
      />

      <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
        <Panel title="Identité de la société" subtitle="Mentions portées sur les factures" noPad>
          <dl className="divide-y divide-border">
            {(rows.length ? rows : [["Chargement…", "—"]]).map(([k, v]) => (
              <div key={k} className="flex items-start justify-between gap-4 px-4 py-2.5">
                <dt className="text-[12px] text-muted-foreground">{k}</dt>
                <dd className="text-right text-[12.5px] font-medium">{v}</dd>
              </div>
            ))}
          </dl>
          <p className="border-t border-border px-4 py-2.5 text-[11px] leading-relaxed text-muted-foreground">
            Les coordonnées se modifient depuis le panneau base de données de la plateforme (table
            <span className="font-mono"> company</span>).
          </p>
        </Panel>

        <Panel title="Taux fiscaux & sociaux" subtitle="Valeurs appliquées par les moteurs de calcul" noPad>
          <Table head={["Paramètre", "Valeur"]}>
            {[
              ["TVA — taux normal", "19 %"],
              ["TVA — taux intermédiaire", "13 %"],
              ["TVA — taux réduit", "7 %"],
              ["TVA — exonéré / export", "0 %"],
              ["Timbre fiscal (facture)", fmtTND(STAMP_DUTY)],
              ["CNSS — part salariale", `${CNSS_EMPLOYEE_RATE} %`],
              ["CNSS — part patronale", `${CNSS_EMPLOYER_RATE} %`],
              ["CSS — contribution de solidarité", `${CSS_RATE} %`],
              ["IS — taux services / industrie", `${IS_RATES[0]} %`],
              ["IS — taux autres sociétés", `${IS_RATES[1]} %`],
              ["Acompte provisionnel", "30 % de l'IS"],
              ["TCL — taux général", `${(TCL_RATES_BP[0] / 10).toFixed(1)} %`],
              ["TCL — hôtellerie", `${(TCL_RATES_BP[1] / 10).toFixed(1)} %`],
              ["Retenue à la source", `${WITHHOLDING_RATES.join(" % / ")} %`],
              ["Abattement chef de famille", `${IRPP_HEAD_OF_FAMILY_DEDUCTION} TND / an`],
              ["Abattement par personne à charge", `${IRPP_DEPENDENT_DEDUCTION} TND / an`],
            ].map(([k, v]) => (
              <tr key={k}>
                <td className="text-muted-foreground">{k}</td>
                <td className="num text-right font-semibold">{v}</td>
              </tr>
            ))}
          </Table>
        </Panel>
      </div>

      <Panel title="Barème IRPP en vigueur" subtitle="8 tranches progressives — 0 % à 40 %" className="mt-4" noPad>
        <Table head={["Tranche", "Bornes annuelles (TND)", "Taux marginal"]}>
          {IRPP_BRACKETS.map((b, i) => (
            <tr key={i}>
              <td className="text-muted-foreground">Tranche {i + 1}</td>
              <td>
                {b.from.toLocaleString("fr-FR")} — {b.to === null ? "au-delà" : b.to.toLocaleString("fr-FR")}
              </td>
              <td className="num text-right font-semibold text-gold">{b.rate} %</td>
            </tr>
          ))}
        </Table>
        <p className="border-t border-border px-4 py-2.5 text-[11px] leading-relaxed text-muted-foreground">
          Barème progressif appliqué au revenu net imposable annualisé, puis divisé par 12 pour la retenue mensuelle
          à la source. Les abattements familiaux sont déduits de l'impôt annuel ainsi calculé.
        </p>
      </Panel>

      <Panel title="Installation & accès réseau" subtitle="PC, réseau local et interface web" className="mt-4">
        <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
          <div className="rounded-lg border border-border bg-secondary/30 p-3">
            <p className="text-[12px] font-semibold text-navy">1 · Installer sur PC</p>
            <p className="mt-1.5 text-[11.5px] leading-relaxed text-muted-foreground">
              Ouvrez l'ERP dans Chrome, Edge ou Safari, puis cliquez sur <strong>⤓ Installer</strong> dans la barre
              supérieure (ou l'icône d'installation dans la barre d'adresse). L'application s'ouvre ensuite dans sa
              propre fenêtre, avec une icône sur le bureau et dans le menu Démarrer — sans navigateur visible.
            </p>
          </div>
          <div className="rounded-lg border border-border bg-secondary/30 p-3">
            <p className="text-[12px] font-semibold text-navy">2 · Accès réseau local</p>
            <p className="mt-1.5 text-[11.5px] leading-relaxed text-muted-foreground">
              Sur le poste serveur, l'ERP écoute sur toutes les interfaces. Les autres postes du bureau y accèdent via
              l'adresse IP locale du serveur, par exemple <span className="font-mono">http://192.168.1.20:3000</span>.
              Aucune installation n'est nécessaire sur les postes clients : un navigateur suffit.
            </p>
          </div>
          <div className="rounded-lg border border-border bg-secondary/30 p-3">
            <p className="text-[12px] font-semibold text-navy">3 · Interface web</p>
            <p className="mt-1.5 text-[11.5px] leading-relaxed text-muted-foreground">
              La même application sert l'interface web et l'API. Après publication, elle est accessible depuis
              n'importe quel navigateur, sur ordinateur comme sur mobile, avec la même base de données.
            </p>
          </div>
        </div>
        <p className="mt-3 rounded-lg bg-gold-soft/50 p-2.5 text-[11px] leading-relaxed text-[hsl(38_72%_30%)]">
          Les données sont stockées côté serveur : tous les postes du réseau voient la même comptabilité, la même paie
          et les mêmes factures, en temps réel.
        </p>
      </Panel>

      <Panel title="Périmètre de l'application" subtitle="Ce que l'ERP fait et ne fait pas" className="mt-4">
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div className="rounded-lg border border-border bg-secondary/30 p-3">
            <p className="text-[12px] font-semibold text-success">Inclus</p>
            <ul className="mt-1.5 space-y-1 text-[11.5px] text-muted-foreground">
              <li>Facturation, achats, TVA et timbre fiscal</li>
              <li>Paie complète : CNSS 9,68 % / 17,07 %, CSS 0,5 %, IRPP 8 tranches</li>
              <li>Comptabilité générale et balance</li>
              <li>Immobilisations et amortissements linéaires</li>
              <li>Trésorerie et tableau de bord</li>
              <li>Calculs TVA, TCL, IS et acomptes provisionnels</li>
              <li>Transmission directe à la Télédéclaration TTN et à e-Fatoura (une fois les clés d'API saisies)</li>
            </ul>
          </div>
          <div className="rounded-lg border border-border bg-secondary/30 p-3">
            <p className="text-[12px] font-semibold text-destructive">Non inclus</p>
            <ul className="mt-1.5 space-y-1 text-[11.5px] text-muted-foreground">
              <li>Envoi d'e-mails ou de factures par e-mail</li>
              <li>Paiement en ligne ou prélèvement bancaire</li>
              <li>Signature électronique des documents</li>
            </ul>
            <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
              La transmission TTN / e-Fatoura nécessite vos identifiants d'API, saisis dans Web Admin → Secrets. Sans
              ces clés, l'ERP refuse l'envoi et l'indique — il ne simule jamais une transmission.
            </p>
          </div>
        </div>
      </Panel>
    </>
  );
}
