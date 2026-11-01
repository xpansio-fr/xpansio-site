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

def cta(title="Parlons de vos partenaires et de vos clients.", text="Un premier échange de 30 minutes pour faire le point sur vos enjeux, sans engagement."):
    return f'''<section class="band ink"><div class="wrap">
  {head("Contact", title, text)}
  <div class="ctas"><a class="btn btn-white" href="contact.html">Prendre rendez-vous {ARR}</a></div>
</div></section>'''

def page_hero(crumbs, title, lead, extra="", cta_btn=None, tiles=""):
    cr = '<span>/</span>'.join(f'<a href="{h}">{t}</a>' if h else f'<span>{t}</span>' for h, t in crumbs)
    return f'''<section class="page-hero{' has-stack' if tiles else ''}"><div class="wrap">
  <nav class="crumbs" aria-label="Fil d’Ariane">{cr}</nav>
  {extra}
  <h1 class="h1">{title}</h1>
  <p class="lead">{lead}</p>
  {f'<div class="ctas"><a class="btn btn-primary" href="contact.html">{cta_btn} {ARR}</a></div>' if cta_btn else ''}
</div>{tiles}</section>'''

def issues(items):
    return '<div class="issues">' + ''.join(
        f'<div class="issue"><span class="num">0{i+1}</span><b>{t}</b><p>{p}</p></div>' for i, (t, p) in enumerate(items)) + '</div>'

def offers(items, cls):
    out = []
    for ico, t, p, tags in items:
        tg = ''.join(f'<li>{x}</li>' for x in tags)
        out.append(f'<div class="offer {cls}"><span class="ico {cls}">{ico}</span><h3>{t}</h3><p>{p}</p><ul>{tg}</ul></div>')
    return '<div class="offers">' + ''.join(out) + '</div>'

def targets(items, cls):
    return f'<div class="targets {cls}">' + ''.join(f'<span class="target"><i></i>{t}</span>' for t in items) + '</div>'

# ---------- Collage de photos du terrain (haut de page) ----------
# Photos Unsplash (licence Unsplash : usage commercial libre, sans attribution obligatoire).
PHOTOS = {
    "espace": "photo-espace.jpg",          # open space, équipe au travail
    "atelier": "photo-atelier.jpg",        # atelier au tableau
    "travail": "photo-travail.jpg",        # travail en équipe autour d'une table
    "restitution": "photo-restitution.jpg", # restitution devant l'équipe
    "scene": "photo-agnes-scene.jpg",      # Agnès en conférence (logos de l'événement effacés)
    "networking": "photo-networking.jpg",  # soirée d'échanges entre professionnels
    "postit": "photo-atelier-postit.jpg",  # mur de post-it pendant un atelier
    "conversation": "photo-conversation.jpg", # deux personnes qui discutent, lumière chaude
}
def collage(keys, note=None, cls=""):
    """Photos en éventail sous le texte du haut de page. Purement décoratif."""
    imgs = ''.join(f'<span class="ph p{i+1}" style="--i:{i}"><img src="assets/{PHOTOS[k]}" alt="" loading="eager" decoding="async"></span>'
                   for i, k in enumerate(keys))
    n = f'<span class="stack-note"><small>{note[0]}</small>{note[1]}</span>' if note else ''
    return f'<div class="stack n{len(keys)} {cls}" aria-hidden="true">{imgs}{n}</div>'
