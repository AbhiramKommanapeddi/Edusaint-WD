# School Review Manager 🏫⭐

A modern Flask web application for managing school reviews with MySQL database integration. Built as part of the Edusaint Web Development Internship assignment.

## 🌟 Features

- **Add Reviews**: Interactive form with star rating system
- **View Reviews**: Toggle between card and table views
- **Modern UI**: Responsive design with Bootstrap 5
- **Database Integration**: MySQL with proper security measures
- **Form Validation**: Client-side and server-side validation
- **Flash Messages**: User feedback for all operations
- **Statistics**: Review analytics and insights

## 🛠️ Tech Stack

- **Backend**: Flask (Python 3.8+)
- **Database**: MySQL with mysql-connector-python
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Template Engine**: Jinja2
- **Environment**: python-dotenv for configuration

## 📁 Project Structure

```
school_review_app/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── reviews.sql          # Database schema and sample data
├── .env.example         # Environment variables template
├── README.md           # Project documentation
├── templates/
│   ├── add_review.html # Add review form
│   └── reviews.html    # Display reviews
└── static/
    └── css/
        └── style.css   # Custom styles
```

## 🚀 Quick Setup

### 1. Prerequisites

- Python 3.8 or higher
- MySQL Server
- Git (optional)

### 2. Installation

1. **Clone or download the project**

   ```bash
   git clone <repository-url>
   cd school_review_app
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**

   ```bash
   # Log into MySQL
   mysql -u root -p

   # Run the SQL script
   source reviews.sql
   # OR manually execute the SQL commands from reviews.sql
   ```

5. **Environment Configuration**

   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env with your database credentials
   # Update DB_PASSWORD with your MySQL password
   ```

6. **Run the application**

   ```bash
   python app.py
   ```

   Visit `http://localhost:5000` in your browser

## 🔧 Configuration

### Environment Variables (.env)

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=school_reviews
DB_PORT=3306
```

### Database Schema

```sql
CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR(100) NOT NULL,
    reviewer_name VARCHAR(100) NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📱 API Endpoints

| Method | Endpoint       | Description              |
| ------ | -------------- | ------------------------ |
| GET    | `/`            | Redirect to reviews page |
| GET    | `/addreview`   | Display add review form  |
| POST   | `/addreview`   | Submit new review        |
| GET    | `/reviews`     | Display all reviews      |
| GET    | `/api/reviews` | Get reviews as JSON      |

## 🎨 Features Showcase

### Interactive Star Rating

- Click to select rating from 1 to 5 stars
- Visual feedback with hover effects
- Required field validation

### Dual View Modes

- **Card View**: Beautiful card layout for better readability
- **Table View**: Compact table format for quick scanning
- **View Preference**: Remembers your choice in localStorage

### Responsive Design

- Mobile-friendly interface
- Bootstrap 5 components
- Modern gradient backgrounds
- Smooth animations and transitions

### Form Validation

- Client-side HTML5 validation
- Server-side Python validation
- User-friendly error messages
- Required field indicators

## 🔒 Security Features

- Parameterized SQL queries (prevents SQL injection)
- Environment variable configuration
- Jinja2 auto-escaping (prevents XSS)
- Input validation and sanitization
- Error handling for database operations

## 🧪 Testing

### Manual Testing Checklist

1. **Add Review Form**

   - [ ] All fields required validation
   - [ ] Star rating functionality
   - [ ] Form submission and redirect
   - [ ] Success/error flash messages

2. **Reviews Display**

   - [ ] Card/table view toggle
   - [ ] Star rating display
   - [ ] Responsive design
   - [ ] Statistics accuracy

3. **Database Operations**
   - [ ] Data persistence
   - [ ] Error handling
   - [ ] Connection management

### Sample Test Data

The application includes sample reviews for testing:

- ABC International School (5 stars)
- Springfield Elementary (4 stars)
- Green Valley High School (3 stars)

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**

   ```
   Error: mysql.connector.errors.ProgrammingError: 1045 (28000): Access denied
   ```

   **Solution**: Check your MySQL credentials in `.env` file

2. **Module Not Found Error**

   ```
   ModuleNotFoundError: No module named 'flask'
   ```

   **Solution**: Activate virtual environment and install requirements

3. **Template Not Found**
   ```
   jinja2.exceptions.TemplateNotFound
   ```
   **Solution**: Ensure templates directory structure is correct

### Database Setup Issues

If you encounter database issues:

1. **Check MySQL Service**

   ```bash
   # Windows
   net start mysql

   # Linux/Mac
   sudo systemctl start mysql
   ```

2. **Verify Database Exists**

   ```sql
   SHOW DATABASES;
   USE school_reviews;
   SHOW TABLES;
   ```

3. **Reset Database**
   ```sql
   DROP DATABASE IF EXISTS school_reviews;
   source reviews.sql
   ```

## 📊 Performance Considerations

- Database connection pooling
- Prepared statements for security
- Responsive image loading
- Minified CSS/JS for production
- Caching strategies for static assets

## 🔄 Future Enhancements

- [ ] User authentication system
- [ ] Review editing and deletion
- [ ] Image upload for schools
- [ ] Advanced search and filtering
- [ ] Email notifications
- [ ] API rate limiting
- [ ] Admin dashboard
- [ ] Review moderation
- [ ] School verification system

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is created for educational purposes as part of the Edusaint Web Development Internship assignment.

## 📞 Support

For support or questions about this project:

- Create an issue in the repository
- Contact the development team
- Review the troubleshooting section

## 🎯 Assignment Requirements

This project fulfills all requirements for the Edusaint Web Development Internship:

- ✅ Flask web application
- ✅ MySQL database integration
- ✅ Add review form with validation
- ✅ Display reviews in table format
- ✅ Bootstrap responsive design
- ✅ Environment variable configuration
- ✅ Clean code structure
- ✅ SQL schema file included
- ✅ Complete documentation

---

**Built with ❤️ for Edusaint Web Development Internship**
