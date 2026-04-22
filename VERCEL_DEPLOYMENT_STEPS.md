# Vercel Deployment Steps

## 🚀 **Ready to Deploy to Vercel!**

### **✅ Current Status:**
- ✅ **Vercel CLI Installed** (version 51.8.0)
- ✅ **Logged into Vercel** successfully
- ✅ **Project ready** for deployment
- ✅ **GitHub repository** available at: https://github.com/FocusOnTheThrone/Church-Attendance-App

---

## 📋 **Step-by-Step Deployment:**

### **Step 1: Start Deployment**
```bash
npx vercel --prod
```

### **Step 2: Answer Vercel Questions**
When you run the command, Vercel will ask:

#### **Question 1: Set up and deploy "Church-Attendance-App"?**
- **Answer**: `Yes` (or press Enter)

#### **Question 2: Which scope do you want to deploy to?**
- **Answer**: Choose your Vercel account (usually option 1)

#### **Question 3: Link to existing project?**
- **Answer**: `No` (since this is first deployment)

#### **Question 4: What's your project's name?**
- **Answer**: `church-attendance-app` (or your preferred name)

#### **Question 5: In which directory is your code located?**
- **Answer**: `./` (current directory)

#### **Question 6: Want to override the settings?**
- **Answer**: `No` (use default settings)

---

## 🔧 **Environment Variables Setup**

### **After Initial Deployment, Set These Environment Variables:**

#### **Method 1: Vercel Dashboard**
1. Go to your Vercel project dashboard
2. Go to **Settings** → **Environment Variables**
3. Add these variables:

```bash
# Required Variables:
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.vercel.app,www.your-domain.vercel.app
DATABASE_URL=postgresql://user:password@host:port/database
DJANGO_SETTINGS_MODULE=config.settings
VERCEL=true

# Security Variables:
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
```

#### **Method 2: Vercel CLI**
```bash
npx vercel env add SECRET_KEY
npx vercel env add DEBUG
npx vercel env add ALLOWED_HOSTS
npx vercel env add DATABASE_URL
npx vercel env add DJANGO_SETTINGS_MODULE
npx vercel env add VERCEL
```

---

## 🗄️ **Database Setup**

### **Option 1: Vercel PostgreSQL (Recommended)**
1. **In Vercel Dashboard**:
   - Go to **Storage** → **Create Database**
   - Choose **PostgreSQL**
   - Select region (closest to your users)
   - Click **Create Database**

2. **Get Connection String**:
   - Click on your database
   - Go to **.env.local** tab
   - Copy the `DATABASE_URL`

3. **Add to Environment Variables**:
   - Add the copied `DATABASE_URL` to your project

### **Option 2: External PostgreSQL**
- Use your existing PostgreSQL database
- Add connection string as `DATABASE_URL`

---

## 🔑 **Generate SECRET_KEY**

### **Create Production Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **Add to Environment Variables:**
- Copy the generated key
- Add as `SECRET_KEY` in Vercel dashboard

---

## 🚀 **Complete Deployment Commands**

### **Full Deployment Process:**
```bash
# 1. Deploy to Vercel (first time)
npx vercel --prod

# 2. Set environment variables (in Vercel dashboard)
# Add all variables listed above

# 3. Set up database (Vercel PostgreSQL recommended)
# Get DATABASE_URL and add to environment variables

# 4. Redeploy with environment variables
npx vercel --prod
```

---

## 🌐 **After Deployment**

### **Your App Will Be Available At:**
- **Primary URL**: `https://church-attendance-app.vercel.app`
- **Custom domain**: Configure in Vercel settings if needed

### **Test Your Live App:**
1. **Homepage**: Should load correctly
2. **Login/Signup**: Test user authentication
3. **Admin Panel**: `/admin/` should work
4. **Member Management**: Add/edit members
5. **Attendance**: Record attendance with comments
6. **Mobile**: Test on mobile devices

---

## 🔍 **Troubleshooting**

### **Common Issues & Solutions:**

#### **500 Server Error:**
- **Cause**: Missing environment variables
- **Fix**: Add all required environment variables
- **Check**: Vercel deployment logs

#### **Static Files Not Loading:**
- **Cause**: Static files configuration
- **Fix**: Check `STATIC_ROOT` settings
- **Solution**: Files should be in `/tmp/static` on Vercel

#### **Database Connection Error:**
- **Cause**: Wrong `DATABASE_URL`
- **Fix**: Verify PostgreSQL connection string
- **Check**: Database is running and accessible

#### **CSRF Token Error:**
- **Cause**: Security settings
- **Fix**: Ensure `CSRF_COOKIE_SECURE=True` on production
- **Check**: Domain matches `ALLOWED_HOSTS`

---

## 📊 **Deployment Checklist**

### **Before Deploying:**
- [ ] All migrations applied locally
- [ ] Static files collected
- [ ] Environment variables documented
- [ ] SECRET_KEY generated

### **After Deploying:**
- [ ] Environment variables set in Vercel
- [ ] Database connected
- [ ] Homepage loads correctly
- [ ] Authentication works
- [ ] All features functional
- [ ] Mobile responsive

---

## 🎯 **Quick Start Commands**

### **One-Line Deployment:**
```bash
npx vercel --prod
```

### **Check Deployment Status:**
```bash
npx vercel ls
```

### **View Deployment Logs:**
```bash
npx vercel logs
```

---

## 🌟 **Success Indicators**

### **When Deployment is Successful:**
- ✅ **Build completes** without errors
- ✅ **Deployment URL** is provided
- ✅ **App loads** in browser
- ✅ **All features** work correctly
- ✅ **HTTPS** is enabled automatically

---

## 📞 **Need Help?**

### **Useful Links:**
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Your Project**: Will appear in dashboard after first deployment
- **Vercel Docs**: https://vercel.com/docs
- **Django on Vercel**: https://vercel.com/guides/deploying-django

---

## 🎉 **Ready to Deploy!**

**Your Church Attendance App is fully prepared for Vercel deployment!**

**Just run `npx vercel --prod` and follow the prompts!** 🚀

**After deployment, set up your environment variables and database, then your app will be live!**
