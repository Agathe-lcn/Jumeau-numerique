import json
import math
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union

with open('salles_R1.json', encoding='utf-8') as f:
    salles = json.load(f)

room_polys = {s['id']: Polygon(s['polygon']) for s in salles if s['polygon'] and len(s['polygon']) >= 3}
all_rooms_union = unary_union(list(room_polys.values()))

nodes = {
    # ── 1. Entrées & Hub Central ────────────────────────────────
    "ESCALIER_SUD":     {"x": 39.0, "y": 18.5, "nom": "Escalier Principal (Sud)"},
    "HUB_CENTRAL":      {"x": 36.0, "y": 18.5, "nom": "Hall Principal (R+1)"},
    "ASCENSEUR":        {"x": 33.2, "y": 19.5, "nom": "Ascenseur R+1 (Accès PMR)"},
    "ROTONDE_ENTREE":   {"x": 36.0, "y": 15.2, "nom": "Rotonde 103 (Carrefour central)"},
    "HUB_SUD_OUEST":    {"x": 28.5, "y": 17.5, "nom": "Jonction Sud-Ouest"},

    # ── 2. Couloir Amphis Est (101 & 102) ──────────────────────
    "HUB_EST":          {"x": 43.8, "y": 18.5, "nom": "Carrefour Amphis Est"},
    "PORTE_101":        {"x": 43.8, "y": 14.5, "nom": "Porte Amphithéâtre 101"},
    "PORTE_102":        {"x": 43.8, "y":  6.5, "nom": "Porte Amphithéâtre 102"},

    # ── 3. Contournement Est du Bureau 117 vers Couloir Sud ────
    "COUL_117_EST":     {"x": 28.5, "y": 11.5, "nom": "Couloir Est Bureau 117"},
    "COUL_117_SUD":     {"x": 28.5, "y":  8.6, "nom": "Angle Couloir Sud-Est"},

    # ── 4. Couloir Bureaux Sud (104 à 111 & 114 à 117) ─────────
    "COUL_SUD_104":     {"x": 25.5, "y":  8.6, "nom": "Porte Bureau 104 / 117"},
    "COUL_SUD_105":     {"x": 22.0, "y":  8.6, "nom": "Porte Bureau 105 / 116"},
    "COUL_SUD_106":     {"x": 19.3, "y":  8.6, "nom": "Porte Bureau 106 / 115"},
    "COUL_SUD_107":     {"x": 16.8, "y":  8.6, "nom": "Porte Bureau 107 / 114"},
    "COUL_SUD_108":     {"x": 14.4, "y":  8.6, "nom": "Porte Bureau 108"},
    "COUL_SUD_109":     {"x": 11.5, "y":  8.6, "nom": "Porte Bureau 109"},
    "COUL_SUD_110":     {"x": 10.5, "y":  8.6, "nom": "Porte Bureau 110"},
    "COUL_SUD_111":     {"x":  8.7, "y":  8.6, "nom": "Porte Bureau 111"},

    # ── 5. Couloir Ouest (112, 113, 118, 119, 120, 121, 126) ──
    "COUL_OUEST_112":   {"x": 10.5, "y": 11.0, "nom": "Porte Bureau 112"},
    "COUL_OUEST_113":   {"x": 10.5, "y": 13.5, "nom": "Porte Bureau 113"},
    "COUL_OUEST_JONCT": {"x": 10.5, "y": 17.5, "nom": "Jonction Ouest"},
    "COUL_OUEST_118":   {"x": 10.5, "y": 22.5, "nom": "Porte Bureau 118"},
    "COUL_OUEST_119":   {"x": 10.5, "y": 26.8, "nom": "Porte Bureau 119 / Dépôt 128"},
    "COUL_OUEST_120":   {"x": 10.5, "y": 29.8, "nom": "Porte Bureau 120"},
    "COUL_OUEST_121":   {"x": 10.5, "y": 34.0, "nom": "Porte Salle TD 121 / TP 127"},
    "COUL_OUEST_126":   {"x": 10.5, "y": 37.0, "nom": "Porte Salle TD 126"},

    # ── 6. Colonne Centrale Nord-Sud (x = 33.2) ────────────────
    "SPINE_1":          {"x": 33.2, "y": 22.5, "nom": "Couloir Central (Local 129)"},
    "SPINE_2":          {"x": 33.2, "y": 25.5, "nom": "Couloir Central (TD 138)"},
    "SPINE_3":          {"x": 33.2, "y": 29.0, "nom": "Couloir Central (TP 130)"},
    "SPINE_4":          {"x": 33.2, "y": 33.5, "nom": "Couloir Central (Technique 137)"},
    "SPINE_5":          {"x": 33.2, "y": 38.0, "nom": "Couloir Central (TD 136)"},
    "SPINE_6":          {"x": 33.2, "y": 42.0, "nom": "Couloir Central (TP 131)"},
    "SPINE_7":          {"x": 33.2, "y": 45.4, "nom": "Carrefour Central Nord"},

    # ── 7. Branche Nord-Ouest (Amphi 123, TD 122, TP 133) ──────
    "COUL_NW_133":      {"x": 28.5, "y": 45.4, "nom": "Porte Salle TP 133 / Dépôt 132"},
    "COUL_NW_123":      {"x": 23.5, "y": 45.0, "nom": "Porte Amphithéâtre 123 / Dépôt 124"},
    "COUL_NW_122":      {"x": 18.5, "y": 45.0, "nom": "Porte Salle TD 122 / Dépôt 125"},

    # ── 8. Branche Nord-Est (TD 135, TD 136, TD 148, TD 149) ───
    "COUL_NE_1":        {"x": 35.0, "y": 45.4, "nom": "Entrée Couloir Nord-Est"},
    "COUL_NE_2":        {"x": 41.0, "y": 45.4, "nom": "Carrefour TD 135 / TD 136"},
    "COUL_NE_3":        {"x": 44.5, "y": 45.4, "nom": "Carrefour TD 148 / TD 149"},
    "PORTE_135":        {"x": 41.0, "y": 51.0, "nom": "Porte Salle TD 135"},
    "PORTE_136":        {"x": 41.0, "y": 41.5, "nom": "Porte Salle TD 136"},
    "PORTE_148":        {"x": 44.5, "y": 51.0, "nom": "Porte Salle TD 148"},
    "PORTE_149":        {"x": 44.5, "y": 41.5, "nom": "Porte Salle TD 149 / Dépôt 150"},

    # ── 9. Couloir Bureaux Est (143, 144, 146) ─────────────────
    "COUL_NE_BUR_JUNCT":{"x": 51.8, "y": 45.4, "nom": "Jonction Bureaux Est"},
    "PORTE_146":        {"x": 51.8, "y": 48.5, "nom": "Porte Bureau 146"},
    "PORTE_144":        {"x": 51.8, "y": 43.5, "nom": "Porte Bureau 144"},
    "PORTE_143":        {"x": 51.8, "y": 38.8, "nom": "Porte Bureau 143"},

    # ── 10. Branche Est (TD 139, Serveurs 140/142, TD 141) ─────
    "COUL_EST_HUB":     {"x": 44.5, "y": 20.0, "nom": "Accès Aile Est"},
    "COUL_EST_139":     {"x": 44.5, "y": 24.5, "nom": "Porte Salle TD 139"},
    "COUL_EST_SERV":    {"x": 44.5, "y": 30.0, "nom": "Porte Serveurs 140 / 142 / TD 141"},
}

