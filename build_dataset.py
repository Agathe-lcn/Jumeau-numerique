import json
import openpyxl
import os

# ─── Load GeoJSON ────────────────────────────────────────────────────────────
with open('c:/Users/21270/OneDrive/Desktop/hackathon/pieces_R+1.geojson', encoding='utf-8') as f:
    geojson = json.load(f)

# ─── Load Real Data from Excel ───────────────────────────────────────────────
wb = openpyxl.load_workbook(
    r'C:/Users/21270/.gemini/antigravity/brain/f9348672-0154-4217-97a5-24b2bdbd8b1d/.user_uploaded/media_1792077011302_85e32eef.xlsx'
)
ws = wb.active

salles_excel = {}
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i == 0:
        headers = row
        continue
    if all(v is None for v in row):
        continue
    d = dict(zip(headers, row))
    num = d.get('numero')
    if num is None:
        continue
    num_str = str(int(num))
    img_raw = d.get('image')
    if img_raw:
        img_clean = img_raw.strip().strip('"')
        img_filename = os.path.basename(img_clean)
        d['image_file'] = f"images/{img_filename}"
    else:
        d['image_file'] = None

    surf = d.get('surface_m2')
    if surf is not None:
        try:
            surf = float(surf)
        except (ValueError, TypeError):
            surf = None
    d['surface_m2_parsed'] = surf

    cap = d.get('Capacité')
    if cap is not None:
        try:
            cap = int(cap)
        except (ValueError, TypeError):
            cap = None
    d['capacite_parsed'] = cap
    salles_excel[num_str] = d

# Known specific occupants for bureaux (from Excel / school data)
known_occupants = {
    "104": {"responsable": "Massinissa Merabet, Stefania Dumbrava", "role": "Enseignants-Chercheurs ensIIE", "email": "merabet@ensiie.fr", "dispo": "Sur rendez-vous"},
    "105": {"responsable": "Vathana Ly Vath", "role": "Enseignant-Chercheur (Finance & Maths)", "email": "vathana.lyvath@ensiie.fr", "dispo": "Sur rendez-vous"},
    "106": {"responsable": "Bureau Enseignants", "role": "Corps professoral ensIIE", "email": "contact106@ensiie.fr", "dispo": "Disponible"},
    "107": {"responsable": "Mathilde Mougeot", "role": "Enseignante-Chercheuse (Machine Learning & Data)", "email": "mathilde.mougeot@ensiie.fr", "dispo": "Sur rendez-vous"},
    "108": {"responsable": "Nicolas Brunel", "role": "Enseignant-Chercheur (Statistiques & IA)", "email": "nicolas.brunel@ensiie.fr", "dispo": "Sur rendez-vous"},
    "109": {"responsable": "Abass Sagna", "role": "Enseignant-Chercheur (Mathématiques Financières)", "email": "abass.sagna@ensiie.fr", "dispo": "Sur rendez-vous"},
    "110": {"responsable": "Catherine Dubois", "role": "Enseignante-Chercheuse (Informatique & Logique)", "email": "catherine.dubois@ensiie.fr", "dispo": "Sur rendez-vous"},
    "111": {"responsable": "David Roussel, Guillaume Bouyer", "role": "Enseignants-Chercheurs (Réalité Virtuelle & Systèmes)", "email": "david.roussel@ensiie.fr", "dispo": "Sur rendez-vous"},
    "112": {"responsable": "Anne-Laure Ligozat", "role": "Enseignante-Chercheuse (Traitement Automatique Langues / NLP)", "email": "anne-laure.ligozat@ensiie.fr", "dispo": "Sur rendez-vous"},
    "113": {"responsable": "Sergio Pulido Nino", "role": "Enseignant-Chercheur (Mathématiques Appliquées)", "email": "sergio.pulido@ensiie.fr", "dispo": "Sur rendez-vous"},
    "114": {"responsable": "Bureau Pédagogique 114", "role": "Personnel enseignant / Réserve matériel", "email": "contact114@ensiie.fr", "dispo": "Disponible"},
    "117": {"responsable": "Bureau & Salle de Réunion 117", "role": "Espace de réunion pédagogique & enseignants", "email": "reunions@ensiie.fr", "dispo": "Réservation sur Aurion"},
    "118": {"responsable": "Obaïda Alrazouk, Aurélien Enfroy, Sofiane Ziani", "role": "Enseignants-Chercheurs (Informatique & Systèmes)", "email": "contact118@ensiie.fr", "dispo": "Sur rendez-vous"},
    "119": {"responsable": "Juhyun Park, Thi Phuong Thuy Vo", "role": "Enseignants-Chercheurs (Mathématiques & Stats)", "email": "contact119@ensiie.fr", "dispo": "Sur rendez-vous"},
    "120": {"responsable": "Christine Arioli", "role": "Enseignante & Coordination Langues / SHS", "email": "christine.arioli@ensiie.fr", "dispo": "Sur rendez-vous"},
    "143": {"responsable": "Raphaël Jadot", "role": "Enseignant-Chercheur & DSI Réseaux", "email": "raphael.jadot@ensiie.fr", "dispo": "Sur rendez-vous"},
    "144": {"responsable": "Gaël Thomas, Mohamed Coulibaly, Nordine Aounallah", "role": "Enseignants-Chercheurs (Systèmes Distribués)", "email": "gael.thomas@ensiie.fr", "dispo": "Sur rendez-vous"},
    "146": {"responsable": "Mohamed Nordine", "role": "Enseignant-Chercheur (Informatique & Architectures)", "email": "mohamed.nordine@ensiie.fr", "dispo": "Sur rendez-vous"},
}

