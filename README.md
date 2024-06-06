# Gmail Unread Messages Analyzer

This project fetches unread messages from your Gmail inbox, saves them to a text file, and analyzes their content using an AI model. The analysis categorizes the emails and provides summaries while warning about potential spam or scams.

## Features

- Authenticate with Gmail using OAuth2.
- List unread messages in your Gmail inbox.
- Fetch email details (sender, subject, and body).
- Mark emails as read.
- Save email content to a text file.
- Analyze and categorize emails using an AI model.
- Summarize email content and warn about potential spam/scams.

## Requirements

- Python 3.7+
- Google API Client Library
- Google OAuth Client Library
- groq Python Library

- 
Example output from running the script:
```
(base) talu in ~/Projects/python/MailLM λ python main.py 
////////////////////
AI is analyzing your e-mails.
Analyze is over. 

------------------------


Here is the categorization of the emails:

---
WORK:
talukudasai@gmail.com -> reminder about tomorrow's business meeting
--

SOCIAL:
talukudasai@gmail.com -> invitation to go to the beach tomorrow with Ali
talukudasai@gmail.com -> social invitation to a fun event (party not specified)

SPAM/SCAM:
talukudasai@gmail.com -> suspicious email with gibberish content (possible spam or phishing attempt)

Warning: Be cautious with the email with a suspicious body content, it may be a spam or phishing attempt. Do not respond or click on any links from unknown senders.
```
