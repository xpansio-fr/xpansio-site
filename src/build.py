#!/usr/bin/env python3
"""Génère le site Xpansio v3 : dist/ (site à héberger) et artifact/ (accueil sans squelette)."""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icons import *

SRC = os.path.dirname(os.path.abspath(__file__))
# Clé publique Web3Forms (formulaire de contact), liée à l'adresse d'Agnès. Elle est faite pour être visible dans la page.
WEB3FORMS_KEY = "98890583-2366-4dbd-afb2-a1896cf89b4d"
ROOT = os.path.dirname(SRC)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Montserrat:wght@400;500;600;700&display=swap">')

NAV = [("index.html", "Accueil", "home"), ("expertises.html", "Nos expertises", "expertises"),
       ("projets.html", "Nos projets", "projets"), ("contact.html", "Contact", "contact")]

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
          <a class="ch" href="experience-channel.html"><span class="ico ch">{I_NET}</span><strong>Channel Performance</strong><span class="d">Programmes partenaires, parcours partenaire, animation de réseaux et Partner Performance Index™.</span></a>
          <a class="cl" href="experience-client.html"><span class="ico cl">{I_USER}</span><strong>Customer Performance</strong><span class="d">Parcours client, satisfaction, segmentation et gestion de crise.</span></a>
        </div>
      </div>
    </div>
  </nav>
</header>'''

FOOTER = '''<footer>
  <div class="wrap">
    <img class="logo" src="assets/logo-white.png" alt="xpansio" width="480" height="140">
    <p class="tagline">Accélérer la performance de vos partenaires.<br>Révéler la valeur de vos clients.</p>
    <nav aria-label="Pied de page"><a href="index.html">Accueil</a><a href="experience-channel.html">Channel Performance</a><a href="experience-client.html">Customer Performance</a><a href="projets.html">Nos projets</a><a href="contact.html">Contact</a><a href="https://www.linkedin.com/in/agnes-chabrier-7186971/" target="_blank" rel="noopener">LinkedIn</a></nav>
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
            f'<meta name="description" content="{desc}">\n{FONTS}\n<link rel="stylesheet" href="styles.css">\n<link rel="icon" href="assets/favicon.png">')
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
# Seule la page Nos projets garde un petit collage (photos 1, 3 et 4 du carrousel de l'accueil).
HT = {"projets": collage(["carnet", "dossier", "dialogue"], cls="sm")}
# Accueil : quatre cartes « cas d'usage », chacune mène à sa page. Titre au repos, réponse courte au survol (toujours visible sur mobile).
HOME_CASES = [
    ("dialogue", "cas-engagement-partenaires.html", "ch", "Channel Performance", "Vos partenaires sont-ils vraiment engagés ?",
     "Impliquez, accompagnez et valorisez vos partenaires pour construire une relation durable et développer leur engagement."),
    ("salle", "cas-valeur-reseau.html", "ch", "Channel Performance", "Quelle valeur apportez-vous à vos partenaires ?",
     "Définissez une proposition de valeur réseau différenciante et traduisez-la en un programme partenaires cohérent."),
    ("carnet", "cas-experience-client.html", "cl", "Customer Performance", "Vos clients sont-ils vraiment satisfaits ?",
     "Écoutez vos clients, impliquez-les dans l’amélioration de leur parcours et transformez leurs irritants en actions concrètes."),
    ("dossier", "cas-valeur-clients.html", "cl", "Customer Performance", "Connaissez-vous vraiment la valeur de vos clients ?",
     "Identifiez les risques, les potentiels et les priorités pour fidéliser et développer durablement votre capital client."),
]
def home_collage():
    cards = ''.join(
        f'<a class="ph p{i+1} {c}" href="{h}" style="--i:{i}"><img src="assets/{PHOTOS[k]}" alt="" decoding="async">'
        f'<span class="cap"><span class="ctag {c}">{tag}</span><span class="t">{t}</span>'
        f'<span class="rev"><span class="a">{a}</span><span class="go">Découvrir le cas {ARR}</span></span></span></a>'
        for i, (k, h, c, tag, t, a) in enumerate(HOME_CASES))
    return f'<nav class="stack n4 links cases" aria-label="Quatre enjeux, quatre cas d’usage">{cards}</nav>'
HOME_COLLAGE = home_collage()

# ---------- ACCUEIL ----------
def real(cls, tag, title, text):
    return f'<article class="pcard rcard {cls}"><span class="tag {cls}">{tag}</span><h3>{title}</h3><p>{text}</p></article>'

REALISATIONS = ''.join([
    real("ch", "Channel Performance", "Conception et refonte d’un programme partenaires", "Définir une stratégie Channel et la traduire en dispositifs concrets."),
    real("ch", "Channel Performance", "Évaluation et développement de l’excellence de service d’un réseau", "Connaissance des partenaires, des critères de performance et des dispositifs de reconnaissance. Valoriser les savoir-faire, assurer la montée en compétences."),
    real("ch", "Channel Performance", "Programme d’engagement des partenaires", "Accroître la fidélité et l’engagement des partenaires au travers de programmes d’accompagnement et de responsabilisation."),
    real("cl", "Customer Performance", "Amélioration de l’expérience client", "Capacité à écouter les clients, définir le parcours client, identifier les irritants et structurer des plans d’amélioration."),
    real("cl", "Customer Performance", "Programme de segmentation clients", "Mesurer la rentabilité réelle des clients et identifier les potentiels pour mettre en place des plans de développement ou de remédiation."),
    real("cl", "Customer Performance", "Customer Success", "Mise en place d’équipes d’accompagnement au développement et à la satisfaction des clients majeurs."),
])

