#!/usr/bin/env python3
"""Génère le site Xpansio v3 : dist/ (site à héberger) et artifact/ (accueil sans squelette)."""
import os, shutil, sys
import hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import *

SRC = os.path.dirname(os.path.abspath(__file__))
# Version de la feuille de style : change à chaque modification de styles.css, ce qui force les navigateurs à recharger le style.
CSS_V = hashlib.md5(open(os.path.join(SRC, "styles.css"), "rb").read()).hexdigest()[:8]
# Clé publique Web3Forms (formulaire de contact), liée à l'adresse d'Agnès. Elle est faite pour être visible dans la page.
WEB3FORMS_KEY = "98890583-2366-4dbd-afb2-a1896cf89b4d"
ROOT = os.path.dirname(SRC)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Montserrat:wght@400;500;600;700&display=swap">')

NAV = [("index.html", "Accueil", "home"), ("realisations.html", "Nos réalisations", "realisations"),
       ("contact.html", "Contact", "contact")]

def header(cur):
    pages = ''.join(
        f'<a href="{h}"{" aria-current=\"page\"" if k == cur else ""}>{l}{ARR}</a>' for h, l, k in NAV)
    return f'''<header class="top">
  <div class="wrap top-bar">
    <button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drop"><span class="bars" aria-hidden="true"><i></i><i></i><i></i></span><span class="txt">Menu</span></button>
    <a class="brand" href="index.html" aria-label="Xpansio, accueil"><img class="full" src="assets/logo.png" alt="xpansio" width="480" height="140"><img class="mark" src="assets/logo-mark.png" alt="" width="256" height="256"></a>
    <div class="top-right"><a class="btn btn-primary btn-sm" href="contact.html">Prendre rendez-vous</a></div>
  </div>
  <nav class="drop" id="drop" hidden aria-label="Menu principal">
    <div class="wrap">
      <div class="drop-col"><span class="label">Pages</span><div class="drop-pages">{pages}</div></div>
      <div class="drop-col"><span class="label">Nos expertises</span>
        <div class="drop-exp">
          <a class="ch" href="experience-channel.html"><span class="ico ch">{I_NET}</span><strong>Channel Performance</strong><span class="d">Parcours partenaires, programmes partenaires, stratégie de réseau, gestion de clubs de partenaires.</span></a>
          <a class="cl" href="experience-client.html"><span class="ico cl">{I_USER}</span><strong>Customer Performance</strong><span class="d">Parcours client, satisfaction, segmentation, rétention.</span></a>
        </div>
      </div>
    </div>
  </nav>
</header>'''

FOOTER = '''<footer>
  <div class="wrap">
    <img class="logo" src="assets/logo-white.png" alt="xpansio" width="480" height="140">
    <p class="tagline">Accélérer la performance de vos partenaires.<br>Révéler la valeur de vos clients.</p>
    <nav aria-label="Pied de page"><a href="index.html">Accueil</a><a href="experience-channel.html">Channel Performance</a><a href="experience-client.html">Customer Performance</a><a href="realisations.html">Nos réalisations</a><a href="contact.html">Contact</a><a href="https://www.linkedin.com/in/agnes-chabrier-7186971/" target="_blank" rel="noopener">LinkedIn</a></nav>
    <div class="foot-bottom"><span>© 2026 Xpansio · Agnès Chabrier, entrepreneure individuelle</span><a href="mentions-legales.html">Mentions légales et confidentialité</a></div>
  </div>
</footer>'''

