"""
Lightweight demo server for OKA + Minted bot.
Proxies chat requests to Claude API. No complex dependencies.
Deploy to VPS: python3 demo_server.py

Endpoints:
  POST /v1/missioncanvas/oka-chat  — OKA learning companion
  POST /api/chat                    — Minted voice bot (text only, no TTS)
  POST /api/tts                     — Rime TTS proxy (if RIME_API_KEY set)
  GET  /health                      — Health check
"""

import os
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PORT = int(os.environ.get('DEMO_PORT', '7890'))
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
RIME_API_KEY = os.environ.get('RIME_API_KEY', '')
ALLOW_ORIGIN = os.environ.get('ALLOW_ORIGIN', '*')

# Load OKA system prompt
OKA_PROMPT_PATH = Path(__file__).parent.parent / 'mission-canvas' / 'oka_system_prompt_active.md'
OKA_SYSTEM_PROMPT = ''
if OKA_PROMPT_PATH.exists():
    OKA_SYSTEM_PROMPT = OKA_PROMPT_PATH.read_text()
else:
    # Fallback minimal prompt
    OKA_SYSTEM_PROMPT = "You are Oka, a friendly dog companion who helps an 8-year-old girl named Nora learn. Keep responses to 1-4 short spoken sentences. Ask only ONE thing at a time."


def call_claude(system_prompt, messages, model='claude-sonnet-4-20250514'):
    """Call Claude API and return the response text."""
    payload = json.dumps({
        'model': model,
        'max_tokens': 300,
        'system': system_prompt,
        'messages': messages
    }).encode()

    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01'
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
        return data['content'][0]['text']


def call_rime_tts(text, speaker='luna', speed=0.82, model='arcana'):
    """Call Rime TTS API and return MP3 bytes."""
    payload = json.dumps({
        'text': text,
        'speaker': speaker,
        'modelId': model,
        'speedAlpha': speed,
        'audioFormat': 'mp3'
    }).encode()

    req = urllib.request.Request(
        'https://users.rime.ai/v1/rime-tts',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {RIME_API_KEY}'
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()


class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/health' or self.path == '/api/health':
            self._json_response(200, {'status': 'ok', 'oka': bool(OKA_SYSTEM_PROMPT), 'tts': bool(RIME_API_KEY)})
        else:
            self._json_response(404, {'error': 'not found'})

    def do_POST(self):
        body = self._read_body()
        if body is None:
            return

        if self.path == '/v1/missioncanvas/oka-chat':
            self._handle_oka(body)
        elif self.path == '/api/chat':
            self._handle_chat(body)
        elif self.path == '/api/tts':
            self._handle_tts(body)
        else:
            self._json_response(404, {'error': 'not found'})

    def _handle_oka(self, body):
        message = body.get('message', '')
        history = body.get('history', [])
        session_id = body.get('session_id', 'demo')

        messages = []
        for h in history[-12:]:
            role = 'assistant' if h.get('role') == 'assistant' else 'user'
            messages.append({'role': role, 'content': str(h.get('content', ''))})
        messages.append({'role': 'user', 'content': message})

        try:
            response = call_claude(OKA_SYSTEM_PROMPT, messages)
            updated_history = history + [
                {'role': 'user', 'content': message},
                {'role': 'assistant', 'content': response}
            ]
            self._json_response(200, {
                'status': 'ok',
                'session_id': session_id,
                'response': response,
                'history': updated_history[-14:]
            })
        except Exception as e:
            self._json_response(500, {'status': 'error', 'message': str(e)})

    def _handle_chat(self, body):
        message = body.get('message', '')
        system = body.get('system', 'You are a helpful voice agent.')
        history = body.get('history', [])

        messages = []
        for h in history[-12:]:
            role = 'assistant' if h.get('role') == 'assistant' else 'user'
            messages.append({'role': role, 'content': str(h.get('content', ''))})
        messages.append({'role': 'user', 'content': message})

        try:
            response = call_claude(system, messages)
            self._json_response(200, {'response': response})
        except Exception as e:
            self._json_response(500, {'error': str(e)})

    def _handle_tts(self, body):
        if not RIME_API_KEY:
            self._json_response(503, {'error': 'TTS not configured'})
            return

        text = body.get('text', '')
        speaker = body.get('speaker', 'luna')
        speed = body.get('speed', 0.82)
        model = body.get('model', 'arcana')

        try:
            audio = call_rime_tts(text, speaker, speed, model)
            self.send_response(200)
            self._cors_headers()
            self.send_header('Content-Type', 'audio/mpeg')
            self.send_header('Content-Length', str(len(audio)))
            self.end_headers()
            self.wfile.write(audio)
        except Exception as e:
            self._json_response(500, {'error': str(e)})

    def _read_body(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(length)
            return json.loads(raw) if raw else {}
        except (json.JSONDecodeError, ValueError):
            self._json_response(400, {'error': 'invalid JSON'})
            return None

    def _json_response(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self._cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _cors_headers(self):
        # Only add CORS headers when running standalone (no nginx proxy)
        # When behind nginx, nginx handles CORS to avoid duplicate headers
        if not os.environ.get('BEHIND_NGINX'):
            self.send_header('Access-Control-Allow-Origin', ALLOW_ORIGIN)
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, fmt, *args):
        print(f"[demo] {args[0]} {args[1]}")


if __name__ == '__main__':
    if not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set")
        exit(1)
    print(f"Demo server starting on :{PORT}")
    print(f"  OKA prompt: {'loaded' if OKA_SYSTEM_PROMPT else 'MISSING'} ({len(OKA_SYSTEM_PROMPT)} chars)")
    print(f"  Rime TTS:   {'available' if RIME_API_KEY else 'not configured'}")
    print(f"  Endpoints:  /v1/missioncanvas/oka-chat, /api/chat, /api/tts, /health")
    HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
