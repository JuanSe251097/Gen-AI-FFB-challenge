import os, psycopg2
from typing import Union
from os.path import join, dirname, realpath
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import sqlite3

from src.api.database.db import create_db
from src.api.extra.is_mutant import is_mutant

db = create_db()
is_mutant = is_mutant()

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




# Non-mutant DNA matrix (should return False)
non_mutant_dna = [
    "ATGCGA",
    "CAGTGC",
    "TTATTT",
    "AGACGG",
    "GCGTCA",
    "TCACTG"
]

# Mutant DNA matrix (should return True)
mutant_dna = [
    "ATGCGA",
    "CAGTGC",
    "TTATGT",
    "AGAAGG",
    "CCCCTA",
    "TCACTG"
]

def is_mutant(dna):
    def has_sequence(sequence):
        count = 1
        for i in range(1, len(sequence)):
            if sequence[i] == sequence[i - 1]:
                count += 1
                if count == 4:
                    return True
            else:
                count = 1
        return False

    def check_horizontal():
        return sum(has_sequence(row) for row in dna)

    def check_vertical():
        return sum(has_sequence([dna[i][j] for i in range(len(dna))]) for j in range(len(dna[0])))

    def check_diagonal():
        n = len(dna)
        found_sequences = 0

        for i in range(n - 3):
            # Check main diagonals from top-left to bottom-right
            found_sequences += has_sequence([dna[i + k][k] for k in range(n - i)])
            found_sequences += has_sequence([dna[k][i + k] for k in range(n - i)])

            # Check anti-diagonals from top-right to bottom-left
            found_sequences += has_sequence([dna[i + k][n - 1 - k] for k in range(n - i)])
            found_sequences += has_sequence([dna[k][n - 1 - i - k] for k in range(n - i)])

        return found_sequences

    # Sum all found sequences
    found_sequences = check_horizontal() + check_vertical() + check_diagonal()
    return found_sequences > 1

# Testing the function
print("Non-mutant test:", is_mutant(non_mutant_dna))  # Expected output: False
print("Mutant test:", is_mutant(mutant_dna))          # Expected output: True
