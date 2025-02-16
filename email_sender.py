import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from typing import List, Optional

class EmailSender:
    def __init__(self, email_host: str, email_port: int, email_user: str, email_password: str):
        """Initialize EmailSender with SMTP server configuration.

        Args:
            email_host (str): SMTP server host (e.g., 'smtp.gmail.com')
            email_port (int): SMTP server port (e.g., 587 for TLS)
            email_user (str): Email username/address
            email_password (str): Email password or app password
        """
        self.email_host = email_host
        self.email_port = email_port
        self.email_user = email_user
        self.email_password = email_password

    def send_email(
        self,
        recipient_email: str,
        sender_name: str,
        email_topic: str,
        email_body: str,
        attachment_files: Optional[List[str]] = None
    ) -> bool:
        """Send an email with optional attachments.

        Args:
            recipient_email (str): Recipient's email address
            sender_name (str): Name to display as sender
            email_topic (str): Email subject line
            email_body (str): Email body content
            attachment_files (Optional[List[str]]): List of file paths to attach

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Create the MIME object
            message = MIMEMultipart()
            message['From'] = f"{sender_name} <{self.email_user}>"
            message['To'] = recipient_email
            message['Subject'] = email_topic

            # Add body to email
            message.attach(MIMEText(email_body, 'plain'))

            # Process attachments if any
            if attachment_files:
                for file_path in attachment_files:
                    try:
                        with open(file_path, 'rb') as file:
                            # Create attachment
                            part = MIMEApplication(file.read(), Name=os.path.basename(file_path))
                            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                            message.attach(part)
                    except Exception as e:
                        print(f"Error attaching file {file_path}: {str(e)}")
                        return False

            # Create SMTP_SSL session for secure connection
            with smtplib.SMTP_SSL(self.email_host, self.email_port) as server:
                server.login(self.email_user, self.email_password)
                server.send_message(message)

            print("Email sent successfully!")
            return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def send_bulk_email(
        self,
        recipient_emails: List[str],
        sender_name: str,
        email_topic: str,
        email_body: str,
        attachment_files: Optional[List[str]] = None
    ) -> dict:
        """Send the same email to multiple recipients.

        Args:
            recipient_emails (List[str]): List of recipient email addresses
            sender_name (str): Name to display as sender
            email_topic (str): Email subject line
            email_body (str): Email body content
            attachment_files (Optional[List[str]]): List of file paths to attach

        Returns:
            dict: A dictionary containing results for each recipient
                 {email: {'success': bool, 'error': Optional[str]}}
        """
        results = {}
        total = len(recipient_emails)

        for index, recipient_email in enumerate(recipient_emails, 1):
            try:
                success = self.send_email(
                    recipient_email=recipient_email,
                    sender_name=sender_name,
                    email_topic=email_topic,
                    email_body=email_body,
                    attachment_files=attachment_files
                )
                results[recipient_email] = {
                    'success': success,
                    'error': None
                }
                print(f"Progress: {index}/{total} - {recipient_email} - {'Success' if success else 'Failed'}")
            except Exception as e:
                results[recipient_email] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"Progress: {index}/{total} - {recipient_email} - Failed: {str(e)}")

        # Print summary
        successful = sum(1 for result in results.values() if result['success'])
        print(f"\nBulk email summary:")
        print(f"Total recipients: {total}")
        print(f"Successful: {successful}")
        print(f"Failed: {total - successful}")

        return results

# Example usage
if __name__ == "__main__":
    # Email configuration
    # Common SMTP settings for different providers:
    # Gmail:    smtp.gmail.com, port 587
    # Outlook:  smtp-mail.outlook.com, port 587
    # Yahoo:    smtp.mail.yahoo.com, port 587
    # Custom:   Your organization's SMTP server and port
    config = {
        'email_host': 'smtp.mail.ru',  # Replace with your email provider's SMTP server
        'email_port': 465,  # Common TLS port, might be different for some providers
        'email_user': 'ttreeq1992@mail.ru',  # Your full email address
        'email_password': 'XVKxAWcF5cQC77e1kAHi'  # Your email password or app-specific password
    }

    # Create EmailSender instance
    sender = EmailSender(**config)

    # Send email
    success = sender.send_email(
        recipient_email='balinteegor@gmail.com',  # Replace with actual recipient
        sender_name='Your Name',  # Replace with your name
        email_topic='Test Email from Python',
        email_body='This is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.his is a test email sent using Python EmailSender class.',
        attachment_files=[]  # Add file paths if you want to attach files
    )

    if success:
        print("Email process completed successfully")
    else:
        print("Email process failed")

    # List of recipient emails
    recipients = [
        'balinteegor@gmail.com',
        # Add more email addresses here
    ]

    # Send bulk email
    results = sender.send_bulk_email(
        recipient_emails=recipients,
        sender_name='Your Name',
        email_topic='Bulk Test Email from Python',
        email_body='This is a test email sent using Python EmailSender class.',
        attachment_files=[]
    )

    # You can process the results if needed
    for email, result in results.items():
        if not result['success']:
            print(f"Failed to send to {email}: {result['error']}")