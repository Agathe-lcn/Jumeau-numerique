// 1. Initialiser la carte Leaflet
const map = L.map('carte', {
    crs: L.CRS.Simple,
    minZoom: -2,
    maxZoom: 4
});

const bornes = [[0, 0], [60, 60]]; 
L.imageOverlay('plans/plan_R+1.png', bornes).addTo(map);
map.fitBounds(bornes);

let couchesSalles = {}; 

// 2. Charger le fichier GeoJSON des pièces
fetch('plans/pieces_R+1.geojson')
    .then(response => response.json())
    .then(geojsonData => {
        L.geoJSON(geojsonData, {
            style: function(feature) {
                return {
                    color: "#0078A8",
                    weight: 1,
                    fillColor: "#0078A8",
                    fillOpacity: feature.properties.fiable ? 0.3 : 0.05
                };
            },
            onEachFeature: function(feature, layer) {
                const props = feature.properties;
                const numero = props.numero;

                if (numero) {
                    couchesSalles[numero] = layer;
                }

                layer.on('click', function(e) {
                    afficherInfosSalle(props);
                    map.fitBounds(e.target.getBounds());
                });
            }
        }).addTo(map);
    })
    .catch(error => console.error("Erreur de chargement :", error));

// Fonction pour afficher les infos dans le panneau
function afficherInfosSalle(props) {
    const numero = props.numero || "Inconnu";
    const libelle = props.libelle || "";
    const surface = props.surface_plan_m2 || props.surface_polygone_m2 || "?";

    document.getElementById('info-content').innerHTML = `
        <h3>Salle ${numero}</h3>
        <p><strong>Type :</strong> ${libelle}</p>
        <p><strong>Surface :</strong> ${surface} m²</p>
        <p><strong>Niveau :</strong> ${props.niveau}</p>
    `;
}

// 3. Logique de recherche
function executerRecherche() {
    const saisie = document.getElementById('search-input').value.trim();
    
    if (couchesSalles[saisie]) {
        const salleLayer = couchesSalles[saisie];
        map.fitBounds(salleLayer.getBounds());
        afficherInfosSalle(salleLayer.feature.properties);
        
        salleLayer.setStyle({ fillColor: '#ff7800', fillOpacity: 0.7 });
        setTimeout(() => {
            salleLayer.setStyle({ fillColor: '#0078A8', fillOpacity: 0.3 });
        }, 2000);
    } else {
        alert("Salle introuvable ! Essayez '104' ou '105'.");
    }
}

document.getElementById('search-button').addEventListener('click', executerRecherche);
document.getElementById('search-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') executerRecherche();
});