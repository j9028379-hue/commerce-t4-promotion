# Commerce T4 · Promotion 1.0.0

[Parcours](https://j9028379-hue.github.io/commerce-t4-promotion/) · [Film sonore](../../releases/tag/commerce-t4-v1.0.0) · [Workflow de livraison](../../actions/workflows/livrer.yml) · [Références et droits](audio/CREDITS.md).

Le catalogue relie six questions (sept valeurs dont la fin facultative), quatre prises, douze écrans, la partition, la voix de démo et le profil musical. `tools/site.py` compile les JSON pour Pages. À la fin du parcours on peut relire un aperçu silencieux et exporter job.json + les quatre vidéos identifiées par SHA-256. Aucun envoi automatique de rushs privés. Le film marchand utilise le son de ses prises, ou uniquement la musique si elles sont silencieuses ; jamais la narration de Boutique Grâce. La démo explicite utilise le WAV approuvé `render/demo/voix/Voix-seule-T4.wav`. L’audio est ajouté par copie du flux vidéo : la typographie et les coupes validées restent inchangées.

## Livrer

Depuis la racine, Python 3.12, FFmpeg/ffprobe, Pillow, numpy, OpenCV et jsonschema : `python render/marchand.py --job DOSSIER --out LIVRAISONS --state /chemin/durable/t4.sqlite`. Garder le même dossier et la même base. Succès : Film.mp4, preuve des textes, crédits, contrôle du mix et RenderResult ; échec : RenderError sans consommation de musique. Même job = même attribution. `--delivery` crée explicitement une identité de livraison distincte. La piste est choisie parmi les moins jouées, après exclusion de la dernière ; égalités départagées aléatoirement. Pas de numéro 5, pas de cycle imposé. En service multi-serveurs il faut un historique commun.

Sur GitHub, `livrer.yml` parcourt réellement les écrans sur Chrome, rend la démo, rend un autre commerce, vérifie le paquet et assemble Wrangler à blanc. Par défaut, le lancement manuel vérifie le rendu sans écrire dans le journal. Seule l’option explicite `livrer=true` sur `main` confirme une nouvelle livraison ; un rerun conserve son identité. Groupe de concurrence unique, lecture de `state/commerce-autoplay:autoplay/etat.json`, écriture conditionnelle après rendu, tests et upload des artefacts. La branche ne contient que des identifiants hachés et numéros de piste dans ce journal, pas de coordonnées client. La base des contre-épreuves est séparée.

### Piste Pixabay nº 2

Quatre choix approuvés ; trois extraits CC BY livrés avec attribution. La seconde n’est **jamais** redistribuée en MP3 dans Git ou le ZIP. Pour l’activer, fournir un extrait autorisé de 30 s à l’hôte privé (`T4_PRIVATE_02` + `T4_PRIVATE_02_SHA256`), ou les secrets Actions `T4_PRIVATE_02_URL` (HTTPS privé) et `T4_PRIVATE_02_SHA256`. Sans fichier, exclusion explicite de cette piste ; une empreinte incorrecte fait échouer le rendu. L’exploitant doit vérifier source, droits et empreinte avant de configurer les secrets. La vidéo livrée contient seulement le mix synchronisé.

### Parité de référence

T1 : journal entre runners, comparaison de révision et dernière livraison réussie. T2/T3 : job navigateur, validation des entrées, rendu marchand sur autres réponses, succès/erreur, golden, paquet/manifeste et Worker GET. T4 conserve le design C, le style A, le prix barré et la règle de rotation non séquentielle demandée. `golden/` fige le job et les titres acceptés ; `qc/` teste le cas sans date, la non-répétition, la concurrence, le job rejoué et le refus des fichiers ou paquets altérés. `package/livrer.py build paquet/COMMERCE-T4-1.0.0.zip` puis `verify` : manifeste de tailles et SHA-256 (intégrité, pas signature). Le contrôle Cloudflare est **lecture seule et dry-run**, pas une mise en production, ni un service d’upload ou d’OTA. Ni Android physique ni orchestration client de production ne sont certifiés.

Le propriétaire a approuvé le mix final du film publié `T4-Promotion-Boutique-Grace.mp4`. Voir [l’empreinte et la décision](approvals/validation.json). Cette approbation concerne le film livré, pas tous les futurs rendus.
