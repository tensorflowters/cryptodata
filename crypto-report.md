# Report: Thinking

<aside>
💡 This page aims at centralizing the thinking about the report. 
It’s like a big draft where we can structure what will ultimately be said in the report.
Everyone can participate.

</aside>

# Introduction

La réalisation du projet “Crypto Viz” consiste en la mise en place d’une application web permettant de visualiser des informations importantes sur le cours des crypto-monnaies. 

Le coeur du projet consiste en la récupération d’articles de news sur des crypto-monnaies, l’analyse de ces derniers, et la présentation de ces analyses sur l’application web. 

Pour ce faire, nous avons choisi de mettre en place des technologies robustes, facilement évolutives.

Nous avons choisi Airflow pour l’orchestration des opérations récurrentes (comme le scraping), Kafka pour la communication entre services, Selenium pour le scraping, HuggingFace transformers pour l’analyse sentimentale, et l’API de Blockchain pour les données en temps réel. Pour la visualisation, nous utiliserons Grafana.

Quant au déploiement, il sera fait grâce à Docker, et Portainer pour l’orchestration et la visualisation des conteneurs.

# L’orchestration des jobs avec Airflow

Apache airflow est une plateforme permettant de mettre en place des workflows, ou suites d’actions, de façon programmatique, en python par exemple.

 

Un workflow s’appelle un Dag (Directed Acyclic Graph), dans le jargon d’Airflow. Un Dag est composé d’une ou multiples tâches. Ces tâches peuvent être inter-dépendantes, et il est possible de passer le résultat d’une tâche à une autre tâche. 

Pour ce projet, nous avons peu utilisé le système de tâches, mais il demeure très puissant.

Un problème souvent rencontré avec les Dags airflow est la gestion des dépendances entre différents Dags, car airflow, par défaut, partage un environnement avec tous ses Dags.

Afin de prévenir des potentiels problèmes sur une codebase plus large, dans le futur, nous avons décidé d’utiliser des opérateur Docker. Ces derniers vont créer des services Docker pour chaque tâche ; cela permet d’assurer une stabilité entre les tâches et une isolation des services. Cela permet aussi de facilement lancer ces tâches manuellement, hors Airflow, de s’assurer de leur bon fonctionnement et de les tester.

Nous avons mis en place deux Dags de scraping pour deux sites différents, sur lesquels nous reviendront un peu plus tard. Après avoir testé ces scripts, nous avons conclu que des intervalles de 5 minutes pour le site “cryptopanic” et de 2 minutes pour le site “binance” nous permettaient d’avoir des résultats suffisants pour ces deux sites, c’est-à-dire que nous ne manquions que très peu d’articles, tout en évitant de stresser les ressources inutilement. 

# Le scraping avec Selenium

