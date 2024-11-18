import os, psycopg2
import pandas as pd
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from src.api.database.db import create_db
from src.api.extra.is_mutant import is_mutant

db = create_db()

app = Flask(__name__)

@app.route('/mutant', methods=['POST'])
def mutant():
    data = request.get_json()
    dna = data.get('dna')

    if not dna or not all(isinstance(row, str) for row in dna):
        return jsonify({"error": "Invalid DNA format"}), 400

    dna_sequence = ','.join(dna)
    existing_record = DNARecord.query.filter_by(sequence=dna_sequence).first()

    if existing_record:
        result = existing_record.is_mutant
    else:
        result = is_mutant(dna)
        new_record = DNARecord(sequence=dna_sequence, is_mutant=result)
        db.session.add(new_record)
        db.session.commit()

    if result:
        return jsonify({"message": "Mutant detected!"}), 200
    else:
        return jsonify({"message": "Human detected!"}), 403

@app.route('/stats', methods=['GET'])
def stats():
    mutants = DNARecord.query.filter_by(is_mutant=True).count()
    humans = DNARecord.query.filter_by(is_mutant=False).count()
    ratio = mutants / (mutants + humans) if (mutants + humans) > 0 else 0
    return jsonify({
        "count_mutant_dna": mutants,
        "count_human_dna": humans,
        "ratio": ratio
    })
    
if __name__ == '__main__':
    app.run(debug = True)
