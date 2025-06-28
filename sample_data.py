import pandas as pd
import os

class IPOClassGenerator:
    """Generates sample IPO class data"""
    
    @staticmethod
    def get_sample_classes():
        """Return sample IPO class data"""
        return [
            {"Class": "1", "Description": "Chemicals used in industry, science and photography, as well as in agriculture, horticulture and forestry"},
            {"Class": "2", "Description": "Paints, varnishes, lacquers; preservatives against rust and against deterioration of wood"},
            {"Class": "3", "Description": "Bleaching preparations and other substances for laundry use; cleaning, polishing, scouring and abrasive preparations"},
            {"Class": "4", "Description": "Industrial oils and greases; lubricants; dust absorbing, wetting and binding compositions"},
            {"Class": "5", "Description": "Pharmaceutical and veterinary preparations; sanitary preparations for medical purposes"},
            {"Class": "6", "Description": "Common metals and their alloys; metal building materials; transportable buildings of metal"},
            {"Class": "7", "Description": "Machines and machine tools; motors and engines (except for land vehicles)"},
            {"Class": "8", "Description": "Hand tools and implements (hand-operated); cutlery; side arms; razors"},
            {"Class": "9", "Description": "Scientific, nautical, surveying, photographic, cinematographic, optical, weighing, measuring, signalling, checking (supervision), life-saving and teaching apparatus and instruments"},
            {"Class": "10", "Description": "Surgical, medical, dental and veterinary apparatus and instruments, artificial limbs, eyes and teeth"},
            {"Class": "11", "Description": "Apparatus for lighting, heating, steam generating, cooking, refrigerating, drying, ventilating, water supply and sanitary purposes"},
            {"Class": "12", "Description": "Vehicles; apparatus for locomotion by land, air or water"},
            {"Class": "13", "Description": "Firearms; ammunition and projectiles; explosives; fireworks"},
            {"Class": "14", "Description": "Precious metals and their alloys and goods in precious metals or coated therewith"},
            {"Class": "15", "Description": "Musical instruments"},
            {"Class": "16", "Description": "Paper, cardboard and goods made from these materials; printed matter; bookbinding material"},
            {"Class": "17", "Description": "Rubber, gutta-percha, gum, asbestos, mica and goods made from these materials"},
            {"Class": "18", "Description": "Leather and imitations of leather, and goods made of these materials"},
            {"Class": "19", "Description": "Building materials (non-metallic); non-metallic rigid pipes for building"},
            {"Class": "20", "Description": "Furniture, mirrors, picture frames; goods of wood, cork, reed, cane, wicker, horn, bone, ivory, whalebone, shell, amber, mother-of-pearl, meerschaum and substitutes for all these materials"},
            {"Class": "21", "Description": "Household or kitchen utensils and containers; combs and sponges; brushes"},
            {"Class": "22", "Description": "Ropes, string, nets, tents, awnings, tarpaulins, sails, sacks and bags"},
            {"Class": "23", "Description": "Yarns and threads, for textile use"},
            {"Class": "24", "Description": "Textiles and textile goods, not included in other classes; bed and table covers"},
            {"Class": "25", "Description": "Clothing, footwear, headgear"},
            {"Class": "26", "Description": "Lace and embroidery, ribbons and braid; buttons, hooks and eyes, pins and needles"},
            {"Class": "27", "Description": "Carpets, rugs, mats and matting, linoleum and other materials for covering existing floors"},
            {"Class": "28", "Description": "Games and playthings; gymnastic and sporting articles not included in other classes"},
            {"Class": "29", "Description": "Meat, fish, poultry and game; meat extracts; preserved, frozen, dried and cooked fruits and vegetables"},
            {"Class": "30", "Description": "Coffee, tea, cocoa, sugar, rice, tapioca, sago, artificial coffee"},
            {"Class": "31", "Description": "Agricultural, horticultural and forestry products and grains not included in other classes"},
            {"Class": "32", "Description": "Beers; mineral and aerated waters and other non-alcoholic drinks"},
            {"Class": "33", "Description": "Alcoholic beverages (except beers)"},
            {"Class": "34", "Description": "Tobacco; smokers' articles; matches"},
            {"Class": "35", "Description": "Advertising; business management; business administration; office functions"},
            {"Class": "36", "Description": "Insurance; financial affairs; monetary affairs; real estate affairs"},
            {"Class": "37", "Description": "Building construction; repair; installation services"},
            {"Class": "38", "Description": "Telecommunications"},
            {"Class": "39", "Description": "Transport; packaging and storage of goods; travel arrangement"},
            {"Class": "40", "Description": "Treatment of materials"},
            {"Class": "41", "Description": "Education; providing of training; entertainment; sporting and cultural activities"},
            {"Class": "42", "Description": "Scientific and technological services and research and design relating thereto"},
            {"Class": "43", "Description": "Services for providing food and drink; temporary accommodation"},
            {"Class": "44", "Description": "Medical services; veterinary services; hygienic and beauty care for human beings or animals"},
            {"Class": "45", "Description": "Legal services; security services for the protection of property and individuals"}
        ]
    
    def create_sample_classes(self, file_path):
        """Create and save sample classes data"""
        sample_classes = self.get_sample_classes()
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Create DataFrame and save
            classes_df = pd.DataFrame(sample_classes)
            classes_df.to_csv(file_path, index=False)
            print(f"✓ Sample IPO classes file created at: {file_path}")
            return classes_df
            
        except Exception as e:
            print(f"✗ Error creating classes file: {e}")
            # Return DataFrame even if we can't save it
            return pd.DataFrame(sample_classes)