HOME = f'''
<section class="hero">
  <div class="wrap">
    <span class="label">Conseil en performance Channel &amp; Customer · B2B Tech</span>
    <h1 class="h1"><span>Accélérer la performance <em>de vos partenaires.</em></span><span>Révéler la valeur <em>de vos clients.</em></span></h1>
    <p class="lead">Xpansio accompagne les constructeurs, éditeurs, distributeurs et revendeurs IT dans le développement de deux leviers de croissance : la performance de leurs réseaux de partenaires et la valeur de leur portefeuille clients.</p>
    <div class="ctas"><a class="btn btn-primary" href="#expertises">Découvrir nos expertises {ARR}</a><a class="btn btn-ghost" href="contact.html">Échanger sur vos enjeux</a></div>
  </div>
  {HOME_COLLAGE}
</section>

<section class="band" id="apropos">
  <div class="wrap about">
    <span class="label">À propos d’Xpansio</span>
    <div class="portrait"><img src="assets/agnes.jpg" alt="Portrait d’Agnès Chabrier" width="800" height="800"></div>
    <div class="sign"><b>Agnès Chabrier</b><span>Fondatrice</span></div>
    <div class="bio">
      <p>Forte de plus de 30 ans d’expérience dans l’écosystème IT et bureautique, au sein de distributeurs et de constructeurs internationaux, j’ai piloté des stratégies Channel, des programmes partenaires, des dispositifs marketing et des démarches d’amélioration de l’expérience client.</p>
      <p>Cette expérience me permet d’aborder les enjeux de performance avec une vision à la fois stratégique et opérationnelle, en tenant compte des réalités des constructeurs comme de celles de leurs partenaires.</p>
      <p class="conviction"><b>Ma conviction :</b> la performance durable repose sur la compréhension des acteurs, la pertinence des priorités et la capacité à transformer une stratégie en actions concrètes.</p>
    </div>
    <div class="timeline"><span>Marketing</span><span>Channel</span><span>Expérience client</span><span>Programmes partenaires</span><span>Customer Success</span><span>Transformation</span><span>Animation de réseaux</span></div>
  </div>
</section>

<section class="band alt" id="expertises">
  <div class="wrap">
    {head("Nos expertises", "Deux expertises, deux leviers de croissance.")}
    <div class="duo">
      <a class="xcard ch" href="experience-channel.html">
        <span class="ico ch">{I_NET}</span>
        <span class="label ch">01 — Channel Performance</span>
        <h3>Faites de votre réseau de partenaires un véritable levier de croissance.</h3>
        <p>Un réseau performant ne se résume pas au nombre de partenaires recrutés. Il repose sur leur engagement, leurs compétences et leur capacité à développer durablement votre business.</p>
        <p>Xpansio vous accompagne dans l’évaluation, la structuration et le développement de votre réseau de distribution indirecte.</p>
        <div class="chips"><span class="chip">Audit réseau</span><span class="chip">Stratégie Channel</span><span class="chip">Programmes partenaires</span><span class="chip">Engagement et animation</span><span class="chip">Performance commerciale</span></div>
        <p class="for">Pour les <b>constructeurs</b>, <b>éditeurs</b> et <b>distributeurs IT</b>.</p>
        <span class="link">Découvrir l’expertise Channel {ARR}</span>
      </a>
      <a class="xcard cl" href="experience-client.html">
        <span class="ico cl">{I_USER}</span>
        <span class="label cl">02 — Customer Performance</span>
        <h3>Développez la valeur de votre portefeuille clients.</h3>
        <p>Tous vos clients ne contribuent pas de la même manière à votre rentabilité et à votre croissance. Encore faut-il disposer des bonnes données et des bons leviers d’action.</p>
        <p>Xpansio vous aide à mieux comprendre votre base clients, identifier les opportunités de développement, sécuriser les comptes stratégiques et améliorer l’expérience client.</p>
        <div class="chips"><span class="chip">Diagnostic de portefeuille</span><span class="chip">Rentabilité client</span><span class="chip">Segmentation</span><span class="chip">Fidélisation</span><span class="chip">Expérience client</span></div>
        <p class="for">Pour les <b>revendeurs</b>, <b>intégrateurs</b>, <b>ESN</b> et <b>entreprises B2B</b> disposant d’une base clients récurrente.</p>
        <span class="link">Découvrir l’expertise Customer {ARR}</span>
      </a>
    </div>
  </div>
</section>

<section class="band" id="approche">
  <div class="wrap">
    {head("Notre approche", "De l’analyse à l’action, pour des résultats mesurables.", "Une démarche pragmatique qui combine connaissance du terrain, analyse des données et accompagnement opérationnel.")}
    <div class="steps">
      <div class="step"><span class="n">01</span><h3>Comprendre</h3><p>Écouter, analyser les données et identifier les enjeux.</p></div>
      <div class="step"><span class="n">02</span><h3>Prioriser</h3><p>Identifier les leviers de performance et définir une feuille de route.</p></div>
      <div class="step"><span class="n">03</span><h3>Accompagner</h3><p>Structurer les actions, mobiliser les équipes et mesurer les progrès.</p></div>
    </div>
  </div>
</section>

<section class="band alt" id="projets">
  <div class="wrap">
    {head("Les projets", "Des expériences concrètes au service de votre performance.")}
    <div class="pgrid">{REALISATIONS}</div>
    <div class="below"><a class="btn btn-ghost" href="projets.html">Voir des projets en détail {ARR}</a></div>
  </div>
</section>

<section class="band" id="pourquoi">
  <div class="wrap">
    {head("Pourquoi Xpansio ?", "Une connaissance de toute la chaîne de valeur, du constructeur au client final.")}
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
    <p class="lead">Vous souhaitez faire évoluer votre stratégie Channel, renforcer l’engagement de vos partenaires ou développer la valeur de votre portefeuille clients ?</p>
    <p class="lead">Échangeons sur vos enjeux et les pistes d’amélioration possibles.</p>
  </div>
  <div class="ctas"><a class="btn btn-white" href="contact.html">Prendre rendez-vous {ARR}</a></div>
  <p class="note">Premier échange de 30 minutes, sans engagement.</p>
</div></section>
'''

