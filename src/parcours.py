"""Visuel « Parcours client B2B · revendeur / intégrateur IT », dessiné en SVG aux couleurs du site.
Données reprises du visuel d'Agnès (exemple illustratif)."""
from html import escape

INK, INK2, MUTED, LINE, SURF = "#0B1017", "#2B3341", "#5E5C56", "#E6E3DC", "#F6F5F2"
CLIENT = "#F2552C"
# Ressenti du client : couleurs d'état (mêmes teintes que l'auto-diagnostic), distinctes des couleurs des métiers
LEVELS = [("Enchanté", "#2E8B57"), ("Satisfait", "#2F45F5"), ("Déçu", "#D9932B"), ("Irrité", "#C0392B")]
E, S, D, I = 0, 1, 2, 3
TEAMS = ["Marketing", "Commercial", "Avant-vente", "Projet & technique", "Support / hotline", "ADV & comptabilité", "Customer Success"]
MK, CO, AV, PT, SU, AD, CS = range(7)

PHASES = [
  ("Découverte & avant-vente", [
    ("Je recherche une solution et je m’informe", S, "Web, salons", [MK]),
    ("Je contacte un commercial ou il me contacte", S, "Téléphone", [CO]),
    ("J’exprime mes besoins lors d’un rendez-vous", E, "Rendez-vous", [CO, AV]),
    ("J’assiste à une démo ou un test", E, "Démo / POC", [CO, AV]),
    ("Je reçois la proposition et je négocie", S, "E-mail, RDV", [CO, AV])]),
  ("Commande & projet", [
    ("Je signe la commande ou le contrat", S, "Contrat", [CO, AD]),
    ("On me présente le projet et le planning", S, "Réunion", [CO, PT])]),
  ("Livraison, installation & onboarding", [
    ("Je reçois le matériel ou les licences", D, "Livraison", [PT, AD]),
    ("Un technicien installe et paramètre", S, "Sur site", [PT]),
    ("Je suis formé à la solution", D, "Formation", [PT, CS]),
    ("Je reçois mes infos de suivi (contacts, portail, support)", D, "E-mail, portail", [CO, SU, AD, CS])]),
  ("Usage & support", [
    ("J’utilise la solution au quotidien", S, "Solution", [SU, CS]),
    ("Je signale un incident au support", I, "Hotline, ticket", [SU]),
    ("Un technicien intervient et résout", E, "Distance, site", [PT, SU]),
    ("Je reçois des mises à jour ou évolutions", S, "E-mail", [SU])]),
  ("Administratif & facturation", [
    ("Je reçois et je règle mes factures", I, "Facture", [AD]),
    ("Je fais une demande (facture, contrat)", D, "E-mail, tél.", [AD]),
    ("Je commande des licences ou options", S, "Portail, commercial", [CO, AD])]),
  ("Suivi & renouvellement", [
    ("Je fais le point avec mon commercial", E, "Revue de compte", [CO, CS]),
    ("Je réponds à une enquête de satisfaction", D, "Enquête", [MK, CS]),
    ("Je suis invité à un événement ou webinaire", S, "Invitation", [MK]),
    ("Je renouvelle ou fais évoluer mon contrat", S, "Rendez-vous", [CO, AD, CS])]),
]

def wrap(text, n):
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + [cur] if cur else lines

def tspans(x, y, text, n, lh, **attrs):
    a = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    t = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{escape(l)}</tspan>' for i, l in enumerate(wrap(text, n)))
    return f'<text x="{x}" y="{y}" {a}>{t}</text>'

