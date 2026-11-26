#!/usr/bin/env python3
"""Génère le site Xpansio v3 : dist/ (site à héberger) et artifact/ (accueil sans squelette)."""
import json, os, shutil, sys
import hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import *
import parcours

def parcours_block():
    """Visuel du parcours client (SVG aux couleurs du site), défilable horizontalement sur mobile."""
    return f'''<figure class="parcours">
      <h3 class="subhead">Le parcours vécu par vos clients</h3>
      <p class="parcours-sub">Exemple illustratif : revendeur ou intégrateur IT, de la découverte au renouvellement.</p>
      <p class="swipe">Utilisez les flèches ou faites glisser le schéma pour voir tout le parcours, ou <a href="assets/parcours-client.svg" target="_blank" rel="noopener">ouvrez-le en grand</a>.</p>
      <div class="parcours-view">
        <button class="pc-nav pc-prev" type="button" aria-label="Voir le début du parcours" disabled><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
        <div class="parcours-scroll" tabindex="0" role="region" aria-label="Parcours client, défilable horizontalement">{parcours.svg()}</div>
        <button class="pc-nav pc-next" type="button" aria-label="Voir la suite du parcours"><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
      </div>
      <figcaption>{parcours.LEGEND}</figcaption>
    </figure>'''


SRC = os.path.dirname(os.path.abspath(__file__))
# Version de la feuille de style : change à chaque modification de styles.css, ce qui force les navigateurs à recharger le style.
CSS_V = hashlib.md5(open(os.path.join(SRC, "styles.css"), "rb").read()).hexdigest()[:8]
# Clé publique Web3Forms (formulaire de contact), liée à l'adresse d'Agnès. Elle est faite pour être visible dans la page.
WEB3FORMS_KEY = "98890583-2366-4dbd-afb2-a1896cf89b4d"
ROOT = os.path.dirname(SRC)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Montserrat:wght@400;500;600;700&display=swap">')

NAV = [("index.html", "Accueil", "home"), ("realisations.html", "Réalisations", "realisations"),
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
      <div class="drop-col"><span class="label">Expertises</span>
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
    <p class="identity">Xpansio est un cabinet de conseil indépendant basé en France, spécialisé dans la performance des réseaux de partenaires et du portefeuille clients des constructeurs, éditeurs, distributeurs et revendeurs IT.</p>
    <nav aria-label="Pied de page"><a href="index.html">Accueil</a><a href="experience-channel.html">Channel Performance</a><a href="experience-client.html">Customer Performance</a><a href="realisations.html">Réalisations</a><a href="auto-diagnostic.html">Auto-diagnostic client</a><a href="auto-diagnostic-channel.html">Auto-diagnostic partenaire</a><a href="contact.html">Contact</a><a href="https://www.linkedin.com/in/agnes-chabrier-7186971/" target="_blank" rel="noopener">LinkedIn</a></nav>
    <div class="foot-bottom"><span>© 2026 Xpansio</span><a href="mentions-legales.html">Mentions légales et confidentialité</a></div>
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
  /* Parcours client : flèches et glisser-déposer pour faire défiler le schéma */
  document.querySelectorAll('.parcours-view').forEach(function(v){
    var sc=v.querySelector('.parcours-scroll'),pv=v.querySelector('.pc-prev'),nx=v.querySelector('.pc-next');
    function upd(){var max=sc.scrollWidth-sc.clientWidth;v.classList.toggle('no-scroll',max<4);pv.disabled=sc.scrollLeft<4;nx.disabled=sc.scrollLeft>max-4;}
    function go(d){sc.scrollBy({left:d*sc.clientWidth*.7,behavior:reduce?'auto':'smooth'});}
    pv.addEventListener('click',function(){go(-1);});nx.addEventListener('click',function(){go(1);});
    sc.addEventListener('scroll',upd,{passive:true});window.addEventListener('resize',upd);upd();
    var down=false,x0=0,l0=0;
    sc.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse')return;down=true;x0=e.clientX;l0=sc.scrollLeft;sc.classList.add('drag');});
    window.addEventListener('pointermove',function(e){if(down)sc.scrollLeft=l0-(e.clientX-x0);});
    window.addEventListener('pointerup',function(){down=false;sc.classList.remove('drag');});
  });
  var b=document.querySelector('.menu-btn'),d=document.getElementById('drop');
  function set(o){d.hidden=!o;b.setAttribute('aria-expanded',String(o));}
  if(b&&d){
    b.addEventListener('click',function(e){e.stopPropagation();set(d.hidden);});
    d.addEventListener('click',function(e){e.stopPropagation();});
    document.addEventListener('click',function(){if(!d.hidden)set(false);});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!d.hidden){set(false);b.focus();}});
  }
  var f=document.querySelector('form.form');
  /* Arrivée depuis l'auto-diagnostic (contact.html?sujet=customer-performance) : sujet et message pré-remplis */
  var sujet=(location.search.match(/[?&]sujet=(customer|channel)-performance(&|$)/)||[])[1];
  if(f&&sujet){
    var sc=document.getElementById(sujet==='channel'?'s-ch':'s-cl'),fm=document.getElementById('f-msg');
    if(sc)sc.checked=true;
    if(fm&&!fm.value)fm.value="Je viens de faire l’auto-diagnostic et je souhaite un débrief.";
  }
  /* Sur ordinateur, « Être rappelé » remplace « Appeler » : message pré-rempli, téléphone obligatoire */
  var rp=document.getElementById('rappel');
  if(f&&rp){rp.addEventListener('click',function(e){
    e.preventDefault();var fm=document.getElementById('f-msg'),ft=document.getElementById('f-tel'),fs=document.getElementById('f-subj');
    if(fm&&!fm.value)fm.value="Merci de me rappeler. Mes disponibilités : ";
    if(fs)fs.value="Demande de rappel depuis xpansio.fr";
    ft.required=true;document.getElementById('l-tel').textContent='Téléphone (pour vous rappeler)';
    ft.scrollIntoView({behavior:'smooth',block:'center'});setTimeout(function(){ft.focus({preventScroll:true});},400);
  });}
  if(f){f.addEventListener('submit',function(e){
    e.preventDefault();var msg=f.querySelector('.form-msg');
    var btn=f.querySelector('button[type=submit]');btn.disabled=true;
    fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Accept':'application/json'},body:new FormData(f)})
      .then(function(r){return r.json();}).then(function(j){btn.disabled=false;if(!j.success)throw 0;msg.textContent='Merci, votre message a bien été envoyé. Réponse sous 48 heures ouvrées.';msg.hidden=false;f.reset();})
      .catch(function(){btn.disabled=false;msg.textContent="Le message n’a pas pu être envoyé. Réessayez dans quelques instants, ou contactez-moi via LinkedIn.";msg.hidden=false;});
  });}
})();
</script>'''

SITE = "https://xpansio.fr/"
OG_IMG = {}   # fichier → (image, largeur, hauteur) ; sinon le logo
def og(fn, title, desc):
    """Aperçu des liens partagés (LinkedIn, WhatsApp, Teams…) : titre, description, image du logo."""
    url = SITE + ("" if fn == "index.html" else fn)
    return (f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="Xpansio">\n<meta property="og:locale" content="fr_FR">\n'
            f'<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{SITE}{OG_IMG.get(fn, ("assets/og-image.png",))[0]}">\n<meta property="og:image:width" content="{OG_IMG.get(fn, (0, 1200))[1]}">\n<meta property="og:image:height" content="{OG_IMG.get(fn, (0, 0, 630))[2]}">\n'
            f'<meta name="twitter:card" content="summary_large_image">')

def ver(f):
    """Version d'un fichier : change à chaque modification, ce qui force les navigateurs à le recharger."""
    return hashlib.md5(open(os.path.join(SRC, f), "rb").read()).hexdigest()[:8]

# Feuilles de style et scripts propres à certaines pages
PAGE_CSS = {"autodiag": ["autodiag.css"], "autodiag-ch": ["autodiag.css"]}
PAGE_JS = {"autodiag": ["autodiag.js"], "autodiag-ch": ["autodiag-channel.js"]}

# Fiche d'identité lisible par les moteurs de recherche et les IA (invisible à l'écran).
# Ni email ni téléphone, conformément aux règles du site.
IDENTITE = ("Xpansio est un cabinet de conseil indépendant basé en France, spécialisé dans la performance des réseaux de partenaires "
            "(Channel) et du portefeuille clients des constructeurs, éditeurs, distributeurs et revendeurs IT.")
LD_ORG = {
  "@context": "https://schema.org", "@type": "ProfessionalService", "@id": SITE + "#xpansio",
  "name": "Xpansio", "url": SITE, "logo": SITE + "assets/logo.png", "image": SITE + "assets/og-image.png",
  "description": IDENTITE,
  "slogan": "Accélérer la performance de vos partenaires. Révéler la valeur de vos clients.",
  "address": {"@type": "PostalAddress", "addressLocality": "Nanterre", "postalCode": "92000", "addressCountry": "FR"},
  "areaServed": {"@type": "Country", "name": "France"},
  "knowsLanguage": ["fr", "en"],
  "knowsAbout": ["Programme partenaires", "Refonte de programme partenaires", "Stratégie de distribution indirecte", "Channel management",
                 "Engagement des partenaires", "Parcours partenaire", "Performance des réseaux de revendeurs", "Partner Performance Index",
                 "Expérience client B2B", "Customer Success", "Fidélisation client"],
  "founder": {"@type": "Person", "name": "Agnès Chabrier", "jobTitle": "Fondatrice, consultante Channel et Customer Performance",
              "url": SITE, "knowsLanguage": ["fr", "en"], "sameAs": ["https://www.linkedin.com/in/agnes-chabrier-7186971/"]},
  "sameAs": ["https://www.linkedin.com/in/agnes-chabrier-7186971/"],
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Missions de conseil", "itemListElement": [
    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": SITE + u}} for n, u in [
      ("Refonte de programme partenaires", "programme-partenaires.html"),
      ("Parcours partenaires", "experience-channel.html#comment-je-travaille"),
      ("Audit de performance du réseau de partenaires", "experience-channel.html#comment-je-travaille"),
      ("Enquête de satisfaction client", "experience-client.html#comment-je-travaille"),
      ("Parcours client", "experience-client.html#comment-je-travaille"),
      ("Segmentation du portefeuille clients", "experience-client.html#comment-je-travaille"),
      ("Mise en place du Customer Success", "experience-client.html#comment-je-travaille")]]},
}
EXTRA_LD = {}   # fichier → données structurées supplémentaires (ex. FAQ)
def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'

def page(key, title, desc, body, full=True, fn="index.html"):
    extra_css = ''.join(f'\n<link rel="stylesheet" href="{f}?v={ver(f)}">' for f in PAGE_CSS.get(key, []))
    extra_js = ''.join(f'\n<script src="{f}?v={ver(f)}"></script>' for f in PAGE_JS.get(key, []))
    head = (f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{desc}">\n<link rel="canonical" href="{SITE}{"" if fn == "index.html" else fn}">\n{og(fn, title, desc)}\n{FONTS}\n<link rel="stylesheet" href="styles.css?v={CSS_V}">{extra_css}\n<link rel="icon" href="assets/favicon.png">'
            f'\n{ld(LD_ORG)}' + ''.join('\n' + ld(x) for x in EXTRA_LD.get(fn, [])))
    inner = f'{header(key)}\n<main>\n{body}\n</main>\n{FOOTER}\n{SCRIPT}{extra_js}'
    if not full:
        return head + '\n' + inner
    return (f'<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}\n</head>\n<body>\n{inner}\n</body>\n</html>\n')

def head(label, title, lead=None, cls=""):
    l = f'<p class="lead">{lead}</p>' if lead else ''
    return f'<div class="head"><span class="label {cls}">{label}</span><h2 class="h2">{title}</h2>{l}</div>'

CTA_T = "Échangeons sur vos enjeux"
CTA_P = "Vous souhaitez faire évoluer votre stratégie Channel, renforcer l’engagement de vos partenaires ou développer la valeur de votre portefeuille clients ? Échangeons sur vos priorités et les pistes d’amélioration possibles."
CTA_NOTE = "Premier échange de 30 minutes, sans engagement."
def cta():
    """Appel à l'action unique, identique sur toutes les pages."""
    return f'''<section class="band ink"><div class="wrap">
  {head("Contact", CTA_T, CTA_P)}
  <div class="ctas"><a class="btn btn-white" href="contact.html">Prendre rendez-vous {ARR}</a></div>
  <p class="note">{CTA_NOTE}</p>
