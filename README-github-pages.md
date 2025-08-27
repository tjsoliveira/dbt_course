# 🚀 GitHub Pages Setup for dbt Course

This document explains how to set up GitHub Pages for your dbt course documentation.

## 📋 Prerequisites

- GitHub repository with your dbt course
- GitHub Pages enabled on your repository
- MkDocs configuration files (already created)

## ⚙️ GitHub Pages Configuration

### 1. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings**
3. Scroll down to **Pages** section
4. Under **Source**, select **GitHub Actions**

### 2. Repository Settings

Make sure your repository has the following settings:

- **Repository visibility**: Public (required for free GitHub Pages)
- **Branch protection**: Main branch should be protected
- **Actions permissions**: Actions should be enabled

## 🔧 Workflow Configuration

The GitHub Actions workflow (`.github/workflows/deploy.yml`) is already configured to:

- Build the MkDocs site on every push to main
- Deploy to GitHub Pages automatically
- Use the latest MkDocs Material theme
- Include all necessary plugins

## 📁 File Structure

```
dbt_course/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── docs/                       # Documentation source
│   ├── index.md               # Home page
│   ├── intro/                 # Introduction section
│   ├── jaffle-shop/          # Jaffle Shop section
│   ├── advanced/              # Advanced concepts
│   ├── best-practices/        # Best practices
│   └── reference/             # Reference section
├── mkdocs.yml                 # MkDocs configuration
├── requirements-mkdocs.txt    # Python dependencies
└── README-github-pages.md     # This file
```

## 🚀 Local Development

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install MkDocs dependencies
pip install -r requirements-mkdocs.txt
```

### 2. Run Locally

```bash
# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

### 3. Preview Changes

- Open http://127.0.0.1:8000 in your browser
- Make changes to markdown files
- See live preview with auto-reload

## 📝 Adding New Content

### 1. Create New Page

```bash
# Create new markdown file in appropriate directory
touch docs/advanced/new-topic.md
```

### 2. Update Navigation

Edit `mkdocs.yml` to add the new page to navigation:

```yaml
nav:
  - Advanced Concepts:
    - New Topic: advanced/new-topic.md
```

### 3. Commit and Push

```bash
git add .
git commit -m "Add new topic documentation"
git push origin main
```

## 🔍 Troubleshooting

### Common Issues

1. **Build fails**: Check GitHub Actions logs
2. **Pages not updating**: Wait for deployment to complete
3. **Styling issues**: Verify MkDocs Material theme is installed

### Debug Commands

```bash
# Check MkDocs version
mkdocs --version

# Validate configuration
mkdocs build --strict

# Check for broken links
mkdocs build --strict --verbose
```

## 🌐 Custom Domain (Optional)

To use a custom domain:

1. Add `CNAME` file in `docs/` directory
2. Configure DNS settings with your domain provider
3. Update `mkdocs.yml` with custom domain

```yaml
site_url: https://yourdomain.com
```

## 📚 Useful Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🎯 Next Steps

1. ✅ **GitHub Pages configured** ← You are here
2. [Add more content to your course](docs/)
3. [Customize the theme](mkdocs.yml)
4. [Set up custom domain](docs/CNAME)

---

**Your documentation is now ready for GitHub Pages!** 🎉

The site will be automatically deployed at: `https://yourusername.github.io/dbt_course`