def svg():
    L, CW = 200, 84                      # colonne des libellés, largeur d'une étape
    steps = [(pi, s) for pi, (_, ss) in enumerate(PHASES) for s in ss]
    W = L + CW * len(steps) + 10
    yPh, hPh = 20, 52                    # bandeau des phases
    yStep = 100                          # étapes vécues
    nl = max(len(wrap(s[1][0], 11)) for s in steps)
    y0 = yStep + 15 * nl + 70
    yLv = [y0 + 50 * k for k in range(4)]  # niveaux de ressenti
    yTp = yLv[-1] + 70                   # points de contact
    yTeam0, dTeam = yTp + 95, 34         # équipes
    yEnd = yTeam0 + dTeam * (len(TEAMS) - 1) + 24
    H = yEnd + 10
    cx = lambda i: L + CW * i + CW / 2
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Montserrat, Arial, sans-serif" role="img" '
         f'aria-label="Parcours client B2B d’un revendeur ou intégrateur IT : 22 étapes en 6 phases, du premier contact au renouvellement, avec le ressenti du client, les points de contact et les équipes impliquées.">']
    # Fonds alternés par phase + bandeaux
    i0 = 0
    for pi, (name, ss) in enumerate(PHASES):
        x, w = L + CW * i0, CW * len(ss)
        if pi % 2 == 0:
            o.append(f'<rect x="{x}" y="{yPh + hPh + 6}" width="{w}" height="{yEnd - yPh - hPh - 6}" fill="{SURF}"/>')
        o.append(f'<rect x="{x + 2}" y="{yPh}" width="{w - 4}" height="{hPh}" rx="10" fill="{INK}"/>')
        two = len(name) * 9 > w - 24
        o.append(tspans(x + w / 2, yPh + (21 if two else 31), name, max(10, int((w - 24) / 9)), 17,
                        text_anchor="middle", fill="#fff", font_size="14", font_weight="600"))
        i0 += len(ss)
    # Libellés de gauche
    def lab(y, t, big=True):
        o.append(f'<text x="0" y="{y}" fill="{INK}" font-size="{15 if big else 13}" font-weight="{600 if big else 500}">{escape(t)}</text>')
    o.append(tspans(0, yStep + 2, "Étapes vécues par le client", 16, 19, fill=INK, font_size="15", font_weight="600"))
    lab(yLv[0] - 40, "Expérience client")
    for (n, c), y in zip(LEVELS, yLv):
        o.append(f'<circle cx="8" cy="{y}" r="7" fill="{c}"/><text x="24" y="{y + 5}" fill="{INK2}" font-size="13">{n}</text>')
        o.append(f'<line x1="{L}" x2="{W}" y1="{y}" y2="{y}" stroke="{LINE}" stroke-dasharray="4 5"/>')
    lab(yTp + 5, "Points de contact")
    lab(yTeam0 - 34, "Équipes impliquées")
    for t, name in enumerate(TEAMS):
        y = yTeam0 + dTeam * t
        o.append(f'<text x="0" y="{y + 5}" fill="{CLIENT if t == CS else INK2}" font-size="13" font-weight="{600 if t == CS else 400}">{escape(name)}</text>')
        o.append(f'<line x1="{L}" x2="{W}" y1="{y}" y2="{y}" stroke="{LINE}"/>')
    # Étapes, courbe, points de contact, équipes
    pts = []
    for i, (pi, (txt, lv, tp, teams)) in enumerate(steps):
        x = cx(i)
        o.append(tspans(x, yStep, txt, 11, 15, text_anchor="middle", fill=INK2, font_size="11.5"))
        pts.append((x, yLv[lv], LEVELS[lv][1]))
        o.append(f'<rect x="{x - 34}" y="{yTp - 16}" width="68" height="40" rx="8" fill="#fff" stroke="{LINE}"/>')
        o.append(tspans(x, yTp - 1 if len(tp) > 11 else yTp + 8, tp, 11, 14, text_anchor="middle", fill=MUTED, font_size="11"))
        for t in teams:
            o.append(f'<circle cx="{x}" cy="{yTeam0 + dTeam * t}" r="7" fill="{CLIENT if t == CS else INK}"/>')
    o.append(f'<polyline points="{" ".join(f"{x},{y}" for x, y, _ in pts)}" fill="none" stroke="#A5AFBE" stroke-width="2.5" stroke-linejoin="round"/>')
    o += [f'<circle cx="{x}" cy="{y}" r="11" fill="{c}" stroke="#fff" stroke-width="3"/>' for x, y, c in pts]
    o.append('</svg>')
    return '\n'.join(o)

LEGEND = ("<b>Lecture :</b> chaque point de la courbe indique le ressenti du client à cette étape. Les points rouges et orange sont les irritants à traiter en priorité ; "
          "les étapes vertes sont des moments de vérité réussis à préserver. Dans les équipes, les points corail signalent le rôle Customer Success, souvent absent "
          "chez les revendeurs : c’est lui qui assure la continuité de la relation entre les étapes. <i>Exemple illustratif, à adapter à chaque entreprise.</i>")

if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w").write(svg())
