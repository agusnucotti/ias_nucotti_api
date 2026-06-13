from app.app import init_db, app

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)  # nosec B104
    