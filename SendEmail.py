import smtplib
from email.mime.text import MIMEText

# Email Configuration
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
QQ_EMAIL = "2573219557@qq.com"  # User's QQ Email Address
QQ_APP_PASSWORD = "xdcencvaxdyxdiec"  # User's Authorization Code
RECIPIENT = "2573219557@qq.com"  # Default to Send to Self

def send_email(subject, content):
    """Send email via QQ SMTP server"""
    try:
        # Create message
        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = QQ_EMAIL
        msg["To"] = RECIPIENT

        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable TLS encryption
        server.login(QQ_EMAIL, QQ_APP_PASSWORD)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent successfully to {RECIPIENT}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage
    subject = "Test from Raspberry Pi"
    content = "Hello World! This message is sent from my Raspberry Pi."
    
    result = send_email(subject, content)
    if result:
        print("Mission accomplished!")
    else:
        print("Mission failed. Check your credentials and network.")    