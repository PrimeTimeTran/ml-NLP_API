from flask import Blueprint, jsonify, request

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def home():
    result = routes_bp.model_instance.do_something()
    return jsonify(result)

@routes_bp.route('/sentiment')
def classifier_sentiment():
    prompt = request.args.get('prompt')
    result = routes_bp.model_instance.sentiment_analysis(prompt)
    return jsonify(result)

@routes_bp.route('/subject')
def classifier_subject():
    prompt = request.args.get('prompt')
    result = routes_bp.model_instance.subject_analysis(prompt)
    return jsonify(result)

@routes_bp.route('/generate')
def generate():
    prompt = request.args.get('prompt')
    result = routes_bp.model_instance.generate(prompt)
    return jsonify(result)

def register_routes(app, model_instance):
    routes_bp.model_instance = model_instance
    app.register_blueprint(routes_bp)
