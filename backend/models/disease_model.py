class DiseaseModel:
    def __init__(self):
        self.diseases = [
            {
                "name": "Sooty Mould",
                "description": "Black fungal growth on leaves caused by insect secretions.",
                "organic_treatment": "Wash leaves + neem oil spray",
                "chemical_treatment": "Use copper-based fungicide"
            },
            {
                "name": "Powdery Mildew",
                "description": "White powder-like fungus on leaves.",
                "organic_treatment": "Use neem oil or baking soda spray",
                "chemical_treatment": "Apply sulfur fungicide"
            },
            {
                "name": "Bacterial Canker",
                "description": "Causes lesions, wilting and dieback.",
                "organic_treatment": "Prune infected parts",
                "chemical_treatment": "Use copper bactericide"
            },
            {
                "name": "Cutting Weevil",
                "description": "Insect pest damaging stems and roots.",
                "organic_treatment": "Apply neem cake in soil",
                "chemical_treatment": "Use chlorpyrifos insecticide"
            },
            {
                "name": "Gall Midge",
                "description": "Larvae cause leaf curling and gall formation.",
                "organic_treatment": "Remove affected leaves + neem oil",
                "chemical_treatment": "Use systemic insecticide"
            },
            {
                "name": "Die Back",
                "description": "Drying of branches from tip downward.",
                "organic_treatment": "Prune infected branches",
                "chemical_treatment": "Apply carbendazim"
            },
            {
                "name": "Anthracnose",
                "description": "Dark lesions on leaves and fruits.",
                "organic_treatment": "Neem oil spray",
                "chemical_treatment": "Use mancozeb fungicide"
            },
            {
                "name": "Healthy",
                "description": "Plant is healthy and disease-free.",
                "organic_treatment": "Maintain proper care",
                "chemical_treatment": "No treatment required"
            }
        ]

    def get_all_diseases(self):
        return self.diseases

    # ✅ IMPROVED SMART MATCHING
    def find_disease(self, user_msg):
        user_msg = user_msg.lower()

        for d in self.diseases:
            name = d["name"].lower()

            # exact match
            if name in user_msg:
                return d

            # word match (handles partial words)
            if any(word in user_msg for word in name.split()):
                return d

        # 🔥 smart keyword detection
        if "white" in user_msg or "powder" in user_msg:
            return next(d for d in self.diseases if d["name"] == "Powdery Mildew")

        if "black" in user_msg or "sooty" in user_msg:
            return next(d for d in self.diseases if d["name"] == "Sooty Mould")

        if "dry" in user_msg or "die" in user_msg:
            return next(d for d in self.diseases if d["name"] == "Die Back")

        if "spot" in user_msg or "lesion" in user_msg:
            return next(d for d in self.diseases if d["name"] == "Anthracnose")

        if "insect" in user_msg or "worm" in user_msg:
            return next(d for d in self.diseases if d["name"] == "Cutting Weevil")

        return None