# Merge conflicts

A conflict happens when two branches change the same lines. Git marks them:

```
<<<<<<< HEAD
the version on your branch
=======
the version coming in
>>>>>>> main
```

Steps:
1. Run `git status` to list conflicted files (explain it if new).
2. For each conflict, explain in plain language what each side intended.
3. Propose a resolution (keep one, or combine both) with the reason.
4. Ask before editing. After approval, edit the file, remove the markers, run tests.
5. `git add <file>` then finish with `git commit` (for a merge) or
   `git rebase --continue` (for a rebase). Explain which applies.
6. If things go wrong, `git merge --abort` returns to before the merge - explain this is
   the safe "undo".

Analogy: two people edited the same sentence in a shared doc; someone has to decide
which wording survives.
