import sqlite3
from database import get_connection, add_plant

# Sample plants data
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
        'medicinal_uses': 'Used in traditional medicine for skin conditions.',
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
        'description': 'A large tree with aerial prop roots, considered sacred.',
        'medicinal_uses': 'Used in traditional medicine for diabetes.',
        'environmental_benefits': 'Provides large canopy for shade.',
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
        'environmental_benefits': 'Attracts pollinators like bees.',
        'image_path': '',
        'qr_code_id': 'QR004',
        'latitude': 28.6150,
        'longitude': 77.2110
    },
    {
        'plant_id': 'P005',
        'plant_name': 'Mango Tree',
        'scientific_name': 'Mangifera indica',
        'kingdom': 'Plantae',
        'family': 'Anacardiaceae',
        'species': 'M. indica',
        'category': 'Tree',
        'description': 'A tropical tree known for its sweet fruit.',
        'medicinal_uses': 'Rich in vitamins, used for digestive health.',
        'environmental_benefits': 'Provides shade and improves air quality.',
        'image_path': '',
        'qr_code_id': 'QR005',
        'latitude': 28.6130,
        'longitude': 77.2085
    },
    {
        'plant_id': 'P006',
        'plant_name': 'Lavender',
        'scientific_name': 'Lavandula angustifolia',
        'kingdom': 'Plantae',
        'family': 'Lamiaceae',
        'species': 'L. angustifolia',
        'category': 'Herb',
        'description': 'A fragrant plant known for its calming properties.',
        'medicinal_uses': 'Used in aromatherapy and for relaxation.',
        'environmental_benefits': 'Attracts pollinators and repels pests.',
        'image_path': '',
        'qr_code_id': 'QR006',
        'latitude': 28.6145,
        'longitude': 77.2095
    },
    {
        'plant_id': 'P007',
        'plant_name': 'Sunflower',
        'scientific_name': 'Helianthus annuus',
        'kingdom': 'Plantae',
        'family': 'Asteraceae',
        'species': 'H. annuus',
        'category': 'Flower',
        'description': 'A tall plant with large yellow flower heads.',
        'medicinal_uses': 'Seeds are rich in healthy fats.',
        'environmental_benefits': 'Attracts bees and butterflies.',
        'image_path': '',
        'qr_code_id': 'QR007',
        'latitude': 28.6160,
        'longitude': 77.2120
    },
    {
        'plant_id': 'P008',
        'plant_name': 'Aloe Vera',
        'scientific_name': 'Aloe barbadensis',
        'kingdom': 'Plantae',
        'family': 'Asphodelaceae',
        'species': 'A. barbadensis',
        'category': 'Succulent',
        'description': 'A succulent plant known for its healing gel.',
        'medicinal_uses': 'Used for skin burns, wounds, and digestion.',
        'environmental_benefits': 'Drought-resistant and easy to grow.',
        'image_path': '',
        'qr_code_id': 'QR008',
        'latitude': 28.6125,
        'longitude': 77.2075
    }
]

def reset_and_add_plants():
    """Clear all plants and add sample plants."""
    print("🔄 Clearing existing plants...")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM plant')
        conn.commit()
        conn.close()
        print("✅ All plants cleared!")
    except Exception as e:
        print(f"❌ Error clearing plants: {e}")
    
    print("\n📝 Adding sample plants...")
    success_count = 0
    
    for plant in sample_plants:
        success, message = add_plant(plant)
        if success:
            print(f"   ✅ Added: {plant['plant_name']}")
            success_count += 1
        else:
            print(f"   ❌ Failed to add {plant['plant_name']}: {message}")
    
    print(f"\n✅ {success_count} sample plants added successfully!")

if __name__ == "__main__":
    reset_and_add_plants()