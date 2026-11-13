# Ma classe de français — l'espace des élèves

Public : **Ma classe**. Famille 1 (applis élèves).
Accueil : titre « Ma classe de français. », Memoji de Ludo (`ludo.png` du suivi,
en base64) et « Je suis Ludo, ton professeur de français ». Puis deux portes : **Mes applis** (écran `#applis` dans la même page)
et **Mon suivi** (ouvre https://ludo1104-rp.github.io/suivi-eleves/, code secret).
Page **non référencée** : `noindex`, aucun lien depuis rprof1.com ni la vitrine.
On la partage par QR code (bouton en haut) ou en webclip.

## État
- Version 1.0, refaite le 13/11/2026 à la demande de Ludo. **Non publiée** (attendre « publie »).
- Adresse prévue : https://ludo1104-rp.github.io/ma-classe/ (libre, vérifiée le 13/11/2026).
  Pas `mes-applis` : « Mes applis. » est déjà le titre de la vitrine applis.rprof1.com.
- Applis : Halloween (histoire + quadrillage), Minecraft (quiz Discovery + commandes),
  Dictée flash, La Foire de Liège. Ordre choisi par Ludo.

## Style (décision de Ludo, 13/11/2026)
Celui de la vitrine `vitrine-applis/` : blanc, noir, Figtree (intégrée en base64),
pastels par petites touches (dessins, surlignage du titre). Le point tombe sur
« classe » / « applis ». Dessins animés au survol (Mac) ou 2 fois à l'apparition (iPad).
Pas de réglage Couleurs/Simple, pas de taille de texte : page de liens, sobre.

## Fichiers
- `index.html` : toute la page. Contenu en haut du script : `SUIVI`, `APPLIS`
  (plusieurs liens = plusieurs boutons), dessins dans `ARTS` (repris de la vitrine).
- `test_page.py` : test de bout en bout (portes, retour, bouton Retour du
  navigateur, nouvel onglet, liens en ligne, QR). `python3 test_page.py`.

## Pièges
- Anonymat : prénom « Ludo » et Memoji seulement, jamais le nom complet ni une vraie photo.
- `verif_ipad.py` signale des faux problèmes ici : boutons « hors de l'écran »
  (la page défile), `visually-hidden` « coupé », point en pleine chute. Rien d'autre.
- Le dépôt GitHub reste visible sur le profil : page discrète, pas secrète.

## Prochaine étape
1. Ludo relit la page.
2. « publie » → dépôt public `ma-classe`, GitHub Pages, format commun.
3. Tester sur iPad : webclip, retour depuis une appli.