Nous avons décidé de récupérer les informations depuis deux sites d’articles : [CryptoPanic](https://cryptopanic.com/) et [Binance](https://www.binance.com/en/feed).

Les scripts de scraping sont simples, et utilisent Selenium avec le webdriver de Firefox.

On récupère les crypto-monnaies concernées par l’article, le titre, le lien vers l’article, et la date de publication. On stocke aussi un hash du lien vers l’article ; ce dernier nous permettra d’éviter les doublons dans la base de données, en rajoutant une contrainte d’unicité sur  ce hash.

Afin d’isoler les services et de garantir au maximum la disponibilité de ces derniers, une fois nos articles récupérés, nous envoyons un évènement via Kafka, en tant que producer donc, qui sera récupéré par un autre service. 

Un autre service donc, qui lui fonctionne en permanence, s’occupe d’ajouter les articles dans la base de données. 

Ce dernier écoute les évènements via Kafka, en tant que consumer donc, et s’occupe de rajouter les articles dans notre base de données. Grâce à la contrainte d’unicité rajoutée précédemment sur le hash de l’url, nous pouvons simplement essayer de rajouter tous les articles reçus dans la base de données et cette dernière se chargera de refuser les doublons.

# Le messaging avec Kafka

Kafka nous permet de transmettre de l’information entre services simplement, séparée par “topics”. De plus, Kafka est une technologie très facilement évolutive ; ce qui peut être utile pour l’avenir. 

La séparation par topic peut être très utile si, à l’avenir, nous récupérons de la donnée d’encore plus de sites. 

Nous utilisons aussi Kafka dans un deuxième cas, où son utilisation est, pour le coup, essentielle. 

# L’analyse de sentiment avec Transformers

Une fois les articles récupérés en surface (le titre, le lien vers l’article), il paraît intéressant de regarder le contenu de ces articles. 

Pour ce faire, nous utiliserons un modèle d’analyse sentimentale, via le package “transformers” de HuggingFace. Le modèle utilisé est un modèle spécialisé dans l’analyse sentimentale pour les textes financiers, “FinBERT”, de ProsusAI.

Ce service fonctionnera en permanence, et écoutera les évènements envoyés par Kafka, en tant que consumer. De ces évènements, on récupèrera le lien de l’article et on viendra récupérer le contenu de ce dernier. On l’analysera donc afin de récupérer la tendance de l’article, c’est-à-dire si l’article est plutôt positif, neutre, ou négatif. 

Étant donné que ce service nécessite ce modèle et la librairie transformers, et que ces derniers sont plutôt lourds, il est clairement plus intéressant de garder un service fonctionnel en permanence et de réaliser cette analyse lorsque les évènements arrivent, plutôt que d’en faire une tâche dans le Dag, car cela rendrait le temps de mise en place du Dag bien plus long. 

Une fois l’analyse faite sur l’article en question, nous pouvons stocker le résultat dans la base de donnée. 

# L’API Blockchain pour les données en temps réel

Les crypto-monnaies étant décentralisées, et souvent motivées par une volonté d’indépendance vis-à-vis des institutions traditionnelles, il existe différentes APIs qui proposent des données historiques et en temps réel gratuitement. 

Nous avons choisi Blockchain car c’est une des plus grandes organisations en place. 

Cette dernière nous propose d’avoir accès à de la donnée en temps réel sur n’importe quelle crypto-monnaie. 

Afin de garantir la sécurité de nos utilisateurs, nous créons un service qui s’occupera de récupérer cette donnée et de la stocker dans notre base de données ; de cette manière nous nous assurons de ne pas exposer la clé API au public. Ce service n’étant pas accessible au public, nous évitons ainsi quelconque brèche de sécurité. 

# Visualisation des données avec Grafana

Après analyse des données sur quelques jours, nous remarquons que le bitcoin est dans sa propre ligue. Il a tendance à tirer les indicateurs des articles vers le haut, car c’est la crypto-monnaie la plus mentionnée dans les articles ; il est en général mentionné dans 5 à 6 fois plus d’articles que la seconde crypto-monnaie la plus mentionnée.  

De ce fait, nous avons décidé de lui dédier un tableau de bord dédié.

## La donnée en temps réel

Pour la visualisation des données en temps réel, nous opterons pour une série chronologique. Nous pourrions aussi opter pour une visualisation en bougies, qui offrirait un peu plus d’information sur les transactions (open, high, low, volume) ; mais à la granularité de la minute, la visualisation de ces bougies n’est pas très parlante. À l’inverse, avec une série chronologique, la visualisation à la granularité de la minute est tout à fait satisfaisante. 
Pour le moment, uniquement la donnée du bitcoin est montrée en temps réel.

## La visualisation de la quantité des articles

En dehors de l’analyse sentimentale du contenu des articles, il y a un certain intérêt à voir les crypto-monnaies “tendances”. Cela permet de voir quelles crypto-monnaies sont au coeur de l’actualité et de pouvoir se renseigner sur ces dernières sur le moment opportun, puis de décider s’il faut plutôt vendre ou acheter.

Pour ce faire, nous avons opté pour plusieurs types de graphiques. 

- Un graphique en barres, afin de visualiser la quantité d’articles publiés et récupérés chaque jour ; cela permet de mettre en perspective les autres chiffres récupérés.
- Deux diagrammes circulaires pour montrer la part des articles par crypto-monnaie, de tout temps et pour le jour en cours. Cela permet de voir quels sont les crypto-monnaies qui prennent la plus grande part de l’actualité.
- Une série chronologique pour montrer le nombre d’articles publiés par crypto-monnaie, par jour ; afin d’avoir une vision d’ensemble et glissante, sur la semaine ou le mois.

## La visualisation des sentiments des articles

L’analyse sentimentale du contenu des articles apporte des informations intéressantes à quiconque souhaite investir dans le marché. 

Cependant, les visualiser d’une manière sufisamment parlante peut être difficile. Il faut rendre cette information disponible, mais aussi faire en sorte que l’utilisateur ne prenne pas non plus l’analyse de ces articles “pour argent comptant”. 

- Les codes de devises sur lesquels il y a le plus d’article aujourd’hui, ceux sur lesquels il y a le plus d’articles positifs, et ceux sur lesquels il y a le plus d’articles négatifs
- Un graphique en barre montrant les TOP crypto-monnaies, avec unratio, c’est-à-dire le nombre d’articles positifs sur le nombre d’articles négatifs, par crypto-monnaie.

 

## Le déploiement avec Docker et Portainer

@Arthur 

# Pistes d’améliorations

## Récupérer plus articles, depuis d'autres sites

L'information sur les crypto-monnaies peut se retrouver sur différents sites, et il est évident que pour tirer des conclusions quant à la tendance, ou la quantité des articles sur une crypto-monnaie en particulier, il est intéressant de récupérer davantage d'articles, depuis des sources variées.

## Récupérer les données en temps réel d'autres crypto-monnaies

Pour le moment, la seule crypto-monnaie pour laquelle nous récupérons le cours en temps réel, c'est le bitcoin.

En dehors des articles, le cours des monnaies est évidemment un acteur important dans la prise de décision. Récupérer d'autres cours en temps réel évite d'avoir un second onglet sur lequel l'utilisateur devrait aller pour récupérer le cours des monnaies.

## Une réorganisation ses tableaux de bords

Pour le moment, il n'y a qu'un unique tableau de bord.

Au vu de la diversité des crypto-monnaies, il peut être intéressant de proposer un tableau de bord général, qui correspondrait à celui actuel, mais aussi des tableaux de bords spécialisés pour chaque monnaie, afin de visualiser les informations de manière plus spécifique ; cela aiderait sûrement à la prise de décision.