# ---------- EXPERTISES ----------
EXPERTISES = f'''
{page_hero([("index.html","Accueil"),(None,"Nos expertises")], "Nos expertises", "Xpansio intervient sur les deux relations qui font la croissance d’un acteur B2B : celle avec ses partenaires de distribution, et celle avec ses clients.")}
<section class="band alt">
  <div class="wrap">
    <div class="duo">
      <a class="xcard ch" href="experience-channel.html">
        <span class="ico ch">{I_NET}</span><span class="label ch">Expertise 01</span>
        <h3>Channel Performance</h3>
        <p>Transformer votre réseau de distribution en avantage concurrentiel durable : un programme partenaires qui engage, fait progresser et fidélise.</p>
        <div class="chips"><span class="chip">Audit réseau</span><span class="chip">Programmes partenaires</span><span class="chip">Parcours partenaire</span><span class="chip">Animation et roadshows</span><span class="chip">Certifications</span><span class="chip">Partner Performance Index™</span></div>
        <p class="for">Constructeurs informatiques, éditeurs de logiciels, distributeurs IT.</p>
        <span class="link">Découvrir l’expertise Channel {ARR}</span>
      </a>
      <a class="xcard cl" href="experience-client.html">
        <span class="ico cl">{I_USER}</span><span class="label cl">Expertise 02</span>
        <h3>Customer Performance</h3>
        <p>Vos futurs revenus sont déjà chez vos clients actuels. Nous vous aidons à les connaître, les fidéliser et les développer.</p>
        <div class="chips"><span class="chip">Parcours client</span><span class="chip">Satisfaction client</span><span class="chip">Segmentation</span><span class="chip">Gestion de crise</span><span class="chip">Programme VIP</span></div>
        <p class="for">Intégrateurs, ESN, revendeurs, concessionnaires bureautique, et éditeurs ou constructeurs en vente directe.</p>
        <span class="link">Découvrir l’expertise Customer {ARR}</span>
      </a>
    </div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Quelle expertise pour vous ?", "Tout dépend de votre place dans la chaîne.")}
    {issues([("Vous vendez via des partenaires","Éditeur, constructeur ou distributeur : votre croissance dépend de l’engagement de votre réseau. Expertise Channel Performance."),
             ("Vous vendez en direct et en indirect","Les deux expertises se complètent : performance du réseau et valeur des clients finaux."),
             ("Vous servez vos propres clients","Intégrateur, ESN, revendeur ou concessionnaire : votre base installée est votre premier levier. Expertise Customer Performance.")])}
  </div>
</section>
{cta()}
'''

