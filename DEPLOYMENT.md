# Deployment Guide for Streamlit Cloud

## Prerequisites

1. A GitHub account
2. Git installed on your local machine
3. Python 3.8 or higher installed

## Step-by-Step Deployment

### Step 1: Prepare Your Code

1. All files are ready in the `trading-dashboard` folder:
   - `app.py` - Main application
   - `indicators.py` - Technical indicators
   - `strategy.py` - Trading strategy
   - `database.py` - Database handler
   - `requirements.txt` - Dependencies
   - `README.md` - Documentation
   - `.gitignore` - Git ignore rules
   - `.streamlit/config.toml` - Streamlit configuration

### Step 2: Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the "+" icon in the top right and select "New repository"
3. Name your repository (e.g., "trading-dashboard")
4. Choose Public or Private
5. Do NOT initialize with README (we already have one)
6. Click "Create repository"

### Step 3: Push Code to GitHub

Open terminal/command prompt in your `trading-dashboard` folder and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: Trading dashboard application"

# Add remote repository (replace YOUR_USERNAME and YOUR_REPO with your info)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "Sign in" and authenticate with your GitHub account

2. **Create New App**:
   - Click "New app" button
   - Select your GitHub repository: `YOUR_USERNAME/trading-dashboard`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: Choose a custom URL or use the auto-generated one

3. **Advanced Settings** (Optional):
   - Python version: 3.9 (recommended)
   - No secrets needed for this app
   - Keep default settings

4. **Deploy**:
   - Click "Deploy!" button
   - Wait 2-5 minutes for deployment
   - Your app will be live at the provided URL

### Step 5: Verify Deployment

1. Once deployed, the app should open automatically
2. Test the following:
   - Enter a symbol (e.g., "GC=F" for Gold)
   - Check if data loads
   - Verify charts display correctly
   - Test the auto-refresh feature
   - Check if recommendations are generated

## Troubleshooting Deployment Issues

### Issue: Dependencies Not Installing

**Solution**: Check `requirements.txt` format
- Ensure no extra spaces
- Use exact version numbers
- Try removing version numbers to get latest versions

### Issue: App Crashes on Startup

**Solution**: Check the logs in Streamlit Cloud
- Click on "Manage app" → "Logs"
- Look for error messages
- Common issues:
  - Import errors: Check all imports in code
  - File path issues: Use relative paths

### Issue: Data Not Loading

**Solution**: 
- Yahoo Finance might be rate-limited
- Try a different symbol
- Check internet connectivity on Streamlit Cloud
- Add error handling in code

### Issue: Database Errors

**Solution**:
- SQLite works fine on Streamlit Cloud
- Database file is created automatically
- No configuration needed

## Updating Your Deployment

To update your live app:

```bash
# Make changes to your code
# Then commit and push

git add .
git commit -m "Description of changes"
git push origin main
```

Streamlit Cloud will automatically detect changes and redeploy (takes 1-2 minutes).

## Resource Limits (Free Tier)

Streamlit Cloud free tier includes:
- 1 GB RAM
- 1 CPU core
- Unlimited public apps
- Apps sleep after 7 days of inactivity (wake up on first visit)

This is sufficient for this trading dashboard!

## Best Practices

1. **Regular Updates**: Update your indicators and strategy as needed
2. **Monitor Usage**: Check if the app is being rate-limited
3. **Backup Data**: Download database periodically if needed
4. **Test Locally First**: Always test changes locally before pushing

## Security Notes

1. **Public App**: Remember your app is public on free tier
2. **No Sensitive Data**: Don't store API keys or personal data
3. **Rate Limiting**: Yahoo Finance is free but has limits

## Making App Private (Paid Tier)

If you want a private app:
1. Upgrade to Streamlit Cloud Team plan
2. Set app visibility to "Private"
3. Share with specific email addresses

## Custom Domain (Optional)

To use your own domain:
1. Upgrade to paid plan
2. Configure DNS settings
3. Add custom domain in Streamlit Cloud settings

## Alternative Deployment Options

If you prefer other platforms:

### Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Create runtime.txt
echo "python-3.9.0" > runtime.txt

# Deploy using Heroku CLI
heroku create your-app-name
git push heroku main
```

### AWS EC2
1. Launch EC2 instance
2. Install Python and dependencies
3. Run: `streamlit run app.py --server.port=8501`
4. Configure security groups to allow port 8501

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## Support

For deployment issues:
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [GitHub Issues](https://github.com/streamlit/streamlit/issues)

---

**You're all set! Your trading dashboard should now be live and accessible to anyone with the URL.**

Happy deploying! 🚀
