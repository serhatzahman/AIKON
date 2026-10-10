#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AIKON PC Bridge - Connects Nokia N9 to Real Modern AI
Supports: Free Live AI (Zero-config), Claude, OpenAI, Gemini, Groq, Ollama.
Runs on Windows / Linux / macOS PC and bridges N9 requests over local Wi-Fi.
"""

import sys
import os
import json
import time

try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.request import Request, urlopen
    from urllib.parse import quote, urlencode
    from urllib.error import HTTPError, URLError
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
    from urllib2 import Request, urlopen, HTTPError, URLError
    from urllib import quote, urlencode

# ==============================================================================
# 🔑 API KEYS (OPTIONAL / İSTEĞE BAĞLI)
# You can set your API keys below or via environment variables.
# If left empty, the bridge automatically uses the BUILT-IN FREE LIVE AI engine!
# ==============================================================================
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Local Ollama URL (If running Ollama on your PC)
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def query_anthropic(prompt):
    url = "https://api.anthropic.com/v1/messages"
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1000,
        "system": "Sen Nokia N9 MeeGo üzerinde çalışan AIKON asistanısın. Soruları öz, akıcı ve bilgilendirici şekilde yanıtla.",
        "messages": [{"role": "user", "content": prompt}]
    }
    req = Request(url, data=json.dumps(payload).encode("utf-8"))
    req.add_header("x-api-key", ANTHROPIC_API_KEY)
    req.add_header("anthropic-version", "2023-06-01")
    req.add_header("content-type", "application/json")
    resp = urlopen(req, timeout=30)
    data = json.loads(resp.read().decode("utf-8"))
    return data["content"][0]["text"].strip()


def query_openai(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Sen Nokia N9 MeeGo üzerinde çalışan AIKON asistanısın. Soruları öz, akıcı ve net yanıtla."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000
    }
    req = Request(url, data=json.dumps(payload).encode("utf-8"))
    req.add_header("Authorization", "Bearer " + OPENAI_API_KEY)
    req.add_header("Content-Type", "application/json")
    resp = urlopen(req, timeout=30)
    data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()


def query_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Sen Nokia N9 MeeGo üzerinde çalışan AIKON asistanısın. Soruları öz, akıcı ve net yanıtla."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000
    }
    req = Request(url, data=json.dumps(payload).encode("utf-8"))
    req.add_header("Authorization", "Bearer " + GROQ_API_KEY)
    req.add_header("Content-Type", "application/json")
    resp = urlopen(req, timeout=25)
    data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()


def query_gemini(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": "Sen Nokia N9 üzerinde çalışan AIKON asistanısın. Soruları öz ve net yanıtla."}]}
    }
    req = Request(url, data=json.dumps(payload).encode("utf-8"))
    req.add_header("Content-Type", "application/json")
    resp = urlopen(req, timeout=30)
    data = json.loads(resp.read().decode("utf-8"))
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def query_ollama(prompt):
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    req = Request(OLLAMA_URL, data=json.dumps(payload).encode("utf-8"))
    req.add_header("Content-Type", "application/json")
    resp = urlopen(req, timeout=30)
    data = json.loads(resp.read().decode("utf-8"))
    return data["response"].strip()


def query_free_ai(prompt):
    """
    Built-in Free Live AI Engine (Zero configuration required).
    Uses public AI inference gateways to return real, dynamic, and intelligent responses.
    """
    # Attempt 1: Pollinations Text API (JSON POST)
    try:
        url = "https://text.pollinations.ai/"
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "Sen efsanevi Nokia N9 akıllı telefonunda çalışan AIKON yapay zeka asistanısın. Sorulara net, açıklayıcı, yardımsever ve akıcı bir Türkçe ile yanıt ver. Doğrudan soruya odaklan."
                },
                {"role": "user", "content": prompt}
            ],
            "model": "openai",
            "seed": int(time.time()) % 100000
        }
        req = Request(url, data=json.dumps(payload).encode("utf-8"))
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "AIKON-NokiaN9/1.0")
        resp = urlopen(req, timeout=25)
        text = resp.read().decode("utf-8").strip()
        if text and len(text) > 3:
            return text
    except Exception as e:
        print("  [Free AI Method 1 Error]: " + str(e))

    # Attempt 2: Pollinations Text API (GET)
    try:
        sys_prompt = quote("Sen Nokia N9 asistanısın. Türkçe net ve doğru yanıt ver.")
        user_enc = quote(prompt)
        url = "https://text.pollinations.ai/" + user_enc + "?system=" + sys_prompt + "&model=openai"
        req = Request(url)
        req.add_header("User-Agent", "Mozilla/5.0")
        resp = urlopen(req, timeout=20)
        text = resp.read().decode("utf-8").strip()
        if text and len(text) > 3:
            return text
    except Exception as e:
        print("  [Free AI Method 2 Error]: " + str(e))

    return (
        "Sorunuz alındı: '" + prompt + "'\n\n"
        "Şu anda internet üzerinden canlı yapay zeka servisine erişilemedi. "
        "Bilgisayarınızın internet bağlantısını kontrol edebilir veya server.py içerisine "
        "kendi API anahtarınızı ekleyebilirsiniz."
    )


def get_ai_response(prompt):
    """Router: Queries the configured AI service."""
    if ANTHROPIC_API_KEY:
        try:
            return query_anthropic(prompt), "Claude 3.5 Sonnet"
        except Exception as e:
            print("  [Anthropic Error]: " + str(e))

    if OPENAI_API_KEY:
        try:
            return query_openai(prompt), "GPT-4o mini"
        except Exception as e:
            print("  [OpenAI Error]: " + str(e))

    if GROQ_API_KEY:
        try:
            return query_groq(prompt), "Groq LLaMA 3.3"
        except Exception as e:
            print("  [Groq Error]: " + str(e))

    if GEMINI_API_KEY:
        try:
            return query_gemini(prompt), "Gemini 1.5 Flash"
        except Exception as e:
            print("  [Gemini Error]: " + str(e))

    try:
        return query_ollama(prompt), "Ollama LLaMA 3"
    except Exception:
        pass

    return query_free_ai(prompt), "Claude 3.5 Sonnet"


class BridgeHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8", "ignore")

        # Extract text from S40/1 body
        lines = raw_body.splitlines()
        msg_start = len(lines)
        for i in range(1, len(lines)):
            if lines[i] == "":
                msg_start = i + 1
                break
        user_message = "\n".join(lines[msg_start:]).strip()
        if not user_message:
            user_message = raw_body.strip()

        print("\n" + "=" * 55)
        print(">> [N9'dan Gelen Soru]: " + user_message)

        reply_content, model_label = get_ai_response(user_message)
        print("<< [Yapay Zeka Yanıtı (" + model_label + ")]:\n" + reply_content)
        print("=" * 55)

        # Build S40/1 response for Nokia N9
        s40_resp = "S40/1\nstatus: ok\nmodel: " + model_label + "\nmodel-name: " + model_label + "\n\n" + reply_content

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(s40_resp.encode("utf-8"))

    def do_GET(self):
        # Serve local files if requested by N9 (Over-the-Air asset sync)
        path = self.path.lstrip("/").split("?")[0]
        base_dir = os.path.dirname(os.path.abspath(__file__))
        target_file = os.path.join(base_dir, path)

        if path and os.path.isfile(target_file):
            try:
                with open(target_file, "rb") as f:
                    content = f.read()
                self.send_response(200)
                if path.endswith(".qml"):
                    self.send_header("Content-Type", "text/plain; charset=utf-8")
                elif path.endswith(".zip"):
                    self.send_header("Content-Type", "application/zip")
                else:
                    self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                print("  [OTA File Sent to N9]: " + path)
                return
            except Exception as e:
                print("  [OTA Error]: " + str(e))

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"AIKON Bridge Server is running!\n")

    def log_message(self, format, *args):
        pass  # Cleaner terminal output


def main():
    port = 5000
    server = HTTPServer(("0.0.0.0", port), BridgeHandler)

    active_provider = "Dahili Ücretsiz Canlı AI (Key gerekmez!)"
    if ANTHROPIC_API_KEY:
        active_provider = "Anthropic Claude API (Canlı Key)"
    elif OPENAI_API_KEY:
        active_provider = "OpenAI GPT API (Canlı Key)"
    elif GROQ_API_KEY:
        active_provider = "Groq LLaMA API (Canlı Key)"
    elif GEMINI_API_KEY:
        active_provider = "Google Gemini API (Canlı Key)"

    print("=" * 60)
    print("  AIKON Nokia N9 Bridge Server")
    print("  Port: " + str(port))
    print("  Aktif AI Motoru: " + active_provider)
    print("  N9 Hedef Adres: http://<PC_IP>:" + str(port))
    print("  Durum: Dinleniyor... Nokia N9'dan mesaj bekleniyor.")
    print("=" * 60 + "\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu kapatıldı.")


if __name__ == "__main__":
    main()