CHANNEL = f'''
{page_hero([("index.html","Accueil"),("expertises.html","Nos expertises"),(None,"Channel Performance")], "Channel Performance",
  "Transformer votre réseau de distribution en avantage concurrentiel durable. Encore faut-il que vos partenaires aient l’envie et les moyens de vendre votre stratégie.",
  f'<span class="pill ch"><span class="ico ch">{I_NET}</span>Expertise 01</span>', cta_btn="Échangeons sur votre réseau de partenaires")}
<section class="band alt">
  <div class="wrap">
    {head("Vos enjeux", "Le marché change plus vite que les réseaux.", cls="ch")}
    {issues([("L’engagement ne s’achète plus avec des remises","Les remises et les fonds marketing ne suffisent pas à créer un engagement durable. Les partenaires privilégient les fournisseurs qui contribuent réellement à leur croissance, à leur rentabilité et à la fidélisation de leurs clients. La qualité de la relation, la confiance et leur implication dans les orientations stratégiques deviennent des leviers essentiels de différenciation."),
             ("Des partenaires référencés, mais pas toujours engagés","Un réseau étendu ne garantit ni son dynamisme ni sa performance. Certains partenaires restent peu actifs, privilégient d’autres fournisseurs ou participent peu aux initiatives proposées. L’enjeu n’est pas seulement de recruter des partenaires, mais de développer leur engagement, leur contribution et leur fidélité dans la durée."),
             ("De la technologie à la valeur métier","Cloud, cybersécurité, automatisation et intelligence artificielle multiplient les opportunités de développement. Mais la valeur ne réside pas dans la technologie elle-même : elle dépend de la capacité des partenaires à l’intégrer aux processus métiers de leurs clients et à démontrer des bénéfices concrets en matière de productivité, de performance et de maîtrise des coûts.")])}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Ce que nous faisons", "Cinq leviers pour un réseau plus performant.", "Du diagnostic à l’activation opérationnelle, des interventions ciblées ou des missions complètes selon la maturité de votre réseau.", cls="ch")}
    {offers([
      (I_MAP,"Audit &amp; diagnostic réseau","Comprendre les forces, les attentes et les irritants de votre réseau.","Analyser la performance et le potentiel du réseau, écouter les partenaires, évaluer leur perception de la marque et identifier les points de friction tout au long de leur parcours.",["Performance","Écoute partenaires","Parcours","Opportunités"]),
      (I_LAYERS,"Stratégie &amp; programme partenaires","Construire une proposition de valeur différenciante pour votre réseau.","Définir la vision et la mission du réseau indirect, le positionnement de la marque auprès de ses partenaires et les engagements réciproques. Structurer un programme cohérent avec cette stratégie : segmentation, niveaux, bénéfices et dispositifs d’accompagnement.",["Vision","Positionnement","Segmentation","Niveaux &amp; bénéfices"]),
      (I_PATH,"Parcours &amp; développement partenaires","Accompagner vos partenaires à chaque étape de leur développement.","Concevoir des parcours adaptés au cycle de vie des partenaires : ciblage et recrutement, onboarding, développement des compétences et du business, accompagnement des partenaires stratégiques et, lorsque nécessaire, transmission ou rapprochement.",["Recrutement","Onboarding","Développement","Transmission"]),
      (I_HANDS,"Engagement &amp; valorisation","Renforcer la confiance, l’implication et la reconnaissance de vos partenaires.","Développer des communautés et des dispositifs de dialogue, associer les partenaires aux réflexions stratégiques et valoriser leurs engagements et leurs réalisations, notamment en matière d’excellence de service, de qualité et de RSE.",["Communautés","Reconnaissance","Excellence","RSE"]),
      (I_SPARK,"Animation &amp; activation du réseau","Transformer la stratégie en actions et en dynamique commerciale.","Mobiliser les partenaires à travers des événements, des challenges, des campagnes conjointes, des outils d’aide à la vente et des plans d’action adaptés aux priorités du réseau.",["Événements","Challenges","Campagnes","Plans d’action"]),
    ],"ch")}
  </div>
</section>
<section class="band alt" id="methode">
  <div class="wrap">
    {head("La méthode", "Partner Performance Framework<sup style='font-size:.4em;font-weight:500'>™</sup>", "Sept étapes, de l’état des lieux à la mise en œuvre opérationnelle.", cls="ch")}
    <div class="seq">
      <div class="sq"><span class="n">01</span><b>Audit</b></div>
      <div class="sq"><span class="n">02</span><b>Écoute interne</b></div>
      <div class="sq"><span class="n">03</span><b>Voice of Partner</b></div>
      <div class="sq"><span class="n">04</span><b>Benchmark</b></div>
      <div class="sq"><span class="n">05</span><b>Stratégie</b></div>
      <div class="sq"><span class="n">06</span><b>Programme</b></div>
      <div class="sq"><span class="n">07</span><b>Déploiement</b></div>
    </div>
  </div>
</section>
<section class="band" id="ppi">
  <div class="wrap">
    <div class="head"><span class="label ch">Diagnostic et développement des partenaires</span><h2 class="h2">Partner Performance Index (PPI)</h2>
      <p class="hook-lg ch">Évaluer les capacités de vos partenaires. Identifier leurs axes de progrès. Accompagner leur développement.</p>
      <p class="lead">La performance d’un réseau repose aussi sur la solidité, les compétences et la capacité d’évolution de chacun de ses partenaires.</p>
      <p class="lead">Le Partner Performance Index est un modèle de diagnostic proposé par Xpansio pour apprécier les forces, les axes de progrès et les besoins d’accompagnement des partenaires. Il vise à structurer un dialogue constructif entre le fournisseur et ses partenaires, à orienter les plans de développement et à suivre les progrès dans le temps.</p>
    </div>
    <h3 class="subhead">Les cinq dimensions du PPI</h3>
    {cards([
      (I_CAP,"Compétences et autonomie","Capacité à commercialiser, déployer et accompagner les solutions : compétences commerciales et techniques, certifications, autonomie opérationnelle."),
      (I_SHIELD,"Excellence opérationnelle","Qualité des prestations, satisfaction des clients finaux, fiabilité du service et capacité à traiter efficacement les incidents."),
      (I_HANDS,"Engagement et coopération","Qualité de la relation avec le constructeur, implication dans les programmes, utilisation des outils et réalisation des engagements partagés."),
      (I_GROW,"Développement commercial","Maturité des pratiques commerciales : prospection, développement des comptes existants, valorisation des offres stratégiques. Les pratiques, et non le chiffre d’affaires réalisé."),
      (I_SPARK,"Transformation et adaptation","Capacité à intégrer de nouvelles technologies, développer les offres de services, faire évoluer les modèles économiques et s’adapter au marché."),
    ],"ch",5)}
    <p class="note">Les critères, les modalités d’évaluation et d’éventuelles pondérations sont définis avec vous, selon les spécificités et les objectifs de votre réseau.</p>
  </div>
</section>
<section class="band alt">
  <div class="wrap">
    {head("À quoi sert le PPI ?", "Un outil de dialogue et de progrès, pas un classement.", "Le PPI complète les indicateurs commerciaux et stratégiques du réseau (chiffre d’affaires, parts de marché, couverture, croissance) sans les remplacer. Il répond à une autre question : vos partenaires disposent-ils des compétences, des capacités et de l’accompagnement nécessaires pour se développer durablement ?", cls="ch")}
    {cards([
      (None,"Identifier les forces et les axes de progrès","Disposer d’une vision structurée des capacités et des besoins de chaque partenaire."),
      (None,"Construire des plans de développement individualisés","Définir des actions adaptées : formation, accompagnement commercial, amélioration du service ou acquisition de nouvelles compétences."),
      (None,"Suivre la progression dans le temps","Observer les évolutions des partenaires et apprécier les effets des actions d’accompagnement."),
      (None,"Identifier les besoins collectifs du réseau","Consolider les diagnostics individuels pour repérer les besoins communs et adapter les dispositifs d’accompagnement du constructeur."),
    ],"ch",4)}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("La démarche", "Une démarche d’amélioration continue, construite avec vos partenaires.", cls="ch")}
    {loop([("Évaluer","Établir un diagnostic des capacités et de la maturité du partenaire."),
           ("Partager","Confronter les résultats aux observations du partenaire et définir ensemble les priorités."),
           ("Accompagner","Construire et mettre en œuvre un plan de développement ciblé."),
           ("Mesurer les progrès","Suivre les évolutions et ajuster les actions.")],"ch","Démarche cyclique en quatre étapes : évaluer, partager, accompagner, mesurer les progrès, puis recommencer")}
    <ul class="principles">
      <li>Le PPI s’adapte au profil, au modèle économique et à la maturité de chaque partenaire.</li>
      <li>Il favorise le dialogue entre le constructeur et son réseau, et révèle les besoins d’accompagnement individuels comme collectifs.</li>
      <li>Les difficultés d’un partenaire peuvent aussi révéler des insuffisances dans les dispositifs d’accompagnement du constructeur.</li>
      <li>La méthodologie est ajustée et validée avec vous lors de sa mise en œuvre.</li>
    </ul>
    <div class="ask ch">
      <p class="q-t">Vous souhaitez mieux comprendre les forces et les besoins de développement de vos partenaires ?</p>
      <p>Échangeons sur la manière de construire un diagnostic adapté à votre réseau et à vos enjeux.</p>
      <div class="ctas"><a class="btn btn-primary" href="contact.html">Échanger sur votre réseau {ARR}</a></div>
    </div>
  </div>
</section>
<section class="band alt">
  <div class="wrap">
    {head("Pour qui", "Les acteurs de l’IT qui vendent en indirect.", cls="ch")}
    {targets(["Constructeurs informatiques","Éditeurs de logiciels","Distributeurs IT","Réseaux de revendeurs B2B"],"c-ch")}
  </div>
</section>
{cta("Et si votre programme partenaires devenait un avantage concurrentiel ?","Demandez une Executive Partner Review : 90 minutes pour analyser l’alignement de votre programme avec votre stratégie et ses leviers de création de valeur.")}
'''