</div></section>'''

def page_hero(crumbs, title, lead, extra="", cta_btn=None, tiles="", h1cls="", cta2=None):
    cr = '<span>/</span>'.join(f'<a href="{h}">{t}</a>' if h else f'<span>{t}</span>' for h, t in crumbs)
    return f'''<section class="page-hero{' has-stack' if tiles else ''}"><div class="wrap">
  <nav class="crumbs" aria-label="Fil d’Ariane">{cr}</nav>
  {extra}
  <h1 class="h1{h1cls}">{title}</h1>
  {''.join(f'<p class="lead">{x}</p>' for x in (lead if isinstance(lead, list) else [lead]))}
  {f'<div class="ctas"><a class="btn btn-primary" href="contact.html">{cta_btn} {ARR}</a>' + (f'<a class="btn btn-ghost" href="{cta2[1]}">{cta2[0]}</a>' if cta2 else '') + '</div>' if cta_btn else ''}
</div>{tiles}</section>'''

def issues(items):
    return f'<div class="issues{" n4" if len(items) == 4 else ""}">' + ''.join(
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
    "analyse": "photo-analyse.jpg",        # stylo pointé sur un rapport chiffré
    "casque": "photo-casque.jpg",          # conseillère avec casque, en échange avec un client
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
  dict(slug="realisation-programme-partenaires.html", cls="ch", kind="x",
    title="Comment construire un programme partenaires qui crée de la valeur dans la durée ?",
    ctx="Un programme partenaires ancien et un marché en pleine mutation : il fallait donner au réseau un nouvel élan.",
    ans="Partir du vécu des partenaires, définir une stratégie de réseau, puis un programme dont chaque élément sert la même proposition de valeur.",
    defi="Sur un marché mature, un réseau de distribution a besoin d’autre chose que de niveaux et de remises. Comment lui redonner du sens, et apporter aux partenaires une valeur concrète qui les aide à progresser et à développer leur activité dans la durée ?",
    reponse="Écouter les partenaires et les équipes sur tout le parcours partenaire, définir avec la direction une stratégie de réseau, puis un programme fondé sur le service, la durabilité et le travail ensemble, avec un nom et une vidéo qui en expliquent le sens.",
    done=["Cartographie du parcours partenaire avec la direction et les équipes",
          "Entretiens avec une dizaine de partenaires, dont six sur site : vécu du parcours, irritants, moments réussis, comparaison avec la concurrence",
          "Enquête de satisfaction à chaque point de contact, et même démarche auprès des responsables régionaux",
          "Atelier d’amélioration avec les équipes, puis stratégie de réseau et de programme avec la direction",
          "Nouveaux niveaux et critères de progression au-delà du chiffre d’affaires : services, plan de développement, certifications, engagements RSE"],
    briques=["Une <b>proposition de valeur réseau</b>, socle de tout le programme. <a class=\"link ch\" href=\"realisation-valeur-marque.html\">Voir la réalisation</a>",
             "Un <b>nom et une vidéo</b> qui expriment le sens du programme : se rencontrer, s’engager et progresser ensemble.",
             "Une <b>certification qualité de service</b> qui valorise les meilleurs partenaires. <a class=\"link ch\" href=\"realisation-certification-qualite-service.html\">Voir la réalisation</a>",
             "Un <b>score RSE des partenaires</b>, construit avec la responsable RSE : charte, brochure, et visite d’usine pour montrer l’exigence de qualité des produits d’origine.",
             "Des <b>clubs de dirigeants et des communautés</b> pour dialoguer avec la direction et entre partenaires. <a class=\"link ch\" href=\"realisation-clubs-partenaires.html\">Voir la réalisation</a>",
             "Une <b>tournée nationale de rencontres</b> en région, construite sur les réussites des partenaires eux-mêmes.",
             "Des <b>pilotes co-construits</b> avec des partenaires sur le terrain, autour des solutions et des services.",
             "Un <b>catalogue d’actions marketing cofinancées</b> pour les principaux partenaires, présenté sur le terrain, avec enquêtes de satisfaction et premiers témoignages clients."],
    res_intro="Le programme vient d’être lancé. Les premiers signaux sont positifs :",
    resultats=["les avenants du nouveau programme sont signés et l’accueil du réseau est positif ;",
               "les rencontres en région ont reçu des retours très positifs, grâce à des contenus utiles et à la participation des partenaires ;",
               "les premiers effets sont visibles sur les revenus récurrents liés aux contrats de service, au cœur de la rentabilité durable du réseau."],
    rlabel="L’enseignement",
    result="Un programme partenaires n’est pas une grille de remises : il traduit une stratégie de réseau. Quand chaque élément, des niveaux aux certifications, des communautés aux rencontres, sert la même proposition de valeur, le programme prend du sens pour les partenaires.",
    xp="Mission de conseil Xpansio auprès d’un constructeur. Le client n’est pas nommé, par confidentialité."),
  dict(slug="realisation-valeur-marque.html", cls="ch", kind="x",
    title="Comment redonner de la valeur à une marque lorsque les discussions se concentrent sur le prix ?",
    ctx="Un constructeur sur un marché mature, des offres premium mais de plus en plus difficiles à différencier et une forte pression sur les prix.",
    ans="Définir une proposition de valeur réseau différenciante, donner aux équipes les moyens de la défendre et aligner les dispositifs.",
    defi="Aux yeux des partenaires, les offres semblent de plus en plus comparables, et les discussions commerciales se concentrent sur le prix. Comment construire une proposition de valeur différenciante, crédible et défendable, puis faire en sorte qu’elle guide réellement la relation avec les partenaires ?",
    reponse="La mission s’est concentrée sur la proposition de valeur destinée aux partenaires : les écouter, ainsi que les équipes internes, définir une proposition spécifique au réseau, donner aux commerciaux les preuves pour la défendre, puis en faire le principe directeur des dispositifs de la relation partenaires.",
    vs=("Deux propositions de valeur, deux publics à convaincre",
        "Dans la distribution indirecte, la valeur d’une offre pour le client final ne suffit pas à convaincre un partenaire de développer la marque. Les deux propositions se travaillent distinctement, tout en restant cohérentes.",
        "Pour le partenaire", "Pourquoi investir dans cette relation plutôt qu’une autre ? Elle motive son engagement : rentabilité, développement, accompagnement, compétences.",
        "Pour le client final", "Pourquoi choisir cette solution plutôt qu’une autre ? Elle permet au partenaire de convaincre ses clients : besoins métiers, performance, coût, service."),
    done=["Consultation des partenaires, des équipes internes et des responsables du réseau : attentes, critères de choix, conditions de création de valeur",
          "Définition d’une proposition de valeur réseau pertinente, différenciante, crédible et cohérente avec le positionnement du constructeur",
          "Analyses, données chiffrées et argumentaires pour permettre aux équipes commerciales de défendre la valeur plutôt que le prix",
          "Alignement des dispositifs : accompagnement, formation et compétences, outils d’aide à la vente, reconnaissance et valorisation",
          "Alignement des orientations du réseau, des objectifs et outils contractuels, et des initiatives de dialogue avec les partenaires"],
    res_intro="Il est encore tôt pour mesurer l’impact chiffré dans la durée, et les données restent confidentielles. Les premiers effets sont déjà visibles :",
    resultats=["des équipes commerciales plus sereines, qui consacrent leur temps au développement du business et à l’accompagnement des partenaires plutôt qu’à la négociation sur les prix ;",
               "des partenaires plus sûrs de la valeur de leur offre face à leurs propres clients ;",
               "un impact positif constaté sur les ventes de produits de la marque."],
    rlabel="L’enseignement",
    result="Une proposition de valeur différenciante n’a d’impact que lorsqu’elle est comprise, démontrée et incarnée par toute l’organisation. Définir la promesse est une première étape : donner aux équipes les moyens de la défendre et aligner les dispositifs sur cette promesse constitue le véritable travail de transformation.",
    xp="Mission de conseil Xpansio auprès d’un constructeur. Le client n’est pas nommé, par confidentialité."),
  dict(slug="realisation-clubs-partenaires.html", cls="ch", kind="x",
    title="Comment rétablir la confiance d’un réseau de partenaires fragilisé ?",
    ctx="Après une période de changements, l’implication des partenaires devait être relancée.",
    ans="Créer et animer des clubs partenaires : un dialogue régulier, des experts, une implication dans la vie du réseau.",
    defi="Un réseau ne peut pas reposer uniquement sur une relation commerciale descendante : les partenaires ont besoin de partager leurs enjeux, de faire entendre leurs attentes, d’accéder à des expertises utiles et de participer à l’évolution du réseau.",
    reponse="Créer et animer des clubs partenaires, clubs technologiques d’expertise et clubs de dirigeants plus stratégiques, pour instaurer un dialogue régulier, faire émerger des réflexions communes et renforcer l’implication des partenaires. Une charte a été élaborée avec eux, l’accès au management de haut niveau facilité, et l’accompagnement renforcé en parallèle.",
    done=["Définition des objectifs et du positionnement des clubs",
          "Sélection des thématiques et des participants",
          "Préparation et animation des réunions, avec l’intervention d’experts sur les sujets identifiés",
          "Recueil des attentes et des contributions des partenaires",
          "Enquête de satisfaction après chaque réunion, exploitée pour préparer les rencontres suivantes"],
    res_html=('<div class="res-lead"><div class="case-kpis"><div class="kpi"><div class="v">100&nbsp;%</div><div class="l">des participants très satisfaits</div></div></div>'
              '<p>Lors de la dernière réunion du club des dirigeants, qui réunit les 15 partenaires les plus moteurs et les plus influents du réseau, après une période de changements : <b>100&nbsp;%</b> des participants se sont déclarés très satisfaits dans l’enquête menée à l’issue de la réunion.</p></div>'
              '<p>Les participants soulignent en particulier l’utilité stratégique des échanges, l’accès à des experts et le dialogue direct avec le constructeur.</p>'
              '<h3 class="res-sub">Ce que disent les partenaires du dispositif mis en place</h3>'
              '<blockquote class="pquote ch"><p>« Ces moments-là sont bien plus qu’une réunion. C’est un rappel qu’avoir rejoint la dynamique de ce fournisseur, c’était le bon choix. »</p><span class="by">— Dirigeant d’un partenaire Silver du réseau, Occitanie</span></blockquote>'
              '<blockquote class="pquote ch"><p>« Merci aux équipes de notre fournisseur pour leur accueil, leur disponibilité et la qualité des échanges. »</p><span class="by">— Partenaire Silver, Île-de-France</span></blockquote>'
              '<blockquote class="pquote ch"><p>« Ce trophée nous donne encore plus envie d’aller chercher le suivant. »</p><span class="by">— Partenaire Gold récompensé lors des trophées du réseau, Rhône-Alpes</span></blockquote>'),
    rlabel="L’enseignement",
    result="Un club partenaires n’est pas un simple événement relationnel, mais un dispositif de dialogue, d’écoute et de coconstruction qui aide le constructeur à mieux comprendre son réseau, et les partenaires à contribuer à son évolution.",
    xp="Mission de conseil Xpansio. Le client n’est pas nommé, par confidentialité."),
  dict(slug="realisation-certification-qualite-service.html", cls="ch", kind="x",
    title="La qualité de service de vos partenaires est-elle à la hauteur de votre marque ?",
    ctx="Un constructeur IT dont l’offre est vendue et maintenue par un réseau de partenaires.",
    ans="Concevoir un programme de certification qui fait progresser le réseau et valorise les meilleurs partenaires auprès de leurs clients.",
    # Rubriques propres à cette fiche (texte fourni par Agnès, repris tel quel)
    cols=[("Le contexte", "<p>Pour le client final, la qualité du service rendu par le partenaire, c’est la qualité de la marque. Or le constructeur n’avait pas de vision objective et comparable de la qualité de service de ses partenaires.</p>"),
          ("L’enjeu", "<p>Mesurer cette qualité de façon juste et partagée, repérer les bonnes pratiques, aider chaque partenaire à progresser, et adapter l’accompagnement du constructeur au niveau de chacun.</p>"),
          ("L’approche", "<ul><li>Conception d’une grille d’audit sur 7 domaines : support client, compétences et certifications, outils et supervision, déploiement et logistique, coopération, connaissance de la base installée, RSE.</li>"
                          "<li>Conception de la méthode de notation : score par domaine et score global, comparés à la moyenne du réseau.</li>"
                          "<li>Conception d’un programme de certification à 3 niveaux, que le partenaire peut utiliser dans sa communication.</li>"
                          "<li>Conception du rapport d’audit type, avec un plan d’action personnalisé construit avec chaque partenaire.</li>"
                          "<li>Mise à disposition de ces outils aux équipes techniques du constructeur, chargées de réaliser les audits sur le terrain.</li></ul>")],
    livrables=["La grille de notation et sa méthode.",
               "Le modèle de rapport d’audit : synthèse, analyse par domaine, recommandations, plan d’action.",
               "Le certificat et les outils de visibilité commerciale.",
               "Une vision consolidée du réseau, pour piloter l’accompagnement."],
    figure=("assets/audit-qualite-services.webp", 1600, 860,
            "Exemple de synthèse d’audit qualité de services d’un partenaire : score par domaine comparé au réseau, radar de maturité et certification. Données fictives.",
            "Exemple de livrable, données fictives."),
    resultats=["75 partenaires audités par les équipes techniques du constructeur dès la première année, à partir de la grille et de la méthode conçues pendant la mission.",
               "Une certification reçue comme une vraie reconnaissance par les partenaires :<blockquote class=\"pquote ch\"><p>« Nous sommes fiers de concrétiser notre partenariat avec notre fournisseur par la remise de notre certificat officiel. Cette distinction vient récompenser la constance de notre engagement mutuel. »</p><span class=\"by\">— Dirigeant d’un intégrateur IT, partenaire Silver, Île-de-France</span></blockquote>",
               "Des axes de progrès clairs et partagés, notamment sur la supervision à distance et la connaissance de la base installée : des leviers directs de satisfaction pour les clients finaux."],
    rlabel="Ce qu’il faut retenir",
    result="Un audit n’est utile que s’il fait progresser. Comparer chaque partenaire au réseau, reconnaître les meilleurs et construire un plan d’action avec chacun transforme un contrôle en levier d’engagement. Et la qualité de service des partenaires devient un argument commercial, pour eux comme pour la marque.",
    xp="Mission de conseil Xpansio auprès d’un constructeur. Le client n’est pas nommé, par confidentialité.",
    og_image=("assets/og-audit-qualite-services.jpg", 1200, 645)),
  dict(slug="realisation-crise-clients-prioritaires.html", cls="cl", kind="a",
    title="Comment préserver la satisfaction client lorsque la crise impose des arbitrages ?",
    ctx="Une crise d’approvisionnement majeure : l’entreprise ne peut plus répondre normalement à toutes les demandes.",
    ans="Mieux connaître le portefeuille pour identifier les clients prioritaires et orienter la fidélisation.",
    defi="Une crise majeure d’approvisionnement dégrade la qualité de service et la satisfaction des clients. Comment préserver les relations stratégiques lorsque les ressources sont contraintes et qu’il faut arbitrer ?",
    reponse="Améliorer la connaissance du portefeuille clients pour identifier les situations prioritaires, en combinant plusieurs dimensions de la valeur client au-delà du seul chiffre d’affaires. Prioriser ne signifie pas abandonner : engagements contractuels, équité et besoins critiques restent pris en compte.",
    done=["Analyse du portefeuille clients",
          "Définition de critères de valeur stratégique adaptés au contexte : économiques, relationnels, fidélité",
          "Conception d’une segmentation des clients prioritaires",
          "Proposition de modalités d’accompagnement différenciées",
          "Identification des conditions nécessaires à la mise en œuvre"],
    result="La démarche et la segmentation ont été conçues. Les clients les plus importants ont été identifiés dans les outils pour une prise en charge dédiée.",
    xp="Expérience professionnelle antérieure de la fondatrice, chez un constructeur international de solutions bureautiques et IT, avant la création d’Xpansio."),
  dict(slug="realisation-au-dela-du-nps.html", cls="cl", kind="a", boucle=True,
    title="Et si mesurer le NPS ne suffisait plus à fidéliser les clients ?",
    ctx="Des mesures de satisfaction existent, mais elles n’expliquent pas l’insatisfaction et ne déclenchent pas d’améliorations.",
    ans="Passer de la mesure à une démarche structurée d’amélioration de l’expérience client.",
    defi="Les causes profondes de l’insatisfaction restent mal identifiées, et l’écoute ne se traduit pas en améliorations concrètes. Comment transformer l’écoute client en actions qui améliorent réellement l’expérience ?",
    reponse="Passer d’une logique de mesure à une démarche structurée d’amélioration : comprendre les irritants, les traiter avec les clients et les équipes, puis rendre les progrès visibles.",
    done=["Analyse des enquêtes et des retours clients",
          "Identification des irritants et des moments critiques du parcours",
          "Ateliers associant clients et équipes internes",
          "Priorisation des chantiers d’amélioration",
          "Plans d’action, suivi et communication sur les progrès"],
    result="Mesurer ne suffit pas : c’est la boucle entre écoute, action et retour vers les clients qui fait progresser l’expérience vécue.",
    xp="Expérience professionnelle antérieure de la fondatrice, en tant que responsable Expérience Client, avant la création d’Xpansio."),
  dict(slug="realisation-customer-success.html", cls="cl", kind="a",
    title="Comment élargir la relation client au-delà du métier historique grâce au Customer Success ?",
    ctx="Une base installée importante dans l’impression, une offre IT à développer, mais une relation centrée sur les équipements.",
    ans="Concevoir et expérimenter une approche Customer Success pour développer la valeur des comptes existants.",
    defi="L’entreprise propose aussi des services IT, mais la relation avec ses clients reste centrée sur l’impression : leurs besoins IT sont mal connus et les opportunités échappent aux équipes. Comment élargir la relation au-delà du métier historique ?",
    vs_label="Et pour vous ?",
    vs=("La même question chez un revendeur ou une ESN",
        "Dès que la relation repose sur un métier historique, la démarche est la même : choisir les comptes à potentiel, définir le rôle du Customer Success, organiser le lien avec les commerciaux et les techniciens.",
        "Revendeur bureautique", "Votre parc de copieurs et vos contrats de maintenance vous donnent un accès régulier à vos clients. Comment en faire le point de départ d’une offre IT : postes de travail, réseau, cybersécurité, cloud ?",
        "ESN ou intégrateur", "Vos contrats d’infogérance, de maintenance ou de licences installent la relation. Comment proposer à ces mêmes clients la cybersécurité, le cloud ou les services managés qu’ils achètent aujourd’hui ailleurs ?"),
    reponse="Concevoir et expérimenter une approche Customer Success : mieux connaître les besoins des clients, mieux les accompagner et faire émerger de nouvelles opportunités.",
    done=["Identification des comptes et segments pertinents",
          "Définition du rôle et des missions des Customer Success Managers",
          "Structuration des interactions avec les équipes commerciales et techniques",
          "Définition des processus de suivi des clients",
          "Expérimentation du dispositif et analyse des enseignements"],
    result="Il s’agissait d’un pilote. Son déploiement n’a pas été généralisé pour des raisons d’organisation, mais des équipes dédiées ont été maintenues, dans le même esprit, pour développer les services IT. L’enseignement : le Customer Success demande des rôles clairs, une coordination entre équipes et un engagement de l’organisation dans la durée.",
    xp="Expérience professionnelle antérieure de la fondatrice, chez un constructeur international de solutions bureautiques et IT, avant la création d’Xpansio."),
]
R = {r["slug"]: r for r in REAL}
OG_IMG.update({r["slug"]: r["og_image"] for r in REAL if "og_image" in r})
R0, R1, R5, R6, R2, R3, R4 = (r["slug"] for r in REAL)
PARENT_CH = {R1, R5, R6}   # réalisations qui sont des éléments du programme partenaires (R0)

def rcard(r):
    """Aperçu court d'une réalisation (accueil, page Réalisations, pages d'expertise)."""
    c = r["cls"]
    return (f'<a class="pcard rcard {c}" href="{r["slug"]}"><span class="tag {c}">{EXP[c][0]}</span>'
            f'<span class="who">{KIND[r["kind"]]}</span><h3>{r["title"]}</h3><p>{r["ctx"]}</p><p class="ans">{r["ans"]}</p>'
            f'<span class="link {c}">Découvrir la réalisation {ARR}</span></a>')

def rgrid(rs):
    return f'<div class="pgrid{ {1: " n1", 2: " n2", 4: " n2", 5: " n2", 6: " n2"}.get(len(rs), "")}">' + ''.join(rcard(r) for r in rs) + '</div>'

KINDS_NOTE = ('<p class="note"><b>Mission Xpansio</b> : intervention de conseil réalisée par Xpansio. '
              '<b>Expérience antérieure</b> : démarche conduite par Agnès Chabrier dans ses fonctions précédentes, avant la création d’Xpansio.</p>')

# Fiches qui renvoient vers l'auto-diagnostic, et la ligne ajoutée en fin de fiche
AUTODIAG_FICHES = {"realisation-au-dela-du-nps.html", "realisation-crise-clients-prioritaires.html", "realisation-customer-success.html"}
PARENT_LINE = f'<p class="autodiag-line">Cette démarche est l’un des éléments de la refonte d’un programme partenaires. <a class="link ch" href="realisation-programme-partenaires.html">Voir la démarche d’ensemble {ARR}</a></p>'
AUTODIAG_LINE = f'<p class="autodiag-line">Et vos clients, êtes-vous certain qu’ils vont renouveler ? <a class="link cl" href="auto-diagnostic.html">Faire l’auto-diagnostic {ARR}</a></p>'

# Fiche NPS : la boucle d'amélioration continue (étapes de « Ce qui a été réalisé »)
BOUCLE_NPS = (head("La démarche", "Une boucle d’amélioration continue", cls="cl")
  + loop([("Écouter","Enquêtes de satisfaction et retours clients."),
          ("Comprendre","Irritants et moments critiques du parcours."),
          ("Co-construire","Ateliers avec les clients et les équipes."),
          ("Agir","Chantiers prioritaires, plans d’action et suivi."),
          ("Informer","Communiquer les progrès aux clients.")],
         "cl n5", "Boucle d’amélioration continue en cinq étapes : écouter, comprendre, co-construire, agir, informer, puis recommencer")
  + '<div class="boucle-gap"></div>')

# « Comment je travaille » : offres par expertise (textes validés par Agnès)
def offres(cls, intro, items):
    cards = ''.join(
        f'<article class="wk {cls}"><span class="wk-d">{d}</span><h3>{t}</h3>'
        f'<div class="wk-s"><span class="label {cls}">Ce que je fais</span><p>{faire}</p></div>'
        f'<div class="wk-s"><span class="label {cls}">Livrables</span><p>{livr}</p></div></article>'
        for t, faire, livr, d in items)
    return (f'<section class="band alt" id="comment-je-travaille"><div class="wrap">'
            + head("Comment je travaille", "Des missions claires, avec des livrables concrets.", intro, cls=cls)
            + f'<div class="wks n{len(items)}">{cards}</div></div></section>')

OFFRES_CH = offres("ch", "Chaque mission peut être menée seule. Le parcours partenaires et l’audit de performance sont souvent la première étape d’une refonte du programme.", [
  ("Parcours partenaires",
   "Atelier avec la direction commerciale sur les étapes du cycle partenaire et les points de contact. Entretiens approfondis avec une dizaine de partenaires et vos commerciaux, et enquête de satisfaction auprès du réseau.",
   "Cartographie du parcours avec irritants et moments réussis, analyse et préconisations.", "3 à 4 semaines"),
  ("Audit de performance du réseau",
   "Analyse des chiffres réels de l’ensemble de vos partenaires : chiffre d’affaires, marge et volumes, formation des équipes, engagement (participation aux événements, utilisation des budgets coop et des outils). Six axes, avec des indicateurs adaptés à votre entreprise : business, compétences, engagement, adoption et transformation, poids, concurrence. Maturité du réseau et couverture territoriale. L’auto-diagnostic partenaire en donne une illustration simplifiée.",
   "Score de performance par axe, points de progrès, analyse complète.", "4 semaines"),
  ("Programme partenaires",
   "Atelier avec la direction (enjeux, objectifs, stratégie). Analyse des ventes, du programme et du contrat actuels, des outils et de la formation. Entretiens avec vos équipes et vos partenaires, en intégrant le parcours partenaires s’il n’a pas encore été réalisé. Puis adaptation du programme existant, ou nouvelle proposition de valeur et nouveau programme : niveaux, devoirs et bénéfices, accréditations et certifications.",
   "Raison d’être et proposition de valeur, programme complet, éléments de communication, guides et outils.", "Environ 6 mois selon la taille du réseau"),
])

OFFRES_CL = offres("cl", "Chaque mission peut être menée seule. L’enquête mesure la satisfaction de l’ensemble de vos clients ; le parcours client en explique les causes, avec certains d’entre eux. La segmentation repère ensuite les clients à risque et ceux à potentiel : elle aide à prioriser les chantiers d’amélioration et à choisir les clients pour lesquels mettre en place une démarche de Customer Success.", [
  ("Enquête de satisfaction client",
   "Questionnaire envoyé à l’ensemble de vos clients, construit avec vos équipes à partir de vos points de contact. Paramétrage, envoi et relances, analyse des réponses.",
   "Niveau de satisfaction par point de contact et par type de client, irritants les plus cités, 3 à 5 actions rapides, restitution à la direction.", "3 à 4 semaines"),
  ("Parcours client",
   "Atelier avec la direction sur le cycle client et les points de contact. Ateliers associant des clients représentatifs et vos équipes (régionaux ou nationaux), pour comprendre, étape par étape, d’où viennent les irritants. Si une enquête a été réalisée, ses résultats servent de point de départ.",
   "Cartographie du parcours avec irritants et moments réussis, préconisations, document d’analyse complet.", "4 à 6 semaines"),
  ("Segmentation du portefeuille clients",
   "Étude de vos clients selon plusieurs dimensions (satisfaction, fidélité, risque, potentiel, contribution), avec la méthode du Customer Capital Index.",
   "Vos clients à risque et à potentiel, le chiffre d’affaires en jeu, l’impact des irritants du parcours client, priorités et recommandations par groupe.", "3 à 4 semaines"),
  ("Mise en place du Customer Success",
   "Souvent après la segmentation, qui identifie les clients à potentiel. Atelier avec la direction générale et commerciale sur les objectifs. Choix des clients concernés et des ressources de Customer Success Managers (internes ou externes). Méthode de suivi et indicateurs adaptés à vos outils ; plan de commissionnement des CSM avec la direction des ressources humaines ; équipes trio ventes, support et administration ; outils de plan de compte, health score et revues d’affaires.",
   "Démarche Customer Success complète : clients concernés, rôles, processus, indicateurs, outils, plan de commissionnement. Pilote accompagné.", "6 mois de préparation, puis 6 mois de pilote avant extension"),
  ("Coordination des chantiers d’amélioration",
   "Pilotage des chantiers issus du parcours client, avec vos équipes : priorités, plans d’action, suivi et communication des progrès aux clients.",
   "Plan de chantiers, tableau de suivi, points d’étape.", "Selon le nombre de chantiers"),
])

def vs_block(r):
    """Encadré facultatif : deux colonnes comparées (ex. valeur pour le partenaire / pour le client final)."""
    if "vs" not in r: return ""
    t, lead, a, pa, b, pb = r["vs"]; c = r["cls"]
    return f'''{head(r.get("vs_label", "Le principe"), t, lead, cls=c)}
    <div class="vs" style="margin:0 auto clamp(56px,7vw,80px)"><div class="vs-col {c}"><span class="label {c}">{a}</span><p>{pa}</p></div><div class="vs-col"><span class="label">{b}</span><p>{pb}</p></div></div>'''

def real_page(r):
    c = r["cls"]; exp, href = EXP[c]; ico = I_NET if c == "ch" else I_USER
    if "cols" in r:
        cols = ''.join(f'<div class="case-col"><span class="label {c}">{t}</span>{h}</div>' for t, h in r["cols"])
    else:
        done = ''.join(f'<li>{x}</li>' for x in r["done"])
        cols = (f'<div class="case-col"><span class="label {c}">Le défi</span><p>{r["defi"]}</p></div>'
                f'<div class="case-col"><span class="label {c}">La réponse apportée</span><p>{r["reponse"]}</p></div>'
                f'<div class="case-col"><span class="label {c}">Ce qui a été réalisé</span><ul>{done}</ul></div>')
    extra = ""
    if "livrables" in r:
        extra += f'<div class="deliv-box"><span class="label {c}">Les livrables</span><ul>' + ''.join(f'<li>{x}</li>' for x in r["livrables"]) + '</ul></div>'
    if "figure" in r:
        src, w, h, alt, cap = r["figure"]
        extra += f'<figure class="shot"><img src="{src}" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async"><figcaption>{cap}</figcaption></figure>'
    if "briques" in r:
        extra += f'<div class="deliv-box"><span class="label {c}">Les éléments du programme</span><ul>' + ''.join(f'<li>{x}</li>' for x in r["briques"]) + '</ul></div>'
    res = ""
    if any(k in r for k in ("resultats", "res_html")):
        res = (f'<div class="results"><span class="label {c}">Les résultats</span>'
               + (f'<p>{r["res_intro"]}</p>' if "res_intro" in r else "")
               + ('<ul>' + ''.join(f'<li>{x}</li>' for x in r["resultats"]) + '</ul>' if "resultats" in r else "")
               + r.get("res_html", "") + '</div>')
    return f'''
{page_hero([("index.html","Accueil"),("realisations.html","Réalisations"),(None, exp)], r["title"], r["ctx"],
  f'<span class="pill {c}"><span class="ico {c}">{ico}</span>{KIND[r["kind"]]} · {exp}</span>', h1cls=" h1-long")}
