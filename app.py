from flask import Flask, render_template_string
import pyotp
import os
from datetime import datetime
import time

app = Flask(__name__)

# Your TOTP secret
TOTP_SECRET = os.environ.get('TOTP_SECRET', 'Y5IV4TS6YC2R4RN6AFGFV37SL2VAD5RO2HCE4DJW3DPHUMSKMKMA')

def generate_otp():
    totp = pyotp.TOTP(TOTP_SECRET)
    return totp.now()

@app.route('/')
def main():
    otp = generate_otp()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    remaining = 30 - (int(time.time()) % 30)
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
        <head>
            <title>OTP Generator</title>
            <meta http-equiv="refresh" content="30">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { 
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: #f0f2f5;
                }
                .container {
                    background: white;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    text-align: center;
                }
                .otp {
                    font-size: 3rem;
                    font-weight: bold;
                    color: #1a73e8;
                    margin: 1rem 0;
                }
                .info {
                    color: #666;
                    margin: 0.5rem 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>OTP Generator</h2>
                <div class="otp">{{otp}}</div>
                <div class="info">Generated at: {{current_time}}</div>
                <div class="info">Refreshes in: {{remaining}} seconds</div>
            </div>
        </body>
    </html>
    ''', otp=otp, current_time=current_time, remaining=remaining)


@app.route('/health')
def health():
    return {"status": "healthy", "timestamp": str(datetime.now())}

@app.route('/api/otp')
def get_otp():
    """JSON endpoint for OTP"""
    otp = generate_otp()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    remaining = 30 - (int(time.time()) % 30)
    
    return jsonify({
        'otp': otp,
        'timestamp': current_time,
        'refresh_in': remaining,
        'status': 'success'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': str(datetime.now())
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)