SCRIPT = '''<script>
(function(){
  /* En-tête compact avec le logo simplifié dès que l'on défile */
  var top=document.querySelector('.top'),tk=false;
  function onScroll(){tk=false;if(top)top.classList.toggle('scrolled',window.scrollY>40);}
  window.addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(onScroll);}},{passive:true});onScroll();
  /* Apparition au défilement : seuls les blocs encore hors écran sont animés, rien ne reste caché sans JS. */
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!reduce&&'IntersectionObserver' in window){
    /* Lignes des étapes tracées et chiffres qui défilent quand ils deviennent visibles */
    var io2=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;var el=e.target;io2.unobserve(el);
      if(el.classList.contains('draw')){el.classList.add('in');return;}
      var m=el.textContent.match(/^([+-]?)(\\d+)(.*)$/);if(!m)return;
      var end=parseInt(m[2],10),pre=m[1],suf=m[3],t0=null,dur=1200;
      function f(ts){if(!t0)t0=ts;var k=Math.min((ts-t0)/dur,1),v=Math.round(end*(1-Math.pow(1-k,3)));el.textContent=pre+v+suf;if(k<1)requestAnimationFrame(f);}
      requestAnimationFrame(f);});},{threshold:.4});
    document.querySelectorAll('.steps,.seq').forEach(function(s){s.classList.add('draw');io2.observe(s);});
    document.querySelectorAll('.kpi .v').forEach(function(v){if(/^[+-]?\\d/.test(v.textContent))io2.observe(v);});
    var sel='.head,.xcard,.stat,.step,.pcard,.issue,.offer,.seg,.dim,.target,.sq,.case-col,.case-kpis .kpi,.coords div,.form,.pillars div,.portrait,.timeline,.chain-wrap,.legal>div,.below';
    var els=[].slice.call(document.querySelectorAll(sel));
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    els.forEach(function(el){
      if(el.getBoundingClientRect().top<window.innerHeight*.92)return;
      var sib=el.parentNode?[].indexOf.call(el.parentNode.children,el):0;
      el.style.setProperty('--d',Math.min(sib,6)*70+'ms');
      el.classList.add('rv');io.observe(el);
    });
  }
  /* Collage de l'accueil : léger effet de profondeur qui suit la souris */
  var st=document.querySelector('.stack.links'),hero=document.querySelector('.hero');
  if(st&&hero&&!reduce&&window.matchMedia('(hover:hover) and (pointer:fine)').matches){
    var raf=0,mx=0,my=0;
    hero.addEventListener('pointermove',function(e){var r=hero.getBoundingClientRect();mx=(e.clientX-r.left)/r.width-.5;my=(e.clientY-r.top)/r.height-.5;
      if(!raf)raf=requestAnimationFrame(function(){raf=0;st.style.setProperty('--mx',mx.toFixed(3));st.style.setProperty('--my',my.toFixed(3));});});
    hero.addEventListener('pointerleave',function(){st.style.setProperty('--mx',0);st.style.setProperty('--my',0);});
  }
  var b=document.querySelector('.menu-btn'),d=document.getElementById('drop');
  function set(o){d.hidden=!o;b.setAttribute('aria-expanded',String(o));}
  if(b&&d){
    b.addEventListener('click',function(e){e.stopPropagation();set(d.hidden);});
    d.addEventListener('click',function(e){e.stopPropagation();});
    document.addEventListener('click',function(){if(!d.hidden)set(false);});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!d.hidden){set(false);b.focus();}});
  }
  var f=document.querySelector('form.form');
  if(f){f.addEventListener('submit',function(e){
    e.preventDefault();var msg=f.querySelector('.form-msg');
    var btn=f.querySelector('button[type=submit]');btn.disabled=true;
    fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Accept':'application/json'},body:new FormData(f)})
      .then(function(r){return r.json();}).then(function(j){btn.disabled=false;if(!j.success)throw 0;msg.textContent='Merci, votre message a bien été envoyé. Réponse sous 48 heures ouvrées.';msg.hidden=false;f.reset();})
      .catch(function(){btn.disabled=false;msg.textContent="Le message n’a pas pu être envoyé. Réessayez dans quelques instants, ou utilisez le bouton Appeler.";msg.hidden=false;});
  });}
})();
</script>'''

