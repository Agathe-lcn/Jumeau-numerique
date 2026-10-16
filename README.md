# Jumeau Numérique 3D & Orientation Indoor — ensIIE (Étage R+1)

Projet développé pour l'école **ensIIE** (École Nationale Supérieure d'Informatique pour l'Industrie et l'Entreprise).

Cette application interactive propose une visualisation 3D en temps réel et un système de guidage indoor complet pour l'étage R+1 du bâtiment principal.

---

## 🌟 Fonctionnalités

- **Plan 3D Interactif** :
  - Modélisation polygonale fidèle des **48 espaces** de l'étage R+1 (Amphithéâtres, Salles de TP, Salles de TD, Bureaux enseignants, Rotonde, Salle des professeurs, Locaux techniques).
  - Code couleur distinct et contrasté par typologie d'espace.
  - Étiquettes 3D flottantes dynamiques affichant le numéro et le type de chaque salle.
  - Indicateur animé de géolocalisation intérieure (« 📍 VOUS ÊTES ICI »).
  - Contrôles de caméra 3D fluides (rotation orbitale, pan, zoom molette).

- **Navigation Indoor & Itinéraire Étape par Étape** :
  - Calcul de chemin optimal via l'algorithme de **Dijkstra**.
  - **100% de circulation dans les couloirs** d'après le plan d'évacuation officiel (zéro traversée de salle fermée).
  - Tracé 3D lumineux en tube fluide (Catmull-Rom).
  - **Guidage pas à pas** avec flèches directionnelles (⬆️ Tout droit, ↰ Gauche, ↱ Droite, 🎯 Arrivée).
  - Estimation de la distance en mètres et du temps de trajet à pied.
  - **Mode Mobilité Réduite (PMR)** : Trajets adaptés via l'ascenseur sans escaliers.

- **Recherche & Fiches Salles** :
  - Barre de recherche instantanée par numéro de salle, type ou nom d'enseignant.
  - Filtres par catégorie (`Tous`, `Amphis`, `Salles TP`, `Salles TD`, `Bureaux`, `Libres`).
  - Fiches détaillées : photo réelle de la salle (agrandissable en plein écran), surface ($m^2$), capacité, statut d'occupation et emploi du temps de la journée.

---

## 📁 Structure du Projet

```text
├── index.html            # Application web autonome complète (Three.js 3D + Interface)
├── three.min.js          # Moteur 3D local
├── OrbitControls.js      # Contrôleur caméra orbitale
├── images/               # Photos réelles des salles et logo officiel ensIIE
├── salles_R1.json        # Base de données des 48 espaces (données réelles)
├── graph_R1.json         # Graphe officiel des couloirs de circulation
├── build_app.py          # Script de génération / mise à jour de l'application
├── build_clean_graph.py  # Script de calcul géométrique des couloirs (Shapely)
├── build_dataset.py      # Script d'assemblage des données CSV et GeoJSON
├── pieces_R+1.geojson    # Géométrie vectorielle du plan d'architecte
├── salles.csv            # Inventaire des salles et enseignants
└── plan_R+1.png          # Plan d'évacuation de référence
```

---

## 🚀 Lancement Rapide

Ouvrez simplement un serveur HTTP local dans le dossier :

```bash
python -m http.server 8080
```

Puis accédez à l'application dans votre navigateur :
👉 **http://localhost:8080**
