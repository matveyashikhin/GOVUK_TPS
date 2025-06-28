import pandas as pd
import yfinance as yf
from fuzzywuzzy import fuzz, process
import re
import json
from datetime import datetime, timedelta
import os

class CompanyMappings:
    """Manages company name to ticker mappings"""
    
class CompanyMappings:
    """Manages company name to ticker mappings"""
    
    @staticmethod
    def get_manual_mappings():
        """Return the manual company mappings dictionary"""
        return {
            # Tech giants and subsidiaries
            'amazon technologies inc': 'AMZN', 'amazon com inc': 'AMZN', 'amazon': 'AMZN',
            'amazon web services': 'AMZN', 'aws': 'AMZN', 'prime video': 'AMZN', 'audible': 'AMZN',
            'whole foods market': 'AMZN', 'zappos': 'AMZN', 'twitch': 'AMZN',
            'apple inc': 'AAPL', 'apple computer inc': 'AAPL', 'apple': 'AAPL',
            'beats electronics': 'AAPL', 'beats': 'AAPL',
            'microsoft corporation': 'MSFT', 'microsoft corp': 'MSFT', 'microsoft': 'MSFT',
            'linkedin corporation': 'MSFT', 'linkedin': 'MSFT', 'skype': 'MSFT',
            'github': 'MSFT', 'xbox': 'MSFT', 'office 365': 'MSFT', 'azure': 'MSFT',
            'google llc': 'GOOGL', 'google inc': 'GOOGL', 'alphabet inc': 'GOOGL', 'google': 'GOOGL',
            'youtube': 'GOOGL', 'android': 'GOOGL', 'chrome': 'GOOGL', 'gmail': 'GOOGL',
            'waymo': 'GOOGL', 'deepmind': 'GOOGL', 'nest': 'GOOGL', 'fitbit': 'GOOGL',
            'facebook inc': 'META', 'meta platforms inc': 'META', 'meta': 'META', 'facebook': 'META',
            'instagram': 'META', 'whatsapp': 'META', 'oculus': 'META', 'threads': 'META',
            'tesla inc': 'TSLA', 'tesla motors inc': 'TSLA', 'tesla': 'TSLA',
            'netflix inc': 'NFLX', 'netflix': 'NFLX',
            'nvidia corporation': 'NVDA', 'nvidia corp': 'NVDA', 'nvidia': 'NVDA',

            # === UK COMPANIES ===
            # UK Automotive
            'jaguar land rover': 'TTM', 'jaguar land rover limited': 'TTM', 'jlr': 'TTM',  # Part of Tata Motors
            'jaguar': 'TTM', 'land rover': 'TTM', 'range rover': 'TTM',
            'rolls royce motor cars': 'BMWYY', 'rolls-royce motor cars': 'BMWYY',  # Owned by BMW
            'bentley motors': 'VLKAF', 'bentley': 'VLKAF',  # Owned by Volkswagen
            'aston martin': 'AML.L', 'aston martin lagonda': 'AML.L',
            'mclaren automotive': 'PRIVATE', 'mclaren': 'PRIVATE',
            'lotus cars': '1211.HK', 'lotus': '1211.HK',  # Owned by Geely

            # UK Retail/Consumer
            'boots': 'WBA', 'boots uk': 'WBA', 'boots plc': 'WBA', 'the boots company': 'WBA',  # Part of Walgreens Boots Alliance
            'tesco': 'TSCO.L', 'tesco plc': 'TSCO.L', 'tesco stores': 'TSCO.L',
            'sainsburys': 'SBRY.L', 'j sainsbury': 'SBRY.L', 'sainsbury\'s': 'SBRY.L',
            'asda': 'PRIVATE', 'asda stores': 'PRIVATE',  # Owned by Issa brothers
            'marks and spencer': 'MKS.L', 'marks & spencer': 'MKS.L', 'm&s': 'MKS.L',
            'next': 'NXT.L', 'next plc': 'NXT.L',
            'primark': 'ABF.L', 'primark stores': 'ABF.L',  # Part of Associated British Foods
            'john lewis': 'PRIVATE', 'john lewis partnership': 'PRIVATE',
            'currys': 'CURY.L', 'currys plc': 'CURY.L', 'pc world': 'CURY.L',
            'argos': 'SBRY.L',  # Owned by Sainsbury's

            # UK Banks/Finance
            'lloyds bank': 'LLOY.L', 'lloyds banking group': 'LLOY.L', 'lloyds': 'LLOY.L',
            'barclays': 'BARC.L', 'barclays bank': 'BARC.L', 'barclays plc': 'BARC.L',
            'hsbc': 'HSBA.L', 'hsbc bank': 'HSBA.L', 'hsbc holdings': 'HSBA.L',
            'royal bank of scotland': 'NWG.L', 'rbs': 'NWG.L', 'natwest': 'NWG.L', 'natwest group': 'NWG.L',
            'santander uk': 'SAN', 'santander': 'SAN',
            'nationwide': 'PRIVATE', 'nationwide building society': 'PRIVATE',
            'halifax': 'LLOY.L',  # Part of Lloyds
            'standard chartered': 'STAN.L', 'standard chartered bank': 'STAN.L',

            # UK Telecom/Media
            'bt group': 'BT-A.L', 'british telecom': 'BT-A.L', 'bt': 'BT-A.L',
            'vodafone': 'VOD.L', 'vodafone group': 'VOD.L', 'vodafone uk': 'VOD.L',
            'sky': 'CMCSA', 'sky uk': 'CMCSA',  # Owned by Comcast
            'virgin media': 'LBTYA', 'virgin media o2': 'LBTYA',  # Part of Liberty Media
            'bbc': 'PRIVATE', 'british broadcasting corporation': 'PRIVATE',
            'itv': 'ITV.L', 'itv plc': 'ITV.L',
            'channel 4': 'PRIVATE', 'channel four': 'PRIVATE',

            # UK Energy/Utilities
            'british gas': 'CNA.L', 'centrica': 'CNA.L',  # British Gas is part of Centrica
            'scottish power': 'IBE', 'scottishpower': 'IBE',  # Owned by Iberdrola
            'eon uk': 'EOAN.DE', 'e.on uk': 'EOAN.DE',
            'edf energy': 'EDF.PA', 'edf': 'EDF.PA',
            'shell uk': 'SHEL', 'shell': 'SHEL',
            'bp': 'BP.L', 'british petroleum': 'BP.L', 'bp plc': 'BP.L',

            # UK Food/Beverage
            'diageo': 'DGE.L', 'diageo plc': 'DGE.L',
            'guinness': 'DGE.L', 'johnnie walker': 'DGE.L', 'smirnoff': 'DGE.L',  # All owned by Diageo
            'cadbury': 'MDLZ', 'cadbury schweppes': 'MDLZ',  # Now owned by Mondelez
            'unilever uk': 'UL', 'unilever plc': 'UL',
            'twinings': 'ABF.L',  # Owned by Associated British Foods
            'walkers': 'PEP', 'walkers crisps': 'PEP',  # Owned by PepsiCo

            # UK Airlines/Transport
            'british airways': 'ICAG.L', 'ba': 'ICAG.L',  # Part of IAG
            'virgin atlantic': 'PRIVATE', 'virgin atlantic airways': 'PRIVATE',
            'easyjet': 'EZJ.L', 'easyjet plc': 'EZJ.L',
            'ryanair': 'RYA.L', 'ryanair holdings': 'RYA.L',

            # === EUROPEAN AUTOMOTIVE ===
            # French
            'renault': 'RNO.PA', 'renault sa': 'RNO.PA', 'renault group': 'RNO.PA',
            'peugeot': 'STLA', 'citroen': 'STLA', 'ds automobiles': 'STLA',  # All part of Stellantis
            'stellantis': 'STLA', 'psa group': 'STLA',

            # German
            'volkswagen': 'VOW3.DE', 'vw': 'VOW3.DE', 'volkswagen group': 'VOW3.DE',
            'audi': 'VOW3.DE', 'porsche': 'P911.DE', 'skoda': 'VOW3.DE', 'seat': 'VOW3.DE',  # VW Group brands
            'bmw': 'BMW.DE', 'bayerische motoren werke': 'BMW.DE', 'bmw group': 'BMW.DE',
            'mini': 'BMW.DE',  # Owned by BMW
            'mercedes': 'MBG.DE', 'mercedes-benz': 'MBG.DE', 'mercedes benz': 'MBG.DE',
            'daimler': 'MBG.DE', 'mercedes-benz group': 'MBG.DE',

            # Korean
            'hyundai': 'HYMTF', 'hyundai motor': 'HYMTF', 'hyundai motors': 'HYMTF',
            'kia': 'KIMTF', 'kia motors': 'KIMTF', 'kia corporation': 'KIMTF',
            'genesis': 'HYMTF',  # Hyundai's luxury brand

            # Japanese
            'toyota': 'TM', 'toyota motor': 'TM', 'toyota motor corporation': 'TM',
            'lexus': 'TM',  # Toyota's luxury brand
            'honda': 'HMC', 'honda motor': 'HMC',
            'nissan': 'NSANY', 'nissan motor': 'NSANY',
            'infiniti': 'NSANY',  # Nissan's luxury brand
            'mazda': 'MZDAY', 'mazda motor': 'MZDAY',
            'mitsubishi motors': 'MMTOF', 'mitsubishi': 'MMTOF',
            'subaru': 'FUJHY', 'subaru corporation': 'FUJHY',
            'suzuki': 'SZKMY', 'suzuki motor': 'SZKMY',
            'isuzu': 'ISUZY', 'isuzu motors': 'ISUZY',

            # Italian
            'ferrari': 'RACE', 'ferrari nv': 'RACE',
            'fiat': 'STLA', 'alfa romeo': 'STLA', 'maserati': 'STLA',  # Part of Stellantis
            'lamborghini': 'VOW3.DE',  # Owned by Volkswagen Group

            # === OTHER INTERNATIONAL COMPANIES ===
            # Chinese Automotive
            'geely': '175.HK', 'geely automobile': '175.HK',
            'byd': 'BYDDY', 'byd company': 'BYDDY', 'byd auto': 'BYDDY',
            'nio': 'NIO', 'nio inc': 'NIO',
            'xpeng': 'XPEV', 'xpeng motors': 'XPEV',
            'li auto': 'LI', 'li motors': 'LI',

            # Swedish
            'volvo cars': 'VOLCAR-B.ST', 'volvo': 'VOLCAR-B.ST',
            'volvo trucks': 'VOLV-B.ST', 'volvo group': 'VOLV-B.ST',
            'saab': 'PRIVATE', 'saab automobile': 'PRIVATE',
            'ikea': 'PRIVATE', 'ikea group': 'PRIVATE',
            'h&m': 'HM-B.ST', 'hennes mauritz': 'HM-B.ST', 'hennes & mauritz': 'HM-B.ST',
            'spotify': 'SPOT', 'spotify technology': 'SPOT',

            # Swiss
            'nestle': 'NESN.SW', 'nestle sa': 'NESN.SW',
            'novartis': 'NOVN.SW', 'novartis ag': 'NOVN.SW',
            'roche': 'ROG.SW', 'roche holding': 'ROG.SW',
            'ubs': 'UBS', 'ubs group': 'UBS',
            'credit suisse': 'PRIVATE',  # Acquired by UBS

            # Dutch
            'asml': 'ASML', 'asml holding': 'ASML',
            'unilever': 'UNA.AS', 'unilever nv': 'UNA.AS',
            'philips': 'PHIA.AS', 'koninklijke philips': 'PHIA.AS', 'royal philips': 'PHIA.AS',
            'shell': 'SHEL', 'royal dutch shell': 'SHEL',
            'ing': 'INGA.AS', 'ing group': 'INGA.AS',

            # === ADDITIONAL MISSING COMPANIES ===
            # Ferrari variations
            'ferrari spa': 'RACE', 'ferrari s.p.a.': 'RACE', 'ferrari s.p.a': 'RACE',
            'ferrari nv': 'RACE', 'ferrari': 'RACE',
            
            # Mattel variations
            'mattel inc': 'MAT', 'mattel incorporated': 'MAT', 'mattel': 'MAT',
            'barbie': 'MAT', 'hot wheels': 'MAT', 'fisher-price': 'MAT',  # Mattel brands
            
            # Nintendo variations
            'nintendo co ltd': 'NTDOY', 'nintendo co., ltd.': 'NTDOY',
            'nintendo company limited': 'NTDOY', 'nintendo': 'NTDOY',
            
            # Warner Bros variations
            'warner bros entertainment inc': 'WBD', 'warner brothers': 'WBD',
            'warner bros': 'WBD', 'warner media': 'WBD', 'hbo': 'WBD',
            'dc comics': 'WBD', 'cnn': 'WBD',  # Warner Bros Discovery brands
            
            # Unilever complex structure
            'unilever global ip limited': 'UL', 'unilever ip holdings bv': 'UL',
            'unilever ip holdings b.v.': 'UL', 'unilever intellectual property': 'UL',
            'unilever holdings': 'UL', 'unilever international': 'UL',
            
            # Mercedes-Benz variations
            'mercedes-benz group ag': 'MBG.DE', 'mercedes benz group': 'MBG.DE',
            'mercedes-benz ag': 'MBG.DE', 'daimler benz': 'MBG.DE',
            
            # Brooks Sports (athletic footwear - different from Brooks Brothers)
            'brooks sports inc': 'BC', 'brooks running': 'BC', 'brooks': 'BC',  # Part of Berkshire Hathaway
            'brooks laboratories': 'BC',  # As you mentioned for shoes
            
            # Nestlé variations (formal French name)
            'societe des produits nestle sa': 'NESN.SW', 'société des produits nestlé s.a.': 'NESN.SW',
            'nestle products': 'NESN.SW', 'nestle international': 'NESN.SW',
            
            # Mizuno (Japanese sporting goods)
            'mizuno corporation': 'MIZUY', 'mizuno': 'MIZUY', 'mizuno usa': 'MIZUY',
            'mizuno co ltd': 'MIZUY',
            
            # BASF (German chemical company)
            'basf se': 'BASFY', 'basf ag': 'BASFY', 'basf': 'BASFY',
            'basf corporation': 'BASFY', 'basf chemicals': 'BASFY',
            
            # Roche Diagnostics (part of Roche Group)
            'roche diagnostics gmbh': 'ROG.SW', 'roche diagnostics': 'ROG.SW',
            'roche molecular systems': 'ROG.SW', 'roche pharma': 'ROG.SW',
            
            # Monster Energy
            'monster energy company': 'MNST', 'monster beverage': 'MNST',
            'monster energy': 'MNST', 'monster': 'MNST',
            
            # ASICS (Japanese athletic footwear)
            'asics corporation': 'ASCCY', 'asics': 'ASCCY', 'asics america': 'ASCCY',
            'asics co ltd': 'ASCCY',
            
            # === RELATED SPORTING GOODS & FOOTWEAR BRANDS ===
            # Athletic footwear companies
            'new balance': 'PRIVATE', 'new balance inc': 'PRIVATE',
            'new balance athletics': 'PRIVATE',
            'under armour': 'UAA', 'under armour inc': 'UAA',
            'puma': 'PUMSY', 'puma se': 'PUMSY', 'puma ag': 'PUMSY',
            'reebok': 'ABG',  # Now owned by Authentic Brands Group
            'vans': 'VFC', 'vans inc': 'VFC',  # Part of VF Corporation
            'timberland': 'VFC',  # Also part of VF Corporation
            'the north face': 'VFC',  # Also VF Corp
            'fila': 'FILA.KS', 'fila holdings': 'FILA.KS',
            
            # Additional Japanese brands
            'yonex': 'PRIVATE', 'yonex co ltd': 'PRIVATE',  # Tennis/badminton equipment
            'bridgestone sports': 'BRDCY',  # Golf equipment, part of Bridgestone
            
            # === ADDITIONAL LUXURY/FASHION BRANDS ===
            # Ferrari luxury/fashion (separate from automotive)
            'ferrari fashion': 'RACE', 'ferrari store': 'RACE',
            
            # LVMH brands (luxury conglomerate)
            'louis vuitton': 'LVMUY', 'christian dior': 'LVMUY',
            'moet chandon': 'LVMUY', 'hennessy': 'LVMUY',
            'bulgari': 'LVMUY', 'tiffany co': 'LVMUY',
            'tag heuer': 'LVMUY', 'fendi': 'LVMUY',
            
            # Kering brands (luxury group)
            'gucci': 'PRTP.PA', 'saint laurent': 'PRTP.PA', 'yves saint laurent': 'PRTP.PA',
            'bottega veneta': 'PRTP.PA', 'balenciaga': 'PRTP.PA',
            'alexander mcqueen': 'PRTP.PA',
            
            # Other luxury brands
            'hermes': 'RMS.PA', 'hermès': 'RMS.PA', 'hermes international': 'RMS.PA',
            'chanel': 'PRIVATE', 'chanel inc': 'PRIVATE',
            'prada': 'PRDSF', 'prada spa': 'PRDSF',
            
            # === ENTERTAINMENT & MEDIA ADDITIONS ===
            # Disney subsidiaries/brands
            'walt disney pictures': 'DIS', 'disney studios': 'DIS',
            'disney parks': 'DIS', 'disney consumer products': 'DIS',
            '20th century studios': 'DIS', 'fox': 'DIS',  # Acquired by Disney
            
            # Universal/NBC Universal (Comcast)
            'universal studios': 'CMCSA', 'universal pictures': 'CMCSA',
            'nbc universal': 'CMCSA', 'nbcuniversal': 'CMCSA',
            
            # Sony entertainment divisions
            'sony pictures': 'SONY', 'sony music': 'SONY',
            'sony interactive entertainment': 'SONY',
            
            # === CHEMICAL & PHARMACEUTICAL ADDITIONS ===
            # Bayer divisions
            'bayer pharmaceuticals': 'BAYRY', 'bayer crop science': 'BAYRY',
            'bayer consumer health': 'BAYRY',
            
            # BASF divisions
            'basf performance products': 'BASFY', 'basf agricultural': 'BASFY',
            'basf coatings': 'BASFY',
            
            # Additional pharma
            'gsk': 'GSK.L', 'gsk plc': 'GSK.L', 'glaxo wellcome': 'GSK.L',
            'astrazeneca': 'AZN', 'zeneca': 'AZN',
            'sanofi': 'SNY', 'sanofi aventis': 'SNY', 'sanofi-aventis': 'SNY',
            
            # === FOOD & BEVERAGE ADDITIONS ===
            # Nestlé brands
            'nescafe': 'NESN.SW', 'kit kat': 'NESN.SW', 'smarties': 'NESN.SW',
            'purina': 'NESN.SW', 'gerber': 'NESN.SW',
            
            # Unilever brands
            'dove': 'UL', 'axe': 'UL', 'lynx': 'UL', 'hellmanns': 'UL',
            'knorr': 'UL', 'lipton': 'UL', 'ben jerrys': 'UL',
            
            # Monster Beverage brands
            'monster ultra': 'MNST', 'reign': 'MNST', 'nos energy': 'MNST',
            
            # Additional beverage brands
            'red bull': 'PRIVATE', 'red bull gmbh': 'PRIVATE',
            'rockstar energy': 'PEP',  # Acquired by PepsiCo
            
            # === TECHNOLOGY HARDWARE ADDITIONS ===
            # Gaming companies
            'valve corporation': 'PRIVATE', 'valve': 'PRIVATE', 'steam': 'PRIVATE',
            'epic games': 'PRIVATE', 'epic': 'PRIVATE', 'unreal engine': 'PRIVATE',
            'activision blizzard': 'MSFT',  # Acquired by Microsoft
            'blizzard entertainment': 'MSFT', 'call of duty': 'MSFT',
            
            # === FORMAL CORPORATE NAMES & INTERNATIONAL VARIATIONS ===
            # Toyota variations
            'toyota jidosha kabushiki kaisha': 'TM',
            'toyota motor corporation': 'TM', 'toyota motor company': 'TM',
            
            # Skechers variations
            'skechers usa inc': 'SKX', 'skechers u.s.a. inc': 'SKX', 'skechers usa': 'SKX',
            'skechers u.s.a., inc. ii': 'SKX', 'skechers usa inc ii': 'SKX',
            
            # Huawei variations
            'huawei technologies co ltd': 'PRIVATE', 'huawei technologies co., ltd.': 'PRIVATE',
            'huawei technologies company': 'PRIVATE', 'huawei tech': 'PRIVATE',
            
            # Bridgestone variations
            'shenzhen bridgestone business co ltd': 'BRDCY', 'bridgestone': 'BRDCY',
            'bridgestone corporation': 'BRDCY', 'bridgestone corp': 'BRDCY',
            
            # Merck variations (distinguish between US and German Merck)
            'merck sharp dohme': 'MRK', 'merck sharp & dohme': 'MRK',
            'merck sharp dohme bv': 'MRK', 'merck sharp & dohme b.v.': 'MRK',
            'msd': 'MRK', 'merck & co inc': 'MRK',
            'merck kgaa': 'MRCG.DE',  # German Merck (different company)
            
            # BMW formal names
            'bayerische motoren werke aktiengesellschaft': 'BMW.DE',
            'bayerische motoren werke ag': 'BMW.DE',
            'bmw aktiengesellschaft': 'BMW.DE', 'bmw ag': 'BMW.DE',
            
            # Eli Lilly variations
            'eli lilly and company': 'LLY', 'eli lilly & company': 'LLY',
            'eli lilly & co': 'LLY', 'lilly usa': 'LLY',
            
            # Bayer variations
            'bayer aktiengesellschaft': 'BAYRY', 'bayer ag': 'BAYRY',
            'bayer corporation': 'BAYRY', 'bayer inc': 'BAYRY',
            'bayer cropscience': 'BAYRY', 'bayer healthcare': 'BAYRY',
            
            # Aldi variations
            'aldi stores limited': 'PRIVATE', 'aldi uk': 'PRIVATE',
            'aldi inc': 'PRIVATE', 'aldi usa': 'PRIVATE',
            'aldi sud': 'PRIVATE', 'aldi north': 'PRIVATE',
            
            # IBM formal names
            'international business machines corporation': 'IBM',
            'ibm corp': 'IBM', 'ibm usa': 'IBM', 'ibm inc': 'IBM',
            
            # Additional formal corporate naming patterns
            # German AG/GmbH companies
            'volkswagen aktiengesellschaft': 'VOW3.DE', 'volkswagen ag': 'VOW3.DE',
            'daimler aktiengesellschaft': 'MBG.DE', 'daimler ag': 'MBG.DE',
            'siemens aktiengesellschaft': 'SIEGY', 'siemens ag': 'SIEGY',
            'sap aktiengesellschaft': 'SAP', 'sap ag': 'SAP', 'sap se': 'SAP',
            'adidas aktiengesellschaft': 'ADDYY', 'adidas ag': 'ADDYY',
            'puma aktiengesellschaft': 'PUMSY', 'puma ag': 'PUMSY',
            
            # French SA companies
            'renault societe anonyme': 'RNO.PA', 'renault sa': 'RNO.PA',
            'peugeot societe anonyme': 'STLA', 'peugeot sa': 'STLA',
            'air liquide societe anonyme': 'AI.PA', 'air liquide sa': 'AI.PA',
            'total societe anonyme': 'TTE', 'total sa': 'TTE', 'totalenergies': 'TTE',
            'lvmh moet hennessy louis vuitton': 'LVMUY', 'lvmh': 'LVMUY',
            
            # Dutch NV/BV companies
            'unilever nv': 'UNA.AS', 'unilever bv': 'UNA.AS',
            'koninklijke philips nv': 'PHIA.AS', 'philips nv': 'PHIA.AS',
            'heineken nv': 'HEINY', 'heineken holding': 'HEINY',
            
            # Japanese kabushiki kaisha companies
            'honda motor kabushiki kaisha': 'HMC', 'honda motor co ltd': 'HMC',
            'nissan motor kabushiki kaisha': 'NSANY', 'nissan motor co ltd': 'NSANY',
            'sony kabushiki kaisha': 'SONY', 'sony corporation': 'SONY',
            'panasonic kabushiki kaisha': 'PCRFY', 'panasonic corporation': 'PCRFY',
            'canon kabushiki kaisha': 'CAJ', 'canon inc': 'CAJ',
            'nintendo kabushiki kaisha': 'NTDOY', 'nintendo co ltd': 'NTDOY',
            'softbank kabushiki kaisha': 'SFTBY', 'softbank corp': 'SFTBY',
            
            # Korean companies
            'samsung electronics co ltd': 'SSNLF', 'samsung electronics': 'SSNLF',
            'lg electronics inc': '066570.KS', 'lg electronics': '066570.KS',
            'sk hynix inc': 'HXSCL', 'sk hynix': 'HXSCL',
            
            # Chinese companies (formal names)
            'alibaba group holding limited': 'BABA', 'alibaba group': 'BABA',
            'tencent holdings limited': 'TCEHY', 'tencent holdings': 'TCEHY',
            'baidu inc': 'BIDU', 'baidu com': 'BIDU',
            'china mobile limited': 'CHL', 'china mobile': 'CHL',
            'petrochina company limited': 'PTR', 'petrochina': 'PTR',
            
            # UK formal names (Plc/Limited)
            'british petroleum plc': 'BP.L', 'bp plc': 'BP.L',
            'royal dutch shell plc': 'SHEL', 'shell plc': 'SHEL',
            'vodafone group plc': 'VOD.L', 'vodafone plc': 'VOD.L',
            'bt group plc': 'BT-A.L', 'british telecom plc': 'BT-A.L',
            'tesco stores limited': 'TSCO.L', 'tesco limited': 'TSCO.L',
            'sainsbury plc': 'SBRY.L', 'j sainsbury plc': 'SBRY.L',
            'marks spencer plc': 'MKS.L', 'marks and spencer plc': 'MKS.L',
            
            # US formal Inc/Corp variations
            'apple computer inc': 'AAPL', 'apple incorporated': 'AAPL',
            'microsoft corp': 'MSFT', 'microsoft incorporated': 'MSFT',
            'amazon com inc': 'AMZN', 'amazon incorporated': 'AMZN',
            'alphabet inc': 'GOOGL', 'google incorporated': 'GOOGL',
            'meta platforms inc': 'META', 'facebook inc': 'META',
            'tesla motors inc': 'TSLA', 'tesla incorporated': 'TSLA',
            'netflix incorporated': 'NFLX', 'netflix inc': 'NFLX',
            'nvidia corp': 'NVDA', 'nvidia incorporated': 'NVDA',
            
            # Pharmaceutical formal names
            'johnson johnson inc': 'JNJ', 'johnson & johnson incorporated': 'JNJ',
            'pfizer incorporated': 'PFE', 'pfizer inc': 'PFE',
            'roche holding ag': 'ROG.SW', 'f hoffmann-la roche': 'ROG.SW',
            'novartis ag': 'NOVN.SW', 'novartis pharma': 'NOVN.SW',
            'glaxosmithkline plc': 'GSK.L', 'gsk plc': 'GSK.L',
            'astrazeneca plc': 'AZN', 'astrazeneca inc': 'AZN',
            'bristol myers squibb company': 'BMY', 'bristol-myers squibb co': 'BMY',
            
            # Food & Beverage formal names
            'nestle sa': 'NESN.SW', 'nestle societe anonyme': 'NESN.SW',
            'unilever united states inc': 'UL', 'unilever usa': 'UL',
            'procter gamble company': 'PG', 'procter & gamble co': 'PG',
            'coca cola company': 'KO', 'coca-cola co': 'KO',
            'pepsico incorporated': 'PEP', 'pepsi-cola company': 'PEP',
            
            # Retail formal names
            'walmart stores inc': 'WMT', 'wal-mart inc': 'WMT',
            'amazon retail llc': 'AMZN', 'amazon services llc': 'AMZN',
            'target brands inc': 'TGT', 'target stores': 'TGT',
            'home depot usa inc': 'HD', 'home depot inc': 'HD',
            'costco wholesale corp': 'COST', 'costco companies': 'COST',

            # === EXISTING US COMPANIES (keeping all previous mappings) ===
            # Consumer brands
            'coca cola company': 'KO', 'coca-cola company': 'KO', 'coca cola': 'KO', 'coca-cola': 'KO',
            'sprite': 'KO', 'fanta': 'KO', 'diet coke': 'KO', 'powerade': 'KO',
            'pepsico inc': 'PEP', 'pepsi': 'PEP', 'pepsico': 'PEP',
            'mountain dew': 'PEP', 'gatorade': 'PEP', 'tropicana': 'PEP', 'quaker oats': 'PEP',
            'frito lay': 'PEP', 'doritos': 'PEP', 'cheetos': 'PEP', 'lays': 'PEP',
            'mcdonalds corporation': 'MCD', 'mcdonald\'s corporation': 'MCD', 'mcdonalds': 'MCD',
            'walmart inc': 'WMT', 'wal-mart stores inc': 'WMT', 'walmart': 'WMT', 'sams club': 'WMT',
            'disney enterprises inc': 'DIS', 'walt disney company': 'DIS', 'disney': 'DIS',
            'marvel entertainment': 'DIS', 'marvel': 'DIS', 'star wars': 'DIS', 'lucasfilm': 'DIS',
            'pixar': 'DIS', 'espn': 'DIS', 'abc': 'DIS', 'disney+': 'DIS', 'hulu': 'DIS',
            'nike inc': 'NKE', 'nike': 'NKE', 'jordan brand': 'NKE', 'air jordan': 'NKE', 'converse': 'NKE',
            'starbucks corporation': 'SBUX', 'starbucks': 'SBUX',
            'home depot inc': 'HD', 'home depot': 'HD',
            'target corporation': 'TGT', 'target corp': 'TGT', 'target': 'TGT',
            'costco wholesale corporation': 'COST', 'costco': 'COST',

            # Tech/Software
            'intel corporation': 'INTC', 'intel corp': 'INTC', 'intel': 'INTC',
            'ibm corporation': 'IBM', 'international business machines': 'IBM', 'ibm': 'IBM', 'red hat': 'IBM',
            'oracle corporation': 'ORCL', 'oracle america inc': 'ORCL', 'oracle': 'ORCL',
            'salesforce inc': 'CRM', 'salesforce.com inc': 'CRM', 'salesforce': 'CRM', 'slack': 'CRM', 'tableau': 'CRM',
            'adobe inc': 'ADBE', 'adobe systems inc': 'ADBE', 'adobe': 'ADBE', 'photoshop': 'ADBE', 'acrobat': 'ADBE',
            'cisco systems inc': 'CSCO', 'cisco': 'CSCO',
            'advanced micro devices': 'AMD', 'amd': 'AMD',
            'qualcomm inc': 'QCOM', 'qualcomm': 'QCOM',

            # Financial
            'visa inc': 'V', 'visa international': 'V', 'visa': 'V',
            'mastercard inc': 'MA', 'mastercard international': 'MA', 'mastercard': 'MA',
            'paypal inc': 'PYPL', 'paypal': 'PYPL', 'venmo': 'PYPL',
            'american express': 'AXP', 'amex': 'AXP',
            'jp morgan chase': 'JPM', 'jpmorgan chase': 'JPM', 'jpmorgan': 'JPM', 'chase bank': 'JPM',
            'bank of america': 'BAC', 'bofa': 'BAC', 'merrill lynch': 'BAC',
            'wells fargo': 'WFC', 'wells fargo bank': 'WFC',
            'goldman sachs': 'GS', 'goldman sachs group': 'GS',
            'citigroup': 'C', 'citi': 'C',

            # Transportation/Logistics
            'uber technologies inc': 'UBER', 'uber': 'UBER', 'uber eats': 'UBER',
            'lyft inc': 'LYFT', 'lyft': 'LYFT',
            'airbnb inc': 'ABNB', 'airbnb': 'ABNB',
            'fedex corporation': 'FDX', 'fedex': 'FDX',
            'united parcel service': 'UPS', 'ups': 'UPS',
            'doordash': 'DASH', 'door dash': 'DASH',

            # Media/Entertainment
            'zoom video communications': 'ZM', 'zoom': 'ZM',
            'spotify technology sa': 'SPOT', 'spotify': 'SPOT',
            'twitter inc': 'TWTR', 'twitter': 'TWTR',
            'snapchat inc': 'SNAP', 'snap inc': 'SNAP', 'snapchat': 'SNAP',
            'roku inc': 'ROKU', 'roku': 'ROKU',
            'roblox corporation': 'RBLX', 'roblox': 'RBLX',
            'world wrestling entertainment': 'WWE', 'wwe': 'WWE',

            # Pharma/Healthcare
            'johnson & johnson': 'JNJ', 'johnson and johnson': 'JNJ', 'jnj': 'JNJ',
            'pfizer inc': 'PFE', 'pfizer': 'PFE',
            'moderna inc': 'MRNA', 'moderna': 'MRNA',
            'abbott laboratories': 'ABT', 'abbott': 'ABT',
            'merck': 'MRK', 'merck & co': 'MRK',
            'bristol myers squibb': 'BMY', 'bristol-myers squibb': 'BMY',
            'eli lilly': 'LLY', 'lilly': 'LLY',

            # Industrial/Energy/Auto
            'general electric': 'GE', 'ge': 'GE',
            'boeing company': 'BA', 'boeing': 'BA',
            'caterpillar inc': 'CAT', 'caterpillar': 'CAT',
            'exxon mobil corporation': 'XOM', 'exxonmobil': 'XOM', 'exxon': 'XOM',
            'chevron corporation': 'CVX', 'chevron': 'CVX',
            'general motors': 'GM', 'gm': 'GM', 'cadillac': 'GM', 'chevrolet': 'GM',
            'ford motor company': 'F', 'ford': 'F',

            # Consumer goods
            'procter & gamble': 'PG', 'procter and gamble': 'PG', 'pg': 'PG',
            'tide': 'PG', 'crest': 'PG', 'gillette': 'PG', 'pampers': 'PG',
            'unilever': 'UL', 'unilever plc': 'UL',
            'colgate palmolive': 'CL', 'colgate-palmolive': 'CL', 'colgate': 'CL',

            # International (updated)
            'samsung electronics': 'SSNLF', 'samsung': 'SSNLF',
            'taiwan semiconductor': 'TSM', 'tsmc': 'TSM',

            # Pharmaceutical/Healthcare (international)
            'boehringer ingelheim': 'PRIVATE', 'boehringer ingelheim international': 'PRIVATE',
            'glaxo group': 'GSK.L', 'glaxosmithkline': 'GSK.L', 'glaxo': 'GSK.L',  # UK listed
            'gilead sciences': 'GILD', 'gilead': 'GILD',

            # Consumer goods/Retail
            'loreal': 'OR.PA', 'l\'oreal': 'OR.PA', 'l oreal': 'OR.PA',
            'barkbox': 'BARK', 'bark': 'BARK',
            'anker innovations': 'PRIVATE', 'anker': 'PRIVATE',
            'skechers': 'SKX', 'skechers usa': 'SKX',

            # Technology/Electronics
            'huawei technologies': 'PRIVATE', 'huawei': 'PRIVATE',
            'lg electronics': '066570.KS', 'lg': '066570.KS',
            'international business machines corporation': 'IBM',
            'fujifilm': 'FUJIY', 'fujifilm corporation': 'FUJIY',
            'shenzhen ske technology': 'PRIVATE',

            # Gaming/Entertainment
            'igt': 'IGT', 'igt nevada': 'IGT',
            'playn go': 'PRIVATE', 'play n go': 'PRIVATE',
            'light & wonder': 'LNW', 'light and wonder': 'LNW',
            'euro games technology': 'PRIVATE',
            'push gaming': 'PRIVATE',
            'mob entertainment': 'PRIVATE',

            # Sports/Recreation
            'karsten manufacturing': 'PRIVATE',
            'topgolf callaway brands': 'MODG', 'callaway': 'MODG', 'topgolf': 'MODG',

            # Tires/Automotive Parts
            'guizhou tyre': 'PRIVATE', 'guizhou tyre import export': 'PRIVATE',

            # Agriculture/Chemicals
            'upl mauritius': 'UPL.NS', 'upl': 'UPL.NS',

            # Tobacco
            'philip morris products': 'PM', 'philip morris': 'PM',

            # Berkshire Hathaway
            'berkshire hathaway inc': 'BRK-A', 'berkshire hathaway': 'BRK-A',
            'geico': 'BRK-A', 'dairy queen': 'BRK-A', 'duracell': 'BRK-A',
        }
    
    @staticmethod
    def get_company_blacklist():
        """Return companies that should be excluded from matching"""
        return {
            'fireheart music', 'fireheart music inc', 'music inc', 'entertainment llc',
            'holdings llc', 'management llc', 'ventures llc', 'capital llc',
            'music publishing', 'records', 'label', 'studio', 'films',
            'production company', 'media group', 'creative', 'design',
            'consulting', 'law firm', 'legal services', 'attorneys',
            # Add some more specific exclusions
            'private limited', 'ltd', 'limited company', 'partnership',
            'independent', 'freelance', 'consultant', 'agency'
        }

