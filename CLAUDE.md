# Mes applis — page d'accueil des élèves

Public : **Ma classe**. Famille 1 (applis élèves), skill `appli-eleve-ipad`.
Les élèves y retrouvent leurs applis et le lien vers leur suivi (code secret).
Page **non référencée** : `noindex` dans le `<head>`, aucun lien depuis
rprof1.com ni la vitrine. On la partage par QR code (bouton en haut) ou webclip.

## État
- Version 1.0, créée le 13/11/2026. **Non publiée** (attendre « publie »).
- Adresse prévue : https://ludo1104-rp.github.io/mes-applis/ (dépôt public `mes-applis`).

## Fichiers
- `index.html` : toute la page (bâtie sur le gabarit de la skill).
- `test_page.py` : test de bout en bout (liens en ligne, nouvel onglet,
  « Dernière ouverte », aide, réglages, QR). `python3 test_page.py`.

## Ajouter ou changer une appli
- Section 2 du script : `SUIVI` (lien du suivi) et `APPLIS`
  (id, nom, matière, phrase, icône, couleur, lien).
- Un nouvel id pour chaque appli (`a7`, `a8`…), jamais réutilisé.
- Icône absente ? En dessiner une dans `ICONS` (SVG plat).
- Ne jamais changer `APP.cle` (`mes-applis`) : il garde les réglages des iPad.

## Pièges
- Les liens s'ouvrent dans un nouvel onglet : la page reste ouverte derrière.
- `robots.txt` ne sert à rien dans un sous-dossier GitHub Pages : c'est la balise `noindex` qui compte.
- Le dépôt GitHub reste visible sur le profil (page discrète, pas secrète).

## Prochaine étape
1. Ludo relit la page et la liste des applis.
2. « publie » → dépôt public `mes-applis`, GitHub Pages, format commun.
3. Tester sur iPad : webclip, retour depuis une appli, voix.
