# -webhook-repo

---

## ⚙️ Setup Instructions

### 1. Clone the repository

bash
git clone https://github.com/your-username/webhook-repo.git
cd webhook-repo

###2. Create virtual environment

#-python -m venv venv
#-.\venv\Scripts\Activate.ps1

#3. Install dependencies
#pip install -r requirements.txt

###4. Configure MongoDB
##Create a .env file in the root directory with:

#MONGO_URI=mongodb+srv://<your-user>:<your-pass>@<cluster-url>/webhook_db?retryWrites=true&w=majority

# Run the Flask App Locally

#python run.py

#### open another terminal and Expose Server with ngrok (for GitHub)

###ngrok http 5000

🔗 Configure GitHub Webhook (in action-repo)
Go to your action-repo on GitHub.

Navigate to:
Settings → Webhooks → Add webhook

Fill in the form:

Payload URL:
https://<your-ngrok-url>/webhook

Content type:
application/json

Events to trigger:
✅ Push
✅ Pull Request
(Bonus: add custom handling for merge if needed)

Click "Add Webhook"
