# Vercel Environment Variables Setup

## 🗄️ **Required Environment Variables**

### **Database Connection:**
```
DATABASE_URL=postgresql://username:password@host:port/database_name
```
*(Copy this from your Vercel database .env.local tab)*

### **Django Settings:**
```
DJANGO_SETTINGS_MODULE=config.settings
VERCEL=true
```

### **Security Settings:**
```
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=church-attendance-qsn45una2-focusonthethrones-p.vercel.app,www.church-attendance-qsn45una2-focusonthethrones-p.vercel.app
```

### **Production Security:**
```
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
```

---

## 🔑 **Generate SECRET_KEY:**

### **Run This Command:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **Example Output:**
```
django-insecure-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

---

## 📋 **Setup Order:**

### **1. Database First:**
- Create PostgreSQL database
- Copy DATABASE_URL
- Add to environment variables

### **2. Django Settings:**
- Add DJANGO_SETTINGS_MODULE
- Add VERCEL=true

### **3. Security Settings:**
- Generate SECRET_KEY
- Add DEBUG=False
- Add ALLOWED_HOSTS

### **4. Production Security:**
- Add SESSION_COOKIE_SECURE=True
- Add CSRF_COOKIE_SECURE=True
- Add SECURE_SSL_REDIRECT=True

---

## 🚀 **After Setup:**

### **Redeploy Your App:**
```bash
npx vercel --prod --scope focusonthethrones-projects
```

### **Test Your Live App:**
Visit: https://church-attendance-qsn45una2-focusonthethrones-p.vercel.app

---

## ✅ **Success Indicators:**

- ✅ Database connects without errors
- ✅ Django admin panel loads (/admin/)
- ✅ User signup/login works
- ✅ All pages load correctly
- ✅ HTTPS security active