<section class="band alt">
  <div class="wrap">
    <div class="case-cols">
      {cols}
    </div>
    {extra}
    {parcours_block() if r.get("parcours") else ""}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {vs_block(r)}
    {BOUCLE_NPS if r.get("boucle") else ""}
    {res}
    <div class="xp {c}"><span class="label {c}">{r.get("rlabel", "Résultats et enseignements")}</span><p>{r["result"]}</p>
      <p class="from"><b>L’expérience mobilisée :</b> {r["xp"]}</p></div>
    <div class="below"><a class="link {c}" href="{href}">Voir l’expertise {exp} {ARR}</a></div>
    {AUTODIAG_LINE if r["slug"] in AUTODIAG_FICHES else ""}
    {PARENT_LINE if r["slug"] in PARENT_CH else ""}
  </div>
</section>
{cta()}
'''

REALISATIONS_PAGE = f'''
{page_hero([("index.html","Accueil"),(None,"Réalisations")], "Réalisations", "Des enjeux concrets. Des réponses adaptées. Des expériences de terrain.").replace('class="page-hero"', 'class="page-hero compact"', 1)}
<section class="band alt tight rsec">
  <div class="wrap">
    <div class="rsec-head"><span class="label ch">Channel Performance</span><h2 class="h2">Réseaux de partenaires</h2>
      <p class="lead">Développer la performance et l’engagement de vos partenaires, à partir d’une stratégie et d’une proposition de valeur adaptées.</p>
      <a class="link ch" href="experience-channel.html">Découvrir l’expertise Channel {ARR}</a></div>
    {rgrid([r for r in REAL if r["cls"]=="ch"])}
    <div class="ask ch tool"><span class="label ch">Outil · Auto-diagnostic partenaire</span>
      <p class="q-t">Ce partenaire est-il vraiment un partenaire performant pour votre réseau ?</p>
      <p>10 questions, 2 minutes : un score, vos signaux d’alerte et 3 pistes d’action.</p>
      <div class="ctas"><a class="btn btn-primary" href="auto-diagnostic-channel.html">Faire l’auto-diagnostic {ARR}</a></div></div>
  </div>
