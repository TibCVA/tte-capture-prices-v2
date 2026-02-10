"""TTE Slides methodology content + SPEC_0 normative rules.

Verbatim text extracted from:
- docs/TTE Slides content 1.docx (Slides 1-13, Q1+Q2)
- docs/TTE Slides content 2.docx (Slides 14-33, Q3+Q4+Q5+Architecture+Pays)
- docs/specs/SPEC_0_normative.md
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Slide 1 — Contexte general et 5 questions
# ---------------------------------------------------------------------------
SLIDES_CONTEXT_INTRO = """\
Slide 1 -- Contexte et 5 questions a traiter

Nous voulons expliquer la dynamique des capture prices des renouvelables intermittents \
en restant sur une approche simple, auditable et utile pour la decision.

Nous traitons 5 questions, dans l'ordre logique des phases de marche.

Bascule phase 1 vers phase 2 : Quels parametres font passer un marche d'un regime \
"confortable" a un regime ou les prix et la valeur des actifs deviennent structurellement \
sous pression. Quels ratios simples expliquent la bascule.

Pente en phase 2 : A quelle vitesse la valeur captee se degrade en phase 2. Quels facteurs \
expliquent cette vitesse et pourquoi elle differe selon les pays.

Sortie de la phase 2 et entree en phase 3 : A quelles conditions la dynamique cesse de \
s'aggraver et commence a se stabiliser. Que faudrait-il pour inverser la tendance.

Role du stockage batteries couple au solaire : Quel niveau de batteries associe au solaire \
change reellement la trajectoire. Comment cette condition depend du cout des batteries, du \
prix du CO2 et du role residuel du thermique.

Impact des commodites et du CO2 : Comment le prix du gaz et le prix du CO2 modifient l'ancre \
des prix et donc les capture prices. Quel niveau de CO2 peut relever le haut de la courbe de prix.
"""

# ---------------------------------------------------------------------------
# Slides 2-7 — Q1 : Passage Phase 1 vers Phase 2
# ---------------------------------------------------------------------------
SLIDES_Q1_METHODOLOGY = """\
Slide 2 -- Question 1 Definition

Question 1. Quels parametres expliquent le passage de la phase de marche 1 a la phase de marche 2.

Definition des phases de marche, en langage simple.
La phase 1 est une situation ou l'electricite renouvelable variable ne change pas encore le \
fonctionnement du marche de facon visible et repetee. La phase 2 est une situation ou la \
production variable cree regulierement des heures de prix tres bas ou negatifs et ou la valeur \
moyenne captee par ces actifs baisse de facon mesurable.

Definitions necessaires.
Le "capture price" d'une filiere est le prix moyen recu pendant les heures ou elle produit, \
pondere par sa production horaire.
Le "capture ratio" est le capture price divise par le prix moyen de marche sur la meme periode.
Un "prix negatif" est un prix day ahead inferieur a zero.
Un "surplus" est une situation ou, sur une heure donnee, la production inflexible plus la \
production renouvelable variable depasse ce que le systeme peut absorber via la demande et les \
flexibilites disponibles.
Le "ratio d'inflexibilite" (IR) est la part de production inflexible par rapport a la demande \
durant les heures creuses, ce qui mesure la rigidite du systeme.
Le "ratio de surplus" (SR) est la part d'energie qui apparait en surplus sur l'annee par rapport \
a l'energie totale produite.
Le "ratio d'absorption par flexibilite" (FAR) est la part de ce surplus que le systeme peut \
absorber via des leviers identifiables comme exportations, pompage, charge batteries et effacements.

Objet de l'analyse pour Q1.
Nous voulons passer d'un constat "il y a des prix negatifs" a une regle simple du type "la \
bascule se produit quand une combinaison de surplus, rigidite et faible capacite d'absorption \
devient recurrente et se reflete dans la distribution des prix et dans le capture ratio".

---

Slide 3 -- Question 1 Hypotheses

Hypothese centrale.
La phase 1 se transforme en phase 2 quand les episodes de surplus deviennent suffisamment \
frequents pour modifier la distribution des prix et donc la valeur captee par le solaire et l'eolien.

Hypotheses minimales a tester :

H1.1. La bascule est d'abord un phenomene physique. Elle commence quand la frequence des heures \
de surplus depasse un niveau qui n'est plus marginal.

H1.2. La bascule arrive plus tot si le systeme est rigide. Un ratio d'inflexibilite eleve \
reduit l'espace disponible pour absorber la production variable en heures creuses.

H1.3. La bascule arrive plus tot si les capacites d'absorption sont limitees. Un ratio \
d'absorption par flexibilite faible signifie que le surplus se transforme en contrainte de marche.

H1.4. La bascule est plus tardive si la production variable est bien alignee avec la demande. \
Une forte correlation horaire entre production solaire et demande reduit les surplus.

H1.5. La bascule depend aussi des regles et incitations. Si des volumes importants sont \
developpes et injectes sans exposition au signal de prix, la phase 2 peut demarrer plus tot ou \
durer plus longtemps car l'investissement ne se freine pas naturellement.

---

Slide 4 -- Question 1 Tests empiriques

Objectif des tests.
Construire une regle de bascule verifiable et replicable, basee sur des donnees observees et \
sur des definitions physiques simples.

