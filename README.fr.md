# okplm : Modèle de température lacustre 'Ottosson-Kettle-Prats'
Copyright 2019 Segula Technologies - Agence Française pour la Biodiversité.

<p align="center">
<img title="banner ALAMODE" src="images/ALAMOD_withlogos.png">
</p>

## Contenu

1. [Qu'est-ce que le paquet `okplm` ?] (#purpose)
2. [Éxigences] (#requirements)
3. [Installation] (#installation)
4. [Dépendances] (#dependencies)
5. [Utilisation] (#usage)
6. [Tests] (#tests)
6. [Exemples] (#Examples)
7. [Références] (#references)

<a name="purpose"> </a>

## 1. Qu'est-ce que le paquet okplm ?

`okplm` est un paquet python du logiciel ALAMODE en Python 3 permettant de simuler les  
évolutions temporelles de la température de l'épilimnion et de 
l'hypolimnion des  plans d’eau d'eau douce à l’aide du modèle OKP 
(Prats & Danis, 2019).

Le modèle OKP simule la température de l’eau à la fréquence quotidienne
en utilisant la température de l’air \[en °C\] et le rayonnement solaire 
\[en W/m<sup>2</sup>\] comme données d'entrée.
Le modèle OKP est le résultat de la combinaison des modèles développés 
par Ottosson & Abrahamsson (1998) et par Kettle *et al.* (2004).

Les températures de l'eau peuvent être calculées à l'aide des 
paramètres par défaut pour les plans d'eau français en fonction des
caractéristiques du plan d'eau, i.e. la latitude, l'altitude, 
la profondeur maximale, la surface et le volume (voir détails dans 
Prats & Danis, 2019).

Sinon, les valeurs des paramètres peuvent être définies par 
l'utilisateur. En particulier, dans le cas d'autres contextes 
géographiques, les valeurs des paramètres se trouvent dans les travaux 
d’Ottosson & Abrahamsson (1998) (lacs suédois) et Kettle *et al.* (2004)
(températures de l'epilimnion pour les lacs du sud-ouest du Groenland).

__Auteurs__ :
* Jordi Prats-Rodríguez (jprats@segula.es)
* Pierre-Alain Danis (pierre-alain.danis@afbiodiversite.fr)

<a name="requirements"> </a>

## 2. Exigences

Il est nécessaire de disposer de Python 3.5 ou d'une version ultérieure 
pour exécuter le paquet `okplm`. Plusieurs versions de Python (2.x et 
3.x) peuvent être installées sur le même système sans problème.

<a name="installation"> </a>

## 3. Installation

### 3.1. Clonage du référentiel
Le paquet `okplm` doit d'abord être cloné avec git :

```bash
clone de git https://gitlab.irstea.fr/alamode/okplm
```

Cette commande crée le répertoire okplm.

Pour installer la branche de développement du projet, après avoir cloné le paquet `okplm`,
 passer à la branche `dev` :

```git
cd okplm
git checkout dev
```

### 3.2 Installation `okplm`
Utilisation du fichier `setup.py` :

```bash
cd okplm
python setup.py install
```

En utilisant pip :

```bash
cd okplm
pip installer -U.
```

<a name="dependencies"> </a>

## 4. Dépendances

Le paquet `okplm` dépend des paquets Python suivants :

* numpy
* plotly (visualisation des résultats des exemples)

<a name="usage"> </a>

## 5. Utilisation

### 5.1. Les fichiers d'entrée

Le modèle lit les données d’entrée et de configuration à partir de 
trois fichiers texte, un fichier obligatoire et deux fichiers facultatifs :

* `meteo_file` contient les données de température de l'air et de 
rayonnement solaire de type  :
    ```bash
    date tair sr
    2015-01-01 -5.33050611827412 71.4207580210686
    2015-01-02 -4.60164477358152 71.5241748509779
    2015-01-03 -5.89963424289161 72.1985317055494
    ...
    2015-12-29 -5.14518104579149 71.285364985302
    2015-12-30 -5.23159986054971 68.6030234341654
    2015-12-31 -5.32627124395189 67.6253583097682
    ```
    où `date` est la date au format `yyyy-mm-dd`, `tair` est la 
    température moyenne (journalière, hebdomadaire ou mensuelle) de
    l'air en °C et `sr` est le rayonnement solaire moyen (journalier, 
    hebdomadaire ou mensuel) en W/m<sup>2</sup>.

* `lake_file` (facultatif) contient les caractéristiques du plan d'eau 
de type de type :
    ```bash
    name ALL04
    altitude 2232
    latitude 44.233
    zmax 51
    surface 528424.501
    volume 9775853.276
    type L
    ```
    où `zmax` est la profondeur maximale et `type` est égale à `L` pour
    les lacs naturels et `R` pour les plans d'eau articifiels. Ce fichier 
    est ignoré si `par_file` est donné en entrée.
* `par_file`  (facultatif) contient les valeurs des paramètres du modèle
    de type :
    ```bash
    A 6.2019195784542305
    B 1.0070000000000001
    C -0.00695984
    D 0.51
    E 0.24475648472125097
    ALPHA 0.070683752757536
    BETA 0.13
    mat -0.40699218131037035
    ```
    où `A` est la température moyenne annuelle de l'épilimnion,
    `B` est un facteur de modulation de l'effet de la température de l'air,
    `C` est un facteur de modulation de l'effect du rayonnement solaire,
    `D` est une constante (égale à 0.51 par défaut), `E` est un paramètre
    relationné avec l'intensité du gradient thermique vertical,
    `ALPHA` est un facteur de lissage exponentiel de la température de l'air,
    `BETA` est un facteur de lissage exponentiel de la température de
    l'hypolimnion, et `mat` est la température moyenne annuelle de l'air. 
    Si ce fichier n'est pas donné par l'utilisateur, le modèle crée 
    ce fichier en calculant les valeurs des paramètres en fonction des 
    caractéristiques du lac définies dans le fichier `lake_file` selon 
    le paramétrage de Prats & Danis (2019) pour les plans d'eau français
    d'eau douce.

Par défaut, la durée de la simulation est déterminée par la longueur 
du fichier `meteo_file`.
De plus, les données météorologiques peuvent être fournies à trois 
fréquences différentes : journalière, hebdomadaire et mensuelle.

Il est indispensable de fournir soit le fichier `lake_file`, 
soit le fichier `par_file`. Si le fichier `par_file` est donné, 
le programme utilise les valeurs de paramètre fournies dans ce fichier.
Sinon, le fichier `lake_file` est nécessaire et le programme calcule 
les paramètres du modèle à partir des caractéristiques du lac incluses
dans le fichier `lake_file`. Voir la documentation complète pour plus
de détails sur le formatage des fichiers d'entrée.

Une fois que vous avez créé les fichiers d’entrée, le paquet `okplm` 
peut être utilisé en ligne de commande ou en module Python.

### 5.2 Les fichiers de sortie

Le modèle produit trois types de fichiers de sortie, un fichier 
obligatoire et deux fichiers optionnels :

* `output_file` contient les résultats de la modélisation des températures
de l'épilimnion et de l'hypolimnoon en °C de type :
    ```bash
    date tepi thyp
    2015-01-01 0.77 4.0
    2015-01-02 0.82 4.00
    ...
    2015-12-29 0.36 4.0
    2015-12-30 0.39 4.0
    2015-12-31 0.42 4.0
    ```
* `par_file` (optionnel) contient les paramètres estimés à partir des
caractéristiques du plan d'eau (cf. ci-dessus) ;

* `err_file` (optionnel) contient les résultats de la validation de
    la modélisation des températures de l'épilimnion et de l'hypolimnoon 
    de type :
    ```bash
    n sd r me mae rmse
    10 2.285 0.871 -0.025 1.555 2.286
    10 0.596 0.757 -0.018 0.452 0.597
    ```

### 5.2 Application en ligne de commande

Pour exécuter `okplm` en ligne de commande dans un terminal, il faut 
être dans le répertoire contenant les fichiers d'entrée et faire :
```bash
run_okp
```

Pour obtenir de l'aide sur l'utilisation de l'application, lancez la commande :
```bash
run_okp -h
```
Par défaut, le modèle recherche les fichiers nommés :
* `meteo.txt` comprenant les données météorologiques ;
* `lake.txt` ou `par.txt` (au choix) comprenant soit les données des 
    caractéristiques du plan d'eau (`lake.txt`), soit les valeurs des 
    paramètres du modèle (`par.txt`).

...et, par défaut, le modèle produit un fichier de sortie nommé :
* 'ouput.txt' comprenant les résultats des modélisations

Vous pouvez indiquer le dossier des données d'entrée avec l'argument 
optionnel `-f`. Par exemple :
```bash
run_okp -f C:/utilisateurs/vous-même/data/lake_data_directory
```
Veuillez noter que le paquet comprend l’extension tilde '~' de la façon 
suivante :
```bash
run_okp -f ~/data/lake_data_directory
```
Pour les fichiers d'entrée, vous pouvez spécifier d’autres noms en 
utilisant un, deux ou trois des arguments optionnels `-m`,` -l` et/ou `-p`, 
respectivement. Par exemple :
```bash
run_okp -m monfichiermeteo.txt
run_okp -l monfichierlac.txt
run_okp -p monfichierpar.txt -l monfichierlac.txt
```
De même, les résultats sont écrits par défaut dans le fichier nommé 
`output.txt`, mais un autre nom de fichier peut être utilisé avec l'option `-o`.

La période de la simulation peut être limitée en spécifiant le début avec 
l'argument optionnel `-s` et la fin avec l'argument optionnel `-e` :
```bash
run_okp -s 2014-01-01 -e 2015-12-31
```

Par défaut, le programme suppose que les données d'entrée sont fournies
à un pas de temps journalier. 
Pour indiquer au modèle la fréquence des données météorologiques 
d'entrée et de la simulation, utiliser les arguments optionnels `-d` 
(*daily* = journalière), `-w` (*weekly* = hebdomadaire) ou `-n` (mensuelle).
Par exemple :
```bash
run_okp -w
```

Pour les simulations journalières, la sortie peut être quotidienne, 
hebdomadaire ou mensuelle en spécifiant l'un des arguments optionnels 
`--daily_output`,` --weekly_output` ou `--monthly_output`.

Il est également possible d’obtenir des statistiques d’erreur des 
simulations journalières en fournissant un fichier de données 
d’observations (par exemple, `obs.txt`) avec l'argument optionnel `-a`
et en fournissant le nom du fichier de résultats de validation 
(par exemple, `err_stats.txt`) avec l'argument optionnel `-b` :

```bash
run_okp -a obs.txt -b err_stats.txt
```

Si ces noms de fichiers ne sont pas fournis, les statistiques de
validation ne sont pas calculées.

### 5.3 Application via les modules Python
Pour utiliser `okplm` en tant que module Python, vous pouvez simplement 
l'importer avec :
```python
import okplm
```
Pour exécuter le modèle, commencez par définir les noms des différents 
dossiers et fichiers d'entrée et de sortie. Par exemple :
```python
import os
folder = path_to_data_repertory
output_file = os.path.join (dossier 'ouput.txt')
meteo_file = os.path.join (dossier, 'meteo.txt')
par_file = os.path.join (dossier, 'par.txt')
lake_file = os.path.join (dossier, 'lake.txt')
```

Il est possible d'utiliser l'extension tilde '~'.

Ensuite, tapez :

```python
okplm.run_okp(output_file = output_file, meteo_file = meteo_file,
               par_file = par_file, lake_file = lake_file)
```

Pour définir une date de début, une date de fin et/ou une périodicité pour les simulations :
```python
okplm.run_okp(output_file = output_file, meteo_file = meteo_file,
               par_file = par_file, lake_file = lake_file, start_date = '2014-01-01',
               end_date = '2015-12-31', periodicity = 'weekly')
```

Le résultat des simulations peut être obtenu aux fréquences journalière ("daily"),
hebdomadaire ("weekly") ou mensuelle ("monthly") en utilisant l'argument `output_periodicity`.

Dans le cas de simulation à fréquence journalière ("daily"), et uniquement dans ce cas, 
en fournissant un nom de fichier contenant des données d'observation (`validation_data_file`)
et un nom de fichier où écrire les résultats de la validation (`validation_res_file`),
les statistiques d'erreur sont calculées et sauvegardées dans le fichier spécifié `validation_res_file`.

Les fonctions `okplm.read_dict()` et `okplm.write_dict()` sont d'autres fonctions utiles
pour lire et écrire les données de lac et les fichiers de paramètres.

Vous pouvez inclure les commandes précédentes dans un script Python (voir l'exemple
script `examples/test_script.py`). Pour exécuter un script python à partir de la ligne de commande, tapez:

```bash
python path_to_script
```

Le script `test_script.py` fait appel à la fonction plotly_output() pour visualiser les résultats.


<a name="tests"> </a>

## 6. Tests

Le dossier `tests` contient 2 scripts permettant de tester les 
fonctionnalités du paquet `okplm` :

* tests/test_okp_model.py : teste la fonction `run_okp()`
* tests/test_validation.py : teste la fonction `error_statistics()`

<a name="Examples"> </a>

## 7. Exemples d'utilisation du paquet `okplm`

Vous pouvez tester le logiciel à l'aide des exemples de fichiers fournis. 
Le paquet contient quatre exemples de données dans le dossier 
`examples`, un exemple de script Python (`tests/test_script.py`),
et un module basée sur le paquet `plotly` (tests/plotly_fonctions.py) et
permettant de visualiser les résultats.

### 7.1 Les données

Dans ces exemples, les données du lac dans le fichier `lake.txt` correspondent à celles du lac d'Allos.
(code du lac = ALL04). Les données météorologiques (`meteo.txt`) sont des données synthétiques
d'une base de données météorologiques. La température de l'air a été créée à l'aide d'une température avec 
une composante saisonnière et un modèle ARMA (REF), tandis que les données de rayonnement solaire correspondent seulement à la
composante saisonnière.

Trois tests peuvent être réalisés avec `test_script.py` pour illustrer 
l’utilisation de `okplm` pour trois différentes fréquences. 
Les données nécessaires pour ces trois tests sont dans les dossiers :

* examples/synthetic_case_daily : données journalières
* examples/synthetic_case_weekly : données hebdomadaires
* examples/synthetic_case_monthly : données mensuelles

### 7.2 Les simulations

Pour ces trois cas, les données météorologiques (`meteo.txt`) et les 
données lacustres (`lake.txt`) sont fournies en entrée au modèle.
Par conséquent, les paramètres du modèle sont calculés à partir des 
caractéristiques du lac dans `lake.txt` avec la formulation suivante :

```python
okplm.run_okp(output_file, meteo_file, par_file, lake_file,
              periodicity=periodchoice)
```
              
Dans le cas d'une simulation avec des données journalières, le script
`test_script.py` donne un exemple de validation des résultats du 
modèle avec une fichier d'observation `obs.txt`.

```python
okplm.run_okp(output_file, meteo_file, par_file, lake_file,
              periodicity=periodchoice,
              validation_data_file=validation_data_file,
              validation_res_file=validation_res_file)
```

Le 4ème exemple réalisable dans le script `test_script.py` est le 
cas où un fichier utilisateur des paramètres du modèle est donné
en entrée. Les données sont dans le dossier :

* examples/synthetic_case_given : données quotidiennes 
 
Le modèle utilise donc les valeurs de paramètre (` par.txt`)
et les données météorologiques journalières (`meteo.txt`).
Le fichier `lake.txt` n'est pas nécessaire.

### 7.3 La visualisation des résultats

La fonction `plotlyoutput()` dans le script `plotly_functions.py` permet
de visualiser les résultats des simulations ainsi que, le cas échéant,
les valeurs des critères de validation (n, sd, r, me, mae et rmse) 
et les observations avec la formulation suivante :

```python
plotlyoutput(folder)
```

Les résultats sont alors présentés sous la forme d'un fichier html de
ce type :

<img src="images/plotlyoutput.png" width="600" alt="Exemple de figure donnée 
par la fonction `plotlyoutput()`">


<a name="references"> </a>

## 8. Références
* Kettle, H.; Thompson, R.; Anderson, N. J.; Livingstone, D. M. (2004)
Empirical modeling of summer lake surface temperatures in southwest Greenland.
*Limnology and Oceanography*, 49 (1), 271-282,
doi: [10.4319/lo.2004.49.1.0271](https://doi.org/10.4319/lo.2004.49.1.0271).
* Ottosson, F.; Abrahamsson, O. (1998) Presentation and analysis of a model
simulating epilimnetic and hypolimnetic temperatures in lakes. *Ecological
Modelling*, 110, 233-253, doi:
[10.1016/S0304-3800(98)00067-2](https://doi.org/10.1016/S0304-3800(98)00067-2).
* Prats, J.; Danis, P.-A. (2019) An epilimnion and hypolimnion temperature
model based on air temperature and lake characteristics. *Knowledge and
Management of Aquatic Ecosystems*, 420, 8, doi:
[10.1051/kmae/2019001](https://doi.org/10.1051/kmae/2019001).