</section>
<section class="band rsec">
  <div class="wrap">
    <div class="rsec-head"><span class="label cl">Customer Performance</span><h2 class="h2">Portefeuille clients</h2>
      <p class="lead">Améliorer la satisfaction et la fidélisation de vos clients, tout en développant la valeur de votre portefeuille.</p>
      <a class="link cl" href="experience-client.html">Découvrir l’expertise Customer {ARR}</a></div>
    {rgrid([r for r in REAL if r["cls"]=="cl"])}
    <div class="ask cl tool"><span class="label cl">Outil · Auto-diagnostic client</span>
      <p class="q-t">Êtes-vous certain que vos clients vont renouveler ?</p>
      <p>10 questions, 2 minutes : un score de solidité, vos signaux d’alerte et 3 pistes d’action.</p>
      <div class="ctas"><a class="btn btn-primary" href="auto-diagnostic.html">Faire l’auto-diagnostic {ARR}</a></div></div>
    {KINDS_NOTE}
  </div>
</section>
{cta()}
'''

# Accueil : six cartes « enjeux » (3 Channel, 3 Customer), chacune mène à la réalisation qui y répond. Titre au repos, réponse courte au survol (toujours visible sur mobile).
HOME_CASES = [
    ("dialogue", R5, "ch", "Channel Performance", "Vos partenaires sont-ils vraiment engagés ?",
     "Impliquez, accompagnez et valorisez vos partenaires pour construire une relation durable et développer leur engagement."),
    ("salle", R1, "ch", "Channel Performance", "Quelle valeur apportez-vous à vos partenaires ?",
     "Définissez une proposition de valeur réseau différenciante et traduisez-la en un programme partenaires cohérent."),
    ("analyse", R6, "ch", "Channel Performance", "La qualité de service de vos partenaires est-elle à la hauteur de votre marque ?",
     "Mesurez la qualité de service de votre réseau, aidez chaque partenaire à progresser et valorisez les meilleurs."),
    ("carnet", R3, "cl", "Customer Performance", "Vos clients sont-ils vraiment satisfaits ?",
     "Écoutez vos clients, impliquez-les dans l’amélioration de leur parcours et transformez leurs irritants en actions concrètes."),
    ("dossier", R2, "cl", "Customer Performance", "Connaissez-vous vraiment la valeur de vos clients ?",
     "Identifiez les risques, les potentiels et les priorités pour fidéliser et développer durablement votre capital client."),
    ("casque", R4, "cl", "Customer Performance", "Vos clients achètent-ils tout ce qu’ils pourraient vous acheter ?",
     "Dépassez une relation centrée sur les équipements pour mieux connaître les besoins et développer la valeur de vos comptes."),
]
def home_collage():
    cards = ''.join(
        f'<a class="ph p{i+1} {c}" href="{h}" style="--i:{i}"><img src="assets/{PHOTOS[k]}" alt="" decoding="async">'
        f'<span class="cap"><span class="ctag {c}">{tag}</span><span class="t">{t.replace(" ?", "&nbsp;?")}</span>'
        f'<span class="rev"><span class="a">{a}</span><span class="go">Voir la réalisation {ARR}</span></span></span></a>'
        for i, (k, h, c, tag, t, a) in enumerate(HOME_CASES))
    return f'<nav class="stack n6 links cases" aria-label="Six enjeux, et les réalisations qui y répondent">{cards}</nav>'
HOME_COLLAGE = home_collage()

# ---------- ACCUEIL ----------
HOME = f'''
<section class="hero">
  <div class="wrap">
    <span class="label">Conseil en performance Channel &amp; Customer · B2B Tech</span>
    <h1 class="h1"><span>Accélérer la performance <em>de vos partenaires.</em></span><span>Révéler la valeur <em>de vos clients.</em></span></h1>
    <p class="lead">Xpansio accompagne les constructeurs, éditeurs, distributeurs et revendeurs IT sur deux leviers de croissance : leurs réseaux de partenaires et leur portefeuille clients.</p>
    <div class="ctas"><a class="btn btn-primary" href="#expertises">Découvrir les expertises {ARR}</a><a class="btn btn-ghost" href="contact.html">Échanger sur vos enjeux</a></div>
  </div>
  {HOME_COLLAGE}
