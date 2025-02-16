from flask import Flask, request, jsonify
from email_sender import EmailSender
import os

app = Flask(__name__)

# Global email sender instance
email_sender = None

@app.route('/api/config', methods=['POST'])
def set_email_config():
    try:
        data = request.get_json()
        required_fields = ['email_host', 'email_port', 'email_user', 'email_password']
        
        # Validate required fields
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': f'Missing required fields. Required: {required_fields}'
            }), 400

        global email_sender
        email_sender = EmailSender(
            email_host=data['email_host'],
            email_port=int(data['email_port']),
            email_user=data['email_user'],
            email_password=data['email_password']
        )

        return jsonify({
            'success': True,
            'message': 'Email configuration set successfully'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/send', methods=['POST'])
def send_email():
    if not email_sender:
        return jsonify({
            'success': False,
            'error': 'Email configuration not set. Please configure email settings first.'
        }), 400

    try:
        data = request.get_json()
        required_fields = ['recipient_emails', 'sender_name', 'email_topic', 'email_body']
        
        # Validate required fields
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': f'Missing required fields. Required: {required_fields}'
            }), 400

        # Handle attachments if provided
        attachment_files = []
        if 'attachment_files' in data and data['attachment_files']:
            attachment_files = data['attachment_files']

        # Send bulk email
        results = email_sender.send_bulk_email(
            recipient_emails=data['recipient_emails'],
            sender_name=data['sender_name'],
            email_topic=data['email_topic'],
            email_body=data['email_body'],
            attachment_files=attachment_files
        )

        return jsonify({
            'success': True,
            'results': results
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)