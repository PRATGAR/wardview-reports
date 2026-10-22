from flask import Flask, jsonify

from . import config, db, storage
from .logging_setup import configure_logging
from .blueprints import auth, doctors, jobs, ops, orders, patients, reports, results, sharing
from .converters import MrnConverter
from .security import load_user


def create_app(overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)
    if overrides:
        app.config.update(overrides)

    configure_logging(app)
    app.url_map.converters["mrn"] = MrnConverter
    app.teardown_appcontext(db.close_db)
    app.before_request(load_user)

    app.register_blueprint(auth.bp)
    app.register_blueprint(patients.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(results.bp)
    app.register_blueprint(reports.bp)
    app.register_blueprint(sharing.bp)
    app.register_blueprint(doctors.bp)
    app.register_blueprint(ops.bp)
    app.register_blueprint(jobs.bp)

    @app.errorhandler(401)
    def unauthenticated(_error):
        return jsonify({"error": "authentication required"}), 401

    @app.errorhandler(403)
    def forbidden(_error):
        return jsonify({"error": "forbidden"}), 403

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "not found"}), 404

    with app.app_context():
        storage.ensure_dirs()

    return app
