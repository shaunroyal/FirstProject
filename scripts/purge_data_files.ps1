
# This script will remove all data-type files (e.g., .csv, .xlsx, .json) from the git history and working tree,
# then force-push the rewritten history to GitHub.
# WARNING: This operation rewrites history. All collaborators must re-clone the repository after this.
# Make a backup before running!

# Step 1: Remove data-type files from working tree
Remove-Item -Path "*.csv" -Recurse -Force
Remove-Item -Path "*.xlsx" -Recurse -Force
Remove-Item -Path "*.json" -Recurse -Force

# Step 2: Remove data-type files from git history (requires git-filter-repo)
# If you don't have git-filter-repo, install it with: pip install git-filter-repo

git filter-repo --path-glob '*.csv' --invert-paths
git filter-repo --path-glob '*.xlsx' --invert-paths
git filter-repo --path-glob '*.json' --invert-paths

# Step 3: Commit removal in working tree (if needed)
git add .
git commit -m "Remove data-type files from working tree"

# Step 4: Force-push rewritten history to GitHub
git push origin --force --all
git push origin --force --tags
