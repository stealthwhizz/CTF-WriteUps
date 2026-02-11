# Just One Commit Ago 🔍

<div align="center">

**Hackdata-TriNetra CTF - Forensics Challenge**

[![Difficulty](https://img.shields.io/badge/Difficulty-Easy-green)]()
[![Category](https://img.shields.io/badge/Category-Git%20Forensics-blue)]()
[![Points](https://img.shields.io/badge/Points-Unknown-green)]()

</div>

---

## 📋 Challenge Description

> Your team has taken over maintenance of a small internal service after a contractor abruptly left the company. The service is open-sourced on GitHub for transparency.
>
> Shortly after deployment, suspicious API activity is detected against a third-party provider. You suspect an API key was accidentally committed to the repository at some point.
>
> The contractor claims they **"deleted it immediately."**
>
> Triage the Git repository and recover the API key.
>
> **Flag Format:** `TriNetra{...}`

**Files Provided:** `justonecommitago.zip`

---

## 🎯 TL;DR

**Flag:** `TriNetra{G!t_B3tter_@t_g!t}` 

The contractor committed a real API key, then "deleted" it by replacing it with a placeholder in a new commit. However, Git preserves all history, so the original key is still recoverable using Git's pickaxe feature (`git log -S`).

---

## 🔬 Solution

### Step 1: Extract and Navigate to Repository

```bash
unzip justonecommitago.zip
cd extracted/claude-quickstarts
```

### Step 2: Check Commit History

```bash
git log --oneline --all
```

**Output:**
```
41de984 (HEAD -> main) Update quickstart README
27ad2cd Initial commit
```

Only 2 commits visible! The challenge title "**Just One Commit Ago**" hints that the API key was in an earlier commit that was later modified.

### Step 3: Search for Content Changes Using Git Pickaxe ⛏️

The key insight is that **deleting != removing from Git history**. When someone "deletes" sensitive data by committing a new change, the old data remains in Git's history.

Use Git's "pickaxe" feature to search for commits where "API" was added or removed:

```bash
git log -p --all -S "API"
```

**Breaking down the command:**
- `git log -p` — Show patch/diff for each commit
- `--all` — Search all branches and refs
- `-S "API"` — Find commits where "API" text was added or removed (Git pickaxe)

### Step 4: Found It! 🎉

The command reveals this critical diff in commit `41de984`:

```diff
diff --git a/.env.example b/.env.example
index abc1234..def5678 100644
--- a/.env.example
+++ b/.env.example
@@ -1,1 +1,1 @@
-export ANTHROPIC_API_KEY='TriNetra{G!t_B3tter_@t_g!t}'
+export ANTHROPIC_API_KEY='your-api-key-here'
```

**The contractor's "fix":**
- **Before:** Real API key `TriNetra{G!t_B3tter_@t_g!t}`
- **After:** Generic placeholder `your-api-key-here`

They thought replacing the key in a new commit would "delete" it, but Git remembers everything!

### Step 5: Verify with Full Commit Details

```bash
git show 41de984
```

This confirms the complete change where the real API key was replaced with a placeholder.

---

## 🔑 The Complete Solution Path

### Alternative: Search with Regex for Better Results

For more targeted results with surrounding context:

```powershell
git log -p --all -S "API" --pickaxe-regex | Select-String -Pattern "API.{0,50}key|sk-|ANTHROPIC" -Context 2
```

Or using grep on Linux:

```bash
git log -p --all -S "API" | grep -E "API.{0,50}key|TriNetra" -A 2 -B 2
```

This narrows down the output to show only lines containing API-related content.

---

## 💡 Key Takeaways

### Why This Works

Git **never forgets** — even when you delete or modify sensitive data in a new commit, the old data stays in the repository's history forever (unless you explicitly rewrite history).

### The Contractor's Mistake

The contractor thought that committing a new change to replace the API key would "delete" it, but:

1. ❌ **What they did:** Replace sensitive data in a new commit
2. ✅ **What they should have done:** Use `git filter-branch`, `BFG Repo Cleaner`, or `git filter-repo` to rewrite history

### Real-World Impact

This is a **critical security issue** in real repositories:
- Leaked API keys in Git history can be discovered years later
- Even if you delete them in new commits, attackers can find them
- Once pushed to GitHub/GitLab, the data is exposed in public history

---

## 🛠️ Essential Git Forensics Commands

| Command | Purpose |
|---------|---------|
| `git log -p --all -S "keyword"` | Find commits where "keyword" was added/removed (pickaxe) |
| `git log -p --all -G "regex"` | Find commits where lines matching regex changed |
| `git log --all --full-history -- path/to/file` | Show all commits affecting a specific file |
| `git rev-list --all \| xargs git grep "pattern"` | Search for pattern across all commits |
| `git show <commit>:<file>` | View file content at specific commit |
| `git diff <commit1> <commit2>` | Compare two commits |
| `git reflog` | Show history of HEAD movements |
| `git fsck --lost-found` | Find dangling/unreachable commits |

### The Winning Command

```bash
git log -p --all -S "API"
```

This searches the **actual content** of files across all commits, not just commit messages — crucial for finding leaked secrets.

---

## 🔐 How to Properly Remove Secrets from Git History

If you accidentally commit secrets, here's the proper way to remove them:

### Option 1: BFG Repo Cleaner (Recommended)

```bash
# Install BFG
brew install bfg  # macOS
# or download from https://rtyley.github.io/bfg-repo-cleaner/

# Remove sensitive data
bfg --replace-text passwords.txt repo.git
cd repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

### Option 2: Git Filter-Repo (Modern)

```bash
# Install
pip install git-filter-repo

# Remove file from history
git filter-repo --path-glob '*.env' --invert-paths

# Force push
git push --force
```

### Option 3: Git Filter-Branch (Legacy)

```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

git push --force --all
```

⚠️ **Important:** After rewriting history, you must:
1. Force push to remote: `git push --force --all`
2. Have all team members re-clone the repository
3. Rotate the leaked credentials immediately

---

## 🎓 Educational Value

The flag **`TriNetra{G!t_B3tter_@t_g!t}`** is a clever pun meaning **"Git better at git"** — this challenge teaches:

1. **Git Pickaxe (`-S`)**: Search for specific text added/removed in commits
2. **Git Never Forgets**: Commits stay in history unless explicitly removed
3. **Shallow "Deletion"**: Replacing content ≠ removing from history
4. **Real-World Security**: This is how actual API leaks happen in production

### Prevention: Avoid This in Real Life 🛡️

**Before committing:**
- Use [git-secrets](https://github.com/awslabs/git-secrets) — Prevents committing passwords and secrets
- Use [pre-commit hooks](https://pre-commit.com/) — Scan for secrets before commit
- Use [truffleHog](https://github.com/trufflesecurity/trufflehog) — Find secrets in Git history

**GitHub's built-in protection:**
- [Secret scanning](https://docs.github.com/en/code-security/secret-scanning) — Automatically detects leaked credentials
- [Push protection](https://docs.github.com/en/code-security/secret-scanning/push-protection-for-repositories-and-organizations) — Blocks pushes containing secrets

---

## 🎯 Why "Just One Commit Ago"?

The challenge name is a hint: the API key was in a commit **just one commit before** the current HEAD. The contractor's "immediate deletion" was just replacing the content in the next commit — classic security mistake!


---

## 🚩 Flag

```
TriNetra{G!t_B3tter_@t_g!t}
```

**Translation:** "Git better at git" — A reminder that Git forensics skills are essential for security incident response!

---

## 📚 Additional Resources

- [Git Documentation - git-log](https://git-scm.com/docs/git-log)
- [Git Pickaxe Documentation](https://git-scm.com/docs/git-log#Documentation/git-log.txt--Sltstringgt)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [BFG Repo Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [Git Filter-Repo](https://github.com/newren/git-filter-repo)
- [TruffleHog - Find Secrets in Git](https://github.com/trufflesecurity/trufflehog)

---

<div align="center">

**Happy Hacking! 🎉**

*Challenge by Hackdata-TriNetra CTF*

**Remember:** Always scan your repositories for secrets before pushing to public remotes!

</div>