class StockMatcher:
    """Enhanced stock matching functionality"""
    
    def __init__(self, config):
        self.config = config
        self.cache_file = config.stock_cache_path  # Use config path instead of hardcoded
        self.stock_cache = self._load_cache()
        self.manual_mappings = CompanyMappings.get_manual_mappings()
        self.company_blacklist = CompanyMappings.get_company_blacklist()
        
        print(f"Loaded {len(self.manual_mappings)} manual company mappings")
        print(f"Loaded {len(self.company_blacklist)} blacklisted terms")
    
    def _load_cache(self):
        """Load stock data cache from file"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cache: {e}")
        return {}
    
    def _save_cache(self):
        """Save stock data cache to file"""
        try:
            # Ensure directory exists (though not needed in flat structure)
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.stock_cache, f)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def normalize_company_name(self, name):
        """Normalize company name for matching"""
        if not name or pd.isna(name):
            return ""
        
        name = str(name).lower().strip()
        
        # Remove common prefixes
        prefixes = ['the ', 'a ', 'an ']
        for prefix in prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]
        
        # Remove common suffixes
        suffixes = ['inc', 'incorporated', 'corp', 'corporation', 'company', 'co', 'ltd', 'limited',
                   'llc', 'technologies', 'technology', 'tech', 'systems', 'solutions',
                   'enterprises', 'holdings', 'group', 'international', 'worldwide', 'global',
                   'services', 'industries']
        
        # Clean punctuation and normalize spaces
        name = re.sub(r'[^\w\s]', ' ', name)
        name = re.sub(r'\s+', ' ', name).strip()
        
        # Remove suffixes
        words = [word for word in name.split() if word not in suffixes]
        return ' '.join(words)
    
    def is_blacklisted_company(self, company_name):
        """Check if company should be excluded from matching"""
        normalized = self.normalize_company_name(company_name)
        
        # Exception list for known entertainment companies that should be matched
        known_entertainment_companies = {
            'world wrestling entertainment', 'wwe', 'light & wonder', 'light and wonder',
            'igt', 'mob entertainment', 'playn go', 'play n go', 'euro games technology',
            'push gaming', 'disney', 'netflix', 'spotify', 'sony', 'warner', 'universal'
        }
        
        # Check if it's a known entertainment company that should be matched
        for known in known_entertainment_companies:
            if known in normalized:
                return False
        
        # Check against blacklist
        for blacklisted in self.company_blacklist:
            if blacklisted in normalized:
                return True
        
        # Additional checks for specific patterns
        if any(term in normalized for term in ['music', 'entertainment', 'wrestling', 'films', 'records']):
            return True
        
        return False
    
    def find_ticker_by_fuzzy_match(self, company_name, threshold=85):
        """Find stock ticker using fuzzy matching"""
        normalized_name = self.normalize_company_name(company_name)
        if not normalized_name:
            return None
        
        # Check blacklist first
        if self.is_blacklisted_company(company_name):
            print(f"Skipping blacklisted company: {company_name}")
            return None
        
        # Check exact matches first
        if normalized_name in self.manual_mappings:
            return self.manual_mappings[normalized_name]
        
        # Enhanced fuzzy matching with stricter criteria
        match = process.extractOne(normalized_name, self.manual_mappings.keys(),
                                 scorer=fuzz.token_sort_ratio, score_cutoff=threshold)
        
        if match:
            matched_key, score = match
            
            # Additional validation: check if key words overlap
            normalized_words = set(normalized_name.split())
            matched_words = set(matched_key.split())
            
            # Require at least one significant word overlap (length > 2)
            significant_overlap = any(
                word in matched_words and len(word) > 2
                for word in normalized_words
            )
            
            # For very short company names, require higher similarity
            if len(normalized_name.split()) <= 2 and score < 95:
                return None
            
            # Require word overlap for medium confidence matches
            if score < 95 and not significant_overlap:
                print(f"Rejecting match: '{normalized_name}' -> '{matched_key}' (score: {score}, no significant word overlap)")
                return None
            
            return self.manual_mappings[matched_key]
        
        return None
    
    def get_stock_info(self, ticker):
        """Get stock information with caching"""
        if ticker in self.stock_cache:
            try:
                cache_time = datetime.fromisoformat(self.stock_cache[ticker]['timestamp'])
                if datetime.now() - cache_time < timedelta(hours=self.config.STOCK_CACHE_HOURS):
                    return self.stock_cache[ticker]['data']
            except Exception:
                pass
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            stock_data = {
                'ticker': ticker,
                'name': info.get('longName', info.get('shortName', ticker)),
                'price': info.get('currentPrice', info.get('regularMarketPrice')),
                'market_cap': info.get('marketCap'),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'country': info.get('country'),
                'exchange': info.get('exchange'),
                'currency': info.get('currency', 'USD'),
                'pe_ratio': info.get('forwardPE', info.get('trailingPE')),
                'dividend_yield': info.get('dividendYield'),
                'valid': True
            }
            self.stock_cache[ticker] = {'data': stock_data, 'timestamp': datetime.now().isoformat()}
            self._save_cache()
            return stock_data
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return {'ticker': ticker, 'valid': False, 'error': str(e)}
    
    def analyze_trademark_companies(self, df, limit=500):
        """Analyze trademark companies for stock market presence"""
        if 'Owner' not in df.columns:
            return pd.DataFrame()
        
        top_companies = df['Owner'].value_counts().head(limit)
        results = []
        matches_found = 0
        rejected_matches = 0
        
        print(f"Analyzing top {len(top_companies)} companies for stock market presence...")
        
        for i, (company, count) in enumerate(top_companies.items()):
            if i % 50 == 0:
                print(f"Progress: {i}/{len(top_companies)} ({i/len(top_companies)*100:.1f}%) - Found {matches_found} matches, rejected {rejected_matches}")
            
            ticker = self.find_ticker_by_fuzzy_match(company)
            if ticker:
                stock_info = self.get_stock_info(ticker)
                if stock_info.get('valid', False):
                    matches_found += 1
                    confidence = 'High'
                    
                    # Determine confidence level
                    normalized_company = self.normalize_company_name(company)
                    if normalized_company in self.manual_mappings:
                        confidence = 'Exact'
                    
                    results.append({
                        'trademark_owner': str(company),
                        'trademark_count': int(count),
                        'ticker': str(ticker),
                        'company_name': str(stock_info.get('name', '')),
                        'current_price': float(stock_info.get('price', 0)) if stock_info.get('price') else None,
                        'market_cap': int(stock_info.get('market_cap', 0)) if stock_info.get('market_cap') else None,
                        'sector': str(stock_info.get('sector', '')) if stock_info.get('sector') else None,
                        'industry': str(stock_info.get('industry', '')) if stock_info.get('industry') else None,
                        'country': str(stock_info.get('country', '')) if stock_info.get('country') else None,
                        'pe_ratio': float(stock_info.get('pe_ratio', 0)) if stock_info.get('pe_ratio') else None,
                        'dividend_yield': float(stock_info.get('dividend_yield', 0)) if stock_info.get('dividend_yield') else None,
                        'match_confidence': confidence
                    })
            else:
                if self.is_blacklisted_company(company):
                    rejected_matches += 1
                
                results.append({
                    'trademark_owner': str(company),
                    'trademark_count': int(count),
                    'ticker': None, 'company_name': None, 'current_price': None,
                    'market_cap': None, 'sector': None, 'industry': None,
                    'country': None, 'pe_ratio': None, 'dividend_yield': None,
                    'match_confidence': 'No Match'
                })
        
        print(f"Analysis complete! Found {matches_found} public companies out of {len(results)} total.")
        print(f"Rejected {rejected_matches} potential false matches.")
        print(f"Match rate: {matches_found/len(results)*100:.1f}%")
        return pd.DataFrame(results)

# For backward compatibility, create an alias
EnhancedStockMatcher = StockMatcher