Jeu de tests simple, en trois blocs.

Bloc A. Construire les indicateurs physiques par pays et par annee.
Nous calculons heure par heure un indicateur de demande residuelle, qui correspond a la demande \
moins la production variable moins la production inflexible.
Nous identifions les heures ou cette demande residuelle devient negative, ce qui signale un \
surplus potentiel.
Nous mesurons le ratio de surplus annuel et le ratio d'inflexibilite sur les heures creuses.

Bloc B. Confronter les indicateurs physiques aux signaux de marche.
Nous comptons le nombre d'heures de prix negatifs et le nombre d'heures de prix tres bas.
Nous calculons le capture ratio solaire et le capture ratio eolien.
Nous verifions que la bascule vers la phase 2 se manifeste a la fois dans les prix et dans la \
valeur captee, et pas uniquement dans un seul indicateur.

Bloc C. Identifier un seuil robuste.
Nous cherchons un point de rupture statistique, par exemple une acceleration du nombre d'heures \
negatives ou une chute du capture ratio au-dela d'un certain niveau de ratio de surplus.
Nous validons le seuil en comparant plusieurs pays et en verifiant qu'il se retrouve avec une \
logique coherente, meme si les valeurs exactes different.

Critere de reussite.
Nous obtenons une regle de bascule qui explique correctement le passage phase 1 a phase 2 sur \
plusieurs pays, et qui reste stable quand on change legerement la periode historique.

---

Slide 5 -- Question 1 Scenarios prospectifs

Pourquoi des scenarios sont necessaires pour Q1.
Le passe ne suffit pas. Nous devons tester comment un pays bascule quand la penetration \
renouvelable continue d'augmenter et quand la demande ou la flexibilite changent.

Principe de scenarisation pragmatique.
Nous ne cherchons pas a simuler un dispatch complet optimise.
Nous cherchons a projeter des ordres de grandeur credibles, avec une logique explicable, \
en faisant varier quelques variables exogenes.

Variables exogenes minimales pour scenarios de bascule.
La trajectoire de demande electrique, avec une hypothese haute et basse.
La trajectoire de capacites solaires et eoliennes.
La trajectoire de production inflexible, ou au minimum sa rigidite en heures creuses.
La trajectoire de capacite d'absorption, via export, pompage, batteries et effacements.
Une hypothese de cadre d'incitation, qui represente la part de nouvelles capacites developpees \
sans exposition forte au prix spot.

Ce que l'on doit obtenir en sortie.
Une annee de bascule probable pour chaque pays et chaque trajectoire.
Une explication causale sous forme de ratios simples qui changent de valeur avant la bascule.

---

Slide 6 -- Question 1 Limites et points de vigilance

Limites structurelles si on reste volontairement simple.

L1.1. Les donnees ne captent pas toutes les flexibilites reelles. Certaines flexibilites sont \
infra horaires ou ne sont pas observables simplement.

L1.2. La correlation n'est pas une preuve de causalite. Une bascule observee peut etre acceleree \
ou freinee par des facteurs non modelises comme des changements de regles de marche.

L1.3. Le role des incitations peut etre determinant. Si l'investissement est guide par des \
mecanismes politiques et non par le marche, une regle purement physique peut sous estimer la \
duree de la phase 2.

L1.4. Les interconnexions peuvent masquer le probleme. Un pays peut absorber son surplus par \
export, mais cela depend de la situation simultanee des voisins.

L1.5. Les annees atypiques peuvent fausser les seuils. Nous devons isoler les chocs extremes \
et tester la stabilite.

Consequence de ces limites.
La bascule doit etre presentee comme une estimation robuste a grosse maille, pas comme une \
date exacte au mois pres.

---

Slide 7 -- Question 1 Livrable attendu

Livrable principal.
Un jeu de "regles de bascule" auditable qui explique le passage de la phase de marche 1 a la \
phase de marche 2.

Contenu concret du livrable.
Nous fournissons une definition claire et unique des phases de marche 1 et 2.
Nous fournissons une liste courte de ratios et une formule de bascule, comprehensible et calculable.
Nous fournissons une justification empirique par pays, basee sur donnees historiques.
Nous fournissons une estimation de seuils de bascule, avec une fourchette et un niveau de confiance.
Nous fournissons un diagnostic des leviers les plus efficaces pour retarder la bascule, en \
distinguant demande, flexibilite et rigidite du parc.

Format de restitution.
Une note courte et structuree.
Un ensemble de graphiques simples et repetables.
Un fichier de calcul permettant de recalculer les ratios avec de nouvelles hypotheses.
"""

# ---------------------------------------------------------------------------
# Slides 8-13 — Q2 : Pente de la Phase 2
# ---------------------------------------------------------------------------
SLIDES_Q2_METHODOLOGY = """\
Slide 8 -- Question 2 Definition

Question 2. Quelle est la pente de la phase de marche 2 et quels facteurs la pilotent.

Definition operationnelle de la "pente".
La pente mesure la vitesse a laquelle la valeur captee se degrade quand la penetration des \
renouvelables variables augmente dans un marche deja entre en phase 2.

