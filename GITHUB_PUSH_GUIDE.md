# GitHub Push Fix Guide

## 🔧 **Git Push Permission Issue (403 Error)**

### **Current Issue:**
```
remote: Permission to MRH-Softwares2025/Church-Attendance-App.git denied to FocusOnTheThrone.
fatal: unable to access 'https://github.com/MRH-Softwares2025/Church-Attendance-App/': The requested URL returned error: 403
```

### **What This Means:**
- Git is trying to push to `MRH-Softwares2025/Church-Attendance-App`
- Getting 403 Forbidden error
- Either wrong repo URL or authentication issue

---

## 🔧 **Solutions to Try:**

### **Solution 1: Check Repository URL**
1. Go to your GitHub repository
2. Copy the correct HTTPS URL
3. Update remote if needed

```bash
# Check current remote
git remote -v

# Update remote if wrong
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### **Solution 2: Re-authenticate with GitHub**
1. **Generate Personal Access Token:**
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token with "repo" permissions
   - Copy the token

2. **Update Git Credentials:**
```bash
# Remove old credentials
git config --global --unset credential.helper

# Set up new push with token
git remote set-url origin https://YOUR_TOKEN@github.com/MRH-Softwares2025/Church-Attendance-App.git
```

### **Solution 3: Use GitHub CLI (Recommended)**
1. **Install GitHub CLI:**
```bash
# Download and install GitHub CLI
# Or: winget install GitHub.cli
```

2. **Authenticate:**
```bash
gh auth login
```

3. **Push with CLI:**
```bash
gh repo create MRH-Softwares2025/Church-Attendance-App --public
git push origin main
```

### **Solution 4: Check Repository Ownership**
1. **Verify you own the repository:**
   - Go to https://github.com/MRH-Softwares2025/Church-Attendance-App
   - Check if you have push access

2. **If not owner, fork the repository:**
   - Click "Fork" on GitHub
   - Update remote to your fork
   - Push to your fork instead

---

## 🚀 **Step-by-Step Fix:**

### **Step 1: Verify Repository Access**
1. Open browser: https://github.com/MRH-Softwares2025/Church-Attendance-App
2. Check if you can see the repository
3. Check if you have "Write" permissions

### **Step 2: Update Git Authentication**
```bash
# Option A: Use Personal Access Token
git remote set-url origin https://YOUR_TOKEN@github.com/MRH-Softwares2025/Church-Attendance-App.git

# Option B: Use GitHub CLI
gh auth login
git remote set-url origin https://github.com/MRH-Softwares2025/Church-Attendance-App.git
```

### **Step 3: Try Push Again**
```bash
git push origin main
```

---

## 🔍 **Debugging Commands:**

### **Check Current Configuration:**
```bash
# Check remote URL
git remote get-url origin

# Check user configuration
git config --global user.name
git config --global user.email

# Check credential helper
git config --global credential.helper
```

### **Test Connection:**
```bash
# Test GitHub connection
git ls-remote origin
```

---

## 🎯 **Most Likely Solutions:**

### **1. Wrong Repository Name**
- Repository might be named differently
- Check actual repository name on GitHub

### **2. Authentication Required**
- GitHub now requires personal access tokens for Git operations
- Generate token at: https://github.com/settings/tokens

### **3. Permission Issue**
- You might not be a collaborator on the repository
- Fork the repository instead

---

## 📋 **Quick Fix Checklist:**

- [ ] Verify repository exists and is accessible
- [ ] Check you have push permissions
- [ ] Generate GitHub personal access token
- [ ] Update Git remote with token
- [ ] Try push again

---

## 🔗 **Helpful Links:**

- **GitHub Personal Access Tokens**: https://github.com/settings/tokens
- **GitHub CLI Documentation**: https://cli.github.com/
- **Git Authentication**: https://git-scm.com/book/en/v2/Git-Tools-Authentication-on-GitHub

---

## 💡 **Pro Tip:**

**For long-term use, set up GitHub CLI:**
```bash
# Install GitHub CLI
winget install GitHub.cli

# Authenticate once
gh auth login

# Use for all future operations
gh repo create
gh pr create
gh issue create
```

---

**Try these solutions in order. The personal access token method usually fixes 403 errors immediately!**