CLIENT = f'''
{page_hero([("index.html","Accueil"),("expertises.html","Nos expertises"),(None,"Customer Performance")], "Votre capital client est votre premier actif. Encore faut-il en prendre toute la mesure.",
  ["Satisfaction, fidélité, expérience vécue, potentiel de développement : la performance de votre capital client ne se résume pas au chiffre d’affaires qu’il génère.",
   "Xpansio vous aide à mieux connaître vos clients, à renforcer durablement leur relation avec votre entreprise et à développer la valeur de votre portefeuille."],
  f'<span class="pill cl"><span class="ico cl">{I_USER}</span>Expertise 02 · Customer Performance</span>', cta_btn="Échanger sur votre capital client", h1cls=" h1-long")}
<section class="band alt">
  <div class="wrap">
    {head("Vos enjeux", "Écouter, fidéliser, développer : trois enjeux liés.", cls="cl")}
    {issues([("Une expérience client insuffisamment maîtrisée","Les enquêtes de satisfaction ne suffisent pas toujours à comprendre ce que vivent réellement les clients. Sans écoute structurée et analyse des moments clés du parcours, certains irritants persistent et les attentes évoluent sans être identifiées."),
             ("Une fidélité que l’on mesure trop tard","Un client qui renouvelle son contrat n’est pas nécessairement un client pleinement satisfait. Suivre les départs, identifier les signaux de fragilité et comprendre les raisons de la fidélité permet d’anticiper les risques plutôt que de réagir lorsqu’il est trop tard."),
             ("Un capital client dont le potentiel reste sous-exploité","La croissance ne repose pas uniquement sur l’acquisition de nouveaux clients. Comprendre la structure du portefeuille, identifier les opportunités de développement et valoriser les clients qui recommandent l’entreprise permet de renforcer sa performance dans la durée.")])}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Performance du capital client", "Trois dimensions complémentaires.", cls="cl")}
    {cards([
      (I_CHAT,"Satisfaction &amp; expérience client","Comprendre les attentes, mesurer la satisfaction et identifier les améliorations prioritaires de l’expérience vécue.","Écoute client · Qualité perçue · Irritants"),
      (I_SHIELD,"Fidélité &amp; stabilité du portefeuille","Mesurer la capacité de l’entreprise à conserver ses clients et à construire des relations durables.","Churn · Fidélité dans la durée · Évolution de la base clients"),
      (I_GROW,"Développement &amp; valeur du capital client","Évaluer la dynamique commerciale du portefeuille, sa contribution à la performance de l’entreprise et sa capacité à générer de nouvelles opportunités.","Croissance · Contribution économique · Potentiel · Recommandation"),
    ],"cl",3)}
  </div>
</section>
<section class="band alt">
  <div class="wrap">
    {head("Ce que nous faisons", "Cinq leviers pour développer votre capital client.", "Des missions concrètes, menées avec vos équipes commerciales, techniques et de direction.", cls="cl")}
    {offers([
      (I_SIGNAL,"Diagnostic &amp; pilotage du capital client","Comprendre la santé et la dynamique de votre portefeuille.","Analyser la satisfaction, la fidélité, la structure et la valeur économique du portefeuille pour identifier les risques, les opportunités et les priorités d’action.",["Satisfaction","Churn","Structure du portefeuille","Valeur"]),
      (I_CHAT,"Écoute &amp; expérience client","Comprendre les attentes et améliorer l’expérience vécue.","Structurer l’écoute client, analyser les moments clés du parcours, identifier les irritants et construire des plans d’amélioration concrets.",["Voix du client","Parcours","Irritants","Amélioration"]),
      (I_SHIELD,"Fidélisation &amp; Customer Success","Renforcer la relation et anticiper les risques de départ.","Développer une démarche proactive d’accompagnement des clients, sécuriser les moments clés de la relation et favoriser l’adoption et la valeur d’usage des solutions.",["Fidélisation","Renouvellement","Proactivité","Valeur d’usage"]),
      (I_GROW,"Développement du capital client","Identifier les opportunités et développer la valeur du portefeuille.","Analyser le potentiel des clients, structurer les actions de développement commercial et adapter les niveaux d’accompagnement aux besoins et aux enjeux économiques.",["Potentiel","Développement","Segmentation","Valeur économique"]),
      (I_STAR,"Recommandation &amp; valorisation des clients","Faire de la satisfaction un levier de confiance et de développement.","Identifier les clients prêts à recommander l’entreprise et développer des dispositifs de références clients, témoignages, communautés et programmes ambassadeurs.",["Références","Ambassadeurs","Témoignages","Communautés"]),
    ],"cl")}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Analyse du portefeuille", "Quatre axes de lecture, pas une typologie figée.", "Un même client peut être à la fois stratégique, fidèle, à fort potentiel et ambassadeur. Ces axes ne sont pas des catégories exclusives : ils se croisent pour éclairer vos décisions.", cls="cl")}
    {cards([
      (None,"Relation et satisfaction","Qualité de la relation, attentes et irritants."),
      (None,"Fidélité et risque","Stabilité de la relation et signaux de départ."),
      (None,"Valeur et potentiel","Contribution économique et opportunités de développement."),
      (None,"Influence et recommandation","Capacité des clients à devenir des références ou des prescripteurs."),
    ],"cl",4)}
    <div class="usecases">
      <h3 class="subhead">La segmentation, un outil de priorisation</h3>
      <p>Mobilisée lorsque les enjeux le justifient, et non de façon systématique, elle aide notamment à :</p>
      <ul class="chips"><li class="chip">Accompagner les clients stratégiques</li><li class="chip">Prioriser la fidélisation en cas de risque de départ</li><li class="chip">Sécuriser les renouvellements</li><li class="chip">Repérer les clients à potentiel</li><li class="chip">Adapter investissements et niveaux de service</li><li class="chip">Gérer une crise ou une forte baisse de satisfaction</li></ul>
    </div>
  </div>
</section>
<section class="band alt" id="cci">
  <div class="wrap">
    <div class="head"><span class="label cl">Modèle d’analyse du portefeuille</span><h2 class="h2">Customer Capital Index (CCI)</h2>
      <p class="hook-lg cl">Mieux comprendre votre portefeuille pour mieux orienter vos décisions.</p>
      <p class="lead">Le Customer Capital Index est un modèle méthodologique proposé par Xpansio pour croiser plusieurs dimensions de la relation client. Il vise à enrichir le diagnostic du portefeuille, identifier les situations nécessitant une attention particulière et orienter les plans d’action.</p>
    </div>
    <div class="dims n5"><div class="dim">Satisfaction</div><div class="dim">Fidélité</div><div class="dim">Risque</div><div class="dim">Potentiel de développement</div><div class="dim">Contribution économique</div></div>
    <p class="note">Les critères d’analyse sont adaptés aux enjeux, aux données disponibles et au modèle économique de chaque entreprise. Le CCI complète vos indicateurs de pilotage du portefeuille, sans les remplacer.</p>
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Pour qui", "Les entreprises qui servent leurs clients en direct.", cls="cl")}
    {targets(["Intégrateurs","ESN","Revendeurs IT","Concessionnaires bureautique","Éditeurs et constructeurs en direct"],"c-cl")}
  </div>
</section>
{cta("Des clients mieux écoutés. Des relations plus solides. Un capital client qui se développe.","Échangeons sur vos enjeux de satisfaction, de fidélisation et de développement de votre portefeuille clients.","Échanger sur votre capital client")}
'''