Definitions necessaires.
Le "capture price" est le prix moyen recu pendant les heures de production d'une filiere, \
pondere par sa production horaire.
Le "capture ratio" est le capture price divise par le prix moyen de marche.
La "penetration" d'une filiere est sa part dans la production totale sur une annee.
L'"ancre thermique des prix" (TTL) est un niveau de prix representatif des heures ou le \
thermique fixe le prix, et il depend surtout du cout du gaz et du prix du CO2.
Le "ratio de surplus" (SR) mesure le volume annuel de surplus rapporte a la production totale.
Le "ratio d'absorption par flexibilite" (FAR) mesure la fraction du surplus absorbee par des \
leviers identifiables.

Mesures possibles de pente, a choisir explicitement.
Nous pouvons mesurer la pente du capture ratio solaire en fonction de la penetration solaire.
Nous pouvons mesurer la pente du nombre d'heures de prix negatifs en fonction de la penetration.
Nous pouvons mesurer la pente de la profondeur des prix negatifs.

Sortie attendue.
Une estimation chiffree de la pente, par pays, avec une explication causale simple des ecarts \
entre pays.

---

Slide 9 -- Question 2 Hypotheses

Hypothese generale.
En phase 2, la pente est pilotee par deux effets qui se cumulent. Le premier effet est \
l'augmentation de la frequence des heures de prix tres bas. Le second effet est la baisse de \
la valeur moyenne captee car la production se concentre sur ces heures.

Hypotheses explicatives de la pente :

H2.1. La pente est plus forte si la production solaire est peu correlee a la demande. Une faible \
correlation augmente les surplus a midi et donc accelere la chute du capture ratio.

H2.2. La pente est plus forte si le systeme est rigide. Un ratio d'inflexibilite eleve reduit \
les marges d'absorption en heures creuses et accelere les heures de prix negatifs.

H2.3. La pente est plus faible si la flexibilite croit vite. Un ratio d'absorption par \
flexibilite eleve reduit la frequence et l'intensite des episodes de prix extremes.

H2.4. La pente depend de l'ancre thermique. Si le cout marginal thermique est eleve, la \
difference entre heures cheres et heures en surplus peut etre plus grande, ce qui peut amplifier \
la cannibalisation en valeur relative.

H2.5. La pente depend des regles d'investissement. Si une grande partie des nouvelles capacites \
est developpee avec une protection hors marche, l'investissement peut continuer malgre des \
signaux spot degrades, ce qui accentue la pente et prolonge la phase 2.

---

Slide 10 -- Question 2 Tests empiriques

Objectif des tests.
Mesurer la pente de facon robuste et expliquer sa variance entre pays par un petit nombre de \
drivers testables.

Test 1. Estimer la pente en phase 2 de maniere simple.
Nous identifions les annees ou un pays est en phase 2 avec des criteres explicites.
Nous regressons le capture ratio solaire sur la penetration solaire sur ces annees.
Nous exprimons la pente en points de capture ratio perdus par point de penetration ajoute.

Test 2. Verifier que la pente n'est pas un artefact d'ancre thermique.
Nous recalculons la pente en controlant l'ancre thermique des prix, qui depend du gaz et du CO2.
Nous distinguons la baisse de valeur due a plus de surplus de la baisse de valeur due a une \
ancre thermique qui change.

Test 3. Expliquer la pente par des drivers simples.
Nous testons si la pente est correlee au ratio de surplus et au ratio d'inflexibilite.
Nous testons si la pente est correlee au ratio d'absorption par flexibilite.
Nous testons si la pente est correlee a un indicateur de correlation production solaire et demande.

Test 4. Tests de robustesse.
Nous excluons les annees de crise et nous verifions si la pente reste du meme ordre de grandeur.
Nous testons la stabilite du resultat si on change la periode et si on change le pays de reference.

---

Slide 11 -- Question 2 Scenarios prospectifs et leviers

Pourquoi faire des scenarios pour la pente.
Meme si la pente est mesuree sur l'historique, elle peut changer si la flexibilite se developpe \
ou si les regles d'investissement changent.

Scenarios simples a construire.
Scenario A. Demande faible et forte croissance solaire. La pente doit s'accentuer si la \
flexibilite ne suit pas.
Scenario B. Demande dynamique via electrification. La pente peut se reduire si les heures de \
surplus diminuent.
Scenario C. Acceleration stockage et effacement. La pente se reduit si le ratio d'absorption \
par flexibilite augmente vite.
Scenario D. Choc gaz et CO2. L'ancre thermique augmente et change la valeur relative, meme si \
le surplus ne change pas.
Scenario E. Maintien d'incitations hors marche sur de gros volumes. La pente peut rester forte \
car l'investissement ne se freine pas naturellement.

Leviers a relier directement aux drivers.
Le levier "flexibilite" agit sur le ratio d'absorption par flexibilite.
Le levier "pilotabilite" agit sur le ratio d'inflexibilite.
Le levier "politique et regles de soutien" agit sur la trajectoire d'investissement et donc \
sur la vitesse d'augmentation de la penetration.

---

Slide 12 -- Question 2 Limites et regles d'interpretation

L2.1. La pente observee sur dix ans peut refleter plusieurs regimes differents. Le marche peut \
changer de regles au milieu de la periode.

L2.2. La pente peut dependre d'effets voisins. L'absorption par export depend aussi de la \
situation simultanee des pays interconnectes.