raw_edges = [
    # Hub & Entrées
    ("ESCALIER_SUD", "HUB_CENTRAL"),
    ("HUB_CENTRAL", "ASCENSEUR"),
    ("HUB_CENTRAL", "ROTONDE_ENTREE"),
    ("HUB_CENTRAL", "HUB_EST"),
    ("HUB_CENTRAL", "HUB_SUD_OUEST"),
    ("ASCENSEUR", "SPINE_1"),

    # Amphis Est
    ("HUB_EST", "PORTE_101"),
    ("PORTE_101", "PORTE_102"),
    ("HUB_EST", "COUL_EST_HUB"),

    # Contournement Bureau 117
    ("HUB_SUD_OUEST", "COUL_117_EST"),
    ("COUL_117_EST", "COUL_117_SUD"),
    ("COUL_117_SUD", "COUL_SUD_104"),

    # Bureaux Sud
    ("COUL_SUD_104", "COUL_SUD_105"),
    ("COUL_SUD_105", "COUL_SUD_106"),
    ("COUL_SUD_106", "COUL_SUD_107"),
    ("COUL_SUD_107", "COUL_SUD_108"),
    ("COUL_SUD_108", "COUL_SUD_109"),
    ("COUL_SUD_109", "COUL_SUD_110"),
    ("COUL_SUD_110", "COUL_SUD_111"),
    ("COUL_SUD_110", "COUL_OUEST_112"),

    # Couloir Ouest
    ("COUL_OUEST_112", "COUL_OUEST_113"),
    ("COUL_OUEST_113", "COUL_OUEST_JONCT"),
    ("HUB_SUD_OUEST", "COUL_OUEST_JONCT"),
    ("COUL_OUEST_JONCT", "COUL_OUEST_118"),
    ("COUL_OUEST_118", "COUL_OUEST_119"),
    ("COUL_OUEST_119", "COUL_OUEST_120"),
    ("COUL_OUEST_120", "COUL_OUEST_121"),
    ("COUL_OUEST_121", "COUL_OUEST_126"),

    # Spine Centrale
    ("SPINE_1", "SPINE_2"),
    ("SPINE_2", "SPINE_3"),
    ("SPINE_3", "SPINE_4"),
    ("SPINE_4", "SPINE_5"),
    ("SPINE_5", "SPINE_6"),
    ("SPINE_6", "SPINE_7"),

    # Nord-Ouest
    ("SPINE_7", "COUL_NW_133"),
    ("COUL_NW_133", "COUL_NW_123"),
    ("COUL_NW_123", "COUL_NW_122"),

    # Nord-Est
    ("SPINE_7", "COUL_NE_1"),
    ("COUL_NE_1", "COUL_NE_2"),
    ("COUL_NE_2", "COUL_NE_3"),
    ("COUL_NE_2", "PORTE_135"),
    ("COUL_NE_2", "PORTE_136"),
    ("COUL_NE_3", "PORTE_148"),
    ("COUL_NE_3", "PORTE_149"),

    # Passage vers Bureaux 143, 144, 146 (y = 45.4)
    ("COUL_NE_3", "COUL_NE_BUR_JUNCT"),
    ("COUL_NE_BUR_JUNCT", "PORTE_146"),
    ("COUL_NE_BUR_JUNCT", "PORTE_144"),
    ("PORTE_144", "PORTE_143"),

    # Est
    ("COUL_EST_HUB", "COUL_EST_139"),
    ("COUL_EST_139", "COUL_EST_SERV"),
]