# ---------- CAS D'USAGE (pages ouvertes depuis les cartes de l'accueil) ----------
def case_page(cls, exp, exp_href, num, title, lead, enjeu, questions, demarche_title, demarche, leviers, leviers_note, benefices, extra="", cta_t="", cta_p=""):
    q = ''.join(f'<li>{x}</li>' for x in questions)
    lv = ''.join(f'<li class="chip">{x}</li>' for x in leviers)
    note = f'<p class="note">{leviers_note}</p>' if leviers_note else ''
    ico = I_NET if cls == "ch" else I_USER
    return f'''
{page_hero([("index.html","Accueil"),(exp_href, exp),(None,"Cas d’usage " + num)], title, lead,
  f'<span class="pill {cls}"><span class="ico {cls}">{ico}</span>Cas d’usage {num} · {exp}</span>', cta_btn="Échanger sur cet enjeu", h1cls=" h1-long")}
<section class="band alt">
  <div class="wrap">
    {head("L’enjeu", enjeu[0], enjeu[1], cls=cls)}
    <ul class="qlist {cls}">{q}</ul>
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("L’approche Xpansio", demarche_title, cls=cls)}
    {demarche}
  </div>
</section>
<section class="band alt">
  <div class="wrap">
    {head("Leviers d’intervention", "Des leviers choisis selon votre contexte.", cls=cls)}
    <ul class="chips lv {cls}">{lv}</ul>
    {note}
    <p class="benef"><b>L’objectif :</b> {benefices}</p>
  </div>
</section>
{extra}
<section class="band{' alt' if extra else ''}">
  <div class="wrap below-x">
    <a class="link {cls}" href="{exp_href}">Voir l’expertise {exp} {ARR}</a>
  </div>
</section>
{cta(cta_t, cta_p, "Échanger sur cet enjeu")}
'''

def numbered(items, cls):
    return f'<ol class="nsteps {cls}">' + ''.join(f'<li><span class="n">0{i+1}</span><p>{x}</p></li>' for i, x in enumerate(items)) + '</ol>'

CAS1 = case_page("ch", "Channel Performance", "experience-channel.html", "01",
  "Vos partenaires sont-ils vraiment engagés ?",
  "Impliquez, accompagnez et valorisez vos partenaires pour construire une relation durable et développer leur engagement.",
  ("L’engagement ne se résume ni aux incentives ni à l’activation commerciale.",
   "Remises, promotions et challenges peuvent stimuler l’activité à court terme. Ils ne suffisent pas à créer un partenariat dans lequel les deux parties ont intérêt à s’investir."),
  ["Que vos partenaires attendent-ils réellement de vous ?", "Sont-ils associés aux réflexions et aux décisions qui concernent le réseau ?",
   "Leur expertise et leurs réussites sont-elles reconnues ?", "Votre accompagnement contribue-t-il au développement de leur activité ?"],
  "Construire l’engagement dans la durée.",
  cards([(I_CHAT,"Écouter","Comprendre les attentes et les besoins du réseau."),
         (I_HANDS,"Impliquer","Associer les partenaires aux réflexions et aux décisions."),
         (I_CAP,"Faire progresser","Former et développer les compétences."),
         (I_STAR,"Reconnaître","Valoriser l’expertise et les réussites des partenaires."),
         (I_NET,"Rassembler","Créer des communautés, clubs et espaces de dialogue."),
         (I_GROW,"Accompagner","Soutenir le développement de leur activité, dans la durée.")],"ch",3),
  ["Écoute du réseau","Comités et groupes de travail partenaires","Parcours de compétences","Dispositifs de reconnaissance","Communautés et clubs","Plans d’accompagnement"],
  "", "passer d’une relation essentiellement transactionnelle à une relation mutuellement bénéfique, fondée sur la confiance et la contribution réciproque.",
  cta_t="Et si vos partenaires devenaient de vrais partenaires ?", cta_p="Échangeons sur l’engagement de votre réseau et les leviers adaptés à votre contexte.")

