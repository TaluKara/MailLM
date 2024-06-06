import os.path
import base64
import json
import time

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds_info = json.load(token)
            creds = Credentials.from_authorized_user_info(creds_info, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def list_unread_messages(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
    messages = results.get('messages', [])
    return messages

def mark_as_read(service, msg_id):
    service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()

def get_message(service, msg_id):
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = message.get('payload', {})
    headers = payload.get('headers', [])
    parts = payload.get('parts', [])
    
    subject = ''
    sender = ''
    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']
        if header['name'] == 'From':
            sender = header['value']
    
    body = ''
    if parts:
        body = base64.urlsafe_b64decode(parts[0]['body']['data']).decode('utf-8')
    
    return sender, subject, body

def main():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    
    messages = list_unread_messages(service)
    
    with open('emails.txt', 'w', encoding='utf-8') as f:
        for msg in messages:
            msg_id = msg['id']
            sender, subject, body = get_message(service, msg_id)
            f.write(f'From: {sender}\n')
            f.write(f'Subject: {subject}\n')
            f.write(f'Body: {body}\n')
            f.write('=' * 50 + '\n')
            mark_as_read(service, msg_id)
            time.sleep(0.5)
    print("////////////////////")
    filepath = "emails.txt"
    with open(filepath, "r") as file:
        mailContent = file.read()

    print("AI is analyzing your e-mails.")
    messages = [  # e-mail analyzer
        {
            "role": "user",
            "content": "categorize the following emails in general according to the following format. summarize the emails of each category with the sender under that category. you should not write the full content of the mail. you should only write a summary of the mail. also warn about spam, scams, etc.\nFormat example:\n---\nWORK:\njack@gmail.com -> there is an urgent meeting tomorrow\nbrian@outlook.com -> I would like to apply for a job\nSOCIAL:\nmichelle@gmail.com -> last night's party was really fun\n---\n\nEmails:\n " + mailContent,
                },
    ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
    )
    sum = chat_completion.choices[0].message.content 
    print("Analyze is over. \n\n------------------------\n\n")
    print(sum)

if __name__ == '__main__':
    main()


