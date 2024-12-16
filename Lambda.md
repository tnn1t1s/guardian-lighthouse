# Running Guardian Lighthouse on a Lambda Cloud A100 GPU Instance

This guide outlines the steps to set up, rebuild, and run the **Guardian Lighthouse** repository from scratch on a Lambda Cloud A100 GPU instance. Follow these instructions to get started after creating a new instance.

---

## 1. Launch a Lambda A100 Instance
- Log in to your Lambda Cloud account.
- Launch an A100 instance (recommended for larger models like `granite-guardian-3.0-2b`).
- SSH into the instance using the provided credentials.

```bash
ssh -i /path/to/your-key.pem ubuntu@<instance-ip>
```

---

## 2. Update the System and Install Dependencies
Ensure the system is up-to-date and required packages are installed.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip git
```

---

## 3. Clone the Repository
Clone the **Guardian Lighthouse** repository.

```bash
git clone https://github.com/tnn1t1s/guardian-lighthouse.git
cd guardian-lighthouse
```

---

## 4. Set Up a Python Virtual Environment
Create and activate a Python virtual environment to isolate dependencies.

```bash
python3 -m venv safeenv
source safeenv/bin/activate
```

---

## 5. Install Python Dependencies
Install required Python packages listed in `requirements.txt`.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 6. Download and Cache Models
Preload the Hugging Face models to avoid redownloading during runtime.

### For Small Models:
```bash
python -c "
from transformers import AutoTokenizer, AutoModelForSequenceClassification;
AutoTokenizer.from_pretrained('ibm-granite/granite-guardian-hap-38m');
AutoModelForSequenceClassification.from_pretrained('ibm-granite/granite-guardian-hap-38m');
"
```

### For Large Models:
```bash
python -c "
from transformers import AutoTokenizer, AutoModelForCausalLM;
AutoTokenizer.from_pretrained('ibm-granite/granite-guardian-3.0-2b');
AutoModelForCausalLM.from_pretrained('ibm-granite/granite-guardian-3.0-2b');
"
```

---

## 7. Running the Scripts
You can now run the test scripts to evaluate prompts for both small and large models.

### Run Small Model (`guardian-tiny.py`):
```bash
python src/guardian-tiny.py
```

### Run Large Model (`guardian-2b.py`):
```bash
python src/guardian-2b.py
```

---

## 8. Shutting Down the Instance
To avoid incurring costs, terminate the instance after use:
1. Log out of the instance:
   ```bash
   exit
   ```
2. Terminate the instance from the Lambda Cloud dashboard.

---

## 9. Notes and Best Practices
- **GitHub Setup**:
  - Ensure your SSH key is configured for pushing changes to GitHub.
  - Use `git push` to save progress before terminating the instance.
  
- **Model Caching**:
  - Models are cached in `~/.cache/huggingface`. Ensure the instance has sufficient disk space.

- **Testing Prompt File**:
  - Modify `prompts.json` as needed to expand testing scenarios.

---

By following this guide, you can quickly set up and run Guardian Lighthouse on Lambda Cloud A100 GPU instances.