CAS2 = case_page("ch", "Channel Performance", "experience-channel.html", "02",
  "Quelle valeur apportez-vous à vos partenaires ?",
  "Définissez une proposition de valeur réseau différenciante et traduisez-la en un programme partenaires cohérent.",
  ("Un programme partenaires ne devrait pas commencer par ses niveaux et ses remises.",
   "Avant de définir les niveaux, avantages, remises ou services d’un programme, un fournisseur doit clarifier la valeur spécifique qu’il apporte à son réseau."),
  ["Pourquoi un partenaire aurait-il intérêt à développer son activité avec vous plutôt qu’avec un autre fournisseur ?"],
  "De la proposition de valeur au programme partenaires.",
  numbered(["Analyser les attentes, les critères de choix et les modèles économiques des partenaires.",
            "Identifier les avantages différenciants du fournisseur pour son réseau.",
            "Définir une proposition de valeur crédible, spécifique et adaptée.",
            "La traduire dans un programme partenaires et des initiatives concrètes."],"ch")
  + '''<div class="vs">
      <div class="vs-col ch"><span class="label ch">Votre valeur pour le partenaire</span><p>Rentabilité, développement commercial, revenus récurrents, compétences, différenciation, accompagnement.</p></div>
      <div class="vs-col"><span class="label">La valeur de votre offre pour le client final</span><p>Usages, bénéfices métiers, performance, fiabilité, maîtrise des coûts.</p></div>
    </div>
    <p class="note">Les deux sont liées, mais ne se confondent pas.</p>''',
  ["Rentabilité et développement économique","Revenus récurrents","Génération de demande","Différenciation concurrentielle","Opportunités de services","Formation et accompagnement","Fiabilité et qualité de la relation","Accès à de nouveaux marchés"],
  "Ces leviers sont des exemples, non une liste obligatoire : ils dépendent de votre marché et de vos partenaires.",
  "donner à vos partenaires une raison claire et durable de s’investir avec vous, et un programme qui la rend concrète.",
  cta_t="Votre programme partenaires dit-il pourquoi vous choisir ?", cta_p="Échangeons sur votre proposition de valeur réseau et sa traduction dans votre programme.")

CAS3 = case_page("cl", "Customer Performance", "experience-client.html", "03",
  "Vos clients sont-ils vraiment satisfaits ?",
  "Écoutez vos clients, impliquez-les dans l’amélioration de leur parcours et transformez leurs irritants en actions concrètes.",
  ("L’expérience client ne se limite pas à mesurer la satisfaction.",
   "Elle consiste à comprendre la réalité vécue par les clients et à construire avec eux une meilleure expérience."),
  ["Savez-vous ce que vivent réellement vos clients aux moments clés de la relation ?", "Quels irritants persistent sans être identifiés ?",
   "Vos clients voient-ils les améliorations engagées suite à leurs remarques ?"],
  "Faire du client un acteur de l’amélioration continue.",
  cards([(I_CHAT,"Écouter","Connaître les clients, écouter et mesurer la satisfaction."),
         (I_PATH,"Comprendre","Analyser le parcours client et les moments de vérité, identifier les irritants."),
         (I_HANDS,"Co-construire","Ateliers associant clients et collaborateurs pour prioriser les chantiers."),
         (I_GROW,"Suivre et informer","Suivre les actions et communiquer les progrès réalisés.")],"cl",4)
  + '<p class="note">Une démarche fondée sur la transparence, la confiance et une relation de partenariat avec vos clients.</p>',
  ["Dispositifs d’écoute","Mesure de la satisfaction","Cartographie du parcours","Ateliers clients et équipes","Priorisation des chantiers","Communication des progrès"],
  "", "des clients mieux compris, des irritants traités en priorité et une relation fondée sur la confiance.",
  extra='''<section class="band"><div class="wrap"><div class="xp cl"><span class="label cl">Expérience de la fondatrice</span>
    <p>Agnès Chabrier a conduit des démarches d’écoute, d’analyse des parcours clients et d’amélioration continue dans ses fonctions antérieures de responsable Expérience Client, avant la création d’Xpansio.</p></div></div></section>''',
  cta_t="Et si vos clients vous aidaient à mieux les servir ?", cta_p="Échangeons sur votre dispositif d’écoute et vos priorités d’amélioration.")

CAS4 = case_page("cl", "Customer Performance", "experience-client.html", "04",
  "Connaissez-vous vraiment la valeur de vos clients ?",
  "Identifiez les risques, les potentiels et les priorités pour fidéliser et développer durablement votre capital client.",
  ("La valeur d’un client ne se résume pas à son chiffre d’affaires.",
   "La connaissance du portefeuille est un outil de décision stratégique : elle éclaire la fidélisation, le développement et l’allocation des ressources."),
  ["Quels clients contribuent réellement à votre performance ?", "Lesquels présentent un risque de départ ?", "Où se trouvent vos potentiels de développement ?"],
  "Des indicateurs adaptés, pas une formule standard.",
  cards([(None,"Contribution économique","Rentabilité et poids dans l’activité."),
         (None,"Fidélité et risque","Stabilité de la relation, exposition au départ."),
         (None,"Potentiel","Opportunités de développement."),
         (None,"Influence","Rôle de référence ou de prescripteur."),
         (None,"Importance stratégique","Criticité de la relation pour l’entreprise.")],"cl",5)
  + '<p class="note">Ces dimensions sont des exemples, non des critères systématiques. Xpansio vous aide à définir les indicateurs pertinents, analyser le portefeuille, identifier les priorités et construire les plans d’action.</p>',
  ["Indicateurs du portefeuille","Analyse et segmentation","Priorisation","Plans de fidélisation","Plans de développement"],
  "", "éclairer vos décisions de fidélisation, de développement et d’allocation des ressources.",
  extra='''<section class="band"><div class="wrap"><div class="xp cl"><span class="label cl">Expérience de la fondatrice</span>
    <h3>Quand la crise impose des choix : comment protéger ses relations clients stratégiques ?</h3>
    <p>Lorsqu’une crise affecte fortement la capacité d’une entreprise à satisfaire ses clients, la connaissance du portefeuille devient un outil d’aide aux arbitrages. Dans une expérience professionnelle antérieure, Agnès Chabrier a conçu une segmentation stratégique pour mieux identifier les clients prioritaires dans un contexte de crise d’approvisionnement, en combinant plusieurs dimensions de la valeur client, au-delà du seul chiffre d’affaires.</p>
    <p>Prioriser ne signifie pas abandonner les autres clients : les engagements contractuels, l’équité et les besoins critiques restent pris en compte.</p>
    <p class="lesson"><b>L’enseignement :</b> une bonne connaissance du capital client facilite les arbitrages lorsque les ressources sont limitées.</p></div></div></section>''',
  cta_t="Votre portefeuille clients guide-t-il vos décisions ?", cta_p="Échangeons sur la connaissance de votre capital client et vos priorités.")

