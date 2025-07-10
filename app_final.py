#!/usr/bin/env python3
"""
School Review Manager - Final Working Version
Simple Flask app with SQLite database
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'school-review-secret-key-2025'

# Database file path
DATABASE = 'reviews.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database if it doesn't exist"""
    if not os.path.exists(DATABASE):
        conn = get_db()
        conn.execute('''
            CREATE TABLE reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT NOT NULL,
                reviewer_name TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert sample data
        sample_data = [
            ('ABC International School', 'John Doe', 5, 'Excellent school with great faculty and infrastructure.'),
            ('Springfield Elementary', 'Jane Smith', 4, 'Good academic programs but could improve extracurricular activities.'),
            ('Green Valley High School', 'Mike Johnson', 3, 'Average school with decent facilities.')
        ]
        
        conn.executemany('''
            INSERT INTO reviews (school_name, reviewer_name, rating, comment) 
            VALUES (?, ?, ?, ?)
        ''', sample_data)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized with sample data")

@app.route('/')
def index():
    return redirect(url_for('reviews'))

@app.route('/addreview', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        school_name = request.form.get('school_name', '').strip()
        reviewer_name = request.form.get('reviewer_name', '').strip()
        rating = request.form.get('rating')
        comment = request.form.get('comment', '').strip()
        
        # Validation
        errors = []
        if not school_name:
            errors.append('School name is required')
        if not reviewer_name:
            errors.append('Reviewer name is required')
        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            errors.append('Rating must be between 1 and 5')
        if not comment:
            errors.append('Comment is required')
            
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('add_review.html')
        
        # Insert into database
        try:
            conn = get_db()
            conn.execute('''
                INSERT INTO reviews (school_name, reviewer_name, rating, comment) 
                VALUES (?, ?, ?, ?)
            ''', (school_name, reviewer_name, int(rating), comment))
            conn.commit()
            conn.close()
            flash('Review submitted successfully!', 'success')
            return redirect(url_for('reviews'))
        except Exception as e:
            logger.error(f"Error inserting review: {e}")
            flash('Error submitting review. Please try again.', 'error')
            return render_template('add_review.html')
    
    return render_template('add_review.html')

@app.route('/reviews')
def reviews():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, school_name, reviewer_name, rating, comment, created_at 
            FROM reviews 
            ORDER BY created_at DESC
        ''')
        reviews_data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return render_template('reviews.html', reviews=reviews_data)
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
        flash('Error loading reviews. Please try again.', 'error')
        return render_template('reviews.html', reviews=[])

@app.route('/api/reviews')
def api_reviews():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, school_name, reviewer_name, rating, comment, created_at 
            FROM reviews 
            ORDER BY created_at DESC
        ''')
        reviews_data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({'reviews': reviews_data})
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': 'Database error'}), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    print("🚀 Starting School Review Manager")
    print("📊 Database ready")
    print("🌐 Visit: http://localhost:5000")
    print("➕ Add Review: http://localhost:5000/addreview")
    print("👁️ View Reviews: http://localhost:5000/reviews")
    print("🔗 API: http://localhost:5000/api/reviews")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
