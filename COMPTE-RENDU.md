# « Rien de grave » — compte rendu de passation (13 octobre 2026)

Projet de Hadrien Basch. Récit interactif web (three.js) sur ce que donnerait une victoire du RN en 2027, vu par Claire, factrice à Valberne (ville fictive), rue des Tilleuls. Destiné surtout aux électeurs RN / indécis, sans les juger. Sortie prévue sur itch.io, puis envoi aux associations, syndicats et médias.

## 1. Où sont les fichiers

Sur le PC, dans `C:\Users\hadri\Music\rien-de-grave\` :

- `source\rien-de-grave.html` : **le jeu, un seul fichier** (HTML + CSS + JS module, three.js 0.160 chargé via importmap jsdelivr). C'est le fichier de référence.
- `source\props\*.glb.wasm` : modèles 3D Poly Haven (CC0), allégés (meshopt, textures JPEG 512 px). Extension `.glb.wasm` parce que l'hébergeur d'artefacts de claude.ai refuse `.glb`. Le build itch les renomme en `.glb`.
- `source\tex\*.jpg` : textures Poly Haven (pavés, asphalte, tuiles, enduit, pierre, bois), réduites et neutralisées pour être teintées.
- `source\sons\amb1-4.mp3` : ambiances (amb1 jour, amb2 nuit/tension, amb3 pluie, amb4 fin). Les bruitages `tampon.mp3`, `lettre.mp3`, `sirene.mp3` sont prévus dans le code mais pas encore fournis (le jeu reste silencieux sans eux).
- `source\glb\` : personnages riggés (homme/femme, animations) — **désactivés** (`const RIGGED = false`), l'auteur préfère les figurines « capsules ».
- `source\tools\build_itch.py` : construit le paquet itch (bundle esbuild + polices auto-hébergées + assets, zip).
- `source\la-rue.html`, `source\la-rue-fp.html` : deux variantes en pause (« Rue des Tilleuls », un jour par an ; et un prototype à la première personne). **Ne pas travailler dessus pour l'instant.**
- `itch\` : `rien-de-grave-itch.zip` (paquet prêt, v24), `page-itch.txt` (texte et réglages de la page itch), `cover-630x500.png` et `cover-1260x1000.png`, `contacts-et-mail.txt` (adresses vérifiées + mail type).
- `assets\` : fichiers bruts téléchargés depuis Poly Haven par Blender.

Version en ligne (compte précédent) : artefact claude.ai « Rien de grave », version 24. Le nouveau compte devra republier depuis `source\rien-de-grave.html` en joignant `props/`, `tex/`, `sons/` (et `glb/` inutile tant que RIGGED = false).

## 2. Contraintes à respecter (demandées par l'auteur)

- **Diffamation** : personnages et ville fictifs. Ne jamais prêter de paroles ou d'actes inventés à une personne réelle. Tout fait réel est sourcé (lien). Une personne mise en examen ou renvoyée devant un tribunal n'est pas « condamnée » (ex. Rachida Dati : non citée).
- **Tampons** sur chaque scène : `real` « Déjà arrivé » (rouge), `prog` « Au programme du RN » (double bordure), `prop` « Déjà proposé » (par d'autres), `fic` « Pas encore arrivé » (bleu pointillé). Chaque tampon a « Lire la source » et éventuellement « En savoir plus : … » (Wikipédia). Préférer le réel à la fiction.
- Privilégier les exemples de **dictatures d'extrême droite** (Vichy, Franco, Salazar, Pinochet, Argentine, Italie fasciste) et l'**actualité américaine** (ICE, CECOT) à la Russie (il reste un exemple russe).
- Le jeu doit marcher **sur mobile** (testé en simulation iPhone).
- Texte à la 2e personne pour la famille de Claire (« ton frère », « ta mère »), la narration parle encore de Claire à la 3e personne.
- Ne pas refaire le paquet itch sans le signaler ; il a été reconstruit à la v24.
- Pas de musique pour l'instant (son : voir § 6).

## 3. Structure du jeu (dans `rien-de-grave.html`)

Moteur maison sur three.js : diorama de rue (maisons générées en code, figurines capsules, vélo, chats et pigeons animés, nuages en coton, pluie en traînées), post-process (GTAO sur ordinateur, bloom, tilt-shift léger, étalonnage « grade » avec saturation par ambiance, grain, vignette), mode test « Vue maquette » (BokehPass, menu ou `?maquette`).

Fonctions clés : `card()`, `say()` (gros plan auto sur le personnage qui parle), `note()`, `hotspots([...])` (pastilles Tournée / Citoyenne, puis pastilles « Relire ↺ »), `paper({kind, from, body, stamps, scene})`, `walk()` (Claire prend son vélo au-delà de 4,5 unités), `focus(x, zoom)`, `setMode('day'|'summer'|'grey'|'dusk'|'rain'|'night')`, `setStage()`, `setDay(texte, indexEre)`, `setEra(i)` (caméras, policiers, budget sécurité dans l'horloge), `closeHouse()`.

Chapitres :
1. **Prologue, 2 mai 2027** : soir de l'élection, TV, Léo « C'est grave, maman ? », SMS de Julien, scène des panneaux électoraux (Le Pen condamnée en appel le 7/07/2026 mais éligible ; Zemmour condamné 2011 et 2018).
2. **An 1, avril 2028** : CAF Benali (Vitrolles + priorité nationale), Local repris (Hénin-Beaumont/Hayange), Le journal au tabac (Bolloré), cantine (Beaucaire), cinéma René-Vautier → Maréchal-Pétain (Elne).
3. **An 2, juillet 2029** : HLM (priorité nationale logement), médiathèque (Orange, Maus), théâtre annulé (Castres, Région AURA/TNG), sortie piscine (Sénat 2019), rassemblement.
4. **An 4, octobre 2031** : Carrefour (Perpignan : 161→199 policiers municipaux ; Hongrie reconnaissance faciale), binationaux Duarte, Office de la famille (Carpentras supprime la subvention du Planning familial, « réarmement démographique », Vichy 1942), panneaux (dissolution LFI, prop), cartable de Léo, voile de Samia, Bourse du travail ; arrestation de Moussa et Bernadette (Herrou, délit de solidarité, détaillé).
5. **An 6, juin 2033, « Le prix »** : boulangerie (Brexit), maison de retraite (Dares, 1 emploi sur 10), fiche de paie (indemnités maladie 2025, Bardella « Nous verrons »), état civil / prénoms (Zemmour, testing Dares), pharmacie / AME (programme RN, Espagne +15 % de mortalité), contrôle de la Brigade (Conseil d'État sur le RIO, ICE masqués, présomption de légitime défense), Julien enlevé (CECOT/HRW, Chili).
6. **An 7, mars 2034, « L'arbitraire »** : rafle à 5 h (Vél' d'Hiv, Italie–Albanie), révision des naturalisations (Vichy, droit du sol), assignation à résidence (COP21), révocation de la maîtresse (Turquie), Inès arrêtée (Öztürk), mur des disparus (Argentine), veillée et Karim tué (Minneapolis 2026, 17 octobre 1961, loi de 2017 / Nahel, présomption de légitime défense).
7. **An 8, avril 2035** : propagande candidat unique (Delgado, Nadejdine), presse suspendue (Hongrie, Franco), Chez Bernadette, lycée de Léo, fin « Oui. C'est grave. »
8. **Écran de fin** : faits classés (France / ailleurs / dictatures d'extrême droite / programme RN / déjà proposé / fiction), liens Institut Montaigne, Datan, NosDéputés, vérification d'inscription électorale, crédits (Hadrien Basch, Poly Haven, three.js, polices).

## 4. Tester et construire

- Mode test : `?fast` (tout accéléré, caméra instantanée, `window.__dbg` pour piloter la caméra). Tests Playwright headless (Chromium swiftshader) : un script clique automatiquement pastilles et boutons jusqu'à l'écran de fin et relève les erreurs. **Attention** : dans le script, sélectionner `.hot:not(.done)` sinon il reclique les pastilles « Relire » à l'infini.
- Les décors se chargent un par un avec un délai maximum de 12 s (sinon le jeu restait bloqué sur « Chargement… » sur certains navigateurs) ; `createImageBitmap` est désactivé pendant le chargement des GLB (sinon textures perdues sur certains GPU).
- Build itch : `python3 tools/build_itch.py <dossier_build>` où `<dossier_build>` contient `node_modules` avec `esbuild`, `three@0.160`, `@fontsource/atkinson-hyperlegible`, `@fontsource/caveat`, `@fontsource/special-elite`.

## 5. Retours de l'auteur déjà intégrés (v23–v24)

Affiche du cinéma lisible ; pastilles relisibles ; candidats condamnés ; Herrou détaillé ; fiche de paie moins fictive ; Office de la famille expliqué + Planning familial ; budget sécurité dans l'horloge ; Perpignan au Carrefour ; ICE / RIO / CECOT ; loi 2017 / Nahel ; tampon fiction du voile retiré ; crédits ; volets qui ne se chevauchent plus ; Morris retirée ; nuages et pluie ; caméra basse avec gros plans ; objets du premier plan qui disparaissent quand la caméra est proche ; rue « plus française » (persiennes, garde-corps, tabac, pharmacie, café, boîte La Poste, potelets, ardoise).

## 5 bis. v25–v26 (14 octobre 2026)

- **Accents cassés sur itch** (« Ã© ») : itch sert `index.html` sans charset UTF-8. `build_itch.py` rend désormais `index.html` 100 % ASCII (entités HTML, échappements CSS). `game.js` l'était déjà.
- **Écran titre** : tient sans scroller en 1280×720 et 960×540 ; bouton « Plein écran » à côté de « Commencer » ; sur téléphone, « Commencer » reste collé en bas.
- **Plein écran** : bouton icône à côté de « Menu » + menu. Masqué là où le navigateur ne le permet pas (iPhone Safari).
- **Lettres** : sur écran large, texte à gauche et tampons à droite (deux colonnes de tampons à partir de 3) ; version compacte sous 640 px de haut ; sur téléphone, bouton « ↓ La suite » quand la lettre dépasse. Bug corrigé : le haut d'une lettre trop longue était coupé (centrage en grille).
- **Pastilles** : anti-chevauchement (cherche la place libre la plus proche, sinon décale vers l'intérieur), bornées entre l'horloge et la légende.
- `?fast` expose aussi `showPaper` dans `window.__dbg` (tests de mise en page des 37 lettres).

## 5 ter. v27–v28 (15 octobre 2026)

- Écran titre : phrase « ce jeu ne te juge pas » retirée (jeu et page itch).
- **Huit ans expliqués** : au début de l'An 2, référendum du 1er juillet 2029 (septennat non renouvelable, mandat en cours prolongé jusqu'en 2035, compteur remis à zéro). Tampons : Le Pen 12/04/2022 (septennat + article 11), de Gaulle 1962, plébiscite de Pinochet 1980. Note de l'An 8 mise à jour.
- **LGBT** : An 2, pastille « La marche des fiertés » (Hongrie 2025, Vichy 6 août 1942, Bardella PMA 2019) ; An 7, lettre « Tribunal · n° 2 » (Laure, mère non biologique de Lina, effacée de l'acte de naissance : Padoue 2023). Personnages : Sophie, Laure, Lina (n° 2, au-dessus de la pharmacie). Faits ajoutés à l'écran de fin.
- **Reprise** : `play()` découpé en chapitres (`CH`), le chapitre en cours est sauvé (localStorage `rien-de-grave-chapitre`) ; bouton « Reprendre : An X » sur l'écran titre si la page a été rechargée (téléphone mis en veille).
- **Téléphone** : 30 images/s, résolution ×1,25 max, ombres 1024 px, pas de flou de maquette, MSAA 2 ; `webglcontextlost` géré.

## 6. Prochaines étapes

1. **Son (bruitages, pas de musique)** : l'auteur hésite entre Soundly (sa bibliothèque), ElevenLabs, ou banques gratuites (Sonniss GDC bundle, Freesound CC0). Proposition : ~20 sons (lettre dans la boîte, tampon, volets, sonnette de vélo, pigeons, pas sur pavés, portières, sirène, terrasse de café, cour d'école, pluie sur zinc, télé) déposés dans `sons\`, puis découpe, normalisation et branchement ; fonds continus (pluie, rumeur) générables en WebAudio. Silence pendant la rafle et la veillée.
2. **Republier** sur le nouveau compte, puis créer la page itch.io avec `itch\page-itch.txt` et la couverture ; mettre le lien dans le mail.
3. **Diffusion** : `itch\contacts-et-mail.txt` (18 adresses vérifiées, autres à relever dans un navigateur). Faire relire par un juriste les tampons nommant des personnes réelles avant l'envoi large.
4. Pistes évoquées, non faites : version à la première personne de « Rien de grave » (prototype dans `la-rue-fp.html`), mode maquette par défaut ou non (test en cours), dépôt GitHub (l'auteur doit créer un dépôt vide `rien-de-grave` sur le compte `hbasch`).

## 7. Outils connectés côté PC

Blender (extension MCP for Blender, version d'extension en retard : `uvx mcp-for-blender install-addon`) a servi à télécharger les assets Poly Haven et à alléger le tronc d'arbre. **Ne pas lancer `read_factory_settings` dans Blender : ça coupe le serveur MCP.**