L2.3. Les incitations politiques sont difficiles a quantifier sans une variable dediee. Si on \
ne modelise pas ce facteur, on peut mal expliquer la duree de phase 2.

L2.4. Une pente statistique n'est pas une loi physique. Elle doit etre interpretee comme un \
ordre de grandeur conditionnel.

Regles de lecture a imposer.
Nous presentons toujours une pente avec un intervalle d'incertitude.
Nous explicitons les annees exclues et la raison.
Nous relions chaque pente a des variables explicatives mesurables, sinon elle n'est pas actionnable.

---

Slide 13 -- Question 2 Livrable attendu

Livrable principal.
Un diagnostic chiffre de la pente en phase 2, et une explication simple des facteurs qui la \
pilotent.

Contenu concret du livrable.
Nous fournissons, par pays, une pente du capture ratio solaire et une pente du capture ratio \
eolien en phase 2.
Nous fournissons une decomposition qualitative et si possible quantitative des drivers, avec un \
ordre de grandeur par driver.
Nous fournissons une lecture operationnelle pour TTE, sous forme de regles simples.
Nous fournissons une analyse de sensibilite a l'ancre thermique via gaz et CO2, car cette ancre \
change le niveau de valeur meme si la cannibalisation relative reste identique.
Nous fournissons un ensemble de scenarios standards pour projeter la pente sur 5 a 10 ans, sans \
faire un modele d'equilibre complexe.

Format de restitution.
Une note structuree.
Un set de graphiques repetes a l'identique pour chaque pays.
Un fichier de calcul pour recalculer les pentes et tester des hypotheses.
"""

# ---------------------------------------------------------------------------
# Slides 14-19 — Q3 : Sortie de Phase 2
# ---------------------------------------------------------------------------
SLIDES_Q3_METHODOLOGY = """\
Slide 14 -- Question 3 (Phase 2 -> Phase 3) -- Definition precise du probleme

La question vise a definir quand et pourquoi un marche sort de la Phase 2 (degradation active \
de la valeur captee par le PV et montee des prix tres bas et negatifs) pour entrer en Phase 3, \
ou le systeme "s'auto-adapte" et ou certains signaux de stress cessent d'empirer, voire \
commencent a se stabiliser.

Definitions cles a rappeler systematiquement. Le capture price PV est le prix moyen pondere par \
la production PV. Le capture ratio PV est le capture price PV divise par le prix moyen "baseload" \
sur la meme periode. Un ratio inferieur a 1 signifie que le PV produit plus souvent quand les \
prix sont bas. Le Surplus Ratio (SR) mesure la frequence et l'ampleur des heures ou la production \
non pilotable excede la demande instantanee. Le Flex Absorption Ratio (FAR) mesure la part de ce \
surplus qui est absorbee par des "puits" de flexibilite (stockage, export, effacements). \
L'Inflexibility Ratio (IR) mesure la rigidite de la production non pilotable en heures creuses \
par rapport a la demande creuse. Le Thermal Tail Level (TTL) represente un niveau de prix eleve \
typique des heures "thermiques" qui sert d'ancre economique hors surplus.

Definition operationnelle de la bascule Phase 2 -> Phase 3. La bascule n'est pas un jugement \
qualitatif. C'est un ensemble de criteres observables et testables qui montrent qu'un ou \
plusieurs mecanismes d'adaptation prennent le dessus sur l'augmentation mecanique du surplus.

---

Slide 15 -- Question 3 -- Hypotheses structurantes

H3.1. La Phase 3 commence quand la croissance de la flexibilite utile depasse durablement la \
croissance du surplus. "Le systeme ajoute plus de capacite a absorber que de capacite a surproduire".

H3.2. Le meilleur signal "pedestre" n'est pas un niveau de prix, mais une combinaison de tendance. \
La Phase 3 est credible si la tendance des heures a prix tres bas ou negatifs s'inflechit, tout \
en observant que la penetration VRE continue de croitre.

H3.3. Le mecanisme d'adaptation peut venir de plusieurs leviers, et il faut les separer pour ne \
pas confondre les causes : hausse de la demande utile aux bonnes heures, hausse de flexibilite, \
reduction de rigidite, recours plus systematique au curtailment, amelioration des interconnexions.

H3.4. Si l'IR est eleve, la Phase 3 est plus difficile a atteindre car une partie du surplus \
est "structurelle" et non liee au PV. L'adaptation ne peut pas reposer uniquement sur des \
batteries couplees au PV.

---

Slide 16 -- Question 3 -- Tests empiriques

T3.1. Detection d'un retournement de tendance. On calcule, par pays et par annee, le nombre \
d'heures a prix negatifs et le nombre d'heures sous un seuil tres bas. On teste si la pente sur \
3 ans devient negative alors que la penetration VRE continue de monter.

T3.2. Test de coherence economique. On verifie que la baisse des heures negatives n'est pas due \
a un choc exogene temporaire. On exclut les annees "anormales" ou on les traite a part. On exige \
un signal sur plusieurs annees consecutives.

T3.3. Decomposition par leviers. On relie le retournement a des variables explicatives simples. \
On compare l'evolution de SR, FAR, IR et des capacites plausibles de flexibilite. Si le \
retournement est observe alors que SR continue d'augmenter et que FAR n'augmente pas, l'hypothese \
"flex" est fragile.

