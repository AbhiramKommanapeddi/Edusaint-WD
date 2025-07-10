from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

class DatabaseManager:
    """Database connection and operations manager"""
    
    @staticmethod
    def get_connection():
        """Create and return database connection"""
        try:
            connection = mysql.connector.connect(**Config.DB_CONFIG)
            return connection
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None):
        """Execute a query and return results"""
        connection = None
        cursor = None
        try:
            connection = DatabaseManager.get_connection()
            if connection is None:
                return None
                
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().lower().startswith('select'):
                results = cursor.fetchall()
                return results
            else:
                connection.commit()
                return cursor.rowcount
                
        except Error as e:
            logger.error(f"Database error: {e}")
            if connection:
                connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

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
        VALUES (%s, %s, %s, %s)
        """
        params = (school_name, reviewer_name, int(rating), comment)
        
        result = DatabaseManager.execute_query(query, params)
        
        if result is not None:
            flash('Review submitted successfully!', 'success')
            return redirect(url_for('reviews'))
        else:
            flash('Error submitting review. Please try again.', 'error')
            return render_template('add_review.html')
    
    return render_template('add_review.html')

@app.route('/reviews')
def reviews():
    """Reviews page - display all reviews"""
    query = """
    SELECT id, school_name, reviewer_name, rating, comment, created_at 
    FROM reviews 
    ORDER BY created_at DESC
    """
    
    reviews_data = DatabaseManager.execute_query(query)
    
    if reviews_data is None:
        flash('Error loading reviews. Please check database connection.', 'error')
        reviews_data = []
    
    return render_template('reviews.html', reviews=reviews_data)

@app.route('/api/reviews')
def api_reviews():
    """API endpoint to get reviews as JSON"""
    query = """
    SELECT id, school_name, reviewer_name, rating, comment, created_at 
    FROM reviews 
    ORDER BY created_at DESC
    """
    
    reviews_data = DatabaseManager.execute_query(query)
    
    if reviews_data is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    return jsonify({'reviews': reviews_data})

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)