</section>

<section class="band alt" id="expertises">
  <div class="wrap">
    {head("Expertises", "Deux expertises, deux leviers de croissance.")}
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
    <div class="duo-sub"><p>Ce partenaire est-il vraiment un partenaire performant pour votre réseau ? <a class="link ch" href="auto-diagnostic-channel.html">Faire l’auto-diagnostic {ARR}</a></p><p>Êtes-vous certain que vos clients vont renouveler ? <a class="link cl" href="auto-diagnostic.html">Faire l’auto-diagnostic {ARR}</a></p></div>
  </div>
</section>

<section class="band alt" id="fondatrice">
  <div class="wrap">
    {head("La fondatrice", "Une expérience de toute la chaîne de valeur IT")}
    <div class="about">
      <div class="portrait"><img src="assets/agnes.jpg" alt="Portrait d’Agnès Chabrier" width="800" height="800"></div>
      <div class="sign"><b>Agnès Chabrier</b><span>Fondatrice d’Xpansio</span></div>
      <div class="bio">
        <p>Plus de 30 ans d’expérience dans l’écosystème IT et bureautique, auprès de distributeurs et de constructeurs internationaux.</p>
        <p>Des responsabilités en marketing, stratégie Channel, développement de programmes partenaires et expérience client, complétées aujourd’hui par des missions de conseil indépendantes.</p>
        <p>Cette double connaissance des enjeux des fournisseurs et de leurs partenaires permet de concevoir des stratégies adaptées aux réalités du terrain et de les traduire en actions concrètes.</p>
        <p class="conviction"><b>Ma conviction :</b> une stratégie ne crée de valeur que lorsqu’elle est comprise, partagée et mise en œuvre.</p>
      </div>
      <div class="ctas"><a class="link" href="realisations.html">Découvrir mes réalisations {ARR}</a><a class="link" href="https://www.linkedin.com/in/agnes-chabrier-7186971/" target="_blank" rel="noopener">LinkedIn {ARR}</a></div>
    </div>
  </div>