T3.4. Test "capture ratio". On observe si la pente de degradation du capture ratio PV cesse de \
s'aggraver quand les signaux de surplus se stabilisent. La Phase 3 est credible si la degradation \
ralentit parce que la distribution des prix en heures PV se redresse.

---

Slide 17 -- Question 3 -- Scenarios prospectifs

Objectif des scenarios. Les scenarios ne cherchent pas a "prevoir le spot". Ils servent a tester \
des conditions de bascule.

S3.A "Demande utile". On augmente la demande annuelle et surtout la demande sur les heures de \
surplus PV. On observe l'effet sur SR et sur le capture ratio PV.

S3.B "Flex". On augmente les puits de flexibilite (batteries, pompage, effacement) et on mesure \
l'impact sur FAR, sur la frequence des heures negatives, et sur le capture ratio PV.

S3.C "Moins de rigidite". On reduit le must-run effectif en creux ou on augmente sa modulation, \
ce qui diminue IR. On mesure l'impact sur SR et sur la probabilite de prix negatifs.

S3.D "Interconnexions et export". On teste une capacite d'export additionnelle, en restant \
prudent sur la synchronisation des surplus entre pays.

---

Slide 18 -- Question 3 -- Limites et points d'attention

L3.1. Endogeneite. En realite, la montee de la flex est souvent une reponse au stress. Un simple \
lien statistique ne prouve pas le mecanisme causal. Il faut trianguler avec des evenements \
concrets et des ordres de grandeur.

L3.2. Confusion entre adaptation et choc temporaire. Un retournement peut venir d'une meteo \
atypique, d'une crise combustible, ou d'un evenement systeme. Il faut donc exiger un signal sur \
plusieurs annees et sur plusieurs indicateurs.

L3.3. Mesure imparfaite de la flexibilite. Certaines flexibilites sont peu visibles dans les \
donnees publiques. Cela peut biaiser l'estimation du FAR.

L3.4. Synchronisation regionale. Les interconnexions ne sont une soupape que si les surplus ne \
sont pas simultanes. C'est une hypothese a tester pays par pays.

---

Slide 19 -- Question 3 -- Livrable attendu

Livrable principal. Une fiche "regles de bascule Phase 2 -> Phase 3" par pays, avec des criteres \
simples, chiffres, et une logique d'attribution des causes.

Contenu minimal de la fiche. La fiche explicite un seuil de FAR durable, une condition sur la \
tendance des heures negatives, et une lecture conjointe SR-IR pour distinguer "surplus PV" et \
"surplus structurel".

Livrable "inversion". Un mini-calculateur qui repond a "Que faudrait-il pour inverser la \
trajectoire". Il donne des ordres de grandeur : hausse de demande ciblee, baisse de rigidite, \
ou ajout de flexibilite en impact sur SR, FAR et capture ratio PV.
"""

# ---------------------------------------------------------------------------
# Slides 20-25 — Q4 : Batteries
# ---------------------------------------------------------------------------
SLIDES_Q4_METHODOLOGY = """\
Slide 20 -- Question 4 (Batteries) -- Definition precise du probleme

La question vise a quantifier combien de batteries il faut pour "neutraliser" la degradation de \
valeur liee au surplus, et comment ce besoin depend du cout des batteries, du CO2, et du role \
residuel du thermique. On exprime le besoin de batteries comme une combinaison de puissance et \
d'energie.

Definitions cles. Une batterie se caracterise par une puissance (GW) et une energie (GWh). La \
duree equivalente est l'energie divisee par la puissance. Le rendement aller-retour reduit \
l'energie utile restituee. Le FAR mesure la part du surplus absorbee par des puits, dont la \
batterie. Le SR mesure l'ampleur du surplus a absorber. L'IR reflete la rigidite qui peut creer \
un surplus meme sans PV. Le TTL est un repere de prix eleve sur heures "thermiques" qui \
conditionne le spread et donc la valeur economique du stockage.

Definition operationnelle du "bon niveau". Le bon niveau de batteries n'est pas "zero heure \
negative". C'est un compromis defini par un critere business explicite, par exemple stabiliser \
le capture ratio PV au-dessus d'un seuil, ou reduire les heures negatives sous un certain niveau.

---

Slide 21 -- Question 4 -- Hypotheses structurantes

H4.1. Les batteries ameliorent le capture ratio PV si elles chargent majoritairement pendant les \
heures PV a bas prix et dechargent pendant les heures non-PV a prix plus eleve.

H4.2. Les batteries reduisent les heures negatives si elles agissent comme un puits pendant les \
heures ou SR est materialise en prix negatif. Cette efficacite depend de la concordance horaire \
entre surplus PV et disponibilite de charge.

H4.3. Rendements decroissants. Au-dela d'un certain niveau, ajouter des batteries reduit peu les \
heures negatives car le surplus restant est soit trop long, soit trop simultane a l'echelle \
regionale, soit d'origine structurelle liee a un IR eleve.

H4.4. Le CO2 et le gaz modifient surtout l'interet economique des batteries via les spreads, \
plus que la physique du surplus. Le SR et l'IR ne changent pas parce que le CO2 change.

