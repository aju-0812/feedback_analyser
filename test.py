from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

# Load your service account JSON
credentials = service_account.Credentials.from_service_account_file(
    "service-account.json",
    scopes=["https://www.googleapis.com/auth/ai.generativelanguage"]
)

authed_session = AuthorizedSession(credentials)

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
payload = {
    "contents": [{"parts": [{"text": "Analyze this feedback: I love this product!"}]}]
}

response = authed_session.post(url, json=payload)
print(response.status_code)
print(response.text)
