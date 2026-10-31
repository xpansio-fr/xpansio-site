# Site xpansio.fr

- Le contenu et la structure des pages sont dans `src/build.py` ; le style dans `src/styles.css`.
- Après toute modification, lancer `python3 src/build.py` puis committer `src/` ET `docs/` : GitHub Pages publie `docs/` tel quel (fichiers `CNAME` et `.nojekyll` générés par le script).
- Le formulaire de contact passe par Web3Forms (clé `WEB3FORMS_KEY` dans `build.py`) ; les messages partent vers l'adresse d'Agnès, qui ne doit pas être affichée sur le site.
- Ne pas afficher le numéro de téléphone (bouton `tel:` uniquement), sauf dans les mentions légales où il est obligatoire.
- Ne citer aucune entreprise cliente dans les références.
- Typographie Montserrat, composition centrée, bleu = expérience channel, corail = expérience client.
