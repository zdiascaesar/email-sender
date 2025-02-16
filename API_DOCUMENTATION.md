# Email Sender API Documentation

This API provides endpoints to configure and send emails through a RESTful interface.

## Base URL

```
http://your-domain.com
```

## Endpoints

### 1. Configure Email Settings

Sets up the email server configuration for sending emails.

```
POST /api/config
```

#### Request Body

```json
{
    "email_host": "smtp.example.com",
    "email_port": 587,
    "email_user": "your-email@example.com",
    "email_password": "your-password"
}
```

#### Required Fields
- `email_host` (string): SMTP server hostname
- `email_port` (integer): SMTP server port
- `email_user` (string): Email account username
- `email_password` (string): Email account password

#### Success Response

```json
{
    "success": true,
    "message": "Email configuration set successfully"
}
```

#### Error Response

```json
{
    "success": false,
    "error": "Missing required fields. Required: ['email_host', 'email_port', 'email_user', 'email_password']"
}
```

### 2. Send Email

Sends emails to one or multiple recipients.

```
POST /api/send
```

#### Request Body

```json
{
    "recipient_emails": ["recipient1@example.com", "recipient2@example.com"],
    "sender_name": "John Doe",
    "email_topic": "Meeting Invitation",
    "email_body": "Hello, this is the email content.",
    "attachment_files": ["file1.pdf", "file2.docx"] // Optional
}
```

#### Required Fields
- `recipient_emails` (array): List of recipient email addresses
- `sender_name` (string): Name of the sender
- `email_topic` (string): Subject of the email
- `email_body` (string): Content of the email
- `attachment_files` (array, optional): List of attachment file names

#### Success Response

```json
{
    "success": true,
    "results": [
        // Array of results for each recipient
    ]
}
```

#### Error Responses

1. Configuration Not Set
```json
{
    "success": false,
    "error": "Email configuration not set. Please configure email settings first."
}
```

2. Missing Required Fields
```json
{
    "success": false,
    "error": "Missing required fields. Required: ['recipient_emails', 'sender_name', 'email_topic', 'email_body']"
}
```

## Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Missing or invalid parameters
- `500 Internal Server Error`: Server-side error

## Notes

1. Make sure to configure email settings using the `/api/config` endpoint before attempting to send emails.
2. All requests must include Content-Type: application/json in the headers.
3. Attachment files must be accessible on the server.
4. The API uses JSON for both request and response bodies.