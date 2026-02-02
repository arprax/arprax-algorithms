# Module 7: Version Control

**Concept:** Git, GitHub, and Collaboration.

In this final module, we secure our code by moving it from your local machine to the cloud. This is the foundation of professional software engineering and "Applied Data Intelligence."

### 📺 The Build Session
<div class="video-wrapper">
    <iframe src="https://www.youtube.com/embed/Srjm76bHPrk" frameborder="0" allowfullscreen></iframe>
</div>

### ⚙️ The Workflow


1.  **Enable Git:** In PyCharm, go to `VCS` -> `Enable Version Control` -> Select **Git**.
2.  **Commit:** This saves a "snapshot" of your code locally. In PyCharm, files change from **Red** (untracked) to **Green** (added) to **Normal** (committed).
3.  **Push:** This sends your local snapshots to **GitHub**. It’s like uploading your project to a secure cloud vault.
4.  **Pull (Sync):** Use the **Update Project** blue arrow to bring changes (like a README update made on the web) back down to your computer.

### 💻 The Terminal Commands (Cheat Sheet)
While PyCharm handles this with buttons, knowing the industrial commands is a must:

```bash
# Initialize a new repository
git init

# Stage your changes
git add .

# Create a snapshot
git commit -m "Industrial: Completed Bootcamp Module 7"

# Push to the cloud
git push origin main
```