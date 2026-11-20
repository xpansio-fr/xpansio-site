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
    function rouge(id){ dimScores[id]=Math.min(dimScores[id],TH_WARN-1); }
    if(opt(0)===0) rouge("perf");   // loin des objectifs
    if(opt(3)===0) rouge("comp");   // plaintes ou escalades fréquentes
    if(opt(9)===0) rouge("fid");    // vend surtout une offre concurrente

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
    if(score>=TH_OK){ status="Partenaire solide"; col=OK; txt="Ce partenaire contribue réellement à votre croissance. Restez attentif, et construisez la suite avec lui."; }
    else if(score>=TH_WARN){ status="À accompagner"; col=WARN; txt="Des fragilités apparaissent. Un plan de progrès partagé peut faire de ce partenaire un vrai relais de croissance."; }
    else { status="À risque"; col=RISK; txt="Plusieurs dimensions du partenariat sont dégradées. Sa contribution à votre croissance n'est pas acquise."; }
    // Une dimension clé dans le rouge (performance commerciale, compétences & qualité de service) = risque, quel que soit le score global.
    var rougesCles=["perf","comp"].filter(function(id){ return Math.round(dimScores[id])<TH_WARN; });
    if(status!=="À risque" && rougesCles.length){
      status="À risque"; col=RISK;
      txt="La performance commerciale ou la qualité de service est dans le rouge : même si le reste va bien, le partenariat est fragile.";
    }
    var has=function(id){ return alerts.some(function(a){return a.id===id;}); };
    if(status!=="À risque" && (has("a1")||has("a4"))){
      status="À risque"; col=RISK;
      txt="Un signal d'alerte majeur est présent (concurrent ou paiements) : quel que soit le score, ce partenaire doit être traité en priorité.";
    } else if(status==="Partenaire solide" && (has("a2")||has("a3"))){
      status="À accompagner"; col=WARN;
      txt="Les résultats sont bons, mais un signal d'alerte appelle votre vigilance : agissez avant qu'il ne pèse sur le partenariat.";
    }

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

    // 3 conseils : alertes d'abord, puis dimensions sous le seuil classées par écart pondéré
    function byGap(a,b){ return (100-dimScores[b.id])*b.w-(100-dimScores[a.id])*a.w; }
    var adv=alerts.map(function(a){return ALERT_ADVICE[a.id];});
    DIMS.filter(function(d){return dimScores[d.id]<TH_OK;}).sort(byGap).forEach(function(d){adv.push(ADVICE[d.id]);});
    if(status==="Partenaire solide"){
      if(adv.length<3) adv.push(KEEP);
      GOOD.forEach(function(g){ if(adv.length<3) adv.push(g); });
    } else {
      DIMS.filter(function(d){return dimScores[d.id]>=TH_OK;}).sort(byGap).forEach(function(d){ if(adv.length<3) adv.push(ADVICE[d.id]); });
      if(adv.length<3) adv.push(GOOD[0]);
    }
    document.getElementById("advice").innerHTML=adv.slice(0,3).map(function(a){return "<li>"+a+"</li>";}).join("");

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
