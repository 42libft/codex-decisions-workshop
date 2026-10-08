# Codex Cloud setup for this repository

## Prerequisites

- Connect GitHub to the ChatGPT/Codex account that will create the Cloud environment.
- Select this GitHub repository. Every collaborator needs repository access and Codex Cloud access on their own account.
- Keep API keys out of GitHub. The workshop key created locally is not bundled with this repository or automatically transferred to Cloud.

## Environment settings

1. In Codex, choose **Work in > Cloud > Select environment > Create environment** and select this repository.
2. Let setup inspect the repository. No package installation is needed. Confirm that Python 3 is available.
3. Verify `python3 -m py_compile decisions_demo.py` and `python3 decisions_demo.py --sample --dry-run`.
4. For live API calls, allow HTTPS to `api.openai.com`. Supply `OPENAI_API_KEY` through each developer's Personal vault or another explicitly approved secret arrangement. The key itself must not appear in a setup script, prompt, log, or repository file.
5. Review the setup report and publish the environment. Run a fresh Cloud task to verify the published version.

The official Cloud guide describes workspace-wide environment sharing for eligible Enterprise workspaces. If that option is unavailable, each collaborator can create their own environment from the same GitHub repository. GitHub branches and pull requests remain the shared review point.

Codex Cloud currently does not support computer or browser use in its task VMs. Use a local browser for any future Sites or plugin UI acceptance checks.

Sources: [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments), [Decisions API](https://developers.openai.com/api/docs/guides/decisions).