HT = {
  "expertises": collage(["atelier", "travail", "restitution"], cls="sm"),
  "channel": collage(["restitution", "atelier", "espace"], cls="sm"),
  "client": collage(["espace", "travail", "atelier"], cls="sm"),
  "projets": collage(["travail", "restitution", "espace"], cls="sm"),
  "contact": collage(["atelier", "travail", "espace"], cls="sm"),
}
# Accueil : chaque photo mène au rail de la page qu'elle illustre.
HOME_RAILS = [
    ("scene", "#apropos", "À propos d’Xpansio"),
    ("networking", "#expertises", "Nos expertises"),
    ("postit", "#projets", "Les projets"),
    ("conversation", "#contact", "Échanger sur vos besoins"),
]
def home_collage():
    cards = ''.join(
        f'<a class="ph p{i+1}" href="{h}" style="--i:{i}"><img src="assets/{PHOTOS[k]}" alt="" decoding="async">'
        f'<span class="cap"><span class="n">0{i+1}</span><span class="t">{t}</span>{ARR}</span></a>'
        for i, (k, h, t) in enumerate(HOME_RAILS))
    note = '<span class="stack-note" aria-hidden="true"><small>Du diagnostic</small>À la mise en œuvre</span>'
    return f'<nav class="stack n4 links" aria-label="Parcourir la page">{cards}{note}</nav>'
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
    <h2 class="h2" style="max-width:24ch">Une double connaissance des réseaux de distribution et des enjeux clients.</h2>
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
{page_hero([("index.html","Accueil"),(None,"Nos expertises")], "Nos expertises", "Xpansio intervient sur les deux relations qui font la croissance d’un acteur B2B : celle avec ses partenaires de distribution, et celle avec ses clients.", tiles=HT["expertises"])}
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
  f'<span class="pill ch"><span class="ico ch">{I_NET}</span>Expertise 01</span>', cta_btn="Échangeons sur votre réseau de partenaires", tiles=HT["channel"])}
