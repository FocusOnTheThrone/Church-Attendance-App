# Vercel Environment Variables Setup

## 🚀 **Required Environment Variables for Vercel**

### **🔐 Security Variables**
```bash
SECRET_KEY=your-unique-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.vercel.app,www.your-domain.vercel.app
```

### **🗄️ Database Variables**
```bash
# Get this from Vercel PostgreSQL dashboard
DATABASE_URL=postgresql://username:password@host:port/database
```

### **🔧 Django Settings**
```bash
DJANGO_SETTINGS_MODULE=config.settings
VERCEL=true
```

### **🛡️ Production Security**
```bash
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
```

---

## 📋 **How to Set Up Vercel Environment Variables:**

### **Method 1: Vercel Dashboard**
1. Go to [vercel.com](https://vercel.com)
2. Select your project
3. Go to Settings → Environment Variables
4. Add each variable from above

### **Method 2: Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Set environment variables
vercel env add SECRET_KEY
vercel env add DATABASE_URL
vercel env add DEBUG
vercel env add ALLOWED_HOSTS
```

---

## 🔑 **Generate New SECRET_KEY**

### **Create Production Secret Key:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### **Or Use Online Generator:**
- Go to: https://djecrety.ir/
- Generate a new Django secret key
- Use this for your SECRET_KEY

---

## 🗄️ **Vercel PostgreSQL Setup**

### **Create Database:**
1. Vercel Dashboard → Storage → PostgreSQL
2. Click "Create Database"
3. Choose region (closest to your users)
4. Wait for creation

### **Get Connection String:**
1. Click on your database
2. Go to ".env.local" tab
3. Copy the DATABASE_URL
4. Add to Vercel environment variables

---

## 🌐 **Domain Configuration**

### **After Deployment:**
1. Your app will be available at: `your-project-name.vercel.app`
2. Add this to ALLOWED_HOSTS environment variable
3. Optionally add custom domain in Vercel settings

---

## ✅ **Pre-Deployment Checklist**

### **Before Deploying:**
- [ ] SECRET_KEY generated and added to Vercel
- [ ] DATABASE_URL obtained from Vercel PostgreSQL
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS set to your Vercel domain
- [ ] All migrations applied locally
- [ ] Static files collected

### **After Deploying:**
- [ ] Test homepage loads
- [ ] Test login/logout
- [ ] Test database operations
- [ ] Check static files are loading
- [ ] Verify HTTPS is working

---

## 🚨 **Troubleshooting**

### **Common Issues:**
1. **500 Error**: Check environment variables
2. **Static Files Not Loading**: Check STATIC_ROOT configuration
3. **Database Error**: Verify DATABASE_URL format
4. **CSRF Error**: Check CSRF_COOKIE_SECURE setting

### **Debug Commands:**
```bash
# Check Vercel logs
vercel logs

# Redeploy with latest changes
vercel --prod
```

---

## 📞 **Support**

### **If You Need Help:**
- Check Vercel documentation: https://vercel.com/docs
- Django deployment guide: https://vercel.com/guides/deploying-django
- Review your deployment logs in Vercel dashboard

---

**Save this file and reference it during Vercel setup!**
