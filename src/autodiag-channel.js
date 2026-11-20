/* Auto-diagnostic Channel « Ce partenaire est-il vraiment un partenaire performant pour votre réseau ? » : version courte (10 questions) d'un audit de performance partenaire.
   Même fonctionnement que autodiag.js (Customer) : 5 dimensions pondérées, signaux d'alerte, 3 pistes d'action. */
(function(){
  /* ---------- Modèle ---------- */
  var DIMS = [
    {id:"perf", name:"Performance commerciale", w:30},
    {id:"comp", name:"Compétences & qualité de service", w:25},
    {id:"off",  name:"Offre & transformation", w:20},
    {id:"eng",  name:"Engagement & coopération", w:15},
    {id:"fid",  name:"Votre place dans son activité", w:10}
  ];
  // Échelle unique : 0 = mauvais, 2 = insuffisant, 4 = bon, 5 = excellent. c = coefficient.
  // Les questions « comp » et « cli » reprennent les domaines de l'audit qualité de services d'Agnès.
  var Q = [
    {d:"perf", c:3, t:"Atteint-il ses objectifs commerciaux (chiffre d'affaires, volumes, marge) ?",
     o:["Loin des objectifs","Partiellement","Atteints","Dépassés"]},
    {d:"perf", c:2, t:"Comment évolue son activité avec vous sur les 12 derniers mois ?",
     o:["En recul","Stable","En croissance","Plus forte croissance que le reste du réseau"]},
    {d:"comp", c:2, t:"Ses équipes sont-elles formées et certifiées sur vos offres (commerciaux, ingénieurs, support) ?",
     o:["Aucune formation récente","Quelques personnes formées","Les trois équipes sont formées","Certifications à jour à tous les niveaux"]},
    {d:"comp", c:3, t:"Comment est organisé son support client (suivi des demandes, délais, escalades vers vous) ?",
     o:["Peu organisé, escalades fréquentes vers vous","Inégal, délais variables","Organisé, délais respectés","Structuré et mesuré, clients très satisfaits"]},
    {d:"comp", c:1, t:"Supervise-t-il à distance la base installée (prise en main à distance, mises à jour) ?",
     o:["Non","Ponctuellement","Régulièrement","Systématiquement, maintenance proactive"]},
    {d:"off",  c:2, t:"Quelle part de votre catalogue vend-il et sait-il maintenir ?",
     o:["Un ou deux produits","Une gamme principale","Plusieurs gammes, avec les services","Tout le catalogue, services compris"]},
    {d:"off",  c:2, t:"Est-il dans une démarche d'amélioration continue, de transformation de son business et de développement de son activité ?",
     o:["Non, pas vraiment : modèle très traditionnel","Ponctuellement, lorsque c'est nécessaire","Il est au fait des dernières tendances (abonnement, IA)","Il est précurseur dans l'adoption de nouvelles pratiques, pour se développer"]},
    {d:"eng",  c:2, t:"Participe-t-il à vos programmes et événements (témoignages clients, remontée de bonnes pratiques, suggestions d'amélioration…) ?",
     o:["Rarement ou jamais","De temps en temps","Régulièrement","Activement, il y contribue"]},
    {d:"eng",  c:1, t:"Partage-t-il les informations et respecte-t-il vos procédures (prévisions, opportunités, outils) ?",
     o:["Rarement, il faut relancer","Partiellement","Oui, de façon fiable","Oui, et il propose des améliorations"]},
    {d:"fid",  c:2, t:"Êtes-vous incontournable pour lui ?",
     o:["Il vend surtout une offre concurrente","Il vend aussi une offre concurrente, ou des produits compatibles","Fournisseur principal, produits d'origine","Fournisseur exclusif, 100 % d'origine"]}
  ];
  var SCORES=[0,2,4,5];
  var ALERTS=[
    {id:"a1", t:"Il a signé avec un concurrent direct, ou oriente ses clients vers une autre marque."},
    {id:"a2", t:"Plusieurs de ses clients se sont plaints de lui, ou l'ont quitté."},
    {id:"a3", t:"Un dirigeant ou des personnes clés sont partis, ou l'entreprise change d'actionnaire."},
    {id:"a4", t:"Il paie avec des retards répétés, ou son encours augmente."}
  ];
  var TERMS=["Moins de 5 %","5 à 15 %","Plus de 15 %","Je ne sais pas"];
  var TH_OK=70, TH_WARN=50;
  var TH_SOLIDE=65;   // statut global « Partenaire solide » à partir de 65 (les couleurs des dimensions restent : vert ≥ 70, orange 50 à 69)

  var ADVICE={
    perf:"<b>Construire un plan d'affaires commun.</b> Revoyez avec lui ses objectifs, son potentiel et ce qui le freine (ressources, ciblage, offre), puis fixez ensemble 3 ou 4 actions suivies chaque trimestre : comptes cibles, campagnes, appui avant-vente.",
    comp:"<b>Renforcer les compétences et la qualité de service.</b> Faites le point sur les formations et certifications de ses équipes, sur l'organisation de son support et sur la supervision à distance de la base installée, avec une grille d'audit partagée. Pour le client final, la qualité du service du partenaire, c'est la qualité de votre marque.",
    off:"<b>Élargir l'offre et accompagner la transformation.</b> Repérez les gammes et services qu'il ne vend pas encore, et aidez-le à faire évoluer son modèle : abonnement, revenus récurrents, nouveaux usages comme l'IA. Partagez avec lui les pratiques des partenaires les plus avancés du réseau.",
    eng:"<b>Réengager le partenaire.</b> Comprenez ce qui freine sa participation : programme peu adapté à sa taille, manque de temps, sentiment de ne pas être écouté. Associez-le à un club, un pilote ou un groupe de travail, et simplifiez les informations que vous lui demandez.",
    fid:"<b>Renforcer votre place dans son activité.</b> Comprenez pourquoi il vend aussi une offre concurrente ou s'approvisionne ailleurs : marge, disponibilité, prix, relation. Rendez votre offre et votre programme plus attractifs que l'alternative, plutôt que de sanctionner."
  };
  var ALERT_ADVICE={
    a1:"<b>Rencontrer sa direction sans attendre.</b> Écoutez ses raisons sans vous défendre (marge, accompagnement, offre, relation), puis proposez un plan concret pour rester son choix principal.",
    a2:"<b>Protéger les clients concernés.</b> Contactez avec lui les clients mécontents, identifiez les causes et fixez un plan de correction suivi. Si rien ne bouge, prévoyez une solution pour ne pas perdre ces clients.",
    a3:"<b>Reconstruire les liens.</b> Rencontrez rapidement les nouveaux décideurs, rappelez la valeur du partenariat avec des chiffres, et vérifiez que les compétences clés sont toujours là.",
    a4:"<b>Comprendre sa situation financière.</b> Abordez le sujet avec tact, avec votre service crédit : des retards répétés signalent souvent une difficulté ou un désengagement."
  };
  var GOOD=[
    "<b>Ancrer une revue d'affaires régulière.</b> Faites le point chaque trimestre ou chaque semestre sur quelques indicateurs partagés : résultats, compétences, qualité de service, engagement. C'est ce qui permet de détecter tôt le moindre changement.",
    "<b>Étendre le diagnostic à tout votre réseau.</b> Ce partenaire va bien, mais les autres ? Évaluez vos principaux partenaires pour comparer les profils et adapter votre accompagnement à chacun."
  ];
  var KEEP="<b>En faire un partenaire de référence.</b> Ce partenaire est solide : construisez avec lui un plan de croissance ambitieux, proposez-lui des pilotes sur vos nouvelles offres et valorisez sa réussite auprès du réseau.";

  /* ---------- Construction du formulaire ---------- */
  var qBox=document.getElementById("questions");
  DIMS.forEach(function(d){
    var sec=document.createElement("section"); sec.className="card";
    sec.innerHTML="<h2>"+d.name+"</h2>";
    Q.forEach(function(q,i){
      if(q.d!==d.id) return;
      var fs=document.createElement("fieldset");
      var h='<legend><span class="num">'+(i+1)+'.</span>'+q.t+'</legend><div class="opts">';
      q.o.forEach(function(lab,k){
        h+='<div class="opt"><input type="radio" name="q'+i+'" id="q'+i+'_'+k+'" value="'+SCORES[k]+'"><label for="q'+i+'_'+k+'">'+lab+'</label></div>';
      });
      fs.innerHTML=h+'</div>'; sec.appendChild(fs);
    });
    qBox.appendChild(sec);
  });
  var aBox=document.getElementById("alerts");
  ALERTS.forEach(function(a){
    aBox.insertAdjacentHTML("beforeend",'<label><input type="checkbox" name="'+a.id+'"> <span>'+a.t+'</span></label>');
  });
  var tBox=document.getElementById("term");
  TERMS.forEach(function(t,k){
    tBox.insertAdjacentHTML("beforeend",'<div class="opt"><input type="radio" name="term" id="t'+k+'" value="'+k+'"'+(k===3?' checked':'')+'><label for="t'+k+'">'+t+'</label></div>');
  });

  /* ---------- Progression ---------- */
  var form=document.getElementById("diag"), go=document.getElementById("go"), hint=document.getElementById("hint");
  function answered(){ var n=0; Q.forEach(function(q,i){ if(form.querySelector('input[name="q'+i+'"]:checked')) n++; }); return n; }
  function update(){
    var n=answered();
    document.getElementById("pbar").style.width=(n/Q.length*100)+"%";
    document.getElementById("ptext").textContent=n+" / "+Q.length+" questions";
    go.disabled=n<Q.length;
    hint.textContent=n<Q.length?("Encore "+(Q.length-n)+" question"+(Q.length-n>1?"s":"")+" pour obtenir votre résultat."):"C'est prêt !";
  }
  form.addEventListener("change",update);

  /* ---------- Calcul ---------- */
  function color(s){ return s>=TH_OK?"var(--ok)":(s>=TH_WARN?"var(--warn)":"var(--risk)"); }
  form.addEventListener("submit",function(e){
    e.preventDefault(); if(answered()<Q.length) return;
    var num={},den={};
    DIMS.forEach(function(d){num[d.id]=0;den[d.id]=0;});
    Q.forEach(function(q,i){
      var v=Number(form.querySelector('input[name="q'+i+'"]:checked').value);
      num[q.d]+=v*q.c; den[q.d]+=5*q.c;
    });
    var dimScores={};
    DIMS.forEach(function(d){ dimScores[d.id]=num[d.id]/den[d.id]*100; });

    /* Règles de lecture : certaines réponses fixent la couleur d'une dimension (rouge < 50). */
    function opt(i){ return SCORES.indexOf(Number(form.querySelector('input[name="q'+i+'"]:checked').value)); }
    // Le score de la dimension est ramené dans la zone de sa couleur : vert ≥ 70, orange 50 à 69, rouge < 50.
    function band(id,col){
      var v=dimScores[id];
      if(col==="vert") dimScores[id]=Math.max(v,TH_OK);
      else if(col==="orange") dimScores[id]=Math.min(Math.max(v,TH_WARN),TH_OK-1);
      else dimScores[id]=Math.min(v,TH_WARN-1);
    }
    var objectifs=opt(0), evolution=opt(1), catalogue=opt(5), transfo=opt(6), place=opt(9);
    // Performance commerciale : loin des objectifs = rouge, même avec une forte croissance.
    // Objectifs atteints ou dépassés : vert si l'activité est stable ou en croissance, orange si elle recule.
    // Objectifs partiellement atteints : orange, sauf en recul (le calcul habituel s'applique).
    // Grille de profils validée par Agnès (objectifs × évolution sur 12 mois).
    var perfProfil;
    if(objectifs===3 && evolution>=2) perfProfil="1";
    else if(objectifs===2 && evolution>=2) perfProfil="2";
    else if(objectifs>=2 && evolution===1) perfProfil="3";
    else if(objectifs>=2) perfProfil="4";                 // atteints ou dépassés, en recul
    else if(objectifs===1) perfProfil = evolution>=2 ? "5" : (evolution===1 ? "6" : "7");
    else perfProfil = evolution>=2 ? "8" : "9";          // loin des objectifs
    band("perf", {"1":"vert","2":"vert","3":"vert","4":"orange","5":"orange","6":"orange","7":"rouge","8":"rouge","9":"rouge"}[perfProfil]);
    // Compétences & qualité de service : grille de profils validée par Agnès.
    // Le support (Q4) donne le ton, la supervision à distance (Q5) et la formation (Q3) nuancent.
    // Aucune formation récente = jamais vert, avec un point de vigilance.
    var fo=opt(2), su=opt(3), sp=opt(4), compProfil;
    if(su>=2){ compProfil = sp>=2 ? (fo>=2 ? "1" : (fo===1 ? "2a" : "2b")) : "3"; }
    else if(su===1){ compProfil = fo>=2 ? "4" : "5"; }
    else { compProfil = fo>=2 ? "6a" : "6b"; }
    band("comp", {"1":"vert","2a":"vert","2b":"orange","3":"orange","4":"orange","5":"orange","6a":"rouge","6b":"rouge"}[compProfil]);
    // Offre & transformation : rouge seulement si un ou deux produits ET modèle très traditionnel.
    // Plusieurs gammes avec les services ou plus : vert, sauf modèle très traditionnel (orange). Sinon : orange.
    if(catalogue===0 && transfo===0) band("off","rouge");
    else if(catalogue>=2 && transfo!==0) band("off","vert");
    else band("off","orange");
    // Votre place dans son activité : fournisseur principal ou exclusif = vert ; aussi une offre concurrente = orange.
    // Vend surtout une autre marque : orange si ses résultats avec vous sont au rendez-vous (objectifs atteints, ou activité en croissance),
    // rouge s'ils ne le sont pas (objectifs non atteints et pas de croissance).
    var concurrentSansResultats = place===0 && objectifs<=1 && evolution<=1;
    // Vend surtout une offre concurrente et activité stable ou en recul (même si les objectifs sont atteints) : échange avec la direction.
    var directionNeeded = place===0 && evolution<=1;
    if(place===0) band("fid", concurrentSansResultats ? "rouge" : "orange");
    else band("fid", place===1 ? "orange" : "vert");

    var gNum=0,gDen=0;
    DIMS.forEach(function(d){ gNum+=dimScores[d.id]*d.w; gDen+=d.w; });
    var score=Math.round(gNum/gDen);
    var alerts=ALERTS.filter(function(a){return form.querySelector('input[name="'+a.id+'"]').checked;});
    var poids=Number(form.querySelector('input[name="term"]:checked').value);

    /* Statut : le score donne la couleur de départ, puis les règles d'Agnès s'appliquent.
       Alertes « concurrent » (a1) et « paiements » (a4) = À risque d'emblée.
       Alertes « clients mécontents » (a2) et « personnes clés / actionnaire » (a3) = au moins À accompagner (orange). */
    var RISK="var(--risk)", WARN="var(--warn)", OK="var(--ok)";
    var status,txt,col;
    if(score>=TH_SOLIDE){ status="Partenaire solide"; col=OK; txt="Ce partenaire contribue réellement à votre croissance. Restez attentif, et construisez la suite avec lui."; }
    else if(score>=TH_WARN){ status="À accompagner"; col=WARN; txt="Des fragilités apparaissent. Un plan de progrès partagé peut faire de ce partenaire un vrai relais de croissance."; }
    else { status="À risque"; col=RISK; txt="Plusieurs dimensions du partenariat sont dégradées. Sa contribution à votre croissance n'est pas acquise."; }
    // Une dimension clé dans le rouge (performance commerciale, compétences & qualité de service) = risque, quel que soit le score global.
    var rougesCles=["perf","comp"].filter(function(id){ return Math.round(dimScores[id])<TH_WARN; });
    if(status!=="À risque" && rougesCles.length){
      status="À risque"; col=RISK;
      txt="La performance commerciale ou la qualité de service est dans le rouge : même si le reste va bien, le partenariat est fragile.";
    }
    // Une autre dimension dans le rouge (offre, engagement, place dans son activité) : jamais « Partenaire solide », au mieux « À accompagner ».
    if(status==="Partenaire solide" && DIMS.some(function(d){ return Math.round(dimScores[d.id])<TH_WARN; })){
      status="À accompagner"; col=WARN;
      txt="Les résultats d'ensemble sont corrects, mais une dimension est dans le rouge : un plan de progrès est nécessaire pour sécuriser le partenariat.";
    }
    // Objectifs pas encore atteints : jamais « Partenaire solide » (la performance commerciale est la priorité n° 1).
    if(status==="Partenaire solide" && objectifs<=1){
      status="À accompagner"; col=WARN;
      txt="Le partenariat est sain sur la plupart des dimensions, mais ses objectifs commerciaux ne sont pas encore atteints : c'est la priorité à travailler avec lui.";
    }
    // Aucune personne formée sur vos offres : jamais « Partenaire solide » (point de vigilance).
    if(status==="Partenaire solide" && fo===0){
      status="À accompagner"; col=WARN;
      txt="Ses résultats d'ensemble sont bons, mais aucune personne n'est formée sur vos offres : un minimum de compétences validées est indispensable pour sécuriser la qualité chez ses clients.";
    }
    // Vend surtout une autre marque : jamais « Partenaire solide », même avec de bons résultats.
    if(status==="Partenaire solide" && place===0){
      status="À accompagner"; col=WARN;
      txt="Ses résultats d'ensemble sont bons, mais votre place dans son activité reste à conquérir.";
    }
    var has=function(id){ return alerts.some(function(a){return a.id===id;}); };
    if(status!=="À risque" && (has("a1")||has("a4"))){
      status="À risque"; col=RISK;
      txt="Un signal d'alerte majeur est présent (concurrent ou paiements) : quel que soit le score, ce partenaire doit être traité en priorité.";
    } else if(status==="Partenaire solide" && (has("a2")||has("a3"))){
      status="À accompagner"; col=WARN;
      txt="Les résultats sont bons, mais un signal d'alerte appelle votre vigilance : agissez avant qu'il ne pèse sur le partenariat.";
    }

    // Offre concurrente : le commentaire du résultat le dit toujours, selon la dynamique de l'activité.
    if(place===0) txt+= directionNeeded
      ? " Il vend surtout une offre concurrente et son activité avec vous stagne ou recule : un échange avec sa direction s'impose sur ses objectifs et sa motivation."
      : " Il vend surtout une offre concurrente, mais il suit son plan de route avec vous : poursuivez la conquête pour prendre progressivement plus de place dans son activité.";
    /* Priorité : le poids du partenaire accélère ou modère l'urgence. */
    var prio;
    if(status==="Partenaire solide") prio="Priorité : consolider et développer.";
    else if(poids===2) prio=(status==="À risque")?"Priorité : urgente, ce partenaire pèse lourd dans votre chiffre d'affaires.":"Priorité : surveillance urgente, ce partenaire pèse lourd dans votre chiffre d'affaires.";
    else if(poids===0) prio=(status==="À risque")?"Priorité : à prendre en compte, avec un plan de progrès dans les prochains mois. Son poids limité laisse un peu de temps.":"Priorité : à suivre lors de vos prochaines revues.";
    else prio=(status==="À risque")?"Priorité : à traiter rapidement.":"Priorité : plan de progrès dans les prochains mois.";

    document.getElementById("score").textContent=score;
    document.getElementById("gauge").style.background="conic-gradient("+col+" "+(score*3.6)+"deg, var(--line) 0)";
    var st=document.getElementById("status"); st.textContent=status; st.style.background=col;
    document.getElementById("statusText").textContent=txt;
    document.getElementById("priority").textContent=prio;

    var ab=document.getElementById("alertBox");
    ab.innerHTML=alerts.length?('<div class="alert-list"><b>'+alerts.length+' signal'+(alerts.length>1?'s':'')+' d\'alerte</b><ul style="margin:6px 0 0;padding-left:18px">'+alerts.map(function(a){return "<li>"+a.t+"</li>";}).join("")+'</ul></div>'):"";

    var dh="";
    DIMS.forEach(function(d){
      var s=Math.round(dimScores[d.id]);
      dh+='<div class="dim"><div class="lbl"><span>'+d.name+'</span><span>'+s+' / 100</span></div><div class="track"><div class="fill" style="width:'+s+'%;background:'+color(s)+'"></div></div></div>';
    });
    document.getElementById("dims").innerHTML=dh;

    // 3 pistes d'action, par ordre de priorité (règle d'Agnès) :
    //   1. le business : performance commerciale, place dans son activité (offre concurrente) et poids du partenaire ;
    //   2. les compétences et la qualité de service ;
    //   3. l'engagement et la coopération.
    // Dans chaque thème, l'alerte correspondante passe avant le conseil de la dimension.
    // On retient d'abord la première piste de chaque thème (1, puis 2, puis 3), puis on complète dans le même ordre.
    function byGap(a,b){ return (100-dimScores[b.id])*b.w-(100-dimScores[a.id])*a.w; }
    // Les conseils sont construits pour CE diagnostic (copie locale) : rien ne se transmet d'une évaluation à la suivante.
    var A={}; for(var key in ADVICE) A[key]=ADVICE[key];
    if(transfo===0) A.off="<b>Accompagner la transformation de son modèle.</b> Son modèle reste très traditionnel : s'il ne s'adapte pas, son activité est à risque. Aidez-le à faire évoluer son offre et ses pratiques (services, abonnement, revenus récurrents, nouveaux usages comme l'IA), en vous appuyant sur l'exemple des partenaires les plus avancés du réseau.";
    if(place===0) A.fid = directionNeeded
      ? "<b>Rencontrer sa direction sur l'offre concurrente.</b> Il vend surtout une autre marque et son activité avec vous stagne ou recule"+(objectifs>=2?", même si ses objectifs sont atteints":"")+" : échangez avec sa direction sur ses objectifs et sur sa motivation réelle vis-à-vis de votre offre et de l'offre concurrente, pour statuer ensemble sur la suite du partenariat."
      : "<b>Gagner progressivement du terrain chez lui.</b> Il vend surtout une autre marque mais suit son plan de route avec vous : avec votre équipe commerciale, retravaillez vos actions (comptes cibles, argumentaires, offres ciblées, appui avant-vente) pour prendre petit à petit plus de place dans son activité et faire reculer l'offre concurrente.";
    else if(place===1) A.fid="<b>Comprendre la place de l'autre marque chez lui.</b> Il vend aussi une offre concurrente. Échangez avec sa direction, dans un esprit de partenariat, sur les raisons pour lesquelles il conserve cette marque (prix, marge, attentes de ses clients, disponibilité, habitudes) et sur ce que vous pourriez faire ensemble pour reprendre progressivement ce business : offres ciblées, appui avant-vente, conditions adaptées.";
    // Compétences & qualité de service : un commentaire par profil (grille validée par Agnès).
    var VIGIL=" Point de vigilance : aucune personne n'est formée sur vos offres. Une erreur de paramétrage ou d'intervention pourrait avoir des conséquences lourdes chez ses clients : être partenaire suppose un minimum de compétences transmises et validées par vous.";
    A.comp={
      "1":"<b>Valoriser sa qualité de service.</b> Qualité de service solide et compétences en place : un atout à valoriser auprès du réseau (partenaire référent, témoignage).",
      "2a":"<b>Sécuriser les compétences.</b> La qualité de service est au rendez-vous malgré un nombre limité de personnes formées. Le risque porte sur la dépendance à quelques personnes : sécurisez les compétences (formation d'un binôme, certifications), sans urgence.",
      "2b":"<b>Point de vigilance : former ses équipes.</b> La qualité de service est au rendez-vous aujourd'hui, mais aucune personne n'est formée sur vos offres. Une erreur de paramétrage ou d'intervention pourrait avoir des conséquences lourdes chez ses clients. Être partenaire suppose un minimum de compétences transmises et validées par vous : planifiez rapidement les formations et certifications de base.",
      "3":"<b>Passer à une maintenance proactive.</b> Son support est bien organisé, mais il réagit aux incidents plus qu'il ne les anticipe. La supervision à distance, avec une maintenance proactive et des mises à jour automatisées, réduirait les incidents, allégerait son support et, surtout, éviterait des failles de sécurité chez ses clients."+(fo===1?" Formez en priorité ceux qui assurent ce suivi.":"")+(fo===0?VIGIL:""),
      "4":"<b>Fiabiliser son organisation du support.</b> Ses équipes sont formées : le problème vient de l'organisation du support. Revoyez avec lui les effectifs de la hotline, le suivi des demandes, les délais et les règles d'escalade, avec des indicateurs partagés.",
      "5":"<b>Organiser le support et former un binôme.</b> Délais variables et peu de personnes formées : la qualité dépend des disponibilités de quelques-uns. Commencez par l'organisation du support (priorités, suivi des demandes), puis formez un binôme pour ne plus dépendre d'une seule personne."+(fo===0?VIGIL:""),
      "6a":"<b>Désengorger son support en priorité.</b> Des équipes formées mais un support débordé, avec des escalades fréquentes vers vous : c'est un problème d'organisation ou d'effectifs, à traiter en priorité. Fixez ensemble des objectifs de délais et un suivi mensuel.",
      "6b":"<b>Redresser la qualité de service.</b> Support débordé et compétences insuffisantes : vos clients en subissent directement les effets. Un plan de redressement s'impose : objectifs de délais, formation accélérée et, à court terme, appui de vos équipes sur les escalades."+(fo===0?VIGIL:"")
    }[compProfil];
    var compPrio = ["2b","3","4","5","6a","6b"].indexOf(compProfil)>=0;   // profils 1 et 2a : seulement s'il reste de la place
    // Performance commerciale : un commentaire par profil (grille validée par Agnès).
    A.perf={
      "1":"<b>Accélérer avec un moteur du réseau.</b> Il dépasse ses objectifs et accélère : c'est un moteur de votre réseau. Construisez avec lui un plan de croissance ambitieux et proposez-lui des pilotes sur vos nouvelles offres.",
      "2":"<b>Consolider la trajectoire.</b> Il atteint ses objectifs avec une dynamique positive : consolidez avec un plan d'affaires annuel partagé et quelques comptes cibles pour aller plus loin.",
      "3":"<b>Relancer la dynamique.</b> Il tient ses objectifs, mais son activité ne progresse plus : identifiez avec lui de nouveaux relais de croissance (comptes cibles, nouvelles offres, base installée) pour éviter le plafonnement.",
      "4":"<b>Comprendre le recul de son activité.</b> Les objectifs sont encore atteints, mais l'activité recule : comprenez-en les causes avec lui (perte de clients, concurrence, ressources) avant que les résultats ne décrochent.",
      "5":"<b>Soutenir sa progression.</b> Il n'atteint pas encore ses objectifs, mais progresse : maintenez l'effort avec un plan d'affaires commun et un appui ciblé (avant-vente, comptes cibles), et vérifiez que le niveau d'objectifs est réaliste.",
      "6":"<b>Comprendre ce qui freine sa progression.</b> Objectifs partiellement atteints et activité qui stagne : cherchez avec lui pourquoi il ne progresse pas. Regardez ses compétences commerciales (équipe, méthodes, connaissance de vos offres) et sa base clients (couverture, clients inactifs, potentiel inexploité), puis fixez ensemble 3 ou 4 actions suivies chaque trimestre.",
      "7":"<b>Mettre en place un plan de redressement.</b> Objectifs non atteints et activité en recul : la tendance est négative. Mettez en place un plan de redressement avec sa direction : causes, objectifs revus, actions et points d'étape mensuels.",
      "8":"<b>Accompagner la montée en puissance.</b> Il reste loin de ses objectifs malgré une nette progression : la dynamique est encourageante, mais le niveau reste insuffisant. Vérifiez que les objectifs sont réalistes et accompagnez la montée en puissance (plan d'affaires, appui avant-vente).",
      "9":"<b>Rencontrer sa direction sur les résultats.</b> Loin de ses objectifs et sans dynamique : rencontrez sa direction pour comprendre les freins (ressources, ciblage, motivation) et décider d'un plan de redressement ou de la suite à donner au partenariat."
    }[perfProfil];
    var perfPrio = ["4","5","6","7","8","9"].indexOf(perfProfil)>=0;   // profils 2 et 3 : seulement s'il reste de la place ; 1 : couvert par « partenaire de référence »
    // Offre concurrente + rencontre avec la direction : une seule piste, qui intègre le plan de redressement (profils 7 et 9).
    var fusion = place===0 && directionNeeded && (perfProfil==="7" || perfProfil==="9") && !has("a1");
    if(fusion){ A.fid = A.fid + " Bâtissez ensemble un plan de redressement."; perfPrio=false; }
    var weak=function(id){ return dimScores[id]<TH_OK; };
    var B=[], Cq=[], E=[], O=[];
    if(has("a1")) B.push(ALERT_ADVICE.a1);
    var fidAdv = (place===0 && !(has("a1") && directionNeeded)) || (place!==0 && weak("fid")) ? A.fid : null;
    if(fidAdv && fusion) fidAdv=A.fid;
    if(place===0){ if(fidAdv) B.push(fidAdv); if(perfPrio) B.push(A.perf); }   // offre concurrente : c'est elle qui guide le business
    else { if(perfPrio) B.push(A.perf); if(fidAdv) B.push(fidAdv); }
    if(has("a4")) B.push(ALERT_ADVICE.a4);
    if(has("a2")) Cq.push(ALERT_ADVICE.a2);
    if(compPrio) Cq.push(A.comp);
    if(has("a3")) E.push(ALERT_ADVICE.a3);
    if(weak("eng")) E.push(A.eng);
    if(weak("off")) O.push(A.off);
    var top=[];
    function add(x){ if(x && top.length<3 && top.indexOf(x)<0) top.push(x); }
    // Partenaire qui pèse lourd chez vous (plus de 15 % du chiffre d'affaires indirect) : le sujet business devient critique.
    if(B.length && poids===2) B[0]=B[0]+" <b>Ce partenaire pèse lourd dans votre chiffre d'affaires indirect : c'est votre priorité.</b>";
    add(B[0]); add(Cq[0]); add(E[0]);
    B.slice(1).concat(Cq.slice(1), E.slice(1), O).forEach(add);
    if(status==="Partenaire solide"){ add(KEEP); if(perfProfil==="2"||perfProfil==="3") add(A.perf); if(compProfil==="1"||compProfil==="2a") add(A.comp); GOOD.forEach(add); }
    else {
      add(GOOD[0]);
      DIMS.filter(function(d){return !weak(d.id);}).sort(byGap).forEach(function(d){ add(A[d.id]); });
    }
    document.getElementById("advice").innerHTML=top.map(function(a){return "<li>"+a+"</li>";}).join("");

    form.style.display="none";
    document.querySelector(".progress").style.display="none";
    var res=document.getElementById("result"); res.style.display="block";
    res.scrollIntoView({behavior:"smooth"});
  });

  document.getElementById("again").addEventListener("click",function(){
    form.reset(); document.getElementById("t3").checked=true; update();
    document.getElementById("result").style.display="none";
    form.style.display="block"; document.querySelector(".progress").style.display="block";
    window.scrollTo({top:0,behavior:"smooth"});
  });
  update();
})();
