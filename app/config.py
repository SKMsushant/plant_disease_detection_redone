from pathlib import Path
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DB_HOSTNAME:str
    DB_USERNAME:str
    DB_PASSWORD:str
    DB_PORT:str
    DB_NAME:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    TEMP_TOKEN_EXPIRE_MINUTES:int
    UPLOAD_DIR: str = "uploads"

    model_config=SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings=Settings()


#paths

BASE_DIR=Path(__file__).resolve().parent.parent
MODEL_DIR=BASE_DIR/"models"
WEIGHTS_PATH=MODEL_DIR/"final_plant_disease_detection_model.weights.h5"
HPS_PATH=MODEL_DIR/"best_hps.json"

IMG_SIZE=224

CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Background_without_leaves', 'Blueberry___healthy', 'Cherry___Powdery_mildew', 'Cherry___healthy',
    'Corn___Cercospora_leaf_spot Gray_leaf_spot', 'Corn___Common_rust', 'Corn___Northern_Leaf_Blight', 'Corn___healthy',
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

REMEDIES = {
    'Apple___Apple_scab': {
        "disease": "Apple Scab (Fungal)",
        "actions": [
            "Rake and destroy fallen leaves in autumn to reduce spore load.",
            "Apply sulfur or copper-based fungicides in early spring during green tip stage.",
            "Plant resistant apple cultivars (e.g., Enterprise, Liberty, Freedom)."
        ]
    },
    'Apple___Black_rot': {
        "disease": "Black Rot (Fungal)",
        "actions": [
            "Prune dead or diseased branches during winter dormancy.",
            "Remove mummified fruit remaining on the trees.",
            "Apply protective fungicides starting from silver tip stage to prevent spore entry."
        ]
    },
    'Apple___Cedar_apple_rust': {
        "disease": "Cedar Apple Rust (Fungal)",
        "actions": [
            "Remove nearby galls on ornamental junipers/red cedars if possible.",
            "Apply immunizing fungicides (e.g., Myclobutanil) when flower buds begin to show color.",
            "Plant rust-resistant apple varieties."
        ]
    },
    'Apple___healthy': {
        "disease": "None (Healthy Apple)",
        "actions": [
            "Maintain regular pruning to improve sunlight penetration and air circulation.",
            "Ensure proper irrigation and balanced nitrogen-phosphorus-potassium (NPK) fertilization.",
            "Monitor regularly for early signs of foliar diseases or pests."
        ]
    },
    'Background_without_leaves': {
        "disease": "None (Non-Plant Background)",
        "actions": [
            "Ensure the camera focuses clearly on foliage or plant tissue.",
            "Capture images under good lighting conditions with minimal clutter.",
            "Re-scan a clear, single leaf centered in the camera frame."
        ]
    },
    'Blueberry___healthy': {
        "disease": "None (Healthy Blueberry)",
        "actions": [
            "Maintain acidic soil pH (between 4.5 and 5.5) using elemental sulfur if necessary.",
            "Apply pine bark or wood chip mulch to preserve moisture and suppress weeds.",
            "Provide regular, deep watering to prevent root desiccation."
        ]
    },
    'Cherry___Powdery_mildew': {
        "disease": "Powdery Mildew (Fungal)",
        "actions": [
            "Apply sulfur-based or potassium bicarbonate sprays at early leaf development.",
            "Prune dense inner branches to maximize sunlight and airflow through the canopy.",
            "Avoid overhead irrigation to keep leaves dry."
        ]
    },
    'Cherry___healthy': {
        "disease": "None (Healthy Cherry)",
        "actions": [
            "Maintain routine winter dormant oil sprays to manage overwintering pests.",
            "Prune annually to maintain an open canopy structure.",
            "Ensure well-draining soil to prevent root rot."
        ]
    },
    'Corn___Cercospora_leaf_spot Gray_leaf_spot': {
        "disease": "Gray Leaf Spot (Fungal)",
        "actions": [
            "Rotate crops annually with non-host species like soybeans.",
            "Till under infected crop residue to accelerate natural decomposition.",
            "Apply strobilurin or triazole fungicides at tasseling stage if disease pressure is high."
        ]
    },
    'Corn___Common_rust': {
        "disease": "Common Rust (Fungal)",
        "actions": [
            "Plant rust-resistant corn hybrids.",
            "Apply foliar fungicides (e.g., mancozeb or azoxystrobin) if pustules appear prior to tasseling.",
            "Plant early in the season to reduce exposure to peak airborne fungal spores."
        ]
    },
    'Corn___Northern_Leaf_Blight': {
        "disease": "Northern Leaf Blight (Fungal)",
        "actions": [
            "Plant resistant hybrids containing specific Ht resistance genes.",
            "Rotate crops and avoid continuous corn planting in the same field.",
            "Apply targeted fungicides when lesions first appear on lower canopy leaves."
        ]
    },
    'Corn___healthy': {
        "disease": "None (Healthy Corn)",
        "actions": [
            "Ensure consistent moisture supply, especially during pollination and silking stages.",
            "Apply nitrogen side-dressings in accordance with soil test results.",
            "Keep fields free of weeds to minimize resource competition."
        ]
    },
    'Grape___Black_rot': {
        "disease": "Black Rot (Fungal)",
        "actions": [
            "Prune infected canes and remove mummified berries from vines and ground.",
            "Apply fungicides (e.g., captan, mancozeb, or myclobutanil) from early bud break through flowering.",
            "Improve trellis airflow through canopy management and shoot thinning."
        ]
    },
    'Grape___Esca_(Black_Measles)': {
        "disease": "Esca / Black Measles (Fungal Complex)",
        "actions": [
            "Prune vines late in winter dormancy and treat pruning wounds with wound sealants.",
            "Excise and remove infected cordon branches showing internal vascular decay.",
            "Avoid excessive vine stress and maintain balanced irrigation."
        ]
    },
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': {
        "disease": "Leaf Blight / Isariopsis Leaf Spot (Fungal)",
        "actions": [
            "Spray copper-based fungicides or Bordeaux mixture post-harvest and pre-bloom.",
            "Collect and destroy fallen leaf debris after defoliation.",
            "Thin out dense foliage around grape clusters to accelerate drying after rain."
        ]
    },
    'Grape___healthy': {
        "disease": "None (Healthy Grape)",
        "actions": [
            "Maintain regular shoot positioning, pruning, and canopy training on trellises.",
            "Ensure good soil drainage and balanced potassium fertilization.",
            "Conduct routine seasonal scouting for leafhoppers and powdery mildew."
        ]
    },
    'Orange___Haunglongbing_(Citrus_greening)': {
        "disease": "Huanglongbing / Citrus Greening (Bacterial)",
        "actions": [
            "Manage and control Asian citrus psyllid vector populations using targeted insecticides.",
            "Promptly remove and destroy confirmed infected trees to protect surrounding groves.",
            "Apply foliar micronutrient sprays (zinc, manganese, iron) to support tree vigor."
        ]
    },
    'Peach___Bacterial_spot': {
        "disease": "Bacterial Spot (Bacterial)",
        "actions": [
            "Apply preventative copper bactericides at late dormancy and petal fall.",
            "Avoid high nitrogen fertilization that stimulates excessively susceptible succulent growth.",
            "Select and plant resistant peach varieties (e.g., Candor, Clayton)."
        ]
    },
    'Peach___healthy': {
        "disease": "None (Healthy Peach)",
        "actions": [
            "Prune to an open-center (vase) shape to maximize sunlight penetration.",
            "Apply dormant copper sprays during winter to prevent peach leaf curl.",
            "Thin developing fruit to avoid branch breakage and optimize fruit size."
        ]
    },
    'Pepper,_bell___Bacterial_spot': {
        "disease": "Bacterial Spot (Bacterial)",
        "actions": [
            "Treat seeds with hot water or buy certified disease-free pepper seeds.",
            "Spray copper fungicides combined with mancozeb to slow bacterial spread.",
            "Avoid overhead sprinkler irrigation to keep leaves dry."
        ]
    },
    'Pepper,_bell___healthy': {
        "disease": "None (Healthy Bell Pepper)",
        "actions": [
            "Maintain consistent soil moisture to prevent blossom end rot.",
            "Stake or cage plants to support heavy fruit load and keep leaves off soil.",
            "Mulch around the base of plants to regulate soil temperature."
        ]
    },
    'Potato___Early_blight': {
        "disease": "Early Blight (Fungal)",
        "actions": [
            "Apply protectant fungicides (chlorothalonil or copper) when lower leaves exhibit concentric ring spots.",
            "Maintain balanced soil nutrition, especially adequate nitrogen and potassium.",
            "Avoid overhead irrigation and practice a 2- to 3-year crop rotation."
        ]
    },
    'Potato___Late_blight': {
        "disease": "Late Blight (Oomycete)",
        "actions": [
            "Destroy infected potato haulms and vines immediately upon detection.",
            "Apply systemic fungicides (e.g., metalaxyl or cymoxanil) before canopy closure.",
            "Hill potatoes well to ensure tubers are covered with sufficient soil to prevent spore wash."
        ]
    },
    'Potato___healthy': {
        "disease": "None (Healthy Potato)",
        "actions": [
            "Hill soil around plant stems as shoots grow to promote tuber growth and prevent greening.",
            "Ensure regular irrigation during flowering and tuber bulking stages.",
            "Rotate potato beds with non-solanaceous crops each season."
        ]
    },
    'Raspberry___healthy': {
        "disease": "None (Healthy Raspberry)",
        "actions": [
            "Prune out spent floricanes immediately after harvesting berries.",
            "Support cane growth on trellises to maintain good aeration.",
            "Mulch with organic material to keep the root zone cool and moist."
        ]
    },
    'Soybean___healthy': {
        "disease": "None (Healthy Soybean)",
        "actions": [
            "Inoculate seeds with Bradyrhizobium japonicum before planting for optimal nitrogen fixation.",
            "Scout regularly for aphid, stink bug, and pod borer infestations.",
            "Practice annual crop rotation with corn or small grains."
        ]
    },
    'Squash___Powdery_mildew': {
        "disease": "Powdery Mildew (Fungal)",
        "actions": [
            "Apply neem oil, horticultural oils, or potassium bicarbonate at the first sign of white powder.",
            "Space plants sufficiently to optimize air movement around broad leaves.",
            "Water early in the morning at ground level using drip or soaker hoses."
        ]
    },
    'Strawberry___Leaf_scorch': {
        "disease": "Leaf Scorch (Fungal)",
        "actions": [
            "Remove and destroy severely spotted and scorched leaves after harvest.",
            "Apply copper- or captan-based fungicides during early spring emergence.",
            "Establish strawberry plants in well-drained soils in full sunlight."
        ]
    },
    'Strawberry___healthy': {
        "disease": "None (Healthy Strawberry)",
        "actions": [
            "Mulch beds with clean straw to protect berries from direct soil contact.",
            "Renovate beds by mowing and fertilizing after the main harvest season.",
            "Keep plants evenly watered, avoiding excess pooling around crowns."
        ]
    },
    'Tomato___Bacterial_spot': {
        "disease": "Bacterial Spot (Bacterial)",
        "actions": [
            "Apply fixed copper sprays combined with mancozeb to reduce bacterial spread.",
            "Avoid working in tomato beds while foliage is wet from rain or dew.",
            "Remove and dispose of diseased lower leaves to slow upward progression."
        ]
    },
    'Tomato___Early_blight': {
        "disease": "Early Blight (Fungal)",
        "actions": [
            "Prune off the lowest 12–18 inches of branches to prevent soil-splash infections.",
            "Apply organic copper or chlorothalonil fungicides every 7–10 days.",
            "Mulch heavily around the plant base to create a physical barrier over the soil."
        ]
    },
    'Tomato___Late_blight': {
        "disease": "Late Blight (Oomycete)",
        "actions": [
            "Remove and bag infected plants completely on dry, sunny days; do not compost.",
            "Apply preventative copper or chlorothalonil sprays during cool, wet conditions.",
            "Plant resistant tomato varieties (e.g., Defiant, Mountain Magic, Iron Lady)."
        ]
    },
    'Tomato___Leaf_Mold': {
        "disease": "Leaf Mold (Fungal)",
        "actions": [
            "Increase greenhouse/hoophouse ventilation and lower relative humidity below 85%.",
            "Prune suckers and lower foliage to improve airflow through dense canopies.",
            "Apply preventive biofungicides (Bacillus subtilis) or copper fungicides."
        ]
    },
    'Tomato___Septoria_leaf_spot': {
        "disease": "Septoria Leaf Spot (Fungal)",
        "actions": [
            "Pick off affected lower leaves showing small circular spots with gray centers.",
            "Water at the base of plants using drip irrigation to keep foliage dry.",
            "Rotate away from Solanaceae family plants for at least two growing seasons."
        ]
    },
    'Tomato___Spider_mites Two-spotted_spider_mite': {
        "disease": "Two-Spotted Spider Mite (Pest Infestation)",
        "actions": [
            "Spray plants with insecticidal soap, horticultural oil, or neem oil, coating leaf undersides.",
            "Introduce beneficial predatory mites (e.g., Phytoseiulus persimilis).",
            "Spray plants with a strong stream of water to knock down webbing and mite colonies."
        ]
    },
    'Tomato___Target_Spot': {
        "disease": "Target Spot (Fungal)",
        "actions": [
            "Apply protective fungicides (e.g., azoxystrobin or chlorothalonil) at disease onset.",
            "Stake and prune plants to improve light penetration and airflow.",
            "Avoid overhead irrigation and clear old crop residue after harvest."
        ]
    },
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
        "disease": "Tomato Yellow Leaf Curl Virus (Viral)",
        "actions": [
            "Control whitefly vectors using yellow sticky cards, insecticidal soap, or imidacloprid.",
            "Use fine mesh insect netting over greenhouse vents or nursery beds.",
            "Rogue out and destroy infected stunting/curling plants immediately to prevent transmission."
        ]
    },
    'Tomato___Tomato_mosaic_virus': {
        "disease": "Tomato Mosaic Virus (Viral)",
        "actions": [
            "Disinfect pruning tools and wash hands thoroughly with soap or milk before handling plants.",
            "Remove and destroy infected plants immediately to prevent sap transmission.",
            "Select and grow mosaic-resistant (ToMV) tomato cultivars."
        ]
    },
    'Tomato___healthy': {
        "disease": "None (Healthy Tomato)",
        "actions": [
            "Provide consistent 1 to 2 inches of water per week to avoid fruit splitting.",
            "Stake or cage vines securely to keep foliage and ripening fruit off the ground.",
            "Side-dress with balanced organic fertilizer or compost once flowering commences."
        ]
    }
}

# Default generic fallback for diseases not fully mapped above
DEFAULT_REMEDY = {
    "disease": "Infectious Spotting / Leaf Disease",
    "actions": ["Prune and destroy infected leaves to limit spore spread.",
                "Avoid overhead irrigation; water the roots directly.",
                "Apply a organic broad-spectrum copper or neem-oil spray in late evening.",
                "Improve spacing between plants to enhance air circulation."]
}




