# E-commerce Price Tracker

A full-stack web application that helps users track and compare product prices across e-commerce platforms.

## Features

- 🔐 User Authentication System
- 💰 Price Comparison Tool
- 📊 Price History Tracking
- 🎨 Modern UI with Tailwind CSS
- 🔒 Secure Backend API

## Tech Stack

### Frontend
- React.js
- Tailwind CSS
- Reusable UI Components

### Backend
- Python Flask
- SQLite Database
- JWT Authentication
- Web Scraping

## Project Structure

```
├── backend/
│   ├── app.py              # Main Flask application
│   ├── database.py         # Database management
│   ├── scraper.py          # Web scraping functionality
│   ├── config.py           # Configuration settings
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.js          # Main React component
│   │   └── index.js        # React entry point
│   └── package.json        # Node.js dependencies
```

## Installation

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Authentication
- POST `/api/register` - User registration
- POST `/api/login` - User login

### Price Operations
- POST `/api/compare` - Compare prices
- GET `/price-history` - Get price history
- POST `/search` - Search products

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
)
```

### Prices Table
```sql
CREATE TABLE prices (
    id INTEGER PRIMARY KEY,
    product_name TEXT,
    url TEXT,
    price REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

## Security Features

- Password hashing with bcrypt
- JWT-based authentication
- Protected API endpoints
- Input validation
- Error handling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

ihithisham n - ihthishamibrahim2003@gmail.com

Project Link: (https://github.com/ihthiibru/pricewise.git) 
