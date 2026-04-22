# Create Superuser for Admin Access

## 🔑 **Create Admin Account**

### **Method 1: Vercel CLI**
```bash
npx vercel env add CREATE_SUPERUSER --scope focusonthethrones-projects
# When prompted, enter:
python manage.py createsuperuser --username admin --email admin@church.com --noinput
```

### **Method 2: Vercel Dashboard**
1. **Project Settings** → **Environment Variables**
2. **Add variable**:
   - **Name**: `CREATE_SUPERUSER`
   - **Value**: `python manage.py createsuperuser --username admin --email admin@church.com --noinput`
3. **Redeploy** to create superuser
4. **Remove variable** after creation

### **Method 3: SSH Access**
```bash
npx vercel exec --scope focusonthethrones-projects
python manage.py createsuperuser
```

---

## 👤 **Default Admin Credentials:**

### **Recommended:**
- **Username**: `admin`
- **Email**: `admin@church.com`
- **Password**: Choose strong password

### **After Creation:**
1. **Visit**: `/admin/` on your live app
2. **Login**: with your superuser credentials
3. **Configure**: Initial church settings
4. **Create**: Fellowships and departments

---

## 🎯 **Admin Panel Features:**

### **What You Can Manage:**
- **Users**: Manage church members
- **Attendance**: View/edit attendance records
- **Fellowships**: Create/manage fellowship groups
- **Departments**: Set up service departments
- **Reports**: Generate attendance reports
- **Follow-up**: Manage member follow-up

---

## 🚀 **After Superuser Creation:**

### **Complete These Tasks:**
1. **Login to admin panel**
2. **Create initial fellowships**
3. **Set up departments**
4. **Test member registration**
5. **Verify attendance recording**
6. **Test mobile responsiveness**

---

## ✅ **Success Indicators:**

- ✅ Admin login successful
- ✅ Can create/edit members
- ✅ Fellowships visible
- ✅ Departments configured
- ✅ Attendance tracking works
- ✅ Reports generate correctly
