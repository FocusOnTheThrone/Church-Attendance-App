# GitHub Secrets Setup for Vercel Deployment

## 🔐 **Required GitHub Secrets**

### **Step 1: Get Vercel Credentials**

#### **1. Get Vercel Token:**
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Get your token
vercel token create
```

#### **2. Get Vercel Organization ID:**
```bash
# List your organizations
vercel teams list

# Copy the organization ID for focusonthethrones-projects
```

#### **3. Get Vercel Project ID:**
```bash
# Go to your project directory
cd "f:\Cursor AI\Church Attendance App"

# Get project ID
vercel link
# Or check Vercel dashboard: https://vercel.com/focusonthethrones-projects/church-attendance-app/settings
```

### **Step 2: Add Secrets to GitHub**

#### **Go to GitHub Repository:**
1. **URL**: https://github.com/FocusOnTheThrone/Church-Attendance-App
2. **Click**: Settings tab
3. **Click**: Secrets and variables → Actions
4. **Click**: New repository secret

#### **Add These Secrets:**

| Secret Name | Value |
|-------------|-------|
| `VERCEL_TOKEN` | Your Vercel token from step 1 |
| `VERCEL_ORG_ID` | Your Vercel organization ID |
| `VERCEL_PROJECT_ID` | Your Vercel project ID |
| `SECRET_KEY` | `v6kldjv10@8b_xwku!v0alu-0s8cv0$)orat_!li=l(7v-56ut` |
| `DATABASE_URL` | Your PostgreSQL connection string |

### **Step 3: Update Vercel Environment Variables**

#### **In Vercel Dashboard:**
1. **Go to**: https://vercel.com/focusonthethrones-projects/church-attendance-app/settings/environment-variables
2. **Add these variables**:
   ```
   SECRET_KEY=v6kldjv10@8b_xwku!v0alu-0s8cv0$)orat_!li=l(7v-56ut
   DEBUG=False
   ALLOWED_HOSTS=church-attendance-okt4hm0q6-focusonthethrones-projects.vercel.app,www.church-attendance-okt4hm0q6-focusonthethrones-projects.vercel.app,church-attendance-app-navy.vercel.app,www.church-attendance-app-navy.vercel.app
   DATABASE_URL=your-postgresql-connection-string
   DJANGO_SETTINGS_MODULE=github_production
   VERCEL=true
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   SECURE_SSL_REDIRECT=True
   ```

### **Step 4: Test GitHub Actions Deployment**

#### **Trigger Deployment:**
1. **Push any changes** to main branch
2. **Go to**: Actions tab in GitHub
3. **Monitor** the deployment workflow
4. **Check logs** for any errors

#### **Expected Workflow Steps:**
- ✅ Checkout code
- ✅ Set up Python
- ✅ Install dependencies
- ✅ Run Django checks
- ✅ Collect static files
- ✅ Run migrations
- ✅ Deploy to Vercel

## 🎯 **Benefits of GitHub Actions:**

### **✅ Advantages:**
- **Automated deployments** on every push
- **CI/CD pipeline** with testing
- **Version control** integration
- **Rollback capabilities**
- **Environment-specific** configurations
- **Better logging** and monitoring

### **🚀 **After Setup:**
- **Push to main** → Automatic deployment
- **Pull requests** → Preview deployments
- **Failed builds** → No deployment
- **Successful builds** → Live deployment

## 📋 **Troubleshooting:**

### **Common Issues:**
- **Missing secrets** → Add all required secrets
- **Wrong Vercel credentials** → Verify token and IDs
- **Environment variables** → Check Vercel dashboard
- **Django errors** → Check workflow logs

### **Debug Steps:**
1. **Check GitHub Actions logs**
2. **Verify all secrets are set**
3. **Check Vercel environment variables**
4. **Test locally** with same settings
