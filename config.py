"""
Configuration and constants for the Medicinal Plant Identification project
"""
import os

# Dataset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'dataset')
TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15

# Image configuration
IMG_HEIGHT = 224
IMG_WIDTH = 224
IMG_CHANNELS = 3
BATCH_SIZE = 32

# Model configuration
EPOCHS = 50
LEARNING_RATE = 0.001
PATIENCE = 10  # For early stopping

# Plant classes - auto-detected from the `dataset/` folder (fallback to defaults)
_default_plant_classes = {
    'Aloevera': {
        'scientific_name': 'Aloe vera',
        'common_names': ['Aloe', 'Aloe barbadensis'],
        'medicinal_uses': ['Promotes healing of burns, cuts, and wounds',
        'Soothes skin irritation, sunburn, and dryness',
        'Supports digestive health and reduces acidity',
        'Acts as a natural anti-inflammatory agent'],
        'overview': 'A succulent plant used topically for burns and as a traditional digestive aid.',
        'preparation': {
            'juice': 'Apply fresh inner gel topically or mix with water for sprays.',
            'powder': 'Dry inner leaf gel and grind to powder for poultices.',
            'decoction': 'Not commonly used; dilute if prepared for topical washes.'
        },
        'dosage': 'Topical: apply to affected area as needed. Internal use should be limited.',
        'safety': 'Avoid prolonged internal use during pregnancy; may cause allergic reactions in sensitive people.',
        'best_time': 'Use topically as needed; internal preparations taken with meals if used.',
        'did_you_know': 'Aloe has been used medicinally since ancient Egypt.',
        'image': 'aloevera.jpg'
    },
    'Amla': {
        'scientific_name': 'Phyllanthus emblica',
        'common_names': ['Indian Gooseberry'],
        'medicinal_uses': ['Boosts immunity due to high Vitamin C content',
        'Acts as a powerful antioxidant to reduce oxidative stress',
        'Improves digestion and metabolism',
        'Supports hair growth and enhances skin health'],
        'overview': 'Amla is a sour fruit prized in Ayurveda for its antioxidant and immune-supporting properties.',
        'preparation': {
            'juice': 'Fresh juice mixed with honey or water.',
            'powder': 'Dried and powdered for use in tonics and churna mixes.',
            'decoction': 'Boil pieces to make a weak decoction for drinking.'
        },
        'dosage': 'Small servings (1–2 teaspoons of powder) or 10–30 ml juice per day as a supplement.',
        'safety': 'Generally safe; large doses may upset digestion in sensitive individuals.',
        'best_time': 'Morning on an empty stomach or with meals depending on tolerance.',
        'did_you_know': 'Amla is one of the main ingredients of the traditional triphala formulation.',
        'image': 'amla.jpg'
    },
    'Amruthaballi': {
        'scientific_name': 'Tinospora cordifolia',
        'common_names': ['Giloy', 'Guduchi'],
        'medicinal_uses': ['Enhances immunity and fights infections',
        'Helps reduce fever and chronic illness symptoms',
        'Supports liver detoxification and function',
        'Acts as an anti-inflammatory and antioxidant'],
        'overview': 'A climbing shrub used in Ayurveda as an immunomodulator and fever reducer.',
        'preparation': {
            'juice': 'Stem extract or juice taken in small amounts.',
            'powder': 'Dried stem powder used in herbal formulations.',
            'decoction': 'Decoction of stem pieces for daily use.'
        },
        'dosage': 'Follow traditional dosing (small daily doses); consult practitioner for long-term use.',
        'safety': 'Generally well-tolerated; consult a practitioner if pregnant or on medication.',
        'best_time': 'Typically consumed in the morning or as advised in formulations.',
        'did_you_know': 'Known as “Guduchi” in Ayurveda and regarded as a rejuvenating herb.',
        'image': 'amruthaballi.jpg'
    },
    'Badipala': {
        'scientific_name': 'Ficus benghalensis (approx.)',
        'common_names': ['Badipala (local)'],
        'medicinal_uses': ['Traditionally used for digestive issues and stomach discomfort',
        'Helps in treating minor infections and inflammation',
        'Used in folk medicine for wound healing',
        'Supports overall gut health'],
        'overview': 'A traditionally used plant with folk remedies for digestion and minor ailments.',
        'preparation': {
            'juice': 'Fresh leaf juice used locally for digestive complaints.',
            'powder': 'Dry leaves ground into a topical or ingestible powder in folk recipes.',
            'decoction': 'Boiled for a light decoction for external or internal use.'
        },
        'dosage': 'Use small traditional doses; follow local guidance.',
        'safety': 'Limited modern data; use cautiously and avoid if allergic.',
        'best_time': 'Take with food when used for digestion.',
        'did_you_know': 'Badipala is more frequently referenced in regional traditional medicine.',
        'image': 'badipala.jpg'
    },
    'Balloon_Vine': {
        'scientific_name': 'Cardiospermum halicacabum',
        'common_names': ['Balloon Vine', 'Love in a Puff'],
        'medicinal_uses': ['Reduces joint pain and inflammation (arthritis relief)',
        'Supports respiratory health and reduces cough',
        'Used for skin diseases and itching',
        'Acts as a natural anti-inflammatory agent'],
        'overview': 'A climbing plant used for joint inflammation and respiratory complaints in folk medicine.',
        'preparation': {
            'juice': 'Leaf juice applied topically for inflammation.',
            'powder': 'Dried plant powdered for poultices.',
            'decoction': 'Decoction used as a mild topical or internal remedy.'
        },
        'dosage': 'Topical application as needed; internal use per traditional recipes.',
        'safety': 'Avoid in pregnancy unless guided by a practitioner.',
        'best_time': 'Topical use as needed; internal formulations per practitioner guidance.',
        'did_you_know': 'Called “love-in-a-puff” for its distinctive inflated fruit pods.',
        'image': 'balloon_vine.jpg'
    },
    'Bhrami': {
        'scientific_name': 'Bacopa monnieri',
        'common_names': ['Brahmi', 'Waterhyssop'],
        'medicinal_uses': ['Enhances memory and cognitive function',
        'Reduces anxiety, stress, and mental fatigue',
        'Supports brain health and concentration',
        'Acts as a natural nervine tonic'],
        'overview': 'A wetland herb used traditionally to support cognitive function and memory.',
        'preparation': {
            'juice': 'Fresh leaf extract taken in small quantities.',
            'powder': 'Dried herb powdered into capsules or mixed with milk.',
            'decoction': 'Mild decoction used in traditional tonics.'
        },
        'dosage': 'Typical herbal doses; follow product instructions or practitioner advice.',
        'safety': 'May interact with thyroid medications; consult a healthcare provider.',
        'best_time': 'Taken with morning meals or as recommended.',
        'did_you_know': 'Brahmi is a staple herb in many Ayurvedic formulations for brain health.',
        'image': 'bhrami.jpg'
    },
    'camphor': {
        'scientific_name': 'Cinnamomum camphora',
        'common_names': ['Camphor'],
        'medicinal_uses': ['Provides relief from cough and nasal congestion',
        'Acts as a topical pain reliever for muscle aches',
        'Has antiseptic and antimicrobial properties',
        'Used in steam inhalation for respiratory issues'],
        'overview': 'Camphor is a strong-smelling topical agent used primarily for topical relief and decongestion.',
        'preparation': {
            'juice': 'Not applicable; camphor used as oil or ointment.',
            'powder': 'Used in very small amounts in traditional topical formulations.',
            'decoction': 'Not commonly used internally; primarily topical or inhalational.'
        },
        'dosage': 'Topical preparations used sparingly; inhalation via steam for congestion.',
        'safety': 'Toxic if ingested in large amounts; avoid use in infants and small children.',
        'best_time': 'Topical use when symptomatic; inhalation as needed.',
        'did_you_know': 'Camphor has been used in religious ceremonies as well as medicine.',
        'image': 'camphor.jpg'
    },
    'Catharanthus': {
        'scientific_name': 'Catharanthus roseus',
        'common_names': ['Periwinkle', 'Vinca'],
        'medicinal_uses': ['Contains compounds used in cancer treatment (alkaloids)',
        'Traditionally used for managing diabetes',
        'Supports blood circulation and healing',
        'Used in controlled medicinal formulations'],
        'overview': 'Periwinkle contains alkaloids that have been used in modern medicine; traditional uses vary.',
        'preparation': {
            'juice': 'Not commonly used as juice; extracts prepared in controlled settings.',
            'powder': 'Used in traditional remedies; active alkaloids require careful handling.',
            'decoction': 'Used in folk decoctions in small amounts.'
        },
        'dosage': 'Not recommended for self-medication; medical supervision required for alkaloid use.',
        'safety': 'Contains powerful alkaloids; can be toxic and interacts with many drugs.',
        'best_time': 'Medical formulations administered as per protocol.',
        'did_you_know': 'Derivatives of periwinkle are used to make chemotherapy agents.',
        'image': 'catharanthus.jpg'
    },
    'Coffee': {
        'scientific_name': 'Coffea spp.',
        'common_names': ['Coffee'],
        'medicinal_uses': ['Acts as a natural stimulant to increase alertness',
        'Improves mental focus and cognitive performance',
        'Contains antioxidants that protect cells',
        'May support metabolism and fat burning'],
        'overview': 'Coffee beans are a widely used stimulant and source of antioxidants.',
        'preparation': {
            'juice': 'Not applicable; brewed beverage is the common preparation.',
            'powder': 'Roasted and powdered beans used for brewing.',
            'decoction': 'Brewed decoction (coffee) consumed as a beverage.'
        },
        'dosage': 'Moderate consumption (1–3 cups) depending on tolerance.',
        'safety': 'Excess caffeine can cause nervousness, sleep disturbances, and palpitations.',
        'best_time': 'Morning or early afternoon to avoid sleep disruption.',
        'did_you_know': 'Coffee is one of the most traded agricultural commodities globally.',
        'image': 'coffee.jpg'
    },
    'Curry': {
        'scientific_name': 'Murraya koenigii',
        'common_names': ['Curry leaf'],
        'medicinal_uses': ['Improves digestion and reduces stomach discomfort',
        'Helps control blood sugar levels',
        'Supports hair growth and reduces hair fall',
        'Acts as an antioxidant and antimicrobial agent'],
        'overview': 'Curry leaves are used in cooking and traditional remedies for digestion and metabolic health.',
        'preparation': {
            'juice': 'Fresh leaf extract used in small amounts.',
            'powder': 'Dried leaves powdered for culinary and medicinal use.',
            'decoction': 'Decoction of leaves used as a digestive aid.'
        },
        'dosage': 'Used commonly in food; therapeutic doses vary by preparation.',
        'safety': 'Generally safe when used in food amounts.',
        'best_time': 'Included with meals to support digestion.',
        'did_you_know': 'Curry leaves are rich in antioxidants and micronutrients.',
        'image': 'curry.jpg'
    },
    'Doddpathre': {
        'scientific_name': 'Acalypha indica (approx.)',
        'common_names': ['Doddpathre (local)'],
        'medicinal_uses': ['Used for treating skin infections and wounds',
        'Acts as a natural antiseptic',
        'Helps reduce inflammation and irritation',
        'Used in traditional remedies for minor ailments'],
        'overview': 'A plant used in traditional topical skin remedies and minor wound care.',
        'preparation': {
            'juice': 'Leaf juice applied to skin for antiseptic effects.',
            'powder': 'Dried leaves powdered for poultices.',
            'decoction': 'Weak decoction used for external washes.'
        },
        'dosage': 'Topical application as needed.',
        'safety': 'External use preferred; avoid ingestion without guidance.',
        'best_time': 'Apply externally when treating skin issues.',
        'did_you_know': 'Often used in folk medicine for minor skin infections.',
        'image': 'doddpathre.jpg'
    },
    'Drumstick': {
        'scientific_name': 'Moringa oleifera',
        'common_names': ['Moringa', 'Drumstick tree'],
        'medicinal_uses': ['Rich in nutrients and boosts overall health',
        'Acts as an anti-inflammatory agent',
        'Helps regulate blood sugar levels',
        'Supports immunity and energy levels'],
        'overview': 'Moringa is a nutrient-dense tree whose leaves and pods are used for nutrition and traditional medicine.',
        'preparation': {
            'juice': 'Fresh leaf or pod extracts consumed as tonic.',
            'powder': 'Dried leaf powder taken in small spoonfuls.',
            'decoction': 'Leaves boiled to prepare tonics.'
        },
        'dosage': 'Small spoonfuls of powder or portions of cooked leaves; follow product guidance.',
        'safety': 'Generally safe in food amounts; large medicinal doses should be supervised.',
        'best_time': 'With meals or as a morning tonic.',
        'did_you_know': 'Moringa is sometimes called the “miracle tree” for its high nutrient content.',
        'image': 'drumstick.jpg'
    },
    'Eucalyptus': {
        'scientific_name': 'Eucalyptus globulus',
        'common_names': ['Eucalyptus'],
        'medicinal_uses': ['Relieves cough, cold, and nasal congestion',
        'Used in steam inhalation for respiratory relief',
        'Acts as an antiseptic for wounds and infections',
        'Helps reduce muscle pain and inflammation'],
        'overview': 'Eucalyptus leaves are used in vapour and topical remedies for respiratory relief.',
        'preparation': {
            'juice': 'Leaf extracts used in diluted form for inhalation or topical rubs.',
            'powder': 'Not commonly used as powder; essential oils are common.',
            'decoction': 'Steam or decoction used for inhalation therapy.'
        },
        'dosage': 'Use inhalation or topical preparations as directed; avoid ingestion.',
        'safety': 'Oil can be toxic if swallowed; keep away from children.',
        'best_time': 'Inhalation during congestion or at bedtime for relief.',
        'did_you_know': 'Eucalyptus oil is a common ingredient in chest rubs.',
        'image': 'eucalyptus.jpg'
    },
    'Ginger': {
        'scientific_name': 'Zingiber officinale',
        'common_names': ['Ginger'],
        'medicinal_uses': [ 'Relieves nausea and vomiting',
        'Improves digestion and reduces bloating',
        'Acts as a natural anti-inflammatory',
        'Helps relieve cold, cough, and sore throat'],
        'overview': 'Ginger root is widely used to relieve nausea, support digestion, and reduce inflammation.',
        'preparation': {
            'juice': 'Fresh ginger juice in water, teas, or syrups.',
            'powder': 'Dried powdered ginger used in capsules or culinary uses.',
            'decoction': 'Boiled in water to make ginger tea.'
        },
        'dosage': 'Small amounts (1–2 g) for nausea; follow product guidance.',
        'safety': 'May interact with blood thinners; consult a doctor if on medication.',
        'best_time': 'Before or with meals for digestion; as needed for nausea.',
        'did_you_know': 'Ginger has been used for thousands of years in traditional medicine.',
        'image': 'ginger.jpg'
    },
    'Henna': {
        'scientific_name': 'Lawsonia inermis',
        'common_names': ['Henna'],
        'medicinal_uses': ['Conditions and cools the scalp and skin',
        'Acts as an antifungal and antibacterial agent',
        'Helps treat dandruff and scalp irritation',
        'Used for wound healing and skin protection'],
        'overview': 'Henna leaves are traditionally used for hair and skin conditioning and as a dye.',
        'preparation': {
            'juice': 'Leaf paste or extract applied topically.',
            'powder': 'Dried and powdered leaves mixed into pastes.',
            'decoction': 'Leaf decoction used for topical rinses.'
        },
        'dosage': 'Topical use only in recommended amounts.',
        'safety': 'Avoid black henna and synthetic additives; do patch tests for allergies.',
        'best_time': 'Apply topically when treating hair or skin conditions.',
        'did_you_know': 'Henna has been used as a cosmetic and antiseptic in many cultures.',
        'image': 'henna.jpg'
    },
    'Mint': {
        'scientific_name': 'Mentha spp.',
        'common_names': ['Mint', 'Peppermint'],
        'medicinal_uses': ['Digestive aid', 'Relieves indigestion and stomach discomfort',
        'Provides cooling effect and reduces body heat',
        'Helps clear nasal congestion',
        'Freshens breath and reduces nausea'],
        'overview': 'Mint leaves are used for digestive comfort, cooling, and mild respiratory relief.',
        'preparation': {
            'juice': 'Fresh leaf infusion or juice in teas.',
            'powder': 'Dried leaves used in teas and formulations.',
            'decoction': 'Mint tea made by steeping leaves in hot water.'
        },
        'dosage': 'Use as a tea or culinary herb; concentrated products follow label dosing.',
        'safety': 'May worsen reflux in some individuals; avoid concentrated oil internally.',
        'best_time': 'After meals for digestion or as a soothing tea.',
        'did_you_know': 'Mint has one of the strongest aromas among culinary herbs.',
        'image': 'mint.jpg'
    },
    'Neem': {
        'scientific_name': 'Azadirachta indica',
        'common_names': ['Neem'],
        'medicinal_uses': ['Treats skin infections, acne, and wounds',
        'Acts as a strong antibacterial and antifungal agent',
        'Supports blood purification',
        'Boosts immunity and detoxification'],
        'overview': 'Neem is used for skin conditions, as an antibacterial agent, and in traditional cleanses.',
        'preparation': {
            'juice': 'Leaf extract used topically or in small internal doses in traditional recipes.',
            'powder': 'Dried neem leaf powder used in topical pastes.',
            'decoction': 'Decoction used externally for washes and internally in small amounts.'
        },
        'dosage': 'Topical as needed; internal medicinal doses should be supervised.',
        'safety': 'Avoid internal use during pregnancy and in young children.',
        'best_time': 'Topical application as required; internal use per practitioner guidance.',
        'did_you_know': 'Neem is often called the “village pharmacy” in South Asia.',
        'image': 'neem.jpg'
    },
    'Tulsi': {
        'scientific_name': 'Ocimum sanctum',
        'common_names': ['Holy Basil', 'Tulsi'],
        'medicinal_uses': ['Relieves cough, cold, and respiratory problems',
        'Reduces stress and improves mental health',
        'Boosts immunity and fights infections',
        'Acts as an anti-inflammatory and antioxidant'],
        'overview': 'Tulsi is a revered herb in Ayurveda used for respiratory support and stress relief.',
        'preparation': {
            'juice': 'Fresh leaf extract or tea prepared from leaves.',
            'powder': 'Dried leaf powder used in tonics.',
            'decoction': 'Decoction (tulsi tea) consumed for respiratory comfort.'
        },
        'dosage': 'Tea or extracts daily; follow product or practitioner guidance.',
        'safety': 'Generally safe; consult a healthcare provider if pregnant or on medication.',
        'best_time': 'Morning or during cold/flu symptoms for symptomatic relief.',
        'did_you_know': 'Tulsi is considered sacred in many Indian households.',
        'image': 'tulsi.jpg'
    },
    'Turmeric': {
        'scientific_name': 'Curcuma longa',
        'common_names': ['Turmeric'],
        'medicinal_uses': ['Reduces inflammation and joint pain',
        'Acts as a powerful antioxidant',
        'Supports wound healing and skin health',
        'Boosts immunity and improves digestion'],
        'overview': 'Turmeric root contains curcumin and is widely used for inflammation and general wellness.',
        'preparation': {
            'juice': 'Fresh root juice mixed with water or milk.',
            'powder': 'Dried root powdered and used in cooking or supplements.',
            'decoction': 'Boiled in milk or water as traditional remedies.'
        },
        'dosage': 'Culinary use is safe; concentrated extracts follow label dosing.',
        'safety': 'May interact with blood thinners; consult doctor for medicinal dosing.',
        'best_time': 'With meals to improve absorption; golden milk at night is common.',
        'did_you_know': 'Turmeric has been used in traditional medicine systems for millennia.',
        'image': 'turmeric.jpg'
    }
}

PLANT_CLASSES = {}
if os.path.isdir(DATASET_PATH):
    for plant in sorted([d for d in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, d))]):
        # Get default data for this plant
        default_data = _default_plant_classes.get(plant, {})

        # Merge default data with dynamic data
        PLANT_CLASSES[plant] = {
            'scientific_name': default_data.get('scientific_name', ''),
            'common_names': default_data.get('common_names', []),
            'medicinal_uses': default_data.get('medicinal_uses', ['Information not available yet']),
            'overview': default_data.get('overview', 'Information not available.'),
            'preparation': default_data.get('preparation', {
                'juice': 'Information not available.',
                'powder': 'Information not available.',
                'decoction': 'Information not available.'
            }),
            'dosage': default_data.get('dosage', 'Information not available.'),
            'safety': default_data.get('safety', 'Information not available.'),
            'best_time': default_data.get('best_time', 'Information not available.'),
            'did_you_know': default_data.get('did_you_know', 'Interesting facts will appear here.'),
            'image': default_data.get('image', f"{plant.lower()}.jpg")
        }
else:
    PLANT_CLASSES = _default_plant_classes

# Model confidence threshold
CONFIDENCE_THRESHOLD = 0.7

# Upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