schedules = {
    "101": [
        {"heure": "09:00 - 10:30", "titre": "Lancement Hackathon ensIIE 2026", "promo": "Promo 2026 & 2027", "statut": "Passé"},
        {"heure": "10:30 - 16:30", "titre": "Hackathon : Session de travail autonome", "promo": "Toutes promos", "statut": "En cours", "actuel": True},
        {"heure": "16:30 - 18:00", "titre": "Conférence Souveraineté Numérique", "promo": "Ouvert à tous", "statut": "À venir"}
    ],
    "102": [
        {"heure": "08:30 - 11:30", "titre": "Conférence Architecture Microservices", "promo": "3A Systèmes d'Information", "statut": "Terminé"},
        {"heure": "11:30 - 14:00", "titre": "Amphi Libre / Pause Déjeuner", "promo": "Libre", "statut": "Libre"},
        {"heure": "14:00 - 17:00", "titre": "Projet Hackathon : Mentorat", "promo": "Équipes P1 & P2", "statut": "À venir"}
    ],
    "103": [
        {"heure": "Journée", "titre": "Espace d'exposition et carrefour de rencontres", "promo": "Tous publics", "statut": "Accès libre", "actuel": True}
    ],
    "121": [
        {"heure": "08:30 - 10:30", "titre": "TD Algorithmique & Structures de Données", "promo": "1A Groupe 1", "statut": "Terminé"},
        {"heure": "10:30 - 13:00", "titre": "Travaux dirigés Hackathon", "promo": "Équipes 1A", "statut": "En cours", "actuel": True},
        {"heure": "14:30 - 17:30", "titre": "TD Systèmes Concurrents", "promo": "2A Groupe 2", "statut": "À venir"}
    ],
    "122": [
        {"heure": "09:00 - 12:00", "titre": "TD Mathématiques Appliquées", "promo": "1A Groupe 3", "statut": "Terminé"},
        {"heure": "14:00 - 17:30", "titre": "TD Probabilités & Statistiques", "promo": "2A Groupe 1", "statut": "À venir"}
    ],
    "123": [
        {"heure": "09:00 - 11:00", "titre": "TD Physique & Electronique", "promo": "1A Groupe 2", "statut": "En cours", "actuel": True},
        {"heure": "14:00 - 16:00", "titre": "TD Automatique", "promo": "2A Groupe 3", "statut": "À venir"}
    ],
    "126": [
        {"heure": "08:30 - 12:00", "titre": "TD Génie Logiciel & Méthodes Agiles", "promo": "2A Groupe 3", "statut": "Terminé"},
        {"heure": "14:00 - 17:00", "titre": "Salle libre – Travail en groupe", "promo": "Tous", "statut": "Libre", "actuel": True}
    ],
    "127": [
        {"heure": "08:30 - 12:00", "titre": "TP Programmation Système Linux / C", "promo": "1A Groupe 3", "statut": "Terminé"},
        {"heure": "12:00 - 14:00", "titre": "Salle Libre – Révisions", "promo": "Libre", "statut": "Libre", "actuel": True},
        {"heure": "14:00 - 18:00", "titre": "TP Réseaux TCP/IP & Wireshark", "promo": "2A Groupe 1", "statut": "À venir"}
    ],
    "130": [
        {"heure": "10:00 - 13:00", "titre": "Hackathon : Salle de dev", "promo": "Équipes Projet 2", "statut": "En cours", "actuel": True},
        {"heure": "14:00 - 17:30", "titre": "Hackathon : Session après-midi", "promo": "Équipes Projet 2", "statut": "À venir"}
    ],
    "131": [
        {"heure": "09:00 - 12:30", "titre": "TP Deep Learning & Vision par Ordinateur", "promo": "3A Intelligence Artificielle", "statut": "Terminé"},
        {"heure": "12:30 - 18:00", "titre": "Salle Libre", "promo": "Accès étudiants", "statut": "Libre", "actuel": True}
    ],
    "133": [
        {"heure": "08:30 - 12:30", "titre": "TP Sécurité des Réseaux & Pentest", "promo": "3A Cybersécurité", "statut": "Terminé"},
        {"heure": "12:30 - 18:00", "titre": "Hackathon – Salle de prototypage", "promo": "Équipes ensIIE", "statut": "En cours", "actuel": True}
    ],
    "135": [
        {"heure": "09:00 - 12:00", "titre": "TD Mathématiques pour l'Ingénieur", "promo": "1A Groupe 4", "statut": "Terminé"},
        {"heure": "12:00 - 18:00", "titre": "Salle Libre (Travail en groupe)", "promo": "Tous", "statut": "Libre", "actuel": True}
    ],
    "136": [
        {"heure": "09:00 - 12:00", "titre": "TD Économie & Management", "promo": "2A", "statut": "En cours", "actuel": True},
        {"heure": "14:00 - 17:00", "titre": "TD Droit du Numérique", "promo": "3A", "statut": "À venir"}
    ],
    "138": [
        {"heure": "10:00 - 12:30", "titre": "TD Bases de Données Relationnelles", "promo": "1A Groupe 2", "statut": "En cours", "actuel": True},
        {"heure": "14:00 - 17:00", "titre": "TD Génie Logiciel & Méthodes Agiles", "promo": "2A Groupe 3", "statut": "À venir"}
    ],
    "139": [
        {"heure": "Toute la journée", "titre": "Salle en libre accès – Travail collaboratif", "promo": "Étudiants ensIIE", "statut": "Libre", "actuel": True}
    ],
    "141": [
        {"heure": "09:00 - 12:00", "titre": "TD Projet Hackathon – Groupe D", "promo": "1A & 2A", "statut": "En cours", "actuel": True},
        {"heure": "14:00 - 17:30", "titre": "Travaux dirigés – Projet intégratif", "promo": "2A Groupe 4", "statut": "À venir"}
    ],
    "148": [
        {"heure": "09:00 - 12:00", "titre": "TD Réseaux & Protocoles", "promo": "2A Groupe 5", "statut": "Terminé"},
        {"heure": "14:00 - 17:30", "titre": "TD Sécurité Informatique", "promo": "3A", "statut": "En cours", "actuel": True}
    ],
    "149": [
        {"heure": "08:30 - 12:00", "titre": "TD Systèmes d'Information", "promo": "3A", "statut": "Terminé"},
        {"heure": "14:00 - 17:30", "titre": "Projet Hackathon – Mentorat", "promo": "Toutes promos", "statut": "À venir"}
    ],
}