---

Slide 22 -- Question 4 -- Tests empiriques

T4.1. Adequation physique simple. On simule un comportement de batterie volontairement simple \
et transparent. La batterie charge pendant les heures de surplus PV, sous contrainte de puissance \
et d'etat de charge. Elle decharge pendant des heures non-surplus, avec une regle fixe et \
explicable. On mesure l'effet sur FAR, sur le nombre d'heures negatives, et sur le capture ratio PV.

T4.2. Courbe de rendement decroissant. On repete le test pour plusieurs tailles de batteries. On \
repere le "point d'inflexion" ou un ajout de capacite apporte de moins en moins de benefice \
marginal sur les memes metriques.

T4.3. Plausibilite economique simplifiee. On relie l'amelioration de capture ratio PV au spread \
entre heures de charge et de decharge. On utilise TTL comme repere des heures cheres et un seuil \
de prix bas comme repere des heures de charge. On compare une valeur annuelle theorique au cout \
annualise de la batterie.

---

Slide 23 -- Question 4 -- Scenarios

Principe. On limite le nombre de scenarios. Chaque scenario doit isoler un mecanisme.

S4.A "PV + stockage". On augmente le PV et on augmente les batteries selon une regle simple, par \
exemple un ratio "GW de batteries par GW de PV" et une duree fixe. On mesure si le capture ratio \
PV se stabilise.

S4.B "Batteries moins cheres". On ne change pas la physique. On change l'acceptabilite economique. \
On observe a partir de quel cout la batterie devient plausible au regard du spread observe ou \
plausible.

S4.C "CO2 plus eleve". On augmente le CO2, ce qui augmente TTL sur les heures thermiques. On \
mesure l'effet sur le spread et donc sur l'economie des batteries. On verifie que le SR ne change \
pas mecaniquement.

S4.D "Gaz plus eleve". On repete l'exercice avec un choc gaz.

---

Slide 24 -- Question 4 -- Limites et garde-fous

L4.1. Dispatch simplifie. Une simulation simple de batterie ne reproduit pas toutes les \
optimisations reelles. Elle peut sous-estimer ou surestimer la valeur selon la regle retenue. \
L'objectif est l'ordre de grandeur.

L4.2. Contraintes reseau. Les prix negatifs sont parfois locaux ou lies a des congestions. Une \
approche agregee peut manquer ce point.

L4.3. Revenus multiples. Une batterie peut capter plusieurs revenus. Une analyse pure spot peut \
etre trop conservative. Cela doit etre explicite comme une limite.

L4.4. Rigidite structurelle. Si IR est eleve, une partie du surplus est structurelle. La batterie \
"PV" ne suffit pas. Il faut alors combiner plusieurs leviers ou changer le point de vue.

---

Slide 25 -- Question 4 -- Livrable attendu

Livrable principal. Une courbe par pays qui relie la taille de batteries a trois resultats : \
la baisse des heures negatives, l'amelioration du capture ratio PV, et l'amelioration du FAR.

Format consultant. Une page par pays avec un tableau d'hypotheses explicites, une courbe \
"benefice marginal", et un encadre "interpretation business".

Livrable CO2 et gaz. Une table de sensibilites qui montre comment la taille "economiquement \
plausible" de batteries evolue quand TTL augmente sous choc CO2 ou gaz.
"""

# ---------------------------------------------------------------------------
# Slides 26-31 — Q5 : CO2 et gaz
# ---------------------------------------------------------------------------
SLIDES_Q5_METHODOLOGY = """\
Slide 26 -- Question 5 (CO2 et gaz) -- Definition precise du probleme

La question vise a comprendre comment le prix du CO2 et le prix du gaz changent la logique \
globale. L'objectif n'est pas de prevoir le CO2 ou le gaz. L'objectif est de quantifier leur \
effet sur l'ancre thermique et sur la valeur relative captee par le PV.

Definitions cles. Le Thermal Tail Level (TTL) est un indicateur simple qui represente un niveau \
de prix eleve sur les heures ou le thermique fixe souvent le prix. On peut l'interpreter comme \
une "ancre economique" du haut de la courbe de prix. Le CO2 et le gaz influencent cette ancre \
parce qu'ils influencent le cout marginal des centrales thermiques. Le capture ratio PV compare \
la valeur captee par le PV a un prix moyen de reference.

Point clef. CO2 et gaz bougent surtout la "hauteur" de la courbe hors surplus. Ils ne \
suppriment pas a eux seuls le surplus. Ils changent donc la valeur absolue, et parfois la valeur \
relative, mais pas forcement la mecanique de Phase 1 et Phase 2.

---

Slide 27 -- Question 5 -- Hypotheses structurantes

H5.1. Quand le gaz et le CO2 augmentent, TTL augmente car le cout marginal thermique augmente. \
Cela rehausse le niveau de prix sur les heures non-surplus.

H5.2. Une hausse de TTL peut augmenter la valeur du stockage car les spreads entre heures cheres \
et heures bon marche peuvent augmenter.

H5.3. Une hausse de TTL n'ameliore pas automatiquement le capture ratio PV. Si le surplus PV \
continue de pousser de nombreuses heures PV vers des prix tres bas, le capture ratio peut rester \
faible meme si l'ancre thermique monte.

