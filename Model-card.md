# Model card

## Problématique
- Identifier les commentaires pertinent ou non d'une vidéo youtube.

## Dataset
- Commentaires youtube récuperer via l'api youtube

## Perimetre
- Limitations du perimetre de donnée au vidéo de type Tech

## Volumetrie du dataset
- 4000 commentaires: 
    - 2000 commentaires
    - Data augmentation traduction Francais->Anglais->Francais (2000)

## Modèle utilisé
- **CountVectorizer**
- **TfidfTransformer**
- **Naive Bayes**


## Metrics
- Utilisation de la **cross_val_score** : Moyenne de 0,85 acc

## Limitation
- Notre modéle ne fonctionerai pas correctement sur des vidéo non Tech
- Si dans une vidéo Tech un youtubeur demande au internaute de repondre à une question cela peut fausser l'interpretation du modèle


