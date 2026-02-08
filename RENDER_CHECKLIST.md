# Render Deployment Checklist

Use this checklist to deploy SignalTrust AI Scanner on Render.

## Pre-Deployment

- [ ] You have a Render.com account (free or paid)
- [ ] You have access to this GitHub repository
- [ ] You have an OpenAI API key (recommended for AI features)
- [ ] Repository is up to date with the latest changes

## Deployment Steps

### Step 1: Access Render Dashboard
- [ ] Go to https://dashboard.render.com
- [ ] Sign in to your account

### Step 2: Create New Service

**Using Blueprint (Recommended):**
- [ ] Click "New +" button
- [ ] Select "Blueprint"
- [ ] Connect to this GitHub repository
- [ ] Render detects `render.yaml` automatically

**OR Using Manual Web Service:**
- [ ] Click "New +" button
- [ ] Select "Web Service"
- [ ] Connect to this GitHub repository
- [ ] Configure build and start commands (see below)

### Step 3: Configure Service (if manual)

If you're NOT using Blueprint, configure these settings:

- [ ] **Name**: `signaltrust-ai-scanner` (or your preferred name)
- [ ] **Environment**: Python 3
- [ ] **Region**: Choose your preferred region
- [ ] **Branch**: `main` (or your deployment branch)
- [ ] **Build Command**: `./build.sh`
- [ ] **Start Command**: `./start-render.sh`
- [ ] **Plan**: Free (or upgrade as needed)

### Step 4: Set Environment Variables

Go to the "Environment" tab and add these variables:

**Required:**
- [ ] `OPENAI_API_KEY` = your_openai_api_key_here

**Recommended (if you have them):**
- [ ] `COINGECKO_API_KEY` = your_coingecko_api_key
- [ ] `ALPHAVANTAGE_API_KEY` = your_alphavantage_api_key
- [ ] `WHALEALERT_API_KEY` = your_whalealert_api_key
- [ ] `NEWS_CATCHER_API_KEY` = your_newscatcher_api_key

**Optional Agent Configuration:**
- [ ] `AGENT_API_KEY` = your_agent_api_key
- [ ] `AGENT_STOCK_ID` = your_stock_agent_id
- [ ] `AGENT_CRYPTO_ID` = your_crypto_agent_id
- [ ] `AGENT_WHALE_ID` = your_whale_agent_id
- [ ] `AGENT_SITE_ID` = your_site_agent_id
- [ ] `AGENT_SUPERVISOR_ID` = your_supervisor_agent_id

**Note**: The following variables are auto-configured by Render:
- `PORT` (auto-generated)
- `SECRET_KEY` (auto-generated)
- `PYTHON_VERSION` (from render.yaml)
- `FLASK_ENV` (from render.yaml)

### Step 5: Deploy
- [ ] Click "Create Web Service" or "Apply" (for Blueprint)
- [ ] Wait for build to complete (usually 3-5 minutes)
- [ ] Watch the build logs for any errors

## Post-Deployment Verification

### Step 1: Check Service Status
- [ ] Service shows as "Live" in Render dashboard
- [ ] No error messages in the Events tab

### Step 2: Test Endpoints

**Health Check:**
- [ ] Visit: `https://your-app-name.onrender.com/health`
- [ ] Should return: `{"status": "healthy", ...}`

**Home Page:**
- [ ] Visit: `https://your-app-name.onrender.com/`
- [ ] Page loads successfully

**Dashboard:**
- [ ] Visit: `https://your-app-name.onrender.com/dashboard`
- [ ] Login page appears or dashboard loads

### Step 3: Check Logs
- [ ] Go to "Logs" tab in Render dashboard
- [ ] Verify no critical errors
- [ ] See successful startup messages

### Step 4: Test AI Features (if OpenAI key is set)
- [ ] Log in to the application
- [ ] Try a market analysis
- [ ] Verify AI predictions work

## Troubleshooting

### Build Fails
- [ ] Check build logs in Render dashboard
- [ ] Verify all files are committed to repository
- [ ] Ensure `build.sh` has execute permissions
- [ ] Check Python version compatibility

### Service Won't Start
- [ ] Check application logs
- [ ] Verify `PORT` environment variable is set
- [ ] Ensure required dependencies are installed
- [ ] Check that `start-render.sh` has execute permissions

