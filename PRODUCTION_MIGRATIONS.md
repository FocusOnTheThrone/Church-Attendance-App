# Production Database Migrations

## 🗄️ **Run Migrations on Vercel**

### **Method 1: Vercel CLI**
```bash
npx vercel env add MIGRATE_COMMAND --scope focusonthethrones-projects
# When prompted, enter: python manage.py migrate
```

### **Method 2: Vercel Dashboard**
1. **Project Settings** → **Environment Variables**
2. **Add new variable**:
   - **Name**: `MIGRATE_COMMAND`
   - **Value**: `python manage.py migrate`
3. **Redeploy** to apply migrations
4. **Remove variable** after migration completes

### **Method 3: SSH Access (Advanced)**
```bash
# Connect to Vercel and run migrations directly
npx vercel exec --scope focusonthethrones-projects
python manage.py migrate
```

---

## 🎯 **What Migrations Do:**
- Create database tables
- Set up relationships
- Initialize church management system
- Enable all Django features

---

## ✅ **After Migrations:**

### **Test These Features:**
1. **Admin Panel**: `/admin/`
2. **User Signup**: `/accounts/signup/`
3. **User Login**: `/accounts/login/`
4. **Member Management**: Add/edit members
5. **Attendance Recording**: Record with comments
6. **Fellowship Management**: Create fellowships
7. **Department Setup**: Manage departments

---

## 🚀 **Complete Setup Checklist:**

- [ ] Database migrations applied
- [ ] Admin panel accessible
- [ ] User authentication working
- [ ] Member management functional
- [ ] Attendance tracking working
- [ ] Mobile responsive confirmed
- [ ] HTTPS security verified

---

## 🎊 **When Complete:**

Your Church Attendance App will be fully functional with:
- **Production database** (PostgreSQL)
- **User management** (secure authentication)
- **Member tracking** (complete system)
- **Mobile access** (responsive design)
- **Global availability** (HTTPS enabled)