<section class="band alt">
  <div class="wrap">
    {head("Vos enjeux", "Le marché change plus vite que les réseaux.", cls="ch")}
    {issues([("Un modèle partenaire qui s’essouffle","Les revenus basculent vers les services et les marges hardware diminuent. Les remises et les fonds marketing ne suffisent plus à engager."),
             ("Des partenaires référencés, pas engagés","Une minorité porte l’essentiel du chiffre d’affaires, et les nouvelles offres peinent à être vendues par le réseau."),
             ("Des compétences à faire progresser","Les compétences deviennent le premier facteur de différenciation. Le réseau doit monter en expertise, de façon mesurable.")])}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Ce que nous faisons", "Cinq leviers pour un réseau plus performant.", "Des interventions ciblées ou des missions complètes, selon la maturité de votre programme partenaires.", cls="ch")}
    {offers([
      (I_MAP,"Audit réseau","Diagnostic du programme existant : structure, performance, perception des partenaires et benchmark du marché.",["Cartographie","Voice of Partner","Benchmark"]),
      (I_LAYERS,"Programme partenaires","Création ou refonte de votre programme : niveaux, critères, bénéfices, alignés sur votre stratégie.",["Niveaux","Bénéfices","Incentives"]),
      (I_PATH,"Parcours partenaire","Du recrutement à l’onboarding, au développement et jusqu’au statut d’ambassadeur de votre marque.",["Recrutement","Onboarding","Ambassadeurs"]),
      (I_SPARK,"Animation et roadshows","Plans d’animation du réseau et tournées partenaires pour lancer un programme, une offre ou une stratégie.",["Événements","Challenges","Communautés"]),
      (I_STAR,"Certifications et formations","Des parcours de montée en compétences à valeur ajoutée, reconnus par le marché.",["Certifications","Formations","Expertise"]),
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
<section class="band">
  <div class="wrap">
    {head("Partner Performance Index<sup style='font-size:.4em;font-weight:500'>™</sup>", "La performance de chaque partenaire, en un score.", "Un indice sur 100 pour mesurer la maturité de chaque partenaire et piloter votre réseau.", cls="ch")}
    <div class="dims" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr))"><div class="dim">Business<small>30 % · croissance, offres stratégiques</small></div><div class="dim">Compétences<small>20 % · certifications, expertise</small></div><div class="dim">Excellence<small>20 % · qualité de service, satisfaction client</small></div><div class="dim">Engagement<small>20 % · événements, communautés</small></div><div class="dim">Transformation<small>10 % · nouveaux outils, RSE, cybersécurité</small></div></div>
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
{page_hero([("index.html","Accueil"),("expertises.html","Nos expertises"),(None,"Customer Performance")], "Customer Performance",
  "Vos meilleurs clients valent beaucoup plus que vous ne l’imaginez. Encore faut-il savoir qui ils sont, ce qu’ils vivent et comment les faire grandir avec vous.",
  f'<span class="pill cl"><span class="ico cl">{I_USER}</span>Expertise 02</span>', cta_btn="Échangeons sur votre base clients", tiles=HT["client"])}
<section class="band alt">
  <div class="wrap">
    {head("Vos enjeux", "Tous les clients ne créent pas la même valeur.", cls="cl")}
    {issues([("Un traitement uniforme","Tous les clients sont traités de la même façon, sans distinction de valeur, de risque ni de cycle de renouvellement."),
             ("Une rentabilité inconnue","Les clients rentables, et ceux qui détruisent la marge, ne sont pas identifiés."),
             ("De la réaction plutôt que de l’anticipation","On subit les résiliations au lieu de les prévenir, avec des surcoûts et de l’insatisfaction.")])}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Ce que nous faisons", "Cinq leviers pour développer votre capital client.", "Des missions concrètes, menées avec vos équipes commerciales, techniques et de direction.", cls="cl")}
    {offers([
      (I_PATH,"Parcours client","Modélisation de chaque étape, de la vente au renouvellement, pour repérer les irritants et les moments qui comptent.",["Cartographie","Irritants","Ateliers"]),
      (I_HEART,"Satisfaction client","Un dispositif d’écoute régulier et des plans d’action priorisés, suivis dans le temps.",["NPS et CSAT","Écoute client","Plans d’action"]),
      (I_SEG,"Segmentation client","Identifier vos VIP, vos clients à potentiel, à risque ou non rentables grâce au Customer Capital Index.",["CRM et ERP","Rentabilité","CCI"]),
      (I_SHIELD,"Satisfaction en période de crise","Quand un incident ou une transformation fragilise la relation : écoute rapide, comptes prioritaires, plan de reconquête.",["Écoute d’urgence","Comptes sensibles","Reconquête"]),
      (I_STAR,"Programme VIP et Customer Success","Une organisation dédiée à vos clients stratégiques pour réduire le churn et développer la base installée.",["Plans de comptes","CSM","Gouvernance"]),
    ],"cl")}
  </div>
</section>
<section class="band alt">
  <div class="wrap">
    {head("Segmentation", "Six profils, six stratégies.", cls="cl")}
    <div class="segs">
      <div class="seg"><b>VIP</b><small>Haute valeur, haute fidélité.</small><em>À chouchouter</em></div>
      <div class="seg"><b>Potentiel</b><small>Valeur croissante.</small><em>À développer</em></div>
      <div class="seg"><b>Rentables</b><small>Stables et profitables.</small><em>À fidéliser</em></div>
      <div class="seg"><b>Influents</b><small>Prescripteurs.</small><em>Ambassadeurs à activer</em></div>
      <div class="seg"><b>Destructeurs de marge</b><small>Contrat non rentable.</small><em>Retour à la rentabilité</em></div>
      <div class="seg"><b>À risque</b><small>Insatisfaits ou inactifs.</small><em>À réengager d’urgence</em></div>
    </div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head("Customer Capital Index", "La valeur réelle de chaque client.", "Un score qui ne s’arrête pas au revenu généré, pour prioriser vos investissements commerciaux.", cls="cl")}
    <div class="dims"><div class="dim">Valeur économique<small>Rentabilité, LTV, marge</small></div><div class="dim">Potentiel<small>Cross-sell, upsell</small></div><div class="dim">Fidélité<small>Ancienneté, renouvellement</small></div><div class="dim">Engagement<small>Usage des services</small></div><div class="dim">Influence<small>Recommandations</small></div><div class="dim">Risque<small>Insatisfaction, signaux faibles</small></div></div>
  </div>
</section>
<section class="band alt">
  <div class="wrap">
    {head("Pour qui", "Les entreprises qui servent leurs clients en direct.", cls="cl")}
    {targets(["Intégrateurs","ESN","Revendeurs IT","Concessionnaires bureautique","Éditeurs et constructeurs en direct"],"c-cl")}
  </div>
</section>
{cta("Vos futurs revenus sont déjà chez vos clients.","Parlons de votre base installée, de vos clients prioritaires et de vos objectifs de fidélisation.")}
'''

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
{page_hero([("index.html","Accueil"),(None,"Contact")], "Alors, on travaille ensemble ?", "Un premier échange de 30 minutes pour comprendre vos enjeux, sans engagement. Réponse sous 48 heures ouvrées.", tiles=HT["contact"])}
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
    ("experience-client.html", "client", "Customer Performance · Xpansio", "Parcours client, satisfaction, segmentation et gestion de la satisfaction en période de crise.", CLIENT),
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
