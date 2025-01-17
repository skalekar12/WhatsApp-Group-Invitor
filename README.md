# WhatsApp-Group-Invitor
This project automates the process of sending WhatsApp group invite links to phone numbers that are not currently members of a specific group. It uses Selenium to automate interactions with WhatsApp Web, including waiting for the WhatsApp Web page to load, clicking the necessary buttons, and sending messages to individuals with a group invite link.

Features:
Automated WhatsApp group invite sending: The script identifies missing members from an Excel file and sends them a group invite link.
Waits for necessary manual actions: The script ensures that you have pressed "Continue to Chat" manually before sending the message.
Message customization: You can customize the message that is sent with the group invite link.
Excel-based phone number import: The script loads mobile numbers from an Excel sheet to send messages to.
Important Note:
Currently, the message sending process is not fully automated. For each missing member, you will need to:

Allow WhatsApp API: You will be prompted to allow WhatsApp API to send messages to the phone number.
Click on "Continue to Chat": After clicking the invite link, you must manually click the "Continue to Chat" button.
Press the Send Button: After the chat is loaded, you will need to manually press the send button to send the message.
Note: The full automation for the message sending part is still in progress.

Requirements:
Python 3.x
Selenium
ChromeDriver (ensure the version is compatible with your installed version of Chrome)
Installation:
Clone the repository or download the script files.

Install required Python packages using pip:

bash
Copy
Edit
pip install -r requirements.txt
Download and install ChromeDriver, ensuring it matches your version of Chrome. Place the chromedriver.exe in the same directory as the script or provide the path.

Usage:
Prepare Excel File:

The Excel file must have a column labeled CONTACT NO. containing phone numbers that you want to check.
Update Constants:

Replace the EXCEL_PATH with the correct path to your Excel file.
Update the GROUP_INVITE_LINK with the WhatsApp group invite link.
Run the Script:

bash
Copy
Edit
python whatsapp_group_invite_automator.py
The script will:

Open WhatsApp Web.
Wait for you to scan the QR code.
Load the group members.
Compare the phone numbers in the Excel file with the group members.
Send an invite link to any missing numbers (manual input required for the message sending).
Important Notes:
Manual input required: You need to manually allow the WhatsApp API and click the "Continue to Chat" button before the message can be sent. Once the chat is open, you must press the send button to complete the process.
Make sure your WhatsApp Web is fully loaded and functional before running the script.
Contributing:
Feel free to fork the repository and submit pull requests. Contributions are welcome!
