from flask import Blueprint, request, jsonify
from backend.models.disease_model import DiseaseModel

chatbot_bp = Blueprint('chatbot_bp', __name__)
disease_model = DiseaseModel()


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    try:
        user_msg = request.json.get('message', '').lower().strip()

        # ✅ Greeting
        if user_msg in ["hi", "hello", "hey"]:
            return jsonify({
                "reply": "👋 Hello! What do you want to ask about plant diseases?"
            })

        # ✅ Use smart function
        disease = disease_model.find_disease(user_msg)

        if disease:
            return jsonify({
                "reply": f"""
🌿 Disease: {disease['name']}

🧾 {disease['description']}

🌱 Organic: {disease['organic_treatment']}
🧪 Chemical: {disease['chemical_treatment']}
"""
            })

        # ✅ Extra smart keyword fallback
        if "white" in user_msg or "powder" in user_msg:
            return jsonify({"reply": "⚠️ This looks like Powdery Mildew."})

        if "black" in user_msg or "sooty" in user_msg:
            return jsonify({"reply": "⚠️ This may be Sooty Mould."})

        if "dry" in user_msg or "die" in user_msg:
            return jsonify({"reply": "⚠️ This could be Die Back disease."})

        if "spot" in user_msg:
            return jsonify({"reply": "⚠️ This may be Anthracnose."})

        return jsonify({
            "reply": "❌ Not found. Try: powdery mildew, black spots, dry leaves"
        })

    except Exception as e:
        print("CHATBOT ERROR:", e)
        return jsonify({"reply": "⚠️ Server error"}), 500