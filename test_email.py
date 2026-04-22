import sys

print("=" * 70)
print("📧 SmartCredit Email Notification Test")
print("=" * 70)

# Test 1: Import email_utils
print("\n[Test 1] Checking if email_utils.py exists...")
try:
    from email_utils import EmailNotifier
    print("✅ PASS: email_utils.py imported successfully")
except ImportError as e:
    print("❌ FAIL: Cannot import email_utils.py")
    print(f"   Error: {e}")
    print("   Solution: Make sure email_utils.py is in the same directory")
    sys.exit(1)

# Test 2: Initialize EmailNotifier
print("\n[Test 2] Initializing EmailNotifier...")
try:
    notifier = EmailNotifier()
    print("✅ PASS: EmailNotifier initialized")
    print(f"   SMTP Server: {notifier.smtp_server}")
    print(f"   SMTP Port: {notifier.smtp_port}")
    print(f"   Sender Email: {notifier.sender_email}")
except Exception as e:
    print("❌ FAIL: Cannot initialize EmailNotifier")
    print(f"   Error: {e}")
    sys.exit(1)

# Test 3: Check credentials
print("\n[Test 3] Checking email credentials...")
if notifier.sender_email == "your-email@gmail.com":
    print("⚠️  WARNING: Email not configured!")
    print("   You're using the default email: your-email@gmail.com")
    print("   Please update email_utils.py with your actual email")
    print("\n   Open email_utils.py and change:")
    print("   Line 29: self.sender_email = 'your-actual-email@gmail.com'")
    print("   Line 30: self.sender_password = 'your-app-password'")
    
    choice = input("\nDo you want to continue with test email anyway? (y/n): ")
    if choice.lower() != 'y':
        sys.exit(0)
else:
    print("✅ PASS: Email configured")
    print(f"   Using: {notifier.sender_email}")

if notifier.sender_password == "your-app-password":
    print("⚠️  WARNING: Password not configured!")
    print("   You're using the default password")
    sys.exit(1)

# Test 4: Send test email
print("\n[Test 4] Sending test email...")
print("=" * 70)

recipient = input("Enter your email address to receive test email: ").strip()

if not recipient or '@' not in recipient:
    print("❌ Invalid email address")
    sys.exit(1)

print(f"\n📧 Sending test email to: {recipient}")
print("   This may take a few seconds...")

try:
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     color: white; padding: 30px; text-align: center; border-radius: 10px; }
            .content { background: #f8f9fa; padding: 30px; border-radius: 10px; margin-top: 20px; }
            .success { color: #28a745; font-size: 24px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏦 SmartCredit Banking</h1>
                <p>Email System Test</p>
            </div>
            <div class="content">
                <div class="success">✅ SUCCESS!</div>
                <h2>Email Configuration Working!</h2>
                <p>If you're reading this, your SmartCredit email notification system 
                   is properly configured and working.</p>
                <p><strong>Next Steps:</strong></p>
                <ol>
                    <li>Run your Flask application: <code>python app.py</code></li>
                    <li>Register a user with a valid email</li>
                    <li>Submit a credit card application</li>
                    <li>Check your email for the notification</li>
                </ol>
                <p>Have a great day! 🎉</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = """
    SmartCredit Banking - Email System Test
    
    SUCCESS! Email Configuration Working!
    
    If you're reading this, your SmartCredit email notification system is 
    properly configured and working.
    
    Next Steps:
    1. Run your Flask application: python app.py
    2. Register a user with a valid email
    3. Submit a credit card application
    4. Check your email for the notification
    
    Have a great day!
    """
    
    success = notifier.send_email(
        to_email=recipient,
        subject="✅ SmartCredit Email Test - Configuration Successful",
        html_content=html_content,
        text_content=text_content
    )
    
    if success:
        print("\n" + "=" * 70)
        print("✅ TEST PASSED!")
        print("=" * 70)
        print("Email sent successfully!")
        print(f"\n📬 Check your inbox: {recipient}")
        print("   (Also check spam/junk folder)")
        print("\nIf you received the email, your configuration is correct!")
        print("\nYou can now run: python app.py")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("❌ TEST FAILED!")
        print("=" * 70)
        print("Email sending failed. Check the error message above.")
        print("\nCommon issues:")
        print("1. Wrong email/password in email_utils.py")
        print("2. Gmail: Need to use App Password (not regular password)")
        print("3. 2-Step Verification not enabled on Gmail")
        print("4. Firewall blocking SMTP connection")
        print("\nSee EMAIL_SETUP_GUIDE.md for detailed troubleshooting")
        print("=" * 70)
        
except Exception as e:
    print("\n" + "=" * 70)
    print("❌ ERROR OCCURRED!")
    print("=" * 70)
    print(f"Error: {str(e)}")
    print("\nDetailed error information:")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 70)
    sys.exit(1)