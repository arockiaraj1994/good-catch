# Good Catch

A HUGO website with custom HTML homepage deployed to GitHub Pages.

## 🚀 Quick Start

### Prerequisites
- Hugo (install from https://gohugo.io/installation/)
- Git

### Local Development

1. **Start the development server:**
   ```bash
   hugo serve
   ```
   Visit `http://localhost:1313` to view the site.

2. **Build for production:**
   ```bash
   hugo --minify
   ```
   Output is generated in the `public/` folder.

### Project Structure

```
good-catch/
├── config.yaml              # Hugo configuration with baseURL for GitHub Pages
├── layouts/
│   └── index.html          # Custom HTML homepage
├── content/                 # Markdown content files (posts, pages)
├── static/                  # Static assets (CSS, JS, images)
├── themes/                  # Hugo themes directory
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions workflow for CI/CD
└── .gitignore              # Git ignore rules
```

## 📝 Customization

### Homepage
Edit `layouts/index.html` to customize your homepage. The default includes:
- Hero section with title and description
- Call-to-action buttons
- Gradient background styling
- Responsive design

### Adding Content
Create markdown files in the `content/` directory:
```
content/
├── posts/
│   ├── my-first-post.md
│   └── another-post.md
└── pages/
    └── about.md
```

### Styling
Add custom CSS files to `static/css/` and link them in your layouts.

## 🚢 Deployment

### GitHub Pages Setup

1. **Ensure `gh-pages` branch exists:**
   ```bash
   git branch gh-pages
   git push origin gh-pages
   ```
   (The GitHub Actions workflow will create this automatically if it doesn't exist)

2. **Configure GitHub Pages in repository settings:**
   - Go to Settings → Pages
   - Set "Source" to "Deploy from a branch"
   - Select `gh-pages` branch
   - Set folder to `/ (root)`

3. **Push to main branch:**
   ```bash
   git add .
   git commit -m "Initial HUGO setup"
   git push origin main
   ```

4. **GitHub Actions will automatically:**
   - Build the site with Hugo
   - Deploy to `gh-pages` branch
   - Site will be live at: `https://arockiaraj1994.github.io/good-catch/`

### Workflow Details
The `.github/workflows/deploy.yml` file:
- Triggers on push to `main` branch
- Uses Hugo to build the site
- Deploys `public/` folder to `gh-pages` branch
- No manual deployment needed

## 🔧 Configuration

### baseURL
The site is configured for project-site deployment with:
```yaml
baseURL: "https://arockiaraj1994.github.io/good-catch/"
```

This ensures all links and assets work correctly on GitHub Pages.

### Hugo Version
The GitHub Actions workflow uses the latest Hugo version. To pin a specific version, edit `.github/workflows/deploy.yml`:
```yaml
hugo-version: '0.123.0'  # Replace with desired version
```

## 📚 Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [Hugo Templating](https://gohugo.io/templates/)
- [GitHub Pages Docs](https://docs.github.com/en/pages)

## 📄 License

Add your license information here.