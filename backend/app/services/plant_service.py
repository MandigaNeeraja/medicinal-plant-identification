import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import PLANT_CLASSES  # noqa: E402


class PlantService:
    @staticmethod
    def list_plants():
        plants = []
        for name, data in PLANT_CLASSES.items():
            plants.append({
                'name': name,
                'scientific_name': data.get('scientific_name', ''),
                'common_names': data.get('common_names', []),
                'overview': data.get('overview', ''),
                'image': data.get('image', ''),
                'medicinal_uses': data.get('medicinal_uses', []),
            })
        return plants

    @staticmethod
    def get_plant(name):
        if name not in PLANT_CLASSES:
            return None

        data = PLANT_CLASSES[name]
        return {
            'name': name,
            'scientific_name': data.get('scientific_name', ''),
            'common_names': data.get('common_names', []),
            'overview': data.get('overview', 'Information not available.'),
            'medicinal_uses': data.get('medicinal_uses', ['Information not available.']),
            'preparation': data.get('preparation', {}),
            'dosage': data.get('dosage', 'Information not available.'),
            'safety': data.get('safety', 'Information not available.'),
            'best_time': data.get('best_time', 'Information not available.'),
            'did_you_know': data.get('did_you_know', 'Interesting facts will appear here.'),
            'image': data.get('image', ''),
        }

    @staticmethod
    def plant_image_path(image_filename):
        if not image_filename:
            return None
        dataset_dir = os.path.join(PROJECT_ROOT, 'dataset')
        for folder in os.listdir(dataset_dir):
            folder_path = os.path.join(dataset_dir, folder)
            if not os.path.isdir(folder_path):
                continue
            candidate = os.path.join(folder_path, image_filename)
            if os.path.exists(candidate):
                return candidate
        return None