# Map every room to its closest doorstep node
room_access = {
    "101": "PORTE_101",
    "102": "PORTE_102",
    "103": "ROTONDE_ENTREE",
    "104": "COUL_SUD_104",
    "105": "COUL_SUD_105",
    "106": "COUL_SUD_106",
    "107": "COUL_SUD_107",
    "108": "COUL_SUD_108",
    "109": "COUL_SUD_109",
    "110": "COUL_SUD_110",
    "111": "COUL_SUD_111",
    "112": "COUL_OUEST_112",
    "113": "COUL_OUEST_113",
    "114": "COUL_SUD_107",
    "115": "COUL_SUD_106",
    "116": "COUL_SUD_105",
    "117": "COUL_SUD_104",
    "118": "COUL_OUEST_118",
    "119": "COUL_OUEST_119",
    "120": "COUL_OUEST_120",
    "121": "COUL_OUEST_121",
    "122": "COUL_NW_122",
    "123": "COUL_NW_123",
    "124": "COUL_NW_123",
    "125": "COUL_NW_122",
    "126": "COUL_OUEST_126",
    "127": "COUL_OUEST_121",
    "128": "COUL_OUEST_119",
    "129": "SPINE_1",
    "130": "SPINE_3",
    "131": "SPINE_6",
    "132": "COUL_NW_133",
    "133": "COUL_NW_133",
    "134": "COUL_NW_123",
    "135": "PORTE_135",
    "136": "PORTE_136",
    "137": "SPINE_4",
    "138": "SPINE_2",
    "139": "COUL_EST_139",
    "140": "COUL_EST_SERV",
    "141": "COUL_EST_SERV",
    "142": "COUL_EST_SERV",
    "143": "PORTE_143",
    "144": "PORTE_144",
    "146": "PORTE_146",
    "148": "PORTE_148",
    "149": "PORTE_149",
    "150": "PORTE_149",
    "ESCALIER_SUD": "ESCALIER_SUD",
    "ASCENSEUR": "ASCENSEUR",
    "VOUS_ETES_ICI": "ESCALIER_SUD"
}