</section>

{cta()}
'''

# ---------- EXPERTISES ----------
CHANNEL = f'''
{page_hero([("index.html","Accueil"),(None,"Channel Performance")], "Channel Performance",
  ["Faire de votre réseau de distribution indirecte un avantage concurrentiel durable.",
   "Pour les constructeurs, éditeurs, distributeurs IT et réseaux de revendeurs B2B."],
  f'<span class="pill ch"><span class="ico ch">{I_NET}</span>Expertise 01</span>', cta_btn="Prendre rendez-vous", cta2=("Faire l’auto-diagnostic partenaire", "auto-diagnostic-channel.html")).replace('class="page-hero"', 'class="page-hero compact"', 1)}
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
    {head("Domaines d’intervention", "Quatre domaines, selon la maturité de votre réseau.", cls="ch")}
    {cards([
      (I_MAP,"Stratégie et pilotage du réseau","Diagnostiquer le réseau, fixer le cap, la gouvernance et les indicateurs de performance."),
      (I_LAYERS,"Proposition de valeur et programme partenaires","Clarifier ce que vous apportez à vos partenaires, distinct de la valeur de vos offres pour le client final, puis le traduire en dispositifs."),
      (I_PATH,"Parcours et engagement des partenaires","Recruter, intégrer, accompagner, rassembler et reconnaître vos partenaires dans la durée."),
      (I_CAP,"Compétences et performance commerciale","Développer les compétences et la vente par la valeur, avec des plans d’action adaptés."),
    ],"ch",4)}
    <figure class="shot">
      <a href="assets/parcours-partenaire-grand.webp" target="_blank" rel="noopener" title="Ouvrir l’image en grand"><img src="assets/parcours-partenaire.webp" width="1600" height="900" alt="Exemple de livrable de diagnostic réseau : courbe d’expérience des partenaires sur 12 étapes, carte de chaleur par partenaire et principaux enseignements. Données fictives." loading="lazy" decoding="async"></a>
      <figcaption>Exemple de livrable : la cartographie du parcours partenaire, consolidée à l’échelle du réseau (données fictives). <a href="assets/parcours-partenaire-grand.webp" target="_blank" rel="noopener">Agrandir</a></figcaption>
    </figure>
    <p class="autodiag-line">Votre programme partenaires doit évoluer ? <a class="link ch" href="programme-partenaires.html">Voir la démarche de refonte {ARR}</a></p>
  </div>
</section>
{OFFRES_CH}
<section class="band" id="ppi">
  <div class="wrap">
    {head("Piloter le réseau", "Mesurer la performance du réseau, accompagner chaque partenaire.", "Deux niveaux de pilotage complémentaires, qui ne se remplacent pas.", cls="ch")}
    <div class="vs">
      <div class="vs-col ch"><span class="label ch">Performance globale du réseau</span><p>Chiffre d’affaires, parts de marché, couverture, croissance : où en est le réseau, et où va-t-il ?</p></div>
      <div class="vs-col"><span class="label">Relation avec chaque partenaire</span><p>Le Partner Performance Index (PPI) structure le dialogue avec chaque partenaire : compétences, qualité de service, engagement, pratiques commerciales, capacité de transformation de ses activités. Un outil de progrès, pas un classement.</p></div>
    </div>
    <p class="note">Critères et pondérations sont définis avec vous, selon votre réseau et vos objectifs.</p>
  </div>
</section>
<section class="band alt">
  <div class="wrap">
    {head("Réalisations associées", "Ce que cela donne sur le terrain.", "Ces missions ont été conduites pour un constructeur dont le réseau compte plus d’une centaine de partenaires.", cls="ch")}
    {rgrid([R[R0], R[R5], R[R1], R[R6]])}
    <p class="autodiag-line">Ce partenaire est-il vraiment un partenaire performant pour votre réseau ? <a class="link ch" href="auto-diagnostic-channel.html">Faire l’auto-diagnostic {ARR}</a></p>
  </div>
</section>
{cta()}
'''

CLIENT = f'''
{page_hero([("index.html","Accueil"),(None,"Customer Performance")], "Votre capital client est votre premier actif. Encore faut-il en prendre toute la mesure.",
  ["Xpansio vous aide à mieux écouter vos clients, à renforcer leur fidélité et à développer la valeur de votre portefeuille.",
   "Pour les revendeurs, intégrateurs, ESN et entreprises B2B disposant d’une base clients récurrente."],
  f'<span class="pill cl"><span class="ico cl">{I_USER}</span>Expertise 02 · Customer Performance</span>', cta_btn="Prendre rendez-vous", h1cls=" h1-long", cta2=("Faire l’auto-diagnostic client", "auto-diagnostic.html")).replace('class="page-hero"', 'class="page-hero compact"', 1)}
<section class="band alt">
  <div class="wrap">
    {head("Vos enjeux", "Écouter, fidéliser, développer : trois enjeux liés.", cls="cl")}
    {issues([("Une expérience client insuffisamment maîtrisée","Les enquêtes ne disent pas toujours ce que vivent réellement les clients, ni quels irritants persistent."),
             ("Une fidélité que l’on mesure trop tard","Un client satisfait en apparence n’est pas forcément un client qui renouvelle. Mieux vaut repérer les signaux de fragilité avant le départ."),
             ("Un potentiel client sous-exploité","La croissance ne repose pas que sur l’acquisition : votre base installée recèle des opportunités de développement.")])}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Domaines d’intervention", "Quatre domaines, de l’écoute à la valeur.", cls="cl")}
    {cards([
      (I_CHAT,"Écoute et satisfaction client","Structurer l’écoute, mesurer la satisfaction et comprendre les attentes."),
      (I_PATH,"Parcours et expérience client","Analyser les moments clés, traiter les irritants, construire des plans d’amélioration."),
      (I_SHIELD,"Fidélisation et Customer Success","Accompagner les clients de façon proactive, sécuriser les renouvellements, anticiper les départs."),
      (I_GROW,"Connaissance et développement du capital client","Analyser le portefeuille, identifier les potentiels et orienter les actions de développement."),
    ],"cl",4)}
    {parcours_block()}
  </div>
</section>
{OFFRES_CL}
<section class="band" id="cci">
  <div class="wrap">
    {head("Analyse du portefeuille", "Customer Capital Index (CCI)", "Un modèle d’analyse qui croise plusieurs dimensions de la relation client, pour éclairer les priorités et les plans d’action.", cls="cl")}
    <div class="dims n5"><div class="dim">Satisfaction</div><div class="dim">Fidélité</div><div class="dim">Risque</div><div class="dim">Potentiel de développement</div><div class="dim">Contribution économique</div></div>
    <p class="note">Ces dimensions sont des exemples, pas une méthodologie universelle : les critères sont adaptés à vos enjeux, à vos données et à votre modèle économique.</p>
    <div class="ask cl">
      <p class="q-t">Êtes-vous certain que vos clients vont renouveler ? Faites le test en 2 minutes</p>
      <p>10 questions sur l’un de vos clients : un score de solidité, vos signaux d’alerte et 3 pistes d’action.</p>
      <div class="ctas"><a class="btn btn-primary" href="auto-diagnostic.html">Faire l’auto-diagnostic {ARR}</a></div>
    </div>
  </div>
</section>
<section class="band alt">
  <div class="wrap">
    {head("Réalisations associées", "Ce que cela donne sur le terrain.", "Ces démarches ont été conduites chez un constructeur, auprès de ses clients directs et au contact de son réseau de revendeurs. Elles sont conçues pour être adaptées à la taille et aux moyens d’un revendeur, d’un intégrateur ou d’une ESN.", cls="cl")}
    {rgrid([R[R2], R[R3], R[R4]])}
  </div>
