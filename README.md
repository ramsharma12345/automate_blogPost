# AI & Open Source GitHub Automator

This project automatically searches GitHub for recent repositories related to AI and Open Source every 30 minutes. It posts the results as a new Issue in this repository, which triggers a default GitHub email notification to your account. It runs entirely on GitHub Actions, requiring no external server hosting or SMTP configuration.

## Setup Instructions

To get this running on your own GitHub account:

1. **Commit and Push:**
   Commit all files in this repository and push them to a repository on your GitHub account.

2. **Watch the Repository:**
   Ensure you are "Watching" the repository (the Eye icon at the top right of the repo page) so that GitHub sends you an email notification whenever a new issue is created. Check your personal GitHub notification settings to ensure email notifications for issues are enabled.

3. **Enable GitHub Actions:**
   - Go to the **Actions** tab in your repository.
   - If prompted, click "I understand my workflows, go ahead and enable them".

4. **Allow Actions to create Issues:**
   - In your repository, go to **Settings** > **Actions** > **General**.
   - Scroll down to **Workflow permissions**.
   - Make sure **Read and write permissions** is selected (this allows the action to create issues).

5. **Test the Workflow manually:**
   - In the **Actions** tab, select the "Fetch and Email AI/Open Source Posts" workflow on the left.
   - Click the **Run workflow** dropdown on the right and click the **Run workflow** button.
   - Wait a minute for the job to finish, check the "Issues" tab on your repo for the new post, and check your email inbox!

## How it works
- The `.github/workflows/schedule.yml` file sets up a cron job to run the Python script every 30 minutes.
- `main.py` queries the GitHub REST API for new repositories matching the keywords `ai` and `open-source`.
- It then uses the default `GITHUB_TOKEN` provided by Actions to create a new Issue with the summary. You receive the email automatically from GitHub's default notification system!