processed_rooms = []
seen_numbers = set()

for i, feature in enumerate(geojson['features']):
    props = feature['properties']
    geom = feature['geometry']
    coords = geom['coordinates'][0]

    cx = sum(c[0] for c in coords) / len(coords)
    cy = sum(c[1] for c in coords) / len(coords)

    num = props.get('numero')
    libelle = props.get('libelle') or ''

    # Rotonde 103
    if not num and i == 74:
        num = "103"
        libelle = "Rotonde"

    if not num:
        continue

    num_str = str(num).strip()
    seen_numbers.add(num_str)

    excel = salles_excel.get(num_str, {})
    libelle_excel = excel.get('libelle', '') or ''
    if libelle_excel:
        libelle = libelle_excel

    # Ensure 114 and 117 are bureaux as in architectural plan
    if num_str in ["114", "117"]:
        libelle = "Bureau"

    # Category
    lib_lower = libelle.lower()
    if "amphi" in lib_lower:
        cat = "amphi"
        cat_nom = "Amphithéâtre"
        couleur = "#2563eb"
    elif "salle de tp" in lib_lower or "tp" in lib_lower:
        cat = "tp"
        cat_nom = "Salle de TP Informatique"
        couleur = "#0284c7"
    elif "salle de td" in lib_lower or "td" in lib_lower:
        cat = "td"
        cat_nom = "Salle de TD"
        couleur = "#3b82f6"
    elif "bureau" in lib_lower or num_str in ["104","105","106","107","108","109","110","111","112","113","114","117","118","119","120","143","144","146"]:
        cat = "bureau"
        cat_nom = "Bureau Enseignant"
        couleur = "#16a34a"
    elif "rotonde" in lib_lower or num_str == "103":
        cat = "rotonde"
        cat_nom = "Espace Central / Vie Étudiante"
        couleur = "#9333ea"
    elif "serveur" in lib_lower:
        cat = "technique"
        cat_nom = "Salle Serveur"
        couleur = "#64748b"
    elif "technique" in lib_lower or "local" in lib_lower:
        cat = "technique"
        cat_nom = "Local Technique"
        couleur = "#64748b"
    elif "dépôt" in lib_lower or "depot" in lib_lower or "réserve" in lib_lower:
        cat = "depot"
        cat_nom = "Dépôt / Réserve"
        couleur = "#94a3b8"
    elif "professeur" in lib_lower:
        cat = "salle_profs"
        cat_nom = "Salle des Professeurs"
        couleur = "#f59e0b"
    else:
        cat = "autre"
        cat_nom = libelle or "Espace Pédagogique"
        couleur = "#3b82f6"

    surf = excel.get('surface_m2_parsed')
    if surf is None:
        surf = props.get('surface_plan_m2') or props.get('surface_polygone_m2') or 20.0
    surf = round(float(surf), 1) if surf else 20.0

    cap_int = excel.get('capacite_parsed')
    if cap_int:
        capacite = f"{cap_int} places"
    elif cat == "amphi":
        capacite = "100 places"
    elif cat == "tp":
        capacite = "30 postes"
    elif cat == "td":
        capacite = "30 places"
    elif cat == "bureau":
        capacite = "1 à 3 enseignants"
    elif cat == "rotonde":
        capacite = "150 personnes"
    else:
        capacite = "Variable"

    # Occupant
    occupant_info = known_occupants.get(num_str)
    if not occupant_info and cat == "bureau":
        occupant_info = {
            "responsable": f"Bureau Enseignant {num_str}",
            "role": "Enseignant-Chercheur ensIIE",
            "email": "contact@ensiie.fr",
            "dispo": "Sur rendez-vous"
        }

    # Schedules
    sched = schedules.get(num_str, [])
    if not sched:
        if cat in ["tp", "td"]:
            sched = [
                {"heure": "09:00 - 12:00", "titre": f"Séance de {cat_nom}", "promo": "Promo ensIIE", "statut": "En cours", "actuel": True},
                {"heure": "12:00 - 14:00", "titre": "Salle Libre", "promo": "Accès libre", "statut": "Libre"},
                {"heure": "14:00 - 17:30", "titre": "Projet / Travail d'équipe", "promo": "Tous cursus", "statut": "À venir"}
            ]
        elif cat == "bureau":
            resp = (occupant_info or {}).get('responsable', f'Bureau {num_str}')
            sched = [
                {"heure": "09h00 - 12h30", "titre": f"Permanence : {resp}", "promo": "Sur place", "statut": "Disponible", "actuel": True},
                {"heure": "14h00 - 17h00", "titre": "Recherche & Préparation de cours", "promo": "En bureau", "statut": "Disponible"}
            ]
        elif cat == "rotonde":
            sched = [
                {"heure": "Journée", "titre": "Espace ouvert – Vie étudiante", "promo": "Tous publics", "statut": "Accès libre", "actuel": True}
            ]
        else:
            sched = [
                {"heure": "Toute la journée", "titre": "Accès selon usage", "promo": "Tous", "statut": "Ouvert", "actuel": True}
            ]

    is_libre = any(s.get('statut') in ['Libre', 'Accès libre'] and s.get('actuel') for s in sched)
    if cat == "bureau":
        is_libre = True

    image_file = excel.get('image_file')

    if cat == "rotonde":
        nom = "Rotonde – 1er Étage"
    elif cat == "bureau" and occupant_info:
        nom = f"Bureau {num_str} – {occupant_info['responsable'].split(',')[0].strip()}"
    else:
        nom = f"{libelle} {num_str}"

    processed_rooms.append({
        "id": num_str,
        "feature_index": i,
        "numero": num_str,
        "nom": nom,
        "libelle": libelle or cat_nom,
        "categorie": cat,
        "categorie_nom": cat_nom,
        "surface": surf,
        "capacite": capacite,
        "couleur": couleur,
        "center": [round(cx, 3), round(cy, 3)],
        "polygon": coords,
        "occupant": occupant_info,
        "planning": sched,
        "actuellement_libre": is_libre,
        "image": image_file,
        "infos_privees": {
            "code_acces": f"Badge Vigik #{1000 + int(num_str) if num_str.isdigit() else 1150}",
            "notes": f"Clés de secours au poste de sécurité RDC. Réf: INV-2026-R1-{num_str}.",
            "statut_materiel": "Matériel conforme"
        }
    })

# ─── Add Bureau 144 & Bureau 146 & Repro 116 & Local 129 if not present ────
extra_rooms = [
    {
        "id": "144",
        "numero": "144",
        "nom": "Bureau 144 – Gaël Thomas",
        "libelle": "Bureau",
        "categorie": "bureau",
        "categorie_nom": "Bureau Enseignant",
        "surface": 18.0,
        "capacite": "1 à 3 enseignants",
        "couleur": "#16a34a",
        "center": [54.7, 43.25],
        "polygon": [[52.78, 40.5], [56.67, 40.5], [56.67, 45.8], [52.78, 45.8], [52.78, 40.5]],
        "occupant": known_occupants["144"],
        "planning": [
            {"heure": "09h00 - 12h30", "titre": "Permanence : Gaël Thomas", "promo": "Sur place", "statut": "Disponible", "actuel": True},
            {"heure": "14h00 - 17h00", "titre": "Recherche & Encadrement", "promo": "En bureau", "statut": "Disponible"}
        ],
        "actuellement_libre": True,
        "image": None,
        "infos_privees": {"code_acces": "Badge Vigik #1144", "notes": "Clés au poste sécurité. Réf: INV-2026-R1-144.", "statut_materiel": "Matériel conforme"}
    },
    {
        "id": "146",
        "numero": "146",
        "nom": "Bureau 146 – Mohamed Nordine",
        "libelle": "Bureau",
        "categorie": "bureau",
        "categorie_nom": "Bureau Enseignant",
        "surface": 21.0,
        "capacite": "1 à 3 enseignants",
        "couleur": "#16a34a",
        "center": [54.7, 48.85],
        "polygon": [[52.78, 46.0], [56.67, 46.0], [56.67, 51.5], [52.78, 51.5], [52.78, 46.0]],
        "occupant": known_occupants["146"],
        "planning": [
            {"heure": "09h00 - 12h30", "titre": "Permanence : Mohamed Nordine", "promo": "Sur place", "statut": "Disponible", "actuel": True},
            {"heure": "14h00 - 17h00", "titre": "Recherche Architectures", "promo": "En bureau", "statut": "Disponible"}
        ],
        "actuellement_libre": True,
        "image": None,
        "infos_privees": {"code_acces": "Badge Vigik #1146", "notes": "Clés au poste sécurité. Réf: INV-2026-R1-146.", "statut_materiel": "Matériel conforme"}
    },
    {
        "id": "116",
        "numero": "116",
        "nom": "Reprographie 116",
        "libelle": "Reprographie",
        "categorie": "technique",
        "categorie_nom": "Local Reprographie",
        "surface": 10.0,
        "capacite": "Personnel",
        "couleur": "#64748b",
        "center": [22.75, 12.4],
        "polygon": [[21.5, 10.38], [24.0, 10.38], [24.0, 14.41], [21.5, 14.41], [21.5, 10.38]],
        "occupant": None,
        "planning": [{"heure": "Toute la journée", "titre": "Imprimantes & Copieurs", "promo": "Personnel", "statut": "Accès libre", "actuel": True}],
        "actuellement_libre": True,
        "image": None,
        "infos_privees": {"code_acces": "Badge Vigik #1116", "notes": "Local technique reprographie.", "statut_materiel": "Copieurs connectés"}
    },
    {
        "id": "129",
        "numero": "129",
        "nom": "Local ménage 129",
        "libelle": "Local ménage",
        "categorie": "technique",
        "categorie_nom": "Local Ménage & Entretien",
        "surface": 8.0,
        "capacite": "Personnel entretien",
        "couleur": "#94a3b8",
        "center": [30.5, 25.0],
        "polygon": [[29.0, 23.5], [32.0, 23.5], [32.0, 26.5], [29.0, 26.5], [29.0, 23.5]],
        "occupant": None,
        "planning": [{"heure": "Journée", "titre": "Local matériel", "promo": "Agents", "statut": "Service", "actuel": True}],
        "actuellement_libre": True,
        "image": None,
        "infos_privees": {"code_acces": "Clé service entretien", "notes": "Local produits entretien.", "statut_materiel": "Conforme"}
    }
]

for extra in extra_rooms:
    if extra["id"] not in seen_numbers:
        processed_rooms.append(extra)
        seen_numbers.add(extra["id"])

# Sort numerically
processed_rooms.sort(key=lambda r: int(r['numero']) if r['numero'].isdigit() else 999)

with open('c:/Users/21270/OneDrive/Desktop/hackathon/salles_R1.json', 'w', encoding='utf-8') as f:
    json.dump(processed_rooms, f, ensure_ascii=False, indent=2)

print(f"Total rooms generated: {len(processed_rooms)}")
b_count = sum(1 for r in processed_rooms if r['categorie'] == 'bureau')
print(f"Total bureaux: {b_count}")
