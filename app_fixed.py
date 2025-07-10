#!/usr/bin/env python3
"""
School Review Manager - Ultra-Reliable Version
Fixed all database connection issues
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
import logging
from contextlib import contextmanager
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'school-review-manager-2025'

# Database configuration
DATABASE = 'reviews.db'
db_lock = threading.Lock()

@contextmanager
def get_db_connection():
    """Context manager for database connections with proper error handling"""
    conn = None
    try:
        with db_lock:
            conn = sqlite3.connect(DATABASE, timeout=30.0)
            conn.row_factory = sqlite3.Row
            conn.execute('PRAGMA journal_mode=WAL')  # Enable WAL mode for better concurrency
            yield conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        if conn:
            conn.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def init_database():
    """Initialize database with proper error handling"""
    try:
        with get_db_connection() as conn:
            # Create table if it doesn't exist
            conn.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    school_name TEXT NOT NULL,
                    reviewer_name TEXT NOT NULL,
                    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                    comment TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Check if we have any data
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM reviews')
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insert sample data
                sample_data = [
                    ('ABC International School', 'John Doe', 5, 'Excellent school with great faculty and infrastructure. My child loves going to school every day.'),
                    ('Springfield Elementary', 'Jane Smith', 4, 'Good academic programs but could improve extracurricular activities.'),
                    ('Green Valley High School', 'Mike Johnson', 3, 'Average school with decent facilities. Teachers are supportive but need more resources.'),
                    ('Riverside Academy', 'Sarah Wilson', 5, 'Outstanding school with dedicated teachers and excellent facilities. Highly recommended!'),
                    ('Sunset Middle School', 'David Brown', 4, 'Good school with strong academic programs. Could use more sports facilities.')
                ]
                
                conn.executemany('''
                    INSERT INTO reviews (school_name, reviewer_name, rating, comment) 
                    VALUES (?, ?, ?, ?)
                ''', sample_data)
                logger.info("Sample data inserted")
            
            conn.commit()
            logger.info(f"Database initialized with {count if count > 0 else len(sample_data)} reviews")
            
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise

@app.route('/')
def index():
    """Home page - redirect to reviews"""
    return redirect(url_for('reviews'))

@app.route('/addreview', methods=['GET', 'POST'])
def add_review():
    """Add review page"""
    if request.method == 'POST':
        # Get and validate form data
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
            with get_db_connection() as conn:
                conn.execute('''
                    INSERT INTO reviews (school_name, reviewer_name, rating, comment) 
                    VALUES (?, ?, ?, ?)
                ''', (school_name, reviewer_name, int(rating), comment))
                conn.commit()
                
            flash('Review submitted successfully!', 'success')
            logger.info(f"Review added: {school_name} by {reviewer_name}")
            return redirect(url_for('reviews'))
            
        except Exception as e:
            logger.error(f"Error adding review: {e}")
            flash('Error submitting review. Please try again.', 'error')
            return render_template('add_review.html')
    
    return render_template('add_review.html')

@app.route('/reviews')
def reviews():
    """Display all reviews"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, school_name, reviewer_name, rating, comment, created_at 
                FROM reviews 
                ORDER BY created_at DESC
            ''')
            reviews_data = [dict(row) for row in cursor.fetchall()]
            
        logger.info(f"Loaded {len(reviews_data)} reviews")
        return render_template('reviews.html', reviews=reviews_data)
        
    except Exception as e:
        logger.error(f"Error loading reviews: {e}")
        flash('Error loading reviews. Please try again.', 'error')
        return render_template('reviews.html', reviews=[])

@app.route('/api/reviews')
def api_reviews():
    """API endpoint for reviews"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, school_name, reviewer_name, rating, comment, created_at 
                FROM reviews 
                ORDER BY created_at DESC
            ''')
            reviews_data = [dict(row) for row in cursor.fetchall()]
            
        return jsonify({'reviews': reviews_data, 'count': len(reviews_data)})
        
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': 'Database error', 'message': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM reviews')
            count = cursor.fetchone()[0]
            
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'reviews_count': count,
            'timestamp': time.time()
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'database': 'disconnected',
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html') if os.path.exists('templates/404.html') else "Page not found", 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return render_template('500.html') if os.path.exists('templates/500.html') else "Internal server error", 500

if __name__ == '__main__':
    try:
        # Initialize database
        init_database()
        
        print("🚀 School Review Manager - Ultra-Reliable Edition")
        print("=" * 50)
        print("✅ Database initialized successfully")
        print("🌐 Application running at: http://localhost:5000")
        print("➕ Add Review: http://localhost:5000/addreview")
        print("👁️  View Reviews: http://localhost:5000/reviews")
        print("🔗 API: http://localhost:5000/api/reviews")
        print("❤️  Health Check: http://localhost:5000/health")
        print("=" * 50)
        
        # Run the app
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        print(f"❌ Error starting application: {e}")
        print("Please check the database file and try again.")