def page(key, title, desc, body, full=True):
    head = (f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{desc}">\n{FONTS}\n<link rel="stylesheet" href="styles.css?v={CSS_V}">\n<link rel="icon" href="assets/favicon.png">')
    inner = f'{header(key)}\n<main>\n{body}\n</main>\n{FOOTER}\n{SCRIPT}'
    if not full:
        return head + '\n' + inner
    return (f'<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}\n</head>\n<body>\n{inner}\n</body>\n</html>\n')

def head(label, title, lead=None, cls=""):
    l = f'<p class="lead">{lead}</p>' if lead else ''
    return f'<div class="head"><span class="label {cls}">{label}</span><h2 class="h2">{title}</h2>{l}</div>'

def cta(title="Parlons de vos partenaires et de vos clients.", text="Un premier échange de 30 minutes pour faire le point sur vos enjeux, sans engagement.", btn="Prendre rendez-vous"):
    return f'''<section class="band ink"><div class="wrap">
  {head("Contact", title, text)}
  <div class="ctas"><a class="btn btn-white" href="contact.html">{btn} {ARR}</a></div>
</div></section>'''

def page_hero(crumbs, title, lead, extra="", cta_btn=None, tiles="", h1cls=""):
    cr = '<span>/</span>'.join(f'<a href="{h}">{t}</a>' if h else f'<span>{t}</span>' for h, t in crumbs)
    return f'''<section class="page-hero{' has-stack' if tiles else ''}"><div class="wrap">
  <nav class="crumbs" aria-label="Fil d’Ariane">{cr}</nav>
  {extra}
  <h1 class="h1{h1cls}">{title}</h1>
  {''.join(f'<p class="lead">{x}</p>' for x in (lead if isinstance(lead, list) else [lead]))}
  {f'<div class="ctas"><a class="btn btn-primary" href="contact.html">{cta_btn} {ARR}</a></div>' if cta_btn else ''}
</div>{tiles}</section>'''

def issues(items):
    return '<div class="issues">' + ''.join(
        f'<div class="issue"><span class="num">0{i+1}</span><b>{t}</b><p>{p}</p></div>' for i, (t, p) in enumerate(items)) + '</div>'

def offers(items, cls):
    """Cartes de leviers : (icône, titre, texte, mots-clés) ou (icône, titre, accroche, texte, mots-clés) ; ces dernières sont numérotées."""
    out = []
    for i, it in enumerate(items):
        if len(it) == 5:
            ico, t, hook, p, tags = it
            n, hk = f'<span class="onum {cls}">0{i+1}</span>', f'<p class="hook">{hook}</p>'
        else:
            (ico, t, p, tags), n, hk = it, '', ''
        tg = ''.join(f'<li>{x}</li>' for x in tags)
        out.append(f'<div class="offer {cls}"><span class="ico {cls}">{ico}</span>{n}<h3>{t}</h3>{hk}<p>{p}</p><ul>{tg}</ul></div>')
    return '<div class="offers">' + ''.join(out) + '</div>'

def cards(items, cls, n=None):
    """Cartes sobres : (icône ou None, titre, texte[, mots-clés en ligne])."""
    out = []
    for it in items:
        ico, t, p = it[:3]
        kw = f'<span class="kw {cls}">{it[3]}</span>' if len(it) > 3 else ''
        ic = f'<span class="ico {cls}">{ico}</span>' if ico else ''
        out.append(f'<div class="card {cls}">{ic}<h3>{t}</h3>{kw}<p>{p}</p></div>')
    return f'<div class="cards{" n"+str(n) if n else ""}">' + ''.join(out) + '</div>'

def loop(steps, cls, label):
    """Schéma cyclique : étapes reliées, la dernière revient à la première."""
    li = ''.join(f'<li class="lp"><span class="n">0{i+1}</span><b>{t}</b><p>{p}</p></li>' for i, (t, p) in enumerate(steps))
    return (f'<div class="loop {cls}" role="group" aria-label="{label}"><ol>{li}</ol>'
            f'<div class="loop-back" aria-hidden="true"><span>Un cycle continu</span></div></div>')

def targets(items, cls):
    return f'<div class="targets {cls}">' + ''.join(f'<span class="target"><i></i>{t}</span>' for t in items) + '</div>'

# ---------- Collage de photos du terrain (haut de page) ----------
# Photos fournies par Agnès (petits logos de marques floutés).
PHOTOS = {
    "carnet": "photo-carnet.jpg",          # consultant qui annote son carnet
    "salle": "photo-salle.jpg",            # salle de réunion, analyse de données projetée
    "dossier": "photo-dossier.jpg",        # séance de travail sur documents chiffrés
    "dialogue": "photo-dialogue.jpg",      # échange en face à face
}
def collage(keys, note=None, cls=""):
    """Photos en éventail sous le texte du haut de page. Purement décoratif."""
    imgs = ''.join(f'<span class="ph p{i+1}" style="--i:{i}"><img src="assets/{PHOTOS[k]}" alt="" loading="eager" decoding="async"></span>'
                   for i, k in enumerate(keys))
    return f'<div class="stack n{len(keys)} {cls}" aria-hidden="true">{imgs}</div>'
# ---------- RÉALISATIONS ----------
# Chaque réalisation : situation réelle, sans client nommé ni résultat non vérifié.
# kind : "x" = mission de conseil Xpansio, "a" = expérience professionnelle antérieure de la fondatrice.
KIND = {"x": "Mission Xpansio", "a": "Expérience antérieure"}
EXP = {"ch": ("Channel Performance", "experience-channel.html"), "cl": ("Customer Performance", "experience-client.html")}

REAL = [
  dict(slug="realisation-valeur-marque.html", cls="ch", kind="x",
    title="Comment redonner de la valeur à une marque lorsque les partenaires ne parlent plus que de prix ?",
    ctx="Un constructeur sur un marché mature, des offres difficiles à différencier et une forte pression sur les prix.",
    ans="Repenser la proposition de valeur pour le réseau et la traduire dans le programme partenaires.",
    defi="Un constructeur présent sur un marché mature, face à une forte pression concurrentielle. Aux yeux de ses partenaires, ses offres se distinguaient mal de celles de ses concurrents, et les négociations se concentraient sur le prix d’achat. Comment convaincre le réseau de privilégier une marque premium et d’en défendre la valeur ?",
    reponse="Repenser la proposition de valeur du fournisseur pour son réseau : ce que la marque apporte au développement de ses partenaires, au-delà de la marge. Puis traduire cette stratégie dans le programme partenaires.",
    done=["Analyse du positionnement et des enjeux économiques du réseau",
          "Construction d’une proposition de valeur partenaire",
          "Traduction dans les dispositifs d’accompagnement et de reconnaissance",
          "Développement de communautés et d’initiatives autour des services",
          "Renforcement des compétences commerciales et de la vente par la valeur"],
    result="Un partenaire défend une marque lorsqu’il comprend ce qu’elle apporte à sa propre activité. La proposition de valeur se construit pour le réseau avant de se décliner en niveaux, remises et avantages.",
    xp="Mission de conseil Xpansio auprès d’un constructeur international. Le client n’est pas nommé, par confidentialité."),
  dict(slug="realisation-crise-clients-prioritaires.html", cls="cl", kind="a",
    title="Comment préserver la satisfaction client lorsque la crise impose des arbitrages ?",
    ctx="Une crise d’approvisionnement majeure : l’entreprise ne peut plus répondre normalement à toutes les demandes.",
    ans="Mieux connaître le portefeuille pour identifier les clients prioritaires et orienter la fidélisation.",
    defi="Une crise majeure d’approvisionnement dégrade la qualité de service et la satisfaction des clients. L’entreprise ne peut plus répondre normalement à toutes les demandes. Comment préserver les relations stratégiques lorsque les ressources sont contraintes et qu’il faut arbitrer ?",
    reponse="Améliorer la connaissance du portefeuille clients pour identifier les situations prioritaires, en combinant plusieurs dimensions de la valeur client au-delà du seul chiffre d’affaires. Prioriser ne signifie pas abandonner : engagements contractuels, équité et besoins critiques restent pris en compte.",
    done=["Analyse du portefeuille clients",
          "Définition de critères de valeur stratégique adaptés au contexte : économiques, relationnels, fidélité",
          "Conception d’une segmentation des clients prioritaires",
          "Proposition de modalités d’accompagnement différenciées",
          "Identification des conditions nécessaires à la mise en œuvre"],
    result="La démarche et la segmentation ont été conçues ; leur déploiement opérationnel complet a été freiné par des contraintes de systèmes d’information. L’enseignement : une bonne connaissance du capital client facilite les arbitrages lorsque les ressources sont limitées.",
    xp="Expérience professionnelle antérieure de la fondatrice, chez un constructeur international de solutions bureautiques et IT, avant la création d’Xpansio."),
  dict(slug="realisation-au-dela-du-nps.html", cls="cl", kind="a",
    title="Et si mesurer le NPS ne suffisait plus à fidéliser les clients ?",
    ctx="Des mesures de satisfaction existent, mais elles n’expliquent pas l’insatisfaction et ne déclenchent pas d’améliorations.",
    ans="Passer de la mesure à une démarche structurée d’amélioration de l’expérience client.",
    defi="L’entreprise mesure la satisfaction de ses clients, mais ces mesures ne suffisent pas à identifier les causes profondes de l’insatisfaction, ni à déclencher des améliorations concrètes. Comment transformer l’écoute client en actions qui améliorent réellement l’expérience ?",
    reponse="Passer d’une logique de mesure à une démarche structurée d’amélioration : comprendre les irritants, les traiter avec les clients et les équipes, puis rendre les progrès visibles.",
    done=["Analyse des enquêtes et des retours clients",
          "Identification des irritants et des moments critiques du parcours",
          "Ateliers associant clients et équipes internes",
          "Priorisation des chantiers d’amélioration",
          "Plans d’action, suivi et communication sur les progrès"],
    result="Mesurer ne suffit pas : c’est la boucle entre écoute, action et retour vers les clients qui fait progresser l’expérience vécue.",
    xp="Expérience professionnelle antérieure de la fondatrice, en tant que responsable Expérience Client, avant la création d’Xpansio."),
  dict(slug="realisation-customer-success.html", cls="cl", kind="a",
    title="Comment transformer un client Print en client Print + IT grâce au Customer Success ?",
    ctx="Une base installée importante dans l’impression, mais une relation centrée sur les équipements.",
    ans="Concevoir et expérimenter une approche Customer Success pour développer la valeur des comptes existants.",
    defi="Une entreprise dispose d’une base installée importante dans l’impression, mais peine à développer une relation plus globale avec ses clients et à identifier les opportunités IT. Comment dépasser une relation centrée sur les équipements ?",
    reponse="Concevoir et expérimenter une approche Customer Success : mieux connaître les besoins des clients, mieux les accompagner et faire émerger de nouvelles opportunités.",
    done=["Identification des comptes et segments pertinents",
          "Définition du rôle et des missions des Customer Success Managers",
          "Structuration des interactions avec les équipes commerciales et techniques",
          "Définition des processus de suivi des clients",
          "Expérimentation du dispositif et analyse des enseignements"],
    result="Il s’agissait d’un pilote. Son déploiement généralisé n’a pas été poursuivi, pour des raisons d’organisation et d’investissement. L’enseignement : le Customer Success demande des rôles clairs, une coordination entre équipes et un engagement de l’organisation dans la durée.",
    xp="Expérience professionnelle antérieure de la fondatrice, chez un constructeur international de solutions bureautiques et IT, avant la création d’Xpansio."),
]
R = {r["slug"]: r for r in REAL}
R1, R2, R3, R4 = (r["slug"] for r in REAL)

def rcard(r):
    """Aperçu court d'une réalisation (accueil, page Nos réalisations, pages d'expertise)."""
    c = r["cls"]
    return (f'<a class="pcard rcard {c}" href="{r["slug"]}"><span class="tag {c}">{EXP[c][0]}</span>'
            f'<span class="who">{KIND[r["kind"]]}</span><h3>{r["title"]}</h3><p>{r["ctx"]}</p><p class="ans">{r["ans"]}</p>'
            f'<span class="link {c}">Découvrir la réalisation {ARR}</span></a>')

def rgrid(rs):
    return f'<div class="pgrid{ {1: " n1", 4: " n2"}.get(len(rs), "")}">' + ''.join(rcard(r) for r in rs) + '</div>'

KINDS_NOTE = ('<p class="note"><b>Mission Xpansio</b> : intervention de conseil réalisée par Xpansio. '
              '<b>Expérience antérieure</b> : démarche conduite par Agnès Chabrier dans ses fonctions précédentes, avant la création d’Xpansio.</p>')

def real_page(r):
    c = r["cls"]; exp, href = EXP[c]; ico = I_NET if c == "ch" else I_USER
    done = ''.join(f'<li>{x}</li>' for x in r["done"])
    return f'''
{page_hero([("index.html","Accueil"),("realisations.html","Nos réalisations"),(None, exp)], r["title"], r["ctx"],
  f'<span class="pill {c}"><span class="ico {c}">{ico}</span>{KIND[r["kind"]]} · {exp}</span>', h1cls=" h1-long")}
<section class="band alt">
  <div class="wrap">
    <div class="case-cols">
      <div class="case-col"><span class="label {c}">Le défi</span><p>{r["defi"]}</p></div>
      <div class="case-col"><span class="label {c}">La réponse apportée</span><p>{r["reponse"]}</p></div>
      <div class="case-col"><span class="label {c}">Ce qui a été réalisé</span><ul>{done}</ul></div>
    </div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    <div class="xp {c}"><span class="label {c}">Résultats et enseignements</span><p>{r["result"]}</p>
      <p class="from"><b>L’expérience mobilisée :</b> {r["xp"]}</p></div>
    <div class="below"><a class="link {c}" href="{href}">Voir l’expertise {exp} {ARR}</a></div>
  </div>
</section>
{cta("Vous faites face à une situation comparable ?", "Échangeons sur votre contexte, lors d’un premier échange de 30 minutes sans engagement.", "Échanger sur votre situation")}
'''

REALISATIONS_PAGE = f'''
{page_hero([("index.html","Accueil"),(None,"Nos réalisations")], "Nos réalisations", "Des situations réelles : ce qui a été entrepris, et ce qu’on en retient.")}
<section class="band alt">
  <div class="wrap">
    {rgrid(REAL)}
    {KINDS_NOTE}
  </div>
</section>
{cta("Votre situation pourrait être la prochaine.", "Racontez-nous votre contexte : nous vous dirons comment nous pourrions vous aider.")}
'''

# Accueil : quatre cartes « enjeux », chacune mène à la réalisation qui y répond. Titre au repos, réponse courte au survol (toujours visible sur mobile).
HOME_CASES = [
    ("dialogue", R1, "ch", "Channel Performance", "Vos partenaires sont-ils vraiment engagés ?",
     "Impliquez, accompagnez et valorisez vos partenaires pour construire une relation durable et développer leur engagement."),
    ("salle", R1, "ch", "Channel Performance", "Quelle valeur apportez-vous à vos partenaires ?",
     "Définissez une proposition de valeur réseau différenciante et traduisez-la en un programme partenaires cohérent."),
    ("carnet", R3, "cl", "Customer Performance", "Vos clients sont-ils vraiment satisfaits ?",
     "Écoutez vos clients, impliquez-les dans l’amélioration de leur parcours et transformez leurs irritants en actions concrètes."),
    ("dossier", R2, "cl", "Customer Performance", "Connaissez-vous vraiment la valeur de vos clients ?",
     "Identifiez les risques, les potentiels et les priorités pour fidéliser et développer durablement votre capital client."),
]
def home_collage():
    cards = ''.join(
        f'<a class="ph p{i+1} {c}" href="{h}" style="--i:{i}"><img src="assets/{PHOTOS[k]}" alt="" decoding="async">'
        f'<span class="cap"><span class="ctag {c}">{tag}</span><span class="t">{t}</span>'
        f'<span class="rev"><span class="a">{a}</span><span class="go">Voir la réalisation {ARR}</span></span></span></a>'
        for i, (k, h, c, tag, t, a) in enumerate(HOME_CASES))
    return f'<nav class="stack n4 links cases" aria-label="Quatre enjeux, et les réalisations qui y répondent">{cards}</nav>'
HOME_COLLAGE = home_collage()

# ---------- ACCUEIL ----------
HOME = f'''
<section class="hero">
  <div class="wrap">
    <span class="label">Conseil en performance Channel &amp; Customer · B2B Tech</span>
    <h1 class="h1"><span>Accélérer la performance <em>de vos partenaires.</em></span><span>Révéler la valeur <em>de vos clients.</em></span></h1>
    <p class="lead">Xpansio accompagne les constructeurs, éditeurs, distributeurs et revendeurs IT sur deux leviers de croissance : leurs réseaux de partenaires et leur portefeuille clients.</p>
    <div class="ctas"><a class="btn btn-primary" href="#realisations">Découvrir nos réalisations {ARR}</a><a class="btn btn-ghost" href="contact.html">Échanger sur vos enjeux</a></div>
  </div>
  {HOME_COLLAGE}
</section>

<section class="band alt" id="expertises">
  <div class="wrap">
    {head("Nos expertises", "Deux expertises, deux leviers de croissance.")}
    <div class="duo">
      <a class="xcard ch" href="experience-channel.html">
        <span class="ico ch">{I_NET}</span>
        <span class="label ch">01 — Channel Performance</span>
        <h3>Faites de votre réseau de partenaires un levier de croissance.</h3>
        <p>Développer la performance et l’engagement de vos partenaires, à partir d’une stratégie et d’une proposition de valeur adaptées.</p>
        <p class="for">Pour les <b>constructeurs</b>, <b>éditeurs</b> et <b>distributeurs IT</b>.</p>
        <span class="link">Découvrir l’expertise Channel {ARR}</span>
      </a>
      <a class="xcard cl" href="experience-client.html">
        <span class="ico cl">{I_USER}</span>
        <span class="label cl">02 — Customer Performance</span>
        <h3>Développez la valeur de votre portefeuille clients.</h3>
        <p>Améliorer la satisfaction et la fidélisation de vos clients, tout en développant la valeur de votre portefeuille.</p>
        <p class="for">Pour les <b>revendeurs</b>, <b>intégrateurs</b>, <b>ESN</b> et <b>entreprises B2B</b>.</p>
        <span class="link">Découvrir l’expertise Customer {ARR}</span>
      </a>
    </div>
  </div>
</section>

<section class="band" id="realisations">
  <div class="wrap">
    {head("Nos réalisations", "Ce qui a réellement été entrepris.")}
    {rgrid(REAL)}
    <div class="below"><a class="btn btn-ghost" href="realisations.html">Toutes nos réalisations {ARR}</a></div>
  </div>
</section>

<section class="band alt" id="pourquoi">
  <div class="wrap">
    {head("Pourquoi Xpansio ?", "Une connaissance de toute la chaîne de valeur, du constructeur au client final.")}
    <div class="about">
      <div class="portrait"><img src="assets/agnes.jpg" alt="Portrait d’Agnès Chabrier" width="800" height="800"></div>
      <div class="sign"><b>Agnès Chabrier</b><span>Fondatrice</span></div>
      <div class="bio">
        <p>Plus de 30 ans dans l’écosystème IT et bureautique, chez des distributeurs et des constructeurs internationaux : stratégies Channel, programmes partenaires, expérience client et Customer Success.</p>
        <p>Connaître de l’intérieur les réalités des constructeurs, des distributeurs, des revendeurs et des clients finaux permet d’articuler stratégie et exécution, en tenant compte des contraintes de chacun.</p>
      </div>
    </div>
    <div class="chain-wrap">
      <div class="chain" role="img" aria-label="Chaîne de valeur B2B : Channel Performance couvre éditeurs et constructeurs, distributeurs et revendeurs ; Customer Performance couvre revendeurs et clients finaux.">
        <span class="span ch">Channel Performance</span>
        <span class="track" aria-hidden="true"><i></i><i></i><i></i></span>
        <div class="node"><span class="k">01</span><b>Éditeurs et constructeurs</b><small>Conçoivent les solutions</small></div>
        <div class="node"><span class="k">02</span><b>Distributeurs IT</b><small>Animent le réseau</small></div>
        <div class="node"><span class="k">03</span><b>Revendeurs, intégrateurs et ESN</b><small>Vendent et installent</small></div>
        <div class="node"><span class="k">04</span><b>Clients finaux</b><small>Entreprises utilisatrices</small></div>
        <span class="span cl">Customer Performance</span>
      </div>
      <div class="chain-legend" aria-hidden="true"><span class="label ch">● Channel Performance</span><span class="label cl">● Customer Performance</span></div>
    </div>
  </div>
</section>

<section class="band ink" id="contact"><div class="wrap">
  <div class="head"><span class="label">Prendre contact</span><h2 class="h2">Identifions ensemble vos prochains leviers de croissance.</h2>
    <p class="lead">Échangeons sur vos partenaires, vos clients et les pistes d’amélioration possibles.</p>
  </div>
  <div class="ctas"><a class="btn btn-white" href="contact.html">Prendre rendez-vous {ARR}</a></div>
  <p class="note">Premier échange de 30 minutes, sans engagement.</p>
</div></section>
'''

# ---------- EXPERTISES ----------
CHANNEL = f'''
{page_hero([("index.html","Accueil"),(None,"Channel Performance")], "Channel Performance",
  ["Faire de votre réseau de distribution indirecte un avantage concurrentiel durable.",
   "Pour les constructeurs, éditeurs, distributeurs IT et réseaux de revendeurs B2B."],
  f'<span class="pill ch"><span class="ico ch">{I_NET}</span>Expertise 01</span>', cta_btn="Échangeons sur votre réseau de partenaires")}
<section class="band alt">
  <div class="wrap">
    {head("Vos enjeux", "Le marché change plus vite que les réseaux.", cls="ch")}
    {issues([("L’engagement ne s’achète plus avec des remises","Les partenaires privilégient les fournisseurs qui contribuent réellement à leur croissance et à leur rentabilité."),
             ("Des partenaires référencés, mais pas toujours engagés","Un réseau étendu ne garantit ni son dynamisme ni sa performance : l’enjeu est l’engagement dans la durée."),
             ("De la technologie à la valeur métier","Cloud, cybersécurité, IA : la valeur dépend de la capacité des partenaires à démontrer des bénéfices concrets à leurs clients.")])}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Nos domaines d’intervention", "Quatre domaines, selon la maturité de votre réseau.", cls="ch")}
    {cards([
      (I_MAP,"Stratégie et pilotage du réseau","Diagnostiquer le réseau, fixer le cap, la gouvernance et les indicateurs de performance."),
      (I_LAYERS,"Proposition de valeur et programme partenaires","Clarifier ce que vous apportez à vos partenaires, puis le traduire en niveaux, bénéfices et dispositifs."),
      (I_PATH,"Parcours et engagement des partenaires","Recruter, intégrer, accompagner, rassembler et reconnaître vos partenaires dans la durée."),
      (I_CAP,"Compétences et performance commerciale","Développer les compétences et la vente par la valeur, avec des plans d’action adaptés."),
    ],"ch",4)}
  </div>
</section>
<section class="band alt" id="ppi">
  <div class="wrap">
    {head("Piloter le réseau", "Mesurer la performance du réseau, accompagner chaque partenaire.", "Deux niveaux de pilotage complémentaires, qui ne se remplacent pas.", cls="ch")}
    <div class="vs">
      <div class="vs-col ch"><span class="label ch">Performance globale du réseau</span><p>Chiffre d’affaires, parts de marché, couverture, croissance : où en est le réseau, et où va-t-il ?</p></div>
      <div class="vs-col"><span class="label">Relation avec chaque partenaire</span><p>Le Partner Performance Index (PPI) structure le dialogue avec chaque partenaire : compétences, qualité de service, engagement, pratiques commerciales, capacité d’adaptation. Un outil de progrès, pas un classement.</p></div>
    </div>
    <p class="note">Critères et pondérations sont définis avec vous, selon votre réseau et vos objectifs.</p>
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Réalisation associée", "Ce que cela donne sur le terrain.", cls="ch")}
    {rgrid([R[R1]])}
  </div>
</section>
{cta("Et si votre programme partenaires devenait un avantage concurrentiel ?","Demandez une Executive Partner Review : 90 minutes pour analyser l’alignement de votre programme avec votre stratégie et ses leviers de création de valeur.")}
'''

CLIENT = f'''
{page_hero([("index.html","Accueil"),(None,"Customer Performance")], "Votre capital client est votre premier actif. Encore faut-il en prendre toute la mesure.",
  ["Xpansio vous aide à mieux écouter vos clients, à renforcer leur fidélité et à développer la valeur de votre portefeuille.",
   "Pour les revendeurs, intégrateurs, ESN et entreprises B2B disposant d’une base clients récurrente."],
  f'<span class="pill cl"><span class="ico cl">{I_USER}</span>Expertise 02 · Customer Performance</span>', cta_btn="Échanger sur votre capital client", h1cls=" h1-long")}
<section class="band alt">
  <div class="wrap">
    {head("Vos enjeux", "Écouter, fidéliser, développer : trois enjeux liés.", cls="cl")}
    {issues([("Une expérience client insuffisamment maîtrisée","Les enquêtes ne disent pas toujours ce que vivent réellement les clients, ni quels irritants persistent."),
             ("Une fidélité que l’on mesure trop tard","Un client qui renouvelle n’est pas forcément satisfait. Mieux vaut repérer les signaux de fragilité avant le départ."),
             ("Un potentiel client sous-exploité","La croissance ne repose pas que sur l’acquisition : votre base installée recèle des opportunités de développement.")])}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Nos domaines d’intervention", "Quatre domaines, de l’écoute à la valeur.", cls="cl")}
    {cards([
      (I_CHAT,"Écoute et satisfaction client","Structurer l’écoute, mesurer la satisfaction et comprendre les attentes."),
      (I_PATH,"Parcours et expérience client","Analyser les moments clés, traiter les irritants, construire des plans d’amélioration."),
      (I_SHIELD,"Fidélisation et Customer Success","Accompagner les clients de façon proactive, sécuriser les renouvellements, anticiper les départs."),
      (I_GROW,"Connaissance et développement du capital client","Analyser le portefeuille, identifier les potentiels et orienter les actions de développement."),
    ],"cl",4)}
  </div>
</section>
<section class="band alt" id="cci">
  <div class="wrap">
    {head("Analyse du portefeuille", "Customer Capital Index (CCI)", "Un modèle d’analyse qui croise plusieurs dimensions de la relation client, pour éclairer les priorités et les plans d’action.", cls="cl")}
    <div class="dims n5"><div class="dim">Satisfaction</div><div class="dim">Fidélité</div><div class="dim">Risque</div><div class="dim">Potentiel de développement</div><div class="dim">Contribution économique</div></div>
    <p class="note">Ces dimensions sont des exemples, pas une recette universelle : les critères sont adaptés à vos enjeux, à vos données et à votre modèle économique.</p>
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Réalisations associées", "Ce que cela donne sur le terrain.", cls="cl")}
    {rgrid([R[R2], R[R3], R[R4]])}
  </div>
</section>
{cta("Des clients mieux écoutés. Des relations plus solides. Un capital client qui se développe.","Échangeons sur vos enjeux de satisfaction, de fidélisation et de développement de votre portefeuille clients.","Échanger sur votre capital client")}
'''

# ---------- ANCIENNES ADRESSES ----------
# GitHub Pages ne fait pas de redirection serveur : ces pages minimales renvoient vers la nouvelle adresse (et l'indiquent aux moteurs de recherche).
REDIRECTS = {
    "projets.html": "realisations.html",
    "expertises.html": "index.html#expertises",
    "cas-engagement-partenaires.html": R1,
    "cas-valeur-reseau.html": R1,
    "cas-experience-client.html": R3,
    "cas-valeur-clients.html": R2,
}
def redirect_page(to):
    canon = "https://xpansio.fr/" + ("" if to.startswith("index.html") else to)
    return (f'<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<title>Xpansio</title>\n'
            f'<meta name="robots" content="noindex">\n<link rel="canonical" href="{canon}">\n'
            f'<meta http-equiv="refresh" content="0; url={to}">\n</head>\n<body>\n'
            f'<p>Cette page a été déplacée : <a href="{to}">continuer vers la nouvelle page</a>.</p>\n</body>\n</html>\n')

CONTACT = f'''
{page_hero([("index.html","Accueil"),(None,"Contact")], "Alors, on travaille ensemble ?", "Un premier échange de 30 minutes pour comprendre vos enjeux, sans engagement. Réponse sous 48 heures ouvrées.")}
<section class="band alt">
  <div class="wrap">
    <dl class="coords" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr));max-width:560px">
      <div><dt>Téléphone</dt><dd><a class="btn btn-primary btn-sm" href="tel:+33689894119" aria-label="Appeler Xpansio">Appeler</a></dd></div>
      <div><dt>LinkedIn</dt><dd><a class="btn btn-ghost btn-sm" href="https://www.linkedin.com/in/agnes-chabrier-7186971/" target="_blank" rel="noopener">Voir le profil</a></dd></div>
    </dl>
    <form class="form" action="https://api.web3forms.com/submit" method="POST">
      <input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
      <input type="hidden" name="subject" value="Nouveau message depuis xpansio.fr">
      <input type="hidden" name="from_name" value="Site xpansio.fr">
      <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
      <div class="field full center"><span class="flabel" id="lbl-sujet">Votre sujet</span>
        <div class="topics" role="radiogroup" aria-labelledby="lbl-sujet">
          <input type="radio" name="sujet" id="s-ch" value="Channel Performance"><label for="s-ch">Channel Performance</label>
          <input type="radio" name="sujet" id="s-cl" value="Customer Performance"><label for="s-cl">Customer Performance</label>
          <input type="radio" name="sujet" id="s-au" value="Autre" checked><label for="s-au">Autre</label>
        </div>
      </div>
      <div class="fields">
        <div class="field"><label for="f-nom">Nom et prénom</label><input id="f-nom" name="nom" autocomplete="name" required></div>
        <div class="field"><label for="f-ent">Entreprise</label><input id="f-ent" name="entreprise" autocomplete="organization" required></div>
        <div class="field"><label for="f-mail">Email professionnel</label><input id="f-mail" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="f-tel">Téléphone (facultatif)</label><input id="f-tel" name="telephone" type="tel" autocomplete="tel"></div>
        <div class="field full"><label for="f-msg">Votre message</label><textarea id="f-msg" name="message" required placeholder="Votre activité, votre réseau ou votre base clients, ce que vous aimeriez améliorer…"></textarea></div>
      </div>
      <label class="consent" for="f-ok"><input id="f-ok" type="checkbox" name="consentement" required><span>J’accepte que mes données soient utilisées pour être recontacté(e). Voir les <a href="mentions-legales.html">mentions légales</a>.</span></label>
      <div class="submit"><button class="btn btn-primary" type="submit">Envoyer le message {ARR}</button></div>
      <p class="form-msg" role="status" hidden></p>
    </form>
  </div>
</section>
'''

LEGAL = f'''
{page_hero([("index.html","Accueil"),(None,"Mentions légales")], "Mentions légales", "Informations légales et politique de confidentialité du site xpansio.")}
<section class="band alt">
  <div class="wrap legal">
    <div><h2>Éditeur du site</h2><p>Agnès Chabrier, entrepreneure individuelle, exerçant sous le nom commercial Xpansio.</p><p>Adresse : 6 rue André Sabatier, 92000 Nanterre<br>SIRET : 939 844 700 00012<br>Téléphone : 06 89 89 41 19<br>Contact : via le <a href="contact.html">formulaire de contact</a></p><p>Directrice de la publication : Agnès Chabrier.</p></div>
    <div><h2>Hébergement</h2><p>GitHub, Inc. (service GitHub Pages)<br>88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis<br>github.com</p></div>
    <div><h2>Propriété intellectuelle</h2><p>L’ensemble des contenus de ce site (textes, logo, visuels, méthode Customer Portfolio Performance Framework™) est la propriété d’Xpansio. Toute reproduction sans autorisation est interdite.</p></div>
    <div><h2>Données personnelles</h2><p>Les informations transmises via le formulaire de contact servent uniquement à répondre à votre demande. Elles ne sont ni vendues ni cédées à des tiers, et sont conservées au maximum trois ans après le dernier échange. Les messages du formulaire sont transmis par email via le service Web3Forms.</p><p>Conformément au RGPD, vous disposez d’un droit d’accès, de rectification et de suppression de vos données. Pour l’exercer, écrivez-nous via le <a href="contact.html">formulaire de contact</a>. Vous pouvez aussi adresser une réclamation à la CNIL.</p></div>
    <div><h2>Cookies</h2><p>Ce site ne dépose pas de cookie publicitaire ni de traceur de mesure d’audience.</p></div>
  </div>
</section>
'''

PAGES = [
    ("index.html", "home", "Xpansio", "Xpansio, conseil en performance Channel & Customer pour les constructeurs, éditeurs, distributeurs et revendeurs IT : réseaux de partenaires et valeur du portefeuille clients.", HOME),
    ("experience-channel.html", "channel", "Channel Performance · Xpansio", "Stratégie de réseau, proposition de valeur et programmes partenaires, parcours et engagement des partenaires : l’expertise Channel Performance d’Xpansio.", CHANNEL),
    ("experience-client.html", "client", "Customer Performance · Xpansio", "Écoute et satisfaction, expérience client, fidélisation et Customer Success, développement du capital client : l’expertise Customer Performance d’Xpansio.", CLIENT),
    ("realisations.html", "realisations", "Nos réalisations · Xpansio", "Des situations réelles en Channel et Customer Performance : contexte, démarche, réalisations et enseignements.", REALISATIONS_PAGE),
] + [(r["slug"], "realisations", r["title"] + " · Xpansio", r["ctx"], real_page(r)) for r in REAL] + [
    ("contact.html", "contact", "Contact · Xpansio", "Contacter Xpansio pour un premier échange.", CONTACT),
    ("mentions-legales.html", "legal", "Mentions légales · Xpansio", "Mentions légales du site Xpansio.", LEGAL),
]

if __name__ == "__main__":
    # Site public (publié par GitHub Pages depuis docs/) ; "--artifact" génère aussi un aperçu sans squelette pour Claude.
    outs = [("docs", True)] + ([("artifact", False)] if "--artifact" in sys.argv else [])
    for out, full_home in outs:
        d = os.path.join(ROOT, out)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(os.path.join(d, "assets"))
        shutil.copy(os.path.join(SRC, "styles.css"), d)
        for f in os.listdir(os.path.join(SRC, "assets")):
            shutil.copy(os.path.join(SRC, "assets", f), os.path.join(d, "assets", f))
        for fn, key, title, desc, body in PAGES:
            with open(os.path.join(d, fn), "w") as fh:
                fh.write(page(key, title, desc, body, full_home or fn != "index.html"))
        for fn, to in REDIRECTS.items():
            open(os.path.join(d, fn), "w").write(redirect_page(to))
    d = os.path.join(ROOT, "docs")
    open(os.path.join(d, "CNAME"), "w").write("xpansio.fr\n")
    open(os.path.join(d, ".nojekyll"), "w").write("")
    print("ok")

