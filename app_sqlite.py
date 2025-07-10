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

class DatabaseManager:
    """Database connection and operations manager for SQLite"""
    
    @staticmethod
    def get_connection():
        """Create and return database connection"""
        try:
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
            return conn
        except Exception as e:
            logger.error(f"Error connecting to SQLite: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None):
        """Execute a query and return results"""
        conn = None
        cursor = None
        try:
            conn = DatabaseManager.get_connection()
            if conn is None:
                logger.error("Failed to get database connection")
                return None
                
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            
            if query.strip().lower().startswith('select'):
                results = cursor.fetchall()
                # Convert sqlite3.Row objects to dictionaries
                return [dict(row) for row in results]
            else:
                conn.commit()
                affected_rows = cursor.rowcount
                logger.info(f"Query executed successfully, {affected_rows} rows affected")
                return affected_rows
                
        except Exception as e:
            logger.error(f"Database error: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

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
        query = """
        INSERT INTO reviews (school_name, reviewer_name, rating, comment) 
        VALUES (?, ?, ?, ?)
        """
        params = (school_name, reviewer_name, int(rating), comment)
        
        logger.info(f"Attempting to insert review: {params}")
        result = DatabaseManager.execute_query(query, params)
        
        if result is not None and result > 0:
            logger.info(f"Review inserted successfully, {result} rows affected")
            flash('Review submitted successfully!', 'success')
            return redirect(url_for('reviews'))
        else:
            logger.error(f"Failed to insert review. Result: {result}")
            flash('Error submitting review. Please try again.', 'error')
            return render_template('add_review.html')
    
    return render_template('add_review.html')

@app.route('/reviews')
def reviews():
    """Reviews page - display all reviews"""
    query = """
    SELECT id, school_name, reviewer_name, rating, comment, 
           datetime(created_at) as created_at
    FROM reviews 
    ORDER BY created_at DESC
    """
    
    reviews_data = DatabaseManager.execute_query(query)
    
    if reviews_data is None:
        flash('Error loading reviews. Please check database connection.', 'error')
        reviews_data = []
    
    # Convert created_at to proper format for template
    for review in reviews_data:
        if 'created_at' in review and review['created_at']:
            # Parse and format the datetime for display
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(review['created_at'])
                review['created_at'] = dt
            except:
                pass
    
    return render_template('reviews.html', reviews=reviews_data)

@app.route('/api/reviews')
def api_reviews():
    """API endpoint to get reviews as JSON"""
    query = """
    SELECT id, school_name, reviewer_name, rating, comment, 
           datetime(created_at) as created_at
    FROM reviews 
    ORDER BY created_at DESC
    """
    
    reviews_data = DatabaseManager.execute_query(query)
    
    if reviews_data is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    # Convert any datetime objects to strings for JSON serialization
    for review in reviews_data:
        if 'created_at' in review and review['created_at']:
            review['created_at'] = str(review['created_at'])
    
    return jsonify({'reviews': reviews_data})

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return f"<h1>404 - Page Not Found</h1><p>The page you're looking for doesn't exist.</p>", 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return f"<h1>500 - Internal Server Error</h1><p>Something went wrong on our end.</p>", 500

if __name__ == '__main__':
    # Check if database exists, if not create it
    if not DB_PATH.exists():
        print("Database not found. Please run 'python setup_sqlite.py' first.")
        print("Creating database automatically...")
        import subprocess
        subprocess.run(['python', 'setup_sqlite.py'])
    
    app.run(debug=True, host='0.0.0.0', port=5000)
