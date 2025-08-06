# 🎯 SkillTrail

<div align="center">

**Your Personal Career Growth Companion**

*Track skills, visualize progress, and unlock your potential with advanced analytics*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4+-orange.svg)](https://sqlalchemy.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-4.6+-purple.svg)](https://getbootstrap.com)
[![Chart.js](https://img.shields.io/badge/Chart.js-3.0+-red.svg)](https://chartjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 🌟 Overview

SkillTrail is a comprehensive personal career growth tracking platform that empowers you to:
- **📊 Track Skills**: Monitor your learning journey across multiple skill categories
- **📈 Visualize Progress**: Beautiful charts and analytics powered by Chart.js
- **🎯 Set Goals**: Define target hours and track completion percentages
- **📋 Generate Reports**: Advanced analytics with pandas-powered insights
- **👑 Premium Features**: Unlock detailed reports and data export capabilities

## ✨ Features

### 🔓 **Free Tier**
- ✅ **Dashboard**: Clean, intuitive overview of your learning journey
- ✅ **Skill Management**: Add, edit, and organize skills by category
- ✅ **Progress Logging**: Daily progress tracking with hours and notes
- ✅ **Basic Charts**: Visual progress overview with Chart.js
- ✅ **User Authentication**: Secure login and registration system

### 👑 **Premium Features**
- 🚀 **Advanced Analytics**: Deep insights into your learning patterns
- 📊 **Learning Velocity Reports**: Track your productivity over time
- 🎯 **Goal Achievement Predictions**: AI-powered completion forecasts
- 📈 **Category Performance Analysis**: Compare progress across skill areas
- 💾 **Data Export**: Download your data in CSV format
- 🔍 **Personalized Recommendations**: Get tailored learning suggestions

## 🎨 Screenshots

### Dashboard
*Clean, modern interface showing your learning overview*

### Charts & Analytics
*Beautiful visualizations powered by Chart.js*
- **Skills Progress Overview** (Doughnut Chart)
- **Learning Trends** (Line Chart)
- **Category Breakdown** (Bar Chart)

### Premium Reports
*Advanced analytics and insights*
- Learning velocity analysis
- Productivity patterns
- Goal achievement tracking
- Personalized recommendations

## 🛠️ Tech Stack

### Backend
- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - Powerful ORM for database operations
- **Flask-Login** - User session management
- **Pandas** - Advanced data analysis and reporting
- **SQLite** - Lightweight database for development

### Frontend
- **Bootstrap 4** - Responsive UI framework
- **Chart.js** - Beautiful, interactive charts
- **FontAwesome** - Professional icons
- **Jinja2** - Template engine

### Development Tools
- **Python 3.8+** - Modern Python features
- **Git** - Version control
- **Virtual Environment** - Isolated dependencies

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Utshah-Neupane/SkillTrail.git
   cd SkillTrail
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python init_db.py
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
SkillTrail/
├── container/
│   ├── __init__.py          # App initialization
│   ├── models.py            # Database models
│   ├── routes.py            # Application routes
│   ├── forms.py             # WTForms definitions
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── charts.html
│   │   ├── reports.html
│   │   └── premium.html
│   └── static/              # CSS, JS, images
├── instance/
│   └── database.db          # SQLite database
├── requirements.txt         # Python dependencies
├── init_db.py              # Database initialization
├── run.py                  # Application entry point
└── README.md               # This file
```

## 💡 Usage Guide

### Getting Started
1. **Register** a new account or **login** to existing one
2. **Add your first skill** from the dashboard
3. **Set target hours** and choose a category
4. **Log daily progress** with hours spent and notes
5. **View charts** to visualize your learning journey

### Premium Access
1. Click the **"Reports"** link in navigation
2. You'll be redirected to the **Premium page**
3. Click **"Demo Upgrade (Free)"** for instant access
4. Enjoy advanced analytics and insights!

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/database.db
```

### Database Models
- **User**: Authentication and premium status
- **Skill**: Skill information and target hours
- **Progress**: Daily progress entries with hours and notes

## 📊 Data Analytics

SkillTrail uses **pandas** for advanced data analysis:

- **Learning Velocity**: Calculate average hours per day
- **Productivity Patterns**: Identify your most productive days
- **Category Performance**: Compare progress across skill areas
- **Goal Predictions**: Estimate completion dates
- **Trend Analysis**: Track learning patterns over time

## 🎯 Roadmap

### Upcoming Features
- [ ] **PDF Export**: Generate beautiful PDF reports
- [ ] **Mobile App**: React Native companion app
- [ ] **Team Features**: Share progress with mentors
- [ ] **Gamification**: Badges and achievement system
- [ ] **API Integration**: Connect with learning platforms
- [ ] **Advanced Charts**: More visualization options

### Technical Improvements
- [ ] **Docker Support**: Containerized deployment
- [ ] **PostgreSQL**: Production database support
- [ ] **Redis Caching**: Improved performance
- [ ] **Unit Tests**: Comprehensive test coverage
- [ ] **CI/CD Pipeline**: Automated deployment

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Utshah Neupane**
- GitHub: [@Utshah-Neupane](https://github.com/Utshah-Neupane)
- LinkedIn: [Your LinkedIn Profile](https://linkedin.com/in/your-profile)

## 🙏 Acknowledgments

- **Flask Community** for the amazing web framework
- **Chart.js** for beautiful data visualizations
- **Bootstrap** for responsive design components
- **SQLAlchemy** for powerful ORM capabilities
- **Pandas** for advanced data analysis features

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

*Built with ❤️ and Python*

</div>