from flask import Blueprint, request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from backend.api.user_routes import token_required
from backend.models.image_model import ImageModel
from backend.models.disease_model import DiseaseModel
from backend.ml_model.predict_service import PredictService
import os
import uuid

scan_bp = Blueprint('scan_bp', __name__)

image_model = ImageModel()
disease_model = DiseaseModel()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@scan_bp.route('/upload-and-analyze', methods=['POST'])
@token_required
def upload_and_analyze(current_user_id):

    try:
        # ✅ CREATE HERE (inside request context)
        predict_service = PredictService()

        # Check image
        if 'image' not in request.files:
            return jsonify({"message": "No image file"}), 400

        image_file = request.files['image']
        tree_id = request.form.get('tree_id')
        scan_latitude = request.form.get('scan_latitude')
        scan_longitude = request.form.get('scan_longitude')

        if image_file.filename == '':
            return jsonify({"message": "No file selected"}), 400

        if not allowed_file(image_file.filename):
            return jsonify({"message": "Invalid file type"}), 400

        # -------- SAVE FILE --------
        filename = secure_filename(image_file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{ext}"

        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        image_file.save(save_path)

        # -------- ML PREDICTION --------
        image_file.seek(0)
        result = predict_service.analyze_image(image_file)

        predicted_class = result['predicted_class']

        # -------- GET DISEASE DETAILS --------
        disease_details = next(
            (d for d in disease_model.get_all_diseases() if d["name"] == predicted_class),
            None
        )

        # -------- SAVE IMAGE --------
        image_id = image_model.create_image(
            user_id=current_user_id,
            file_path=f"uploads/{unique_filename}",
            tree_id=int(tree_id) if tree_id else None,
            status='analyzed',
            scan_latitude=float(scan_latitude) if scan_latitude else None,
            scan_longitude=float(scan_longitude) if scan_longitude else None
        )

        if not image_id:
            raise Exception("Image insert failed")

        # -------- SAVE PREDICTION --------
        image_model.save_prediction(
            image_id=image_id,
            predicted_class=predicted_class,
            confidence_score=result['confidence_score'],
            raw_output=result['raw_output']
        )

        # -------- RESPONSE --------
        image_url = url_for('serve_uploaded_file', filename=unique_filename, _external=True)

        return jsonify({
            "message": "Success",
            "image_id": image_id,
            "file_path": image_url,
            "result": {
                "class": predicted_class,
                "confidence": result['confidence_score'],
                "treatment_details": {
                    "organic": disease_details.get('organic_treatment', "N/A") if disease_details else "N/A",
                    "chemical": disease_details.get('chemical_treatment', "N/A") if disease_details else "N/A"
                },
                "raw_data": result.get('raw_output', {})
            }
        }), 200

    except Exception as e:
        print("MAIN ERROR:", e)

        if 'save_path' in locals() and os.path.exists(save_path):
            os.remove(save_path)

        return jsonify({
            "message": "Server error",
            "error": str(e)
        }), 500


@scan_bp.route('/gallery', methods=['GET'])
@token_required
def get_gallery(current_user_id):

    images = image_model.get_user_gallery(current_user_id)

    if images is None:
        images = []

    for image in images:
        image['file_path'] = url_for(
            'serve_uploaded_file',
            filename=image['file_path'].split('/')[-1],
            _external=True
        )

    return jsonify(images), 200