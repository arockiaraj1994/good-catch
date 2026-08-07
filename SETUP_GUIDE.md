# goodcatch.in Implementation — Setup Guide

## Status

✅ **Completed:**
- Config updated with PaperMod theme and Giscus settings
- All layout templates created (single.html, list.html, partials)
- Content structure set up with sample post
- .gitmodules file prepared for PaperMod submodule

⏳ **Remaining:**
- Initialize PaperMod submodule
- Local testing and verification
- Deploy to GitHub Pages

---

## Next Steps

### 1. Initialize PaperMod Submodule

Run these commands in your terminal:

```bash
cd /workspaces/good-catch
git submodule init
git submodule update --remote
```

Or, if the submodule hasn't been initialized yet:

```bash
cd /workspaces/good-catch
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

### 2. Verify Theme Installation

Check that PaperMod files are present:

```bash
ls -la themes/PaperMod/
```

You should see directories like `layouts/`, `assets/`, `static/`, etc.

### 3. Test Locally

Start the Hugo development server:

```bash
cd /workspaces/good-catch
hugo serve
```

Then visit `http://localhost:1313` and verify:

- **Homepage** displays the terminal hero
- **Posts link** appears in the navigation
- **/posts/** page shows the sample post
- **Sample post page** displays:
  - Title, date, author
  - Post content
  - Giscus comments iframe at bottom
- **No console errors** (check browser dev tools)

### 4. Test Giscus Comments

On the sample post page:
1. Look for a Giscus comments section at the bottom
2. Click "Sign in with GitHub" (if not already signed in)
3. Post a test comment
4. Verify the comment appears in the repo's Discussions tab on GitHub

### 5. Commit and Push

```bash
cd /workspaces/good-catch
git add .
git commit -m "feat: add PaperMod theme, post layouts, and Giscus comments"
git push origin main
```

### 6. Monitor Deployment

1. Go to your repo on GitHub → **Actions** tab
2. Watch the deploy workflow run
3. Verify it completes without errors
4. Visit `https://arockiaraj1994.github.io/good-catch/` to see the live site

---

## Configuration Summary

### Current Setup

- **Theme:** PaperMod (themes/PaperMod)
- **Post Structure:** `content/posts/*.md`
- **Post Layout:** `layouts/posts/single.html` + Giscus comments
- **Comments:** Giscus (GitHub Discussions-backed)
  - Repo: arockiaraj1994/good-catch
  - Category: General
  - Theme: Dark

### Content Front Matter Example

All posts should use this front matter:

```yaml
---
title: "Post Title"
date: 2026-01-15T10:30:00Z
author: "Author Name"
categories: ["Category Name"]
tags: ["tag1", "tag2"]
draft: false
---
```

---

## Troubleshooting

### Hugo build fails

- Ensure PaperMod is installed in `themes/PaperMod/`
- Check `config.yaml` syntax is valid YAML
- Run `hugo serve -v` for verbose error messages

### Giscus not showing

- Verify Giscus script loads in browser dev tools (Network tab)
- Check that `params.giscus` values in `config.yaml` match your GitHub setup
- Ensure the repo discussions are enabled on GitHub

### Posts not appearing

- Ensure posts are in `content/posts/*.md`
- Check front matter doesn't have `draft: true`
- Run `hugo serve --buildDrafts` to include draft posts

---

## After Verification

Once everything works locally and on GitHub Pages, you can:

1. **Delete the sample post:**
   ```bash
   rm content/posts/chatgpt-sydney-capital.md
   git add . && git commit -m "remove: sample post" && git push
   ```

2. **Ready for the automated agent:**
   The daily workflow will now be able to:
   - Create new posts in `content/posts/`
   - Open PRs with the posts
   - Merge triggers rebuilds → new posts go live

---

## Files Modified/Created

| File | Status | Purpose |
|------|--------|---------|
| `config.yaml` | ✅ Modified | Theme, Giscus, taxonomies |
| `layouts/posts/single.html` | ✅ Created | Individual post page |
| `layouts/posts/list.html` | ✅ Created | Post archive listing |
| `layouts/_default/list.html` | ✅ Created | Fallback list layout |
| `layouts/partials/giscus.html` | ✅ Created | Giscus comments widget |
| `content/posts/_index.md` | ✅ Created | Posts section metadata |
| `content/posts/chatgpt-sydney-capital.md` | ✅ Created | Sample post (delete after testing) |
| `.gitmodules` | ✅ Created | PaperMod submodule definition |
| `.github/workflows/deploy.yml` | ✅ Unchanged | Auto-deploy on push |

---

## Next Phase: Daily Agent Setup

Once the site is live and verified, Phase 3 (from the original plan) will implement:
- GitHub Actions scheduled workflow (daily cron)
- Anthropic API integration for content discovery
- Automatic PR generation for new posts