</section>
{cta()}
'''

# ---------- ANCIENNES ADRESSES ----------
# GitHub Pages ne fait pas de redirection serveur : ces pages minimales renvoient vers la nouvelle adresse (et l'indiquent aux moteurs de recherche).
REDIRECTS = {
    "projets.html": "realisations.html",
    "expertises.html": "index.html#expertises",
    "cas-engagement-partenaires.html": R5,
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
{page_hero([("index.html","Accueil"),(None,"Contact")], CTA_T, [CTA_P, CTA_NOTE + " Réponse sous 48 heures ouvrées."])}
<section class="band alt">
  <div class="wrap">
    <dl class="coords" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr));max-width:560px">
      <div><dt>Téléphone</dt><dd><a class="btn btn-primary btn-sm on-touch" href="tel:+33689894119" aria-label="Appeler Xpansio">Appeler</a><a class="btn btn-primary btn-sm on-desk" href="#f-tel" id="rappel">Être rappelé</a></dd></div>
      <div><dt>LinkedIn</dt><dd><a class="btn btn-ghost btn-sm" href="https://www.linkedin.com/in/agnes-chabrier-7186971/" target="_blank" rel="noopener">Voir le profil</a></dd></div>
    </dl>
    <form class="form" action="https://api.web3forms.com/submit" method="POST">
      <input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
      <input type="hidden" name="subject" id="f-subj" value="Nouveau message depuis xpansio.fr">
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
        <div class="field"><label for="f-tel" id="l-tel">Téléphone (facultatif)</label><input id="f-tel" name="telephone" type="tel" autocomplete="tel"></div>
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
    <div><h2>Propriété intellectuelle</h2><p>L’ensemble des contenus de ce site (textes, logo, visuels) est la propriété d’Xpansio. Toute reproduction sans autorisation est interdite.</p></div>
    <div><h2>Données personnelles</h2><p>Les informations transmises via le formulaire de contact servent uniquement à répondre à votre demande. Elles ne sont ni vendues ni cédées à des tiers, et sont conservées au maximum trois ans après le dernier échange. Les messages du formulaire sont transmis par email via le service Web3Forms.</p><p>Conformément au RGPD, vous disposez d’un droit d’accès, de rectification et de suppression de vos données. Pour l’exercer, faites votre demande via le <a href="contact.html">formulaire de contact</a>. Vous pouvez aussi adresser une réclamation à la CNIL.</p></div>
    <div><h2>Cookies</h2><p>Ce site ne dépose pas de cookie publicitaire ni de traceur de mesure d’audience.</p></div>
  </div>
</section>
'''

AUTODIAG = f'''
{page_hero([("index.html","Accueil"),("experience-client.html","Customer Performance"),(None,"Auto-diagnostic")], "Êtes-vous certain que ce client va renouveler ?",
  "Un client satisfait en apparence n’est pas forcément un client qui renouvelle. Cet auto-diagnostic vous aide à repérer les signaux faibles avant l’échéance du contrat.",
  f'<span class="pill cl"><span class="ico cl">{I_USER}</span>Auto-diagnostic · Customer Performance</span>').replace('class="page-hero"', 'class="page-hero compact"', 1)}
<section class="band alt tight">
  <div class="wrap">
<div id="auto-diagnostic">
  <ul class="how">
    <li><b>1.</b> Pensez à <b>un client important</b> de votre portefeuille.</li>
    <li><b>2.</b> Répondez à <b>10 questions</b> (2 minutes), le plus honnêtement possible.</li>
    <li><b>3.</b> Obtenez un <b>score de solidité de la relation</b>, vos signaux d'alerte et <b>3 pistes d'action</b>.</li>
  </ul>

<div class="progress" aria-hidden="true">
  <div class="bar"><span id="pbar"></span></div>
  <small id="ptext">0 / 10 questions</small>
</div>

<form id="diag" novalidate>
  <div id="questions"></div>

  <section class="card alerts">
    <h2>Signaux d'alerte</h2>
    <p class="sub">Cochez ce que vous constatez aujourd'hui chez ce client (aucune case si rien ne s'applique).</p>
    <div id="alerts"></div>
  </section>

  <section class="card">
    <h2>Échéance du contrat</h2>
    <p class="sub">Dans combien de temps arrive la fin du contrat principal ou son renouvellement&nbsp;?</p>
    <div class="opts" id="term"></div>
    <div style="height:14px"></div>
  </section>

  <div class="center">
    <button type="submit" class="btn" id="go" disabled>Voir mon résultat</button>
    <p class="hint" id="hint">Répondez aux 10 questions pour obtenir votre résultat.</p>
  </div>
</form>

<section id="result" aria-live="polite">
  <div class="card">
    <h2>Votre résultat</h2>
    <div class="score-box">
      <div class="gauge" id="gauge"><div><span><strong id="score">0</strong><br><small>/ 100</small></span></div></div>
      <div>
        <span class="status" id="status"></span>
        <p id="statusText" style="margin:10px 0 0"></p>
        <p id="priority" style="margin:6px 0 0;font-weight:600"></p>
      </div>
    </div>
    <div id="alertBox"></div>
    <div class="dims" id="dims"></div>
  </div>

  <div class="card">
    <h2>Vos 3 pistes d'action prioritaires</h2>
    <ol class="advice" id="advice"></ol>
  </div>

  <div class="cta">
    <h2>Allons plus loin sur l'ensemble de votre portefeuille</h2>
    <p>Ce diagnostic porte sur un seul client et 10 critères : c'est une illustration simplifiée de ma démarche. Une analyse de portefeuille s'appuie sur vos données réelles et sur des indicateurs adaptés à votre activité, avec des signaux d'alerte et un tableau de bord de tout votre portefeuille, avec le chiffre d'affaires à risque. Je vous propose un débrief de 30 minutes, offert et sans engagement, pour lire vos résultats ensemble.</p>
    <a class="btn" href="contact.html?sujet=customer-performance">Réserver mon débrief offert</a>
    <button type="button" class="btn secondary" id="again">Évaluer un autre client</button>
  </div>

  <p class="note">Résultat indicatif, calculé uniquement à partir de vos réponses. Aucune donnée n'est enregistrée ni transmise : tout se passe dans votre navigateur.</p>
</section>
</div>
  </div>
</section>
'''

# Auto-diagnostic Channel (aperçu) : même mise en page que l'auto-diagnostic client, contenu propre au réseau de partenaires
AUTODIAG_CH = (AUTODIAG
  .replace(page_hero([("index.html","Accueil"),("experience-client.html","Customer Performance"),(None,"Auto-diagnostic")], "Êtes-vous certain que ce client va renouveler ?",
  "Un client satisfait en apparence n’est pas forcément un client qui renouvelle. Cet auto-diagnostic vous aide à repérer les signaux faibles avant l’échéance du contrat.",
  f'<span class="pill cl"><span class="ico cl">{I_USER}</span>Auto-diagnostic · Customer Performance</span>').replace('class="page-hero"', 'class="page-hero compact"', 1),
   page_hero([("index.html","Accueil"),("experience-channel.html","Channel Performance"),(None,"Auto-diagnostic")], "Ce partenaire est-il vraiment un partenaire performant pour votre réseau ?",
  "Un partenaire qui vend aujourd’hui n’est pas forcément celui qui fera votre croissance demain. Cet auto-diagnostic évalue ses résultats, ses compétences, sa qualité de service, son engagement et sa capacité à faire évoluer son modèle.",
  f'<span class="pill ch"><span class="ico ch">{I_NET}</span>Auto-diagnostic · Channel Performance</span>').replace('class="page-hero"', 'class="page-hero compact"', 1))
  .replace("Pensez à <b>un client important</b> de votre portefeuille.", "Pensez à <b>un partenaire</b> de votre réseau.")
  .replace("Répondez à <b>10 questions</b> (2 minutes)", "Répondez à <b>10 questions</b> (2 minutes)")
  .replace("un <b>score de solidité de la relation</b>", "un <b>score de performance du partenaire</b>")
  .replace("0 / 10 questions", "0 / 10 questions")
  .replace("Cochez ce que vous constatez aujourd'hui chez ce client", "Cochez ce que vous constatez aujourd'hui chez ce partenaire")
  .replace("<h2>Échéance du contrat</h2>", "<h2>Poids du partenaire</h2>")
  .replace("Dans combien de temps arrive la fin du contrat principal ou son renouvellement&nbsp;?", "Quelle part de votre chiffre d'affaires indirect représente-t-il&nbsp;?")
  .replace("Répondez aux 10 questions", "Répondez aux 10 questions")
  .replace("Allons plus loin sur l'ensemble de votre portefeuille", "Allons plus loin sur l'ensemble de votre réseau")
  .replace("Ce diagnostic porte sur un seul client et 10 critères : c'est une illustration simplifiée de ma démarche. Une analyse de portefeuille s'appuie sur vos données réelles et sur des indicateurs adaptés à votre activité, avec des signaux d'alerte et un tableau de bord de tout votre portefeuille, avec le chiffre d'affaires à risque.",
           "Ce diagnostic porte sur un seul partenaire et 10 critères : c'est une illustration simplifiée de ma démarche. Un audit de performance s'appuie sur les chiffres réels de tout votre réseau (chiffre d'affaires, marge, volumes, formation des équipes, participation aux événements, utilisation des budgets coop et des outils) et sur des indicateurs adaptés à votre entreprise, avec un plan d'action construit avec chaque partenaire.")
  .replace("contact.html?sujet=customer-performance", "contact.html?sujet=channel-performance")
  .replace("Évaluer un autre client", "Évaluer un autre partenaire"))
assert AUTODIAG_CH.count("Channel Performance") >= 2 and "10 questions" in AUTODIAG_CH and "channel-performance" in AUTODIAG_CH