H5.4. L'impact relatif du CO2 depend de la technologie marginale. Un systeme charbon est plus \
sensible au CO2 qu'un systeme gaz. Un systeme avec beaucoup de nucleaire ou d'hydro est moins \
sensible car le thermique ne marginalise qu'en pointe.

---

Slide 28 -- Question 5 -- Tests empiriques

T5.1. Pass-through "grosses mailles". On compare l'evolution de TTL avec l'evolution des prix \
gaz et CO2, annee par annee, par pays. On teste si le lien est stable hors annees de crise.

T5.2. Decomposition "niveau vs valeur relative". On observe separement le baseload, le TTL, et \
le capture price PV. On verifie si la hausse de TTL s'accompagne d'une hausse du capture price \
PV. Si ce n'est pas le cas, le capture ratio se degrade.

T5.3. Test "Phase 1 et Phase 2". On verifie si les seuils de bascule Phase 1 -> Phase 2 \
s'expliquent par des variables de surplus et de flex, plutot que par gaz et CO2. L'objectif est \
de ne pas attribuer aux commodites un phenomene qui vient d'abord de la saturation horaire.

---

Slide 29 -- Question 5 -- Scenarios

Principe. On definit quelques "etats du monde" coherents.

S5.A "Commodites basses". Gaz et CO2 bas. TTL bas. Les spreads sont plus faibles, donc les \
flexibilites sont moins naturellement rentables. Les prix negatifs peuvent rester frequents si \
SR est eleve.

S5.B "CO2 eleve". CO2 haut. TTL monte fortement dans les pays carbones. Les spreads peuvent \
augmenter. La valeur du stockage et de l'effacement devient plus plausible.

S5.C "Gaz eleve". Gaz haut. TTL monte plutot dans les systemes gaz-marginaux. Le signal \
d'investissement dans des flexibilites peut s'accroitre.

S5.D "CO2 et gaz eleves". On teste un etat stressant ou TTL est tres haut. On verifie si cela \
change l'ordre de priorite des leviers.

---

Slide 30 -- Question 5 -- Limites et points ouverts

L5.1. Pass-through imparfait. Les prix de marche ne suivent pas mecaniquement le cout marginal, \
car il y a de la concurrence, de l'hydraulique, des imports, des contraintes reseau, et parfois \
des mecanismes de capacite.

L5.2. Couplage europeen. Le gaz et le CO2 n'agissent pas seulement au niveau national. Ils se \
propagent via les echanges.

L5.3. Reglementation. Les prix observes peuvent etre influences par des mecanismes de soutien, \
des contrats, ou des regles d'export.

---

Slide 31 -- Question 5 -- Livrable attendu

Livrable principal. Une table de sensibilites par pays qui donne l'effet d'un choc CO2 et d'un \
choc gaz sur TTL.

Livrable "CO2 necessaire". Un calcul simple qui repond a la question "Quel CO2 faut-il pour \
remonter le haut de la courbe de prix de X EUR/MWh". On l'exprime comme une relation entre CO2, \
technologie marginale, rendement et facteur d'emission.

Livrable "implications pour la flex". Une synthese qui relie la hausse de TTL a une hausse \
attendue de la valeur des flexibilites, tout en rappelant que SR et IR gouvernent l'existence \
du surplus.
"""

# ---------------------------------------------------------------------------
# Slide 32 — Architecture macro
# ---------------------------------------------------------------------------
SLIDES_ARCHITECTURE = """\
Slide 32 -- Architecture macro de l'outil et plan de construction (Phase 1 vs Phase 2)

Choix d'architecture. La meilleure approche est une architecture hybride. On construit une base \
commune integree, puis cinq modules d'analyse alignes avec les cinq questions. Cette approche \
evite une usine a gaz car la base commune reutilise les memes donnees et les memes definitions, \
et chaque module reste focalise sur une decision.

Ce que contient la base commune. La base commune contient une table d'hypotheses par pays et par \
annee, des series horaires de demande, de production PV et eolienne, de production rigide, \
d'echanges et de prix day-ahead. Elle calcule des indicateurs simples et audites : le capture \
price PV et le capture ratio PV, SR, FAR et IR (qui decrivent la mecanique de surplus et de \
flex), et TTL comme repere du haut de courbe en heures thermiques.

Ce qui est construit en Phase 1. La Phase 1 construit la base commune et les modules de preuves \
historiques. Elle produit les regles de bascule Phase 1 -> Phase 2, la pente de Phase 2, et une \
lecture robuste des signaux par pays. Elle integre des sensibilites simples CO2 et gaz via \
l'impact sur TTL, sans dynamique d'investissement. Elle se limite volontairement a des scenarios \
statiques lisibles.

Ce qui est ajoute en Phase 2. La Phase 2 ajoute une couche prospective minimale. Elle ajoute \
un moteur de scenarios coherents a horizon 3 a 10 ans avec peu de leviers. Elle ajoute une \
logique d'evolution des capacites PV et de flex qui reste explicable.