### Health Check Fails
- [ ] Check if `/health` endpoint is accessible
- [ ] Review application logs for errors
- [ ] Verify Flask is running properly

### AI Features Not Working
- [ ] Confirm `OPENAI_API_KEY` is set correctly
- [ ] Check OpenAI account has credits
- [ ] Review logs for API errors
- [ ] Test with a simple query first

## Configuration Options

### Free Tier Limitations
- [ ] **Aware**: Service sleeps after 15 minutes of inactivity
- [ ] **Aware**: Cold starts take ~30 seconds
- [ ] **Aware**: 100 GB bandwidth/month limit
- [ ] **Aware**: No persistent disk storage

### Upgrade Options (if needed)
- [ ] Upgrade to Starter plan ($7/month) for no sleep
- [ ] Upgrade to Standard plan for more resources
- [ ] Add persistent disk for data storage
- [ ] Enable auto-scaling

### Auto-Deploy Setup (optional)
- [ ] Go to Settings → "Auto-Deploy"
- [ ] Enable auto-deploy
- [ ] Select your branch (e.g., `main`)
- [ ] Every push will trigger deployment

### Custom Domain (optional)
- [ ] Go to Settings → "Custom Domains"
- [ ] Add your domain
- [ ] Configure DNS as shown
- [ ] Wait for SSL certificate (automatic)

## Security Checklist

- [ ] All API keys are set as environment variables (not in code)
- [ ] `.env` file is in `.gitignore`
- [ ] HTTPS is enabled (automatic on Render)
- [ ] SECRET_KEY is auto-generated or set securely
- [ ] No sensitive data in logs

## Optimization

### Cost Optimization
- [ ] Use `gpt-4o-mini` instead of `gpt-4` (10x cheaper)
- [ ] Set appropriate timeout values
- [ ] Enable compression for cloud storage
- [ ] Monitor bandwidth usage

### Performance Optimization
- [ ] Consider upgrading plan if needed
- [ ] Monitor response times in Render metrics
- [ ] Check worker count (default: 2)
- [ ] Review timeout settings (default: 120s)

## Maintenance

### Regular Tasks
- [ ] Monitor service health weekly
- [ ] Check logs for errors
- [ ] Review bandwidth usage
- [ ] Update dependencies periodically
- [ ] Rotate API keys every 3-6 months

### Backup Strategy
- [ ] Enable cloud storage if using paid plan
- [ ] Configure `CLOUD_PROVIDER` and credentials
- [ ] Enable `CLOUD_AUTO_SYNC` for automatic backups
- [ ] Test restore process

## Getting Help

If you encounter issues:

1. **Check Documentation**
   - [ ] Review `RENDER_DEPLOYMENT.md`
   - [ ] Check `RENDER_FIX_SUMMARY.md`
   - [ ] Read main `README.md`

2. **Check Render Resources**
   - [ ] Render documentation: https://render.com/docs
   - [ ] Render community: https://community.render.com
   - [ ] Render status page: https://status.render.com

3. **Debug Process**
   - [ ] Check Render logs (Logs tab)
   - [ ] Check Events tab for deployment history
   - [ ] Review environment variables
   - [ ] Test health endpoint

4. **Contact Support**
   - [ ] Create issue on GitHub repository
   - [ ] Contact Render support for platform issues

## Completion

Once all steps are complete:

- [ ] Service is deployed and running
- [ ] Health check passes
- [ ] Main pages load correctly
- [ ] AI features work (if configured)
- [ ] Logs show no critical errors
- [ ] Documentation reviewed

**Congratulations! Your SignalTrust AI Scanner is now live on Render! 🎉**

---

## Quick Reference

**Service URL**: `https://your-app-name.onrender.com`
**Health Check**: `https://your-app-name.onrender.com/health`
**Dashboard**: `https://dashboard.render.com`

**Key Files:**
- `render.yaml` - Service configuration
- `build.sh` - Build script
- `start-render.sh` - Startup script
- `runtime.txt` - Python version
- `.python-version` - Python version (alternative)

**Support Documents:**
- `RENDER_DEPLOYMENT.md` - Full deployment guide
- `RENDER_FIX_SUMMARY.md` - Changes summary
- `README.md` - Application documentation
