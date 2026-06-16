from app.app import app, init_db

with app.app_context():
    init_db()

if __name__ == '__main__':
    import os
    debug = os.environ.get('DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=5000, debug=debug)