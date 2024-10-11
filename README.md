[![Run Python Script](https://github.com/prudhvi1709/gitactions/actions/workflows/run-python-script.yml/badge.svg?branch=main&event=push)](https://github.com/prudhvi1709/gitactions/actions/workflows/run-python-script.yml)


## Workflow Overview

The workflow is defined in the `.github/workflows/run-python-script.yml` file and is scheduled to run every Sunday at midnight (UTC). It checks out the repository, sets up Python, installs dependencies, and runs the specified Python script.

## Prerequisites

1. **GitHub Repository**: Ensure you have a GitHub repository where you want to set up this workflow.
2. **Python Script**: Place your Python script (e.g., `script.py`) in the root of your repository or adjust the path in the workflow file accordingly.
3. **Requirements File**: If your script has dependencies, create a `requirements.txt` file listing all required packages.

## Setting Up Secrets

To securely use sensitive information (like tokens), you need to set up GitHub Secrets:

1. Go to your GitHub repository.
2. Click on `Settings`.
3. In the left sidebar, click on `Secrets and variables`, then `Actions`.
4. Click on `New repository secret`.
5. Add a secret with the name `PERSNOL_TOKEN` and the corresponding value.

## Modifying the Workflow

If you need to change the schedule or Python version, edit the `.github/workflows/run-python-script.yml` file:

- **Cron Schedule**: Modify the `cron` value under the `on.schedule` section to change when the workflow runs.
- **Python Version**: Change the `python-version` value under the `Set up Python` step to the desired version.

## Running the Workflow

Once everything is set up, the workflow will automatically run based on the defined schedule. You can check the workflow runs in the `Actions` tab of your GitHub repository.

## Troubleshooting

- If the workflow fails, check the logs in the `Actions` tab for error messages.
- Ensure that all dependencies are correctly listed in `requirements.txt`.
