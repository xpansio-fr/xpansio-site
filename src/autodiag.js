/* Auto-diagnostic « Êtes-vous certain que ce client va renouveler ? » : version courte (10 questions) du fichier _sources/auto-diagnostic-sante-client.html : questions 5 et 8 et alerte « décideur insatisfait » retirées à la demande d’Agnès ; libellés de la question 1 et règles de couleur par dimension ajoutés (voir « Règles de lecture »). */
(function(){
  /* ---------- Modèle (version courte du Health Score Xpansio) ---------- */
  var DIMS = [
    {id:"sol", name:"Solutions & adoption", w:25},
    {id:"irr", name:"Irritants", w:20},
    {id:"rel", name:"Relation", w:20},
    {id:"val", name:"Valeur ressentie", w:25},
    {id:"eng", name:"Engagement", w:10}
  ];
  // Échelle unique : 0 = mauvais, 2 = insuffisant, 4 = bon, 5 = excellent. c = coefficient.
  var Q = [
    {d:"sol", c:3, t:"Ce client utilise-t-il vraiment les solutions et services qu'il a achetés ?",
     o:["Très peu ou pas du tout","Une minorité d'utilisateurs concernés l'utilisent","La plupart des utilisateurs potentiels l'utilisent","Intensivement, c'est critique pour lui"]},
    {d:"sol", c:3, t:"Est-il satisfait des solutions et services en place ?",
     o:["Très insatisfait","Moyennement satisfait","Satisfait","Très satisfait"]},
    {d:"sol", c:2, t:"Quelle part de ses besoins IT vous confie-t-il ?",
     o:["Une seule brique, sans service","Une brique + maintenance ou support","Plusieurs briques ou domaines","Vous êtes son partenaire IT global"]},
    {d:"irr", c:3, t:"Comment se passe la résolution de ses incidents techniques ?",
     o:["Incidents qui traînent, sans visibilité","Lente, il doit relancer","Dans les délais","Rapide, il est informé à chaque étape"]},
    {d:"irr", c:2, t:"Comment sont traitées ses demandes administratives (factures, contrat, commandes) ?",
     o:["En retard, nombreuses relances","Avec retard","Dans les délais","Rapidement, sans relance"]},
    {d:"rel", c:2, t:"Quelle est votre relation avec le décideur ?",
     o:["Tendue","Distante, peu de contacts","Bonne","Il vous soutient activement"]},
    {d:"rel", c:1, t:"Avez-vous d'autres soutiens chez ce client (direction, DSI, achats, métiers) ?",
     o:["Aucun contact en dehors du décideur","D'autres contacts, mais neutres","Un soutien","Plusieurs soutiens à différents niveaux"]},
    {d:"val", c:3, t:"Ses objectifs (ceux qui ont motivé l'achat) sont-ils atteints ?",
     o:["Non, il est déçu","Partiellement","Oui","Dépassés"], na:"Aucun objectif n'a été défini"},
    {d:"val", c:2, t:"Quand avez-vous fait le point avec lui sur la valeur apportée (revue de compte) ?",
     o:["Jamais","Il y a plus de 6 mois","Dans les 6 derniers mois","Ce trimestre, chiffres à l'appui"]},
    {d:"eng", c:2, t:"Accepterait-il de vous recommander ?",
     o:["Non","Il accepterait d'être cité","Témoignage écrit ou vidéo","Il interviendrait lors d'un événement"]}
  ];
  var SCORES=[0,2,4,5];
  var ALERTS=[
    {id:"a1", t:"Il a évoqué une résiliation, un appel d'offres ou la consultation d'un concurrent."},
    {id:"a2", t:"Un incident critique reste non résolu, avec un impact sur son activité."},
    {id:"a4", t:"Un nouveau décideur est arrivé, et il ne vous est pas favorable."},
    {id:"a5", t:"Il paie avec des retards répétés, sans litige de votre côté."}
  ];
  var TERMS=["Moins de 6 mois","6 à 12 mois","Plus de 12 mois","Je ne sais pas"];
  var TH_OK=70, TH_WARN=50;

  var ADVICE={
    sol:"<b>Relancer l'adoption.</b> Organisez une session de prise en main avec les utilisateurs clés, partagez les bonnes pratiques et mesurez l'usage réel. Un client qui n'utilise pas ce qu'il paie ne renouvelle pas.",
    irr:"<b>Traiter les causes des retards.</b> Analysez en interne, voire avec le client, les raisons des retards de réponse ou de résolution, puis agissez pour faciliter le traitement : circuit simplifié, interlocuteur identifié, suivi de l'avancement partagé avec le client. Si ce client est important et à potentiel, envisagez de lui dédier un Customer Success Manager.",
    rel:"<b>Élargir et réchauffer la relation.</b> Planifiez un échange avec le décideur centré sur ses enjeux, pas sur vos offres, et identifiez un second soutien (direction, DSI, métiers) pour ne pas dépendre d'un seul interlocuteur.",
    val:"<b>Rendre la valeur visible.</b> Préparez une revue de compte avec des indicateurs concrets : gains, disponibilité, incidents évités, projets livrés. Un client ne valorise que ce qu'on lui montre.",
    eng:"<b>Renforcer l'implication du client.</b> Associez-le davantage : enquête de satisfaction, invitation à un événement, puis, une fois la relation consolidée, proposition de témoignage. Un client impliqué est un client attaché."
  };
  var ALERT_ADVICE={
    a1:"<b>Contre-attaque commerciale immédiate.</b> Le client prépare un départ : rencontrez le décideur rapidement, écoutez ses motifs sans vous défendre, et présentez un plan concret avant la date de décision.",
    a2:"<b>Escalade de l'incident critique.</b> Mobilisez un responsable technique, donnez une date de résolution et appelez vous-même le client à chaque étape. La façon dont vous gérez une crise compte autant que la résolution.",
    a4:"<b>Reconstruire la relation avec le nouveau décideur.</b> Demandez un rendez-vous de présentation, rappelez la valeur apportée jusqu'ici avec des chiffres, et appuyez-vous sur vos autres soutiens dans l'entreprise.",
    a5:"<b>Comprendre les retards de paiement.</b> Ils signalent souvent une difficulté financière ou un désengagement. Abordez le sujet avec tact et vérifiez qu'ils ne cachent pas une insatisfaction."
  };
  var GOOD=[
    "<b>Ancrer un rituel de suivi.</b> Planifiez une revue de compte chaque trimestre ou chaque semestre, avec quelques indicateurs simples : c'est ce qui permet de détecter tôt le moindre changement.",
    "<b>Étendre le diagnostic à tout votre portefeuille.</b> Ce client va bien, mais les autres ? Évaluez vos 20 à 30 premiers comptes pour repérer ceux qui risquent de partir avant leur échéance."
  ];
  var KEEP="<b>Consolider et développer.</b> Ce client est en bonne santé : c'est le moment d'en parler en revue de compte, d'identifier ses prochains projets et de lui proposer d'être client référent.";

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
      h+='</div>';
      if(q.na){ h+='<div class="na"><input type="radio" name="q'+i+'" id="q'+i+'_na" value="na"> <label for="q'+i+'_na">Non applicable : '+q.na+'</label></div>'; }
      fs.innerHTML=h; sec.appendChild(fs);
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
      var v=form.querySelector('input[name="q'+i+'"]:checked').value;
      if(v==="na") return;
      num[q.d]+=Number(v)*q.c; den[q.d]+=5*q.c;
    });
    var dimScores={}, gNum=0, gDen=0;
    DIMS.forEach(function(d){ if(den[d.id]>0) dimScores[d.id]=num[d.id]/den[d.id]*100; });

    /* Règles de lecture (définies par Agnès) : elles fixent la couleur de certaines dimensions,
       le score de la dimension est alors ramené dans la zone de cette couleur (vert ≥ 70, orange 50 à 69, rouge < 50). */
    function opt(i){ var c=form.querySelector('input[name="q'+i+'"]:checked'); return (c&&c.value!=="na")?SCORES.indexOf(Number(c.value)):null; }
    function band(id,col){
      var v=dimScores[id]; if(v===undefined) return;
      if(col==="vert") dimScores[id]=Math.max(v,TH_OK);
      else if(col==="orange") dimScores[id]=Math.min(Math.max(v,TH_WARN),TH_OK-1);
      else dimScores[id]=Math.min(v,TH_WARN-1);
    }
    var usage=opt(0), satisf=opt(1), brique=opt(2), decideur=opt(5), soutiens=opt(6), recommande=opt(9);
    // Solutions & adoption : client satisfait et solutions bien utilisées = vert, même avec une seule brique.
    // Peu utilisées et une seule brique sans service = fragilité (orange) si le client est satisfait, risque (rouge) sinon.
    if(satisf>=2 && usage>=2) band("sol","vert");
    else if(usage<=1 && brique===0) band("sol", satisf>=2 ? "orange" : "rouge");
    // Relation : bonne relation avec le décideur = vert, quels que soient les autres soutiens.
    if(decideur>=2) band("rel","vert");
    else if(decideur===1 && soutiens<=1) band("rel","orange");
    else if(decideur===0 && soutiens<=1) band("rel","rouge");
    // Engagement : refuse d'être cité = rouge ; accepte d'être cité = orange ; témoignage ou plus = vert.
    if(recommande!==null) band("eng", recommande===0 ? "rouge" : (recommande===1 ? "orange" : "vert"));

    DIMS.forEach(function(d){ if(dimScores[d.id]!==undefined){ gNum+=dimScores[d.id]*d.w; gDen+=d.w; } });
    var score=gDen?Math.round(gNum/gDen):0;
    var alerts=ALERTS.filter(function(a){return form.querySelector('input[name="'+a.id+'"]').checked;});
    var term=Number(form.querySelector('input[name="term"]:checked').value);

    var status,txt,col;
    if(alerts.length>0){ status="À risque"; col="var(--risk)";
      txt="Au moins un signal d'alerte est présent : quel que soit le score, ce client doit être traité en priorité."; }
    else if(score>=TH_OK){ status="Sain"; col="var(--ok)"; txt="La relation est solide. Restez attentif, et profitez-en pour développer le compte."; }
    else if(score>=TH_WARN){ status="À surveiller"; col="var(--warn)"; txt="Des fragilités apparaissent. Elles peuvent se transformer en risque si elles ne sont pas traitées."; }
    else { status="À risque"; col="var(--risk)"; txt="Plusieurs dimensions de la relation sont dégradées. Le renouvellement n'est pas acquis."; }

    var prio="";
    if(status==="À risque" && term===0) prio="Priorité : urgente, l'échéance approche.";
    else if(status==="À risque" || (status==="À surveiller" && term===0)) prio="Priorité : à sécuriser rapidement.";
    else if(status==="À surveiller") prio="Priorité : à surveiller dans les prochains mois.";
    else prio="Priorité : consolider et développer.";

    document.getElementById("score").textContent=score;
    document.getElementById("gauge").style.background="conic-gradient("+col+" "+(score*3.6)+"deg, var(--line) 0)";
    var st=document.getElementById("status"); st.textContent=status; st.style.background=col;
    document.getElementById("statusText").textContent=txt;
    document.getElementById("priority").textContent=prio;

    var ab=document.getElementById("alertBox");
    ab.innerHTML=alerts.length?('<div class="alert-list"><b>'+alerts.length+' signal'+(alerts.length>1?'s':'')+' d\'alerte</b><ul style="margin:6px 0 0;padding-left:18px">'+alerts.map(function(a){return "<li>"+a.t+"</li>";}).join("")+'</ul></div>'):"";

    var dh="";
    DIMS.forEach(function(d){
      if(dimScores[d.id]===undefined){ dh+='<div class="dim"><div class="lbl"><span>'+d.name+'</span><span>non évalué</span></div><div class="track"></div></div>'; return; }
      var s=Math.round(dimScores[d.id]);
      dh+='<div class="dim"><div class="lbl"><span>'+d.name+'</span><span>'+s+' / 100</span></div><div class="track"><div class="fill" style="width:'+s+'%;background:'+color(s)+'"></div></div></div>';
    });
    document.getElementById("dims").innerHTML=dh;

    // 3 conseils : alertes d'abord, puis dimensions sous le seuil "Sain" classées par écart pondéré, sinon consolider
    var adv=alerts.map(function(a){return ALERT_ADVICE[a.id];});
    DIMS.filter(function(d){return dimScores[d.id]!==undefined && dimScores[d.id]<TH_OK;})
        .sort(function(a,b){return (100-dimScores[b.id])*b.w-(100-dimScores[a.id])*a.w;})
        .forEach(function(d){adv.push(ADVICE[d.id]);});
    if(adv.length<3) adv.push(KEEP);
    GOOD.forEach(function(g){ if(adv.length<3) adv.push(g); });
    // Retards (incidents lents ou qui traînent, demandes traitées avec retard ou pire) : le conseil sur les irritants figure toujours dans les 3.
    // Il remplace le conseil sur l'engagement s'il y en a un, sinon le dernier conseil qui ne répond pas à une alerte.
    var top=adv.slice(0,3), inc=opt(3), adm=opt(4);
    var retards=(inc!==null && inc<=1) || (adm!==null && adm<=1);
    if(retards && top.indexOf(ADVICE.irr)<0){
      var k=top.indexOf(ADVICE.eng);
      if(k<0){ k=2; for(var m=2;m>=0;m--){ var isAlert=false; alerts.forEach(function(a){ if(ALERT_ADVICE[a.id]===top[m]) isAlert=true; }); if(!isAlert){ k=m; break; } } }
      top[k]=ADVICE.irr;
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