Lien avec les cinq questions. Chaque module reprend SR, FAR, IR, TTL et capture ratio PV dans \
une fiche question. Le module Q3 ajoute des tests de tendance. Le module Q4 ajoute une courbe \
"benefice marginal des batteries". Le module Q5 ajoute la table CO2 et gaz et la traduction en TTL.
"""

# ---------------------------------------------------------------------------
# Slide 33 — Perimetre pays
# ---------------------------------------------------------------------------
SLIDES_COUNTRY_SCOPE = """\
Slide 33 -- Perimetre pays recommande

Principe de selection. On choisit des pays qui maximisent la diversite des mecanismes sans \
multiplier la complexite.

Noyau Phase 1 (6 pays). Allemagne (grand systeme, forte penetration VRE, forte exposition \
echanges), Espagne (PV en forte croissance, profils de demande saisonniers marques), France \
(rigidite non pilotable elevee, sensibilite a la modulation), Italie (gaz-marginal, contraintes \
regionales, forte sensibilite commodites), Royaume-Uni (wind-dominant, mecanismes de contrats), \
Pays-Bas (tres couple, tres expose aux prix gaz).

Extension Phase 2 (2 pays). Danemark (cas extreme VRE, limites absorption locale), Pologne (cas \
carbone, sensibilite CO2 maximale, ancrage thermique).

Critere de stop. Si une question est deja demontree de maniere robuste sur le noyau, on n'etend \
pas. L'extension ne se justifie que si elle change une conclusion ou securise un point strategique.
"""

# ---------------------------------------------------------------------------
# SPEC_0 — Regles de calcul normatives
# ---------------------------------------------------------------------------
SPEC_0_NORMATIVE_RULES = """\
SPEC 0 -- Conventions, definitions, regles d'audit (normative)

Objet : Cette specification fixe les regles MUST/SHALL communes au socle et aux modules Q1..Q5 \
en mode HIST et SCEN.

Regles non negociables :
- Granularite unique: horaire (1H).
- Index interne timezone-aware UTC.
- Aucune interpolation silencieuse des prix, load ou generation.
- Regimes A/B/C/D calcules sans utiliser le prix (anti-circularite).
- Cle API ENTSOE uniquement via ENTSOE_API_KEY (jamais committee).

Definitions canoniques :
- NRL = load_mw - gen_vre_mw - gen_must_run_mw
- surplus_mw = max(0, -NRL)
- surplus_unabsorbed_mw = max(0, surplus_mw - flex_effective_mw)
- SR = surplus_energy / generation_energy (fallback explicite SR_load si generation indisponible)
- FAR = surplus_absorbed_energy / surplus_energy, NaN si surplus nul
- IR = P10(must_run_mw) / P10(load_mw)
- capture_price_X = sum(price_used * gen_X) / sum(gen_X)
- capture_ratio_X = capture_price_X / baseload_price
- TTL = P95(price_used | regime in {C, D})

Regimes :
- A: surplus non absorbe (surplus_unabsorbed_mw > 0)
- B: surplus absorbe (surplus_mw > 0 et surplus_unabsorbed_mw = 0)
- D: tension (NRL > seuil_P90_NRL_positif)
- C: autre heure non surplus

Auditabilite :
Chaque run doit produire :
- run_id deterministe (hash code+config+datasets)
- snapshot des hypotheses utilisees
- manifest des datasets utilises (source, extraction, checksum)
- export des tables et checks

Tests minimaux :
- invariants physiques (hard)
- qualite donnees (hard/warn)
- reality checks marche/physique (warn)

Explicabilite UI :
Toute metrique affichee doit fournir : definition simple, formule, intuition, limites, \
dependances aux hypotheses.
"""

# ---------------------------------------------------------------------------
# Map et fonction d'assemblage
# ---------------------------------------------------------------------------
QUESTION_SLIDES_MAP: dict[str, str] = {
    "Q1": SLIDES_Q1_METHODOLOGY,
    "Q2": SLIDES_Q2_METHODOLOGY,
    "Q3": SLIDES_Q3_METHODOLOGY,
    "Q4": SLIDES_Q4_METHODOLOGY,
    "Q5": SLIDES_Q5_METHODOLOGY,
}


def get_full_methodology_context(question_id: str) -> str:
    """Assemble the complete methodology context for a given question.

    Returns intro + Q-specific slides + architecture + SPEC_0 normative rules.
    """
    qid = question_id.upper()
    q_slides = QUESTION_SLIDES_MAP.get(qid, "")
    parts = [
        "=== METHODOLOGIE TTE CAPTURE PRICES V2 ===",
        "",
        "--- CONTEXTE GENERAL (Slide 1) ---",
        SLIDES_CONTEXT_INTRO,
        "",
        f"--- METHODOLOGIE DETAILLEE {qid} ---",
        q_slides,
        "",
        "--- ARCHITECTURE DE L'OUTIL (Slide 32) ---",
        SLIDES_ARCHITECTURE,
        "",
        "--- PERIMETRE PAYS (Slide 33) ---",
        SLIDES_COUNTRY_SCOPE,
        "",
        "--- REGLES DE CALCUL NORMATIVES (SPEC_0) ---",
        SPEC_0_NORMATIVE_RULES,
        "",
        "Tu dois utiliser ces definitions, hypotheses, tests et limites comme cadre "
        "de reference pour ton analyse des donnees ci-dessous.",
    ]
    return "\n".join(parts)
