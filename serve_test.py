#!/usr/bin/env python3
"""
Simple HTTP server to serve the test interface and avoid CORS issues.
"""
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def main():
    # Change to the project directory
    os.chdir('/Users/yuvalgilad/Documents/mvp-generation-agent')
    
    with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
        print(f"🌐 Test Interface Server starting on http://localhost:{PORT}")
        print(f"📁 Serving from: {os.getcwd()}")
        print(f"🎯 Test Interface: http://localhost:{PORT}/frontend-test.html")
        print(f"🔧 Backend API: http://localhost:8003")
        print("=" * 60)
        print("Press Ctrl+C to stop the server")
        
        # Auto-open the test interface
        webbrowser.open(f'http://localhost:{PORT}/frontend-test.html')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
            sys.exit(0)

if __name__ == "__main__":
    main()
