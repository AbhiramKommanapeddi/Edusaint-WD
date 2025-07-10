from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret-key-123'

def get_db():
    conn = sqlite3.connect('reviews.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists('reviews.db'):
        conn = get_db()
        conn.execute('''CREATE TABLE reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            school_name TEXT NOT NULL,
            reviewer_name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Add sample data
        conn.execute('INSERT INTO reviews (school_name, reviewer_name, rating, comment) VALUES (?, ?, ?, ?)',
                    ('ABC School', 'John Doe', 5, 'Great school'))
        conn.execute('INSERT INTO reviews (school_name, reviewer_name, rating, comment) VALUES (?, ?, ?, ?)',
                    ('XYZ Academy', 'Jane Smith', 4, 'Good education'))
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return redirect(url_for('reviews'))

@app.route('/addreview', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        school_name = request.form['school_name']
        reviewer_name = request.form['reviewer_name']
        rating = int(request.form['rating'])
        comment = request.form['comment']
        
        conn = get_db()
        conn.execute('INSERT INTO reviews (school_name, reviewer_name, rating, comment) VALUES (?, ?, ?, ?)',
                    (school_name, reviewer_name, rating, comment))
        conn.commit()
        conn.close()
        
        flash('Review added successfully!', 'success')
        return redirect(url_for('reviews'))
    
    return render_template('add_review.html')

@app.route('/reviews')
def reviews():
    conn = get_db()
    reviews = conn.execute('SELECT * FROM reviews ORDER BY created_at DESC').fetchall()
    conn.close()
    
    # Format the reviews for better display
    formatted_reviews = []
    for review in reviews:
        review_dict = dict(review)
        # Format the date if it exists
        if review_dict['created_at']:
            try:
                # Try to parse and format the date
                dt = datetime.strptime(review_dict['created_at'], '%Y-%m-%d %H:%M:%S')
                review_dict['formatted_date'] = dt.strftime('%B %d, %Y')
                review_dict['formatted_date_short'] = dt.strftime('%m/%d/%Y')
            except:
                review_dict['formatted_date'] = review_dict['created_at']
                review_dict['formatted_date_short'] = review_dict['created_at']
        else:
            review_dict['formatted_date'] = 'Unknown date'
            review_dict['formatted_date_short'] = 'N/A'
        formatted_reviews.append(review_dict)
    
    return render_template('reviews.html', reviews=formatted_reviews)

@app.route('/api/reviews')
def api_reviews():
    conn = get_db()
    reviews = conn.execute('SELECT * FROM reviews ORDER BY created_at DESC').fetchall()
    conn.close()
    reviews_list = [dict(row) for row in reviews]
    return jsonify({'reviews': reviews_list})

if __name__ == '__main__':
    init_db()
    print("🚀 Simple Flask App Starting")
    print("Visit: http://localhost:5000")
    app.run(debug=True, port=5000)