# Build graph structure
adj = {k: [] for k in nodes}
for u, v in raw_edges:
    p1 = (nodes[u]["x"], nodes[u]["y"])
    p2 = (nodes[v]["x"], nodes[v]["y"])
    d = round(math.hypot(p1[0] - p2[0], p1[1] - p2[1]), 2)
    adj[u].append({"node": v, "dist": d})
    adj[v].append({"node": u, "dist": d})

for k in nodes:
    nodes[k]["voisins"] = adj[k]

# Save to graph_R1.json
graph_export = {
    "nodes": nodes,
    "room_access": room_access
}

with open('graph_R1.json', 'w', encoding='utf-8') as f:
    json.dump(graph_export, f, indent=2, ensure_ascii=False)

print(f"graph_R1.json generated with {len(nodes)} nodes and {len(raw_edges)} edges.")
print(f"Room access map contains {len(room_access)} entries (covers all 48 rooms + entrances).")

# Verification: Run Dijkstra from VOUS_ETES_ICI to EVERY room
def dijkstra(start, target):
    dist = {n: float('inf') for n in nodes}
    prev = {}
    q = set(nodes.keys())
    dist[start] = 0
    while q:
        u = min(q, key=lambda n: dist[n])
        if u == target or dist[u] == float('inf'):
            break
        q.remove(u)
        for edge in nodes[u]["voisins"]:
            v = edge["node"]
            if v in q:
                alt = dist[u] + edge["dist"]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
    path = []
    cur = target
    while cur:
        path.insert(0, cur)
        cur = prev.get(cur)
    return path

all_ok = True
for r in salles:
    rid = r['id']
    door = room_access.get(rid)
    if not door:
        print(f"ERROR: Room {rid} has no door!")
        all_ok = False
        continue
    path = dijkstra("ESCALIER_SUD", door)
    if not path or path[0] != "ESCALIER_SUD":
        print(f"ERROR: No path to room {rid} (door {door})")
        all_ok = False
        continue
    # Check that EVERY segment of path has ZERO room intersections!
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        p1 = (nodes[u]["x"], nodes[u]["y"])
        p2 = (nodes[v]["x"], nodes[v]["y"])
        line = LineString([p1, p2])
        inter = all_rooms_union.intersection(line)
        if inter.length > 0.05:
            print(f"CRITICAL: Path to room {rid} intersects room at {u} <-> {v} (len={inter.length:.2f}m)")
            all_ok = False

if all_ok:
    print("AUDIT PASSED: 100% of the 48 rooms are reachable, and NOT A SINGLE PATH EVER CUTS INTO ANY ROOM!")