def case(i, title, ctx, obj, livr, kpis):
    li = ''.join(f'<li>{x}</li>' for x in livr)
    kp = ''.join(f'<div class="kpi"><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in kpis)
    alt = ' alt' if i % 2 == 0 else ''
    return f'''<section class="band{alt}"><div class="wrap">
  <div class="head"><span class="tag cl">Customer Performance · Solutions bureautiques et IT</span><h2 class="h2">{title}</h2></div>
  <div class="case-cols">
    <div class="case-col"><span class="label">Contexte</span><p>{ctx}</p></div>
    <div class="case-col"><span class="label">Objectif</span><p>{obj}</p></div>
    <div class="case-col"><span class="label">Livrables</span><ul>{li}</ul></div>
  </div>
  <div class="case-kpis">{kp}</div>
</div></section>'''

PROJETS = f'''
{page_hero([("index.html","Accueil"),(None,"Nos projets")], "Nos projets", "Des missions menées pour un acteur national des solutions bureautiques et IT, avec des résultats suivis sur deux ans.", tiles=HT["projets"])}
{case(0,"Programme d’écoute client",
  "Une base installée nationale confrontée à une hausse de l’insatisfaction et des résiliations.",
  "Identifier les irritants clients et les prioriser.",
  ["Enquêtes de satisfaction","Ateliers régionaux réunissant clients et collaborateurs","Cartographie du parcours client","Plan d’action en 7 chantiers"],
  [("7","chantiers identifiés"),("+15&nbsp;pts","de NPS en 2 ans")])}
{case(1,"Analyse de la base client",
  "Une baisse de la rentabilité et des équipes démotivées.",
  "Identifier les clients prioritaires et non rentables, puis mettre en place des plans d’action spécifiques.",
  ["Analyse de la base clients (CRM)","Rentabilité par client (ERP, Power BI)","Segmentation VIP avec le Customer Capital Index","Plans d’action pour les clients non rentables"],
  [("+50&nbsp;%","de rétention sur les clients VIP en 2 ans")])}
{case(2,"Approche Customer Success",
  "Une position fragile sur les ETI et une activité en transformation vers l’IT.",
  "Une équipe de suivi dédiée aux ETI à fort score CCI pour augmenter chiffre d’affaires, lifetime value et fidélité.",
  ["Recrutement d’une équipe de Customer Success Managers","Plans de compte et matrice de risque","Trinôme commercial, technicien, administratif","Pilote de 12 mois, puis déploiement"],
  [("+50&nbsp;%","de rétention en 2 ans"),("+20&nbsp;%","de lifetime value en 2 ans")])}
{cta("Votre projet pourrait être le prochain.","Racontez-nous votre contexte : nous vous dirons comment nous pourrions vous aider.")}
'''

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
    ("expertises.html", "expertises", "Nos expertises · Xpansio", "Channel Performance et Customer Performance : les deux expertises d’Xpansio.", EXPERTISES),
    ("experience-channel.html", "channel", "Channel Performance · Xpansio", "Programmes partenaires, animation de réseaux de distribution, cartographie du channel et parcours partenaire.", CHANNEL),
    ("experience-client.html", "client", "Customer Performance · Xpansio", "Satisfaction et expérience client, fidélisation et développement de la valeur du capital client : l’accompagnement Customer Performance d’Xpansio.", CLIENT),
    ("cas-engagement-partenaires.html", "cas", "Vos partenaires sont-ils vraiment engagés ? · Xpansio", "Développer l’engagement des partenaires : écoute, implication, compétences, reconnaissance et accompagnement dans la durée.", CAS1),
    ("cas-valeur-reseau.html", "cas", "Quelle valeur apportez-vous à vos partenaires ? · Xpansio", "Construire une proposition de valeur réseau différenciante et la traduire en un programme partenaires cohérent.", CAS2),
    ("cas-experience-client.html", "cas", "Vos clients sont-ils vraiment satisfaits ? · Xpansio", "Faire du client un acteur de l’amélioration continue : écoute, parcours, irritants et plans d’amélioration.", CAS3),
    ("cas-valeur-clients.html", "cas", "Connaissez-vous vraiment la valeur de vos clients ? · Xpansio", "Piloter et développer la valeur de son capital client : risques, potentiels et priorités.", CAS4),
    ("projets.html", "projets", "Nos projets · Xpansio", "Projets réalisés par Xpansio et résultats obtenus.", PROJETS),
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
    d = os.path.join(ROOT, "docs")
    open(os.path.join(d, "CNAME"), "w").write("xpansio.fr\n")
    open(os.path.join(d, ".nojekyll"), "w").write("")
    print("ok")
