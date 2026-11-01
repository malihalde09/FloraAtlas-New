import sqlite3
from database import get_connection, add_plant

# Sample plant data
sample_plants = [
    {
        'plant_id': 'P001',
        'plant_name': 'Neem Tree',
        'scientific_name': 'Azadirachta indica',
        'kingdom': 'Plantae',
        'family': 'Meliaceae',
        'species': 'A. indica',
        'category': 'Tree',
        'description': 'A fast-growing tree known for its medicinal properties.',
        'medicinal_uses': 'Used in traditional medicine for skin conditions and infections.',
        'environmental_benefits': 'Improves air quality and provides shade.',
        'image_path': '',
        'qr_code_id': 'QR001',
        'latitude': 28.6139,
        'longitude': 77.2090
    },
    {
        'plant_id': 'P002',
        'plant_name': 'Tulsi (Holy Basil)',
        'scientific_name': 'Ocimum sanctum',
        'kingdom': 'Plantae',
        'family': 'Lamiaceae',
        'species': 'O. sanctum',
        'category': 'Herb',
        'description': 'A sacred plant in Hinduism, known for its medicinal value.',
        'medicinal_uses': 'Used for respiratory issues and stress relief.',
        'environmental_benefits': 'Attracts beneficial insects.',
        'image_path': '',
        'qr_code_id': 'QR002',
        'latitude': 28.6140,
        'longitude': 77.2100
    },
    {
        'plant_id': 'P003',
        'plant_name': 'Banyan Tree',
        'scientific_name': 'Ficus benghalensis',
        'kingdom': 'Plantae',
        'family': 'Moraceae',
        'species': 'F. benghalensis',
        'category': 'Tree',
        'description': 'A large tree with aerial prop roots, considered sacred in India.',
        'medicinal_uses': 'Used in traditional medicine for diabetes and inflammation.',
        'environmental_benefits': 'Provides large canopy for shade and habitat.',
        'image_path': '',
        'qr_code_id': 'QR003',
        'latitude': 28.6120,
        'longitude': 77.2080
    },
    {
        'plant_id': 'P004',
        'plant_name': 'Rose',
        'scientific_name': 'Rosa indica',
        'kingdom': 'Plantae',
        'family': 'Rosaceae',
        'species': 'R. indica',
        'category': 'Flower',
        'description': 'A beautiful flowering plant known for its fragrance.',
        'medicinal_uses': 'Used in aromatherapy and skin care.',
        'environmental_benefits': 'Attracts pollinators like bees and butterflies.',
        'image_path': '',
        'qr_code_id': 'QR004',
        'latitude': 28.6150,
        'longitude': 77.2110
    }
]

def add_sample_plants():
    """Add sample plants to the database."""
    print("Adding sample plants...")
    
    for plant in sample_plants:
        success, message = add_plant(plant)
        if success:
            print(f"✅ Added: {plant['plant_name']}")
        else:
            print(f"❌ Failed to add {plant['plant_name']}: {message}")
    
    print("\nSample plants added successfully!")

if __name__ == "__main__":
    add_sample_plants()