# ---------- REFONTE DE PROGRAMME PARTENAIRES ----------
# Page qui répond directement à la question d'un directeur channel / des ventes indirectes.
FAQ_PROG = [
  # Textes validés par Agnès
  ('Quand faut-il faire évoluer un programme partenaires ?',
   'Quand le programme n’a pas changé depuis plusieurs années alors que vos offres et votre marché ont évolué ; quand les niveaux reposent surtout sur le chiffre d’affaires et les remises ; quand une partie du réseau est référencée mais peu active ; ou quand vous lancez de nouvelles offres (services, cloud, solutions logicielles) que les partenaires doivent savoir vendre. Et surtout, lorsque vous vous apercevez que les différents leviers du programme sont sans effet sur votre stratégie ou vos objectifs. Car ce sont bien vos objectifs qui doivent être sous-jacents derrière les règles du programme. Un programme qui ne sert plus vos objectifs est un programme devenu caduc.'),
  ('Combien de temps dure une refonte de programme partenaires ?',
   'Environ 6 mois selon la taille du réseau, de l’écoute des partenaires au programme complet. Le parcours partenaires (3 à 4 semaines) et l’audit de performance du réseau (4 semaines) peuvent être menés seuls, en première étape. Mais en réalité, c’est très variable et totalement dépendant de votre réalité. Si votre stratégie de distribution différenciatrice est claire, si les objectifs du programme sont déjà établis, le temps nécessaire à la refonte sera plus faible. En revanche, s’il faut travailler en amont une stratégie de différenciation et des objectifs liés, alors ce travail, basé sur des ateliers avec la direction des ventes, voire le Comex, prendra un temps indispensable et nécessaire avant toute refonte.'),
  ('Faut-il repartir de zéro ?',
   'Non. Selon la situation, on adapte le programme existant ou l’on construit une nouvelle proposition de valeur et un nouveau programme : niveaux, devoirs et bénéfices, accréditations et certifications.'),
  ('Cabinet de conseil, agence channel marketing ou grand cabinet : que choisir ?',
   'Les approches sont complémentaires. Une agence channel marketing met en œuvre des campagnes et des actions marketing avec les partenaires. Xpansio intervient en amont : stratégie de réseau, proposition de valeur, conception du programme et mesure de la performance des partenaires, avec une démarche à taille humaine et une connaissance vécue du terrain, côté constructeur comme côté partenaires.'),
  ('Comment impliquer les partenaires dans la refonte ?',
   'En partant de leur vécu : entretiens approfondis avec une dizaine de partenaires, enquête de satisfaction auprès du réseau, ateliers avec vos équipes, puis pilotes co-construits avec des partenaires sur le terrain. Un programme compris et partagé est un programme appliqué.'),
  ('Comment mesurer l’efficacité d’un programme partenaires ?',
   'Sur deux niveaux : la performance globale du réseau (chiffre d’affaires, parts de marché, couverture, croissance), sa capacité à répondre à vos objectifs, et la relation avec chaque partenaire, structurée par le Partner Performance Index (compétences, qualité de service, engagement, pratiques commerciales, capacité de transformation).'),
  ('Pour quelles entreprises ?',
   'Les constructeurs, éditeurs et distributeurs IT et bureautique qui vendent par un réseau de revendeurs, d’intégrateurs ou d’ESN. Mon terrain principal est la France. Pour un programme qui s’étend à l’international, je peux travailler en anglais avec vos équipes et vos partenaires anglophones. Les entretiens approfondis avec les partenaires se font en français ou en anglais.'),
]
EXTRA_LD["programme-partenaires.html"] = [
  {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ_PROG]},
  {"@context": "https://schema.org", "@type": "Service", "name": "Refonte de programme partenaires",
   "serviceType": "Conseil en stratégie channel et programme partenaires", "provider": {"@id": SITE + "#xpansio"},
   "areaServed": {"@type": "Country", "name": "France"}, "url": SITE + "programme-partenaires.html",
   "audience": {"@type": "BusinessAudience", "audienceType": "Directeurs channel, directeurs des ventes indirectes, responsables de programmes partenaires"}},
]
def faq(items, cls):
    return f'<div class="faq {cls}">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'

PROG = f"""
{page_hero([("index.html","Accueil"),("experience-channel.html","Channel Performance"),(None,"Programme partenaires")], "Faire évoluer votre programme partenaires",
  ["Un programme plus efficace, adapté à vos nouveaux enjeux, et qui a du sens pour vos partenaires.",
   "Pour les directeurs channel et ventes indirectes : constructeurs, éditeurs, distributeurs IT."],
  f'<span class="pill ch"><span class="ico ch">{I_NET}</span>Channel Performance</span>', cta_btn="Échanger sur votre programme", cta2=("Faire l’auto-diagnostic partenaire", "auto-diagnostic-channel.html")).replace('class="page-hero"', 'class="page-hero compact"', 1)}
<section class="band alt">
  <div class="wrap">
    {head("Les signaux", "Votre programme sert-il encore votre réseau, et vos objectifs ?", cls="ch")}
    {issues([("Un programme qui n’a pas suivi le marché","Vos offres, vos modèles de vente et vos partenaires ont changé ; le programme, lui, est resté le même."),
             ("Des niveaux fondés sur le chiffre d’affaires et les remises","Les partenaires comparent les conditions, pas la valeur que vous leur apportez."),
             ("Des partenaires référencés, mais peu engagés","Une partie du réseau signe le contrat, puis s’investit peu : formation, événements, outils, budgets."),
             ("Des leviers et critères qui ne répondent plus à vos objectifs","Niveaux, remises, bénéfices : les règles du programme ne font plus avancer votre stratégie.")])}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Vos nouveaux enjeux", "Un programme partenaires traduit une stratégie de réseau.", "Pas une grille de remises : chaque élément sert la même proposition de valeur.", cls="ch")}
    {cards([
      (I_LAYERS,"Services et revenus récurrents","Valoriser les partenaires qui développent les contrats de service, au cœur de la rentabilité durable du réseau."),
      (I_CAP,"Cloud, cybersécurité, IA","Aider les partenaires à démontrer une valeur métier à leurs clients, au-delà de la technologie."),
      (I_MAP,"Des critères au-delà du chiffre d’affaires","Services, plan de développement, certifications, qualité de service, engagements RSE."),
      (I_PATH,"L’engagement plutôt que les remises","Rencontres, clubs, pilotes co-construits : des partenaires qui progressent avec vous."),
    ],"ch",4)}
  </div>
</section>
<section class="band alt">
  <div class="wrap">
    {head("La démarche", "Partir du vécu des partenaires, jusqu’au pilotage du réseau.", "Environ 6 mois selon la taille du réseau. Chaque étape peut aussi être menée seule.", cls="ch")}
    {loop([("Écouter","Parcours partenaires : entretiens, enquête, irritants et moments réussis."),
           ("Mesurer","Audit de performance du réseau, sur six axes."),
           ("Définir","Stratégie de réseau et proposition de valeur, avec la direction."),
           ("Construire","Niveaux, devoirs et bénéfices, certifications, communication."),
           ("Piloter","Indicateurs du réseau et Partner Performance Index.")],
          "ch n5", "Démarche en cinq étapes : écouter, mesurer, définir, construire, piloter, puis recommencer")}
    <p class="autodiag-line">Durées et livrables de chaque mission : <a class="link ch" href="experience-channel.html#comment-je-travaille">Comment je travaille {ARR}</a></p>
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Réalisation", "Ce que cela donne sur le terrain.", "Mission conduite pour un constructeur dont le réseau compte plus d’une centaine de partenaires.", cls="ch")}
    {rgrid([R[R0]])}
  </div>
</section>
<section class="band alt" id="questions">
  <div class="wrap">
    {head("Questions fréquentes", "Faire évoluer un programme partenaires : vos questions.", cls="ch")}
    {faq(FAQ_PROG, "ch")}
  </div>
</section>
{cta()}
"""

PAGES = [
    ("index.html", "home", "Xpansio · Conseil en performance Channel et Customer, B2B IT", "Xpansio, conseil en performance Channel & Customer pour les constructeurs, éditeurs, distributeurs et revendeurs IT : réseaux de partenaires et valeur du portefeuille clients.", HOME),
    ("experience-channel.html", "channel", "Channel Performance : réseaux et programmes partenaires · Xpansio", "Stratégie de réseau, proposition de valeur et programmes partenaires, parcours et engagement des partenaires : l’expertise Channel Performance d’Xpansio.", CHANNEL),
    ("experience-client.html", "client", "Customer Performance : satisfaction, fidélisation, Customer Success · Xpansio", "Écoute et satisfaction, expérience client, fidélisation et Customer Success, développement du capital client : l’expertise Customer Performance d’Xpansio.", CLIENT),
    ("programme-partenaires.html", "channel", "Refonte de programme partenaires : conseil channel pour constructeurs, éditeurs et distributeurs IT · Xpansio", "Faire évoluer votre programme partenaires : signaux, nouveaux enjeux, démarche en cinq étapes, réalisation et questions fréquentes. Xpansio, conseil indépendant en performance Channel.", PROG),
    ("realisations.html", "realisations", "Réalisations · Xpansio", "Des situations réelles en Channel et Customer Performance : contexte, démarche, réalisations et enseignements.", REALISATIONS_PAGE),
] + [(r["slug"], "realisations", r["title"] + " · Xpansio", r["ctx"], real_page(r)) for r in REAL] + [
    ("auto-diagnostic.html", "autodiag", "Auto-diagnostic : êtes-vous certain que ce client va renouveler ? · Xpansio", "10 questions, 2 minutes : évaluez la solidité de la relation avec l’un de vos clients clés et repérez les signaux de risque avant l’échéance du contrat.", AUTODIAG),
    ("auto-diagnostic-channel.html", "autodiag-ch", "Auto-diagnostic : ce partenaire est-il vraiment un partenaire performant pour votre réseau ? · Xpansio", "10 questions, 2 minutes : évaluez la performance de l’un de vos partenaires (résultats, compétences, qualité de service, engagement, transformation) et repérez les signaux d’alerte.", AUTODIAG_CH),
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
        for f in ["styles.css", "autodiag.css", "autodiag.js", "autodiag-channel.js"]:
            shutil.copy(os.path.join(SRC, f), d)
        open(os.path.join(d, "assets", "parcours-client.svg"), "w").write(parcours.svg())
        for f in os.listdir(os.path.join(SRC, "assets")):
            shutil.copy(os.path.join(SRC, "assets", f), os.path.join(d, "assets", f))
        for fn, key, title, desc, body in PAGES:
            with open(os.path.join(d, fn), "w") as fh:
                fh.write(page(key, title, desc, body, full_home or fn != "index.html", fn))
        for fn, to in REDIRECTS.items():
            open(os.path.join(d, fn), "w").write(redirect_page(to))
    d = os.path.join(ROOT, "docs")
    open(os.path.join(d, "CNAME"), "w").write("xpansio.fr\n")
    open(os.path.join(d, ".nojekyll"), "w").write("")
    # Référencement Google : plan du site et fichier robots (les pages de redirection n'y figurent pas)
    open(os.path.join(d, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + ''.join(f'  <url><loc>{SITE}{"" if fn == "index.html" else fn}</loc></url>\n' for fn, *_ in PAGES) + '</urlset>\n')
    open(os.path.join(d, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
    print("ok")

