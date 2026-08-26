# Moving this folder into the life-os repository

This scaffold was built inside the `Source` repo because the building agent had no write access to `life-os`. To move it (one time, then delete this file):

```bash
git clone https://github.com/amikiste/life-os.git ~/life-os
git clone https://github.com/amikiste/Source.git /tmp/source && cd /tmp/source && git checkout cursor/life-os-scaffold-39e9
cp -a /tmp/source/life-os/. ~/life-os/        # -a preserves dotfiles (.claude, .gitignore, ...)
cd ~/life-os
rm MIGRATE.md
git add -A && git commit -m "scaffold: specs + skills + memory + automation (PRD Phase 2)" && git push
```

Then open `~/life-os` in Claude Code and run `/setup`.

To let Cursor cloud agents work in `life-os` directly in the future: GitHub → Settings → Applications → Cursor → Repository access → add `life-os`.
