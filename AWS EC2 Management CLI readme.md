# ☁ AWS EC2 Management CLI (v1.0)
This repository documents a production-inspired, interactive command-line
<!-- -------------------------------------------------- -->
tool built with **boto3**. It allows users to manage AWS EC2 instances using named profiles and dynamic region selection. The goal is to create a tool that prioritizes clarity, predictability, and safe infrastructure operations over simple abstraction.
<!-- -------------------------------------------------- -->
![CLI Diagram](ec2-cli/cli-diagram.png)
<!-- -------------------------------------------------- -->
![Main Interface](ec2-cli/main-interface.jpg)
<!-- -------------------------------------------------- -->
⚙ Tech Stack
<!-- -------------------------------------------------- -->
• 🐍 Python 3.x – Core Logic
<!-- -------------------------------------------------- -->
• 🛠 boto3 – AWS SDK for Python
<!-- -------------------------------------------------- -->
• ☁ Amazon EC2 – Infrastructure Management
<!-- -------------------------------------------------- -->
• 🔐 AWS IAM – Named Profiles & Security
<!-- -------------------------------------------------- -->
• 🐧 Fedora Linux – Built and Tested Environment
<!-- -------------------------------------------------- -->
⸻
<!-- -------------------------------------------------- -->
📚 *Table of Contents*
<!-- -------------------------------------------------- -->
### Overview & Safety
<!-- -------------------------------------------------- -->
1. 📖 [Project Overview](#project-overview)
<!-- -------------------------------------------------- -->
2. 🛡 [Safety Mechanisms](#safety-mechanisms)
<!-- -------------------------------------------------- -->

3. 📂 [Project Structure](#project-structure)
<!-- -------------------------------------------------- -->
### Installation & Setup
<!-- -------------------------------------------------- -->
4. 📋 [Requirements](#requirements)

5. ⚙ [Installation Guide](#installation-guide)
<!-- -------------------------------------------------- -->
### Workflow
<!-- -------------------------------------------------- -->
6. 🚀 [Usage & Example Workflow](#usage--example-workflow)
<!-- -------------------------------------------------- -->
7. 🚧 [Limitations & Roadmap](#limitations--roadmap)
<!-- -------------------------------------------------- -->
⸻
### IMPORTANT:
<!-- -------------------------------------------------- -->
In this section, I’m going to explain how this CLI manages real AWS infrastructure.
<!-- -------------------------------------------------- -->
(Comment before you read this document: This tool was designed as a learning project to implement real-world architectural patterns. Use it only in controlled environments where you understand the cost and operational impact.)
<!-- -------------------------------------------------- -->
⸻
<!-- -------------------------------------------------- -->
## Project Overview
<!-- -------------------------------------------------- -->
⸻
<!-- -------------------------------------------------- -->
This project provides an inventory-aware interactive CLI that allows users to manage EC2 resources safely and explicitly.
<!-- -------------------------------------------------- -->
It implements structured session handling, contextual validation of tags and instance IDs, and safeguards against destructive mistakes.
<!-- -------------------------------------------------- -->
The core features include:
<!-- -------------------------------------------------- -->
* **Dynamic Selection:** AWS profile and region selection.
<!-- -------------------------------------------------- -->
* **Interactive Inventory:** Always displays current state before actions.
<!-- -------------------------------------------------- -->
* **Creation:** Custom or Default AMI support with mandatory tagging.
<!-- -------------------------------------------------- -->
* **Termination:** By ID or Tag (validated against live inventory).
<!-- -------------------------------------------------- -->
⸻
<!-- -------------------------------------------------- -->
## Safety Mechanisms

This tool incorporates safeguards inspired by real production workflows. The CLI always validates against the current AWS inventory before executing destructive actions.
<!-- -------------------------------------------------- -->
Key safety features implemented:
<!-- -------------------------------------------------- -->
* **DryRun Validation:** Checks permissions before termination.
<!-- -------------------------------------------------- -->
* **Explicit Confirmation:** Prompts (Y/n) before destructive ops.
<!-- -------------------------------------------------- -->
* **State Validation:** Prevents targeting invalid resources.
<!-- -------------------------------------------------- -->
* **Context-Aware Tags:** Validates that tag keys exist and values match.
<!-- -------------------------------------------------- -->
⸻
<!-- -------------------------------------------------- -->
## Project Structure
<!-- -------------------------------------------------- -->
Here is how the application logic is organized to separate concerns effectively:
```text
ec2_cli/
├── aws/          # AWS session and client configuration
├── cli/          # User interaction and menu flow
├── services/     # EC2 operations and business logic
├── utils/        # Validators and shared utilities
└── main.py       # Entry point
pyproject.toml    # Packaging configuration
```
⸻
<!-- -------------------------------------------------- -->
## Requirements
<!-- -------------------------------------------------- -->
Before installing, ensure you have the following environment set up:
<!-- -------------------------------------------------- -->
* **Python 3.10+**
<!-- -------------------------------------------------- -->
* **AWS Credentials:** Configured via `~/.aws/credentials` (Named profiles).
<!-- -------------------------------------------------- -->
* **IAM Permissions:** Sufficient rights for EC2 management.
<!-- -------------------------------------------------- -->
* **Virtual Environment:** Highly recommended.
<!-- -------------------------------------------------- -->
⸻
<!-- -------------------------------------------------- -->
## Installation Guide
<!-- -------------------------------------------------- -->
First, clone the repository to your local machine:
<!-- -------------------------------------------------- -->
```bash
git clone <repository-url>
cd <repository-folder>
```
<!-- -------------------------------------------------- -->
Next, create and activate a virtual environment to isolate dependencies:
<!-- -------------------------------------------------- -->
```bash
python -m venv .venv
source .venv/bin/activate
```
<!-- -------------------------------------------------- -->
Finally, install the project in editable mode:

```bash
pip install -e .
```
<!-- -------------------------------------------------- -->
⸻
## Usage & Example Workflow
<!-- -------------------------------------------------- -->
Once installed, you can run the tool directly without needing python -m:
<!-- -------------------------------------------------- -->
```bash
ec2-cli
```
<!-- -------------------------------------------------- -->
Typical Workflow:
<!-- -------------------------------------------------- -->
Select your AWS Profile.
<!-- -------------------------------------------------- -->
![Paso 1](ec2-cli/select_profile.png)
<!-- -------------------------------------------------- -->
Select the AWS Region.
<!-- -------------------------------------------------- -->
![Paso 2](ec2-cli/select_region.png)
<!-- -------------------------------------------------- -->
Review the existing EC2 instances table.
<!-- -------------------------------------------------- -->
![Paso 3](ec2-cli/list_instances.png)
<!-- -------------------------------------------------- -->
Create: Launch a new instance with specific tags.
<!-- -------------------------------------------------- -->
![Paso 4](ec2-cli/create_instances.png)
<!-- -------------------------------------------------- -->
Terminate: Select instances by ID or Tag (Validated + Confirmed).
<!-- -------------------------------------------------- -->
![Paso 5](ec2-cli/delete_instances.png)
<!-- -------------------------------------------------- -->
⸻
<!-- -------------------------------------------------- -->
## Limitations & Roadmap
<!-- -------------------------------------------------- -->
Current Limitations (v1.0)
<!-- -------------------------------------------------- -->
Interactive mode only (no argument-based CLI yet).
<!-- -------------------------------------------------- -->
No automated unit tests (planned for v2).
<!-- -------------------------------------------------- -->
Scope limited to EC2 standard instances.
<!-- -------------------------------------------------- -->
## Planned Improvements (v2+)
<!-- -------------------------------------------------- -->
Argument-based execution (non-interactive mode).
<!-- -------------------------------------------------- -->
Logging system integration.
<!-- -------------------------------------------------- -->
Unit and integration tests.
<!-- -------------------------------------------------- -->
Structured error handling and retries.
<!-- -------------------------------------------------- -->
Support for additional AWS services.
<!-- -------------------------------------------------- -->

