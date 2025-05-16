from application import app, db

with app.app_context():
    db.create_all()
    app.run(debug=1, host="0.0.0.0", port=5000)