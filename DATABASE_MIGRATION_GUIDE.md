# Database Migration Guide: SQLite to PostgreSQL

## 🎯 **Migration Progress: Step 2 of 5**

### ✅ **Completed So Far:**
1. **Dependencies Added** - Production database packages added to requirements.txt
2. **Settings Updated** - Database configuration now supports both SQLite and PostgreSQL
3. **Environment Ready** - .env file prepared for production database URL

### 📦 **New Dependencies Added:**
```
dj-database-url==2.1.0    # Parse DATABASE_URL environment variable
whitenoise==6.6.0          # Serve static files in production
gunicorn==21.2.0            # Production web server
```

### 🔧 **Settings.py Changes:**
```python
# Added database URL parsing
import dj_database_url

# Conditional database configuration
if os.getenv('DATABASE_URL'):
    # Production (PostgreSQL)
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }
else:
    # Development (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

## 🚀 **Next Steps for Vercel Deployment:**

### **Step 3: Create Database Migration Script**
```bash
# Create migrations for production
python manage.py makemigrations

# Apply migrations to production database
python manage.py migrate
```

### **Step 4: Set Up Vercel PostgreSQL**
1. Go to Vercel Dashboard
2. Create new PostgreSQL database
3. Get connection string (DATABASE_URL)
4. Add to Vercel environment variables

### **Step 5: Environment Variables for Vercel**
```bash
# Required Vercel Environment Variables:
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.vercel.app
DATABASE_URL=postgresql://user:pass@host:port/db
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
```

## 🔄 **Testing Database Migration:**

### **Development (Current):**
- Uses SQLite (`db.sqlite3`)
- Works with `python manage.py runserver`
- No DATABASE_URL environment variable needed

### **Production (Vercel):**
- Uses PostgreSQL (via DATABASE_URL)
- Works with Vercel deployment
- Automatic database switching based on environment

## 📋 **Migration Commands:**

### **Before Deployment:**
```bash
# 1. Create all migrations
python manage.py makemigrations

# 2. Test migrations locally
python manage.py migrate

# 3. Create superuser for production
python manage.py createsuperuser
```

### **For Vercel Deployment:**
```bash
# 1. Install new dependencies
pip install -r requirements.txt

# 2. Test with PostgreSQL locally (optional)
# Set DATABASE_URL environment variable and test
```

## 🎯 **Current Status:**

| Component | Status | Progress |
|-----------|--------|----------|
| Dependencies | ✅ Complete | 100% |
| Settings Update | ✅ Complete | 100% |
| Environment Config | ✅ Complete | 100% |
| Database Migration | 🟡 Ready | 0% |
| Vercel Setup | ❌ Not Started | 0% |

**Database Migration Configuration: 75% Complete**

## 🔍 **How It Works:**

### **Development Mode:**
- No `DATABASE_URL` environment variable
- Uses SQLite automatically
- Perfect for local development

### **Production Mode:**
- `DATABASE_URL` environment variable set
- Uses PostgreSQL automatically
- Ready for Vercel deployment

### **Automatic Switching:**
```python
if os.getenv('DATABASE_URL'):
    # Production database
else:
    # Development database
```

## 🚀 **Ready for Next Step:**

Your database configuration is now ready for Vercel! The next steps are:

1. **Test locally** with the new configuration
2. **Set up Vercel PostgreSQL** database
3. **Configure Vercel environment variables**
4. **Deploy to Vercel**

**Would you like me to help you test the database configuration locally, or proceed with Vercel setup?**
