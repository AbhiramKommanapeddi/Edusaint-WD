from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import logging
from pathlib import Path
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Database path
DB_PATH = Path("reviews.db")

def get_db_connection():
    """Get database connection"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    """Home page - redirect to reviews"""
    return redirect(url_for('reviews'))

@app.route('/addreview', methods=['GET', 'POST'])
def add_review():
    """Add review page - form to submit new reviews"""
    if request.method == 'POST':
        # Get form data
        school_name = request.form.get('school_name', '').strip()
        reviewer_name = request.form.get('reviewer_name', '').strip()
        rating = request.form.get('rating')
        comment = request.form.get('comment', '').strip()
        
        # Server-side validation
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
        
        # Insert review into database
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO reviews (school_name, reviewer_name, rating, comment) 
                    VALUES (?, ?, ?, ?)
                ''', (school_name, reviewer_name, int(rating), comment))
                conn.commit()
                flash('Review submitted successfully!', 'success')
                return redirect(url_for('reviews'))
            except Exception as e:
                logger.error(f"Error inserting review: {e}")
                flash('Error submitting review. Please try again.', 'error')
            finally:
                conn.close()
        else:
            flash('Database connection failed. Please try again.', 'error')
    
    return render_template('add_review.html')

@app.route('/reviews')
def reviews():
    """Reviews page - display all reviews"""
    conn = get_db_connection()
    reviews_data = []
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, school_name, reviewer_name, rating, comment, created_at 
                FROM reviews 
                ORDER BY created_at DESC
            ''')
            rows = cursor.fetchall()
            reviews_data = [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error fetching reviews: {e}")
            flash('Error loading reviews. Please try again.', 'error')
        finally:
            conn.close()
    else:
        flash('Database connection failed.', 'error')
    
    return render_template('reviews.html', reviews=reviews_data)

@app.route('/api/reviews')
def api_reviews():
    """API endpoint to get reviews as JSON"""
    conn = get_db_connection()
    
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, school_name, reviewer_name, rating, comment, created_at 
            FROM reviews 
            ORDER BY created_at DESC
        ''')
        rows = cursor.fetchall()
        reviews_data = [dict(row) for row in rows]
        return jsonify({'reviews': reviews_data})
    except Exception as e:
        logger.error(f"Error in API: {e}")
        return jsonify({'error': 'Database query failed'}), 500
    finally:
        conn.close()

@app.errorhandler(404)
def not_found(error):
    return f"<h1>404 - Page Not Found</h1><p>The page you're looking for doesn't exist.</p>", 404

@app.errorhandler(500)
def internal_error(error):
    return f"<h1>500 - Internal Server Error</h1><p>Something went wrong on our end.</p>", 500

if __name__ == '__main__':
    # Check if database exists
    if not DB_PATH.exists():
        print("Database not found. Please run 'python setup_sqlite.py' first.")
        import subprocess
        subprocess.run(['python', 'setup_sqlite.py'])
    
    app.run(debug=True, host='0.0.0.0', port=5000)
