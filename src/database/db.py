from flask_sqlalchemy import SQLAlchemy

def create_db():
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dna_records.db'
  db = SQLAlchemy(app)
  
  # Database Model
  class DNARecord(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      sequence = db.Column(db.String, unique=True, nullable=False)
      is_mutant = db.Column(db.Boolean, nullable=False)
  
  # Create the database
  with app.app_context():
      db.create_all()

