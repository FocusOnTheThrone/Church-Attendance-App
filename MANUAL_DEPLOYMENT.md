# Manual Vercel Deployment Steps

## Step 1: Backup Current Setup
```bash
git status
git add .
git commit -m "Backup before manual fix"
```

## Step 2: Remove Complex Configurations
```bash
# Remove vercel.json temporarily
del vercel.json
# Or: rm vercel.json
```

## Step 3: Use Vercel Web Dashboard
1. Go to: https://vercel.com/dashboard
2. Select: church-attendance-app
3. Click: Settings
4. Go to: Build & Development Settings
5. Set:
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `.`
   - Install Command: `pip install -r requirements.txt`
   - Framework: Python
6. Save settings

## Step 4: Check Environment Variables
1. Go to: Settings > Environment Variables
2. Ensure these are set:
   ```
   SECRET_KEY=v6kldjv10@8b_xwku!v0alu-0s8cv0$)orat_!li=l(7v-56ut
   DEBUG=False
   ALLOWED_HOSTS=church-attendance-koys94wzp-focusonthethrones-projects.vercel.app,www.church-attendance-koys94wzp-focusonthethrones-projects.vercel.app,church-attendance-app-navy.vercel.app,www.church-attendance-app-navy.vercel.app
   DATABASE_URL=your-postgresql-connection-string
   DJANGO_SETTINGS_MODULE=config.settings
   VERCEL=true
   ```

## Step 5: Redeploy from Web Dashboard
1. Go to: Deployments tab
2. Click: Redeploy
3. Wait for deployment
4. Check logs for errors

## Step 6: Test Deployment
Visit your app URL and check for 500 errors.

## Step 7: If Still Failing - Try Minimal Setup
1. Create simple test file
2. Deploy with minimal configuration
3. Gradually add complexity

## Step 8: Debug with Logs
1. Check Vercel deployment logs
2. Look for specific error messages
3. Fix issues one by one

## Step 9: Final Configuration
Once working, restore proper vercel.json configuration.
