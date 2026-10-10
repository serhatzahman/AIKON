# -*- coding: utf-8 -*-
"""
AIKON Client - Protocol S40/1 Implementation for Nokia N9 (MeeGo Harmattan)
Compatible with both Python 2.7 (MeeGo Harmattan native) and Python 3.x.
"""

import sys
import os
import time
import uuid
import ssl

try:
    # Python 3
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
    from urllib.parse import urljoin, quote
except ImportError:
    # Python 2
    from urllib2 import Request, urlopen, HTTPError, URLError
    from urlparse import urljoin
    from urllib import quote


class S40Response(object):
    """Represents a parsed S40/1 protocol response."""
    def __init__(self, headers, body, raw=""):
        self.headers = headers
        self.body = body
        self.raw = raw
        self.status = headers.get("status", "unknown")

    def get(self, key, default=None):
        return self.headers.get(key, default)

    def is_ok(self):
        return self.status == "ok"

    def __repr__(self):
        return "<S40Response status={0} headers={1} body_len={2}>".format(
            self.status, list(self.headers.keys()), len(self.body)
        )


class AikonClient(object):
    """
    Client for interacting with the AIKON Go Gateway server using S40/1 protocol.
    Designed for MeeGo 1.2 Harmattan (Nokia N9).
    """

    def __init__(self, base_url="https://localhost:443", token="", verify_ssl=False):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.verify_ssl = verify_ssl

        # Prepare SSL context for older devices / self-signed CAs
        self._ssl_context = None
        if hasattr(ssl, "_create_unverified_context") and not self.verify_ssl:
            self._ssl_context = ssl._create_unverified_context()

    def set_token(self, token):
        self.token = token

    def set_base_url(self, base_url):
        self.base_url = base_url.rstrip("/")

    # -------------------------------------------------------------
    # Protocol S40/1 Parsing & Serializing
    # -------------------------------------------------------------
    @staticmethod
    def encode_s40(headers, body=""):
        lines = ["S40/1"]
        for key, value in headers.items():
            if value is not None:
                if sys.version_info[0] < 3 and isinstance(value, unicode):
                    value = value.encode("utf-8")
                lines.append("{0}: {1}".format(key, value))
        lines.append("")
        if body:
            if sys.version_info[0] < 3 and isinstance(body, unicode):
                body = body.encode("utf-8")
            elif sys.version_info[0] >= 3 and isinstance(body, str):
                body = body.encode("utf-8")
            lines.append(body)
        if sys.version_info[0] >= 3:
            return "\n".join([l.decode("utf-8", "ignore") if isinstance(l, bytes) else str(l) for l in lines]).encode("utf-8")
        else:
            return "\n".join([l.encode("utf-8") if isinstance(l, unicode) else str(l) for l in lines])

    @staticmethod
    def decode_s40(raw_bytes):
        """Decodes raw S40/1 response bytes into headers dict and body string."""
        if sys.version_info[0] >= 3:
            raw_text = raw_bytes.decode("utf-8", errors="replace")
        else:
            raw_text = raw_bytes.decode("utf-8", "replace")

        lines = raw_text.splitlines()
        if not lines or lines[0].strip() != "S40/1":
            # If server returned non-S40 response (e.g. plain text or 500 error)
            return S40Response({"status": "raw"}, raw_text, raw=raw_text)

        headers = {}
        body_start_index = len(lines)
        for i in range(1, len(lines)):
            line = lines[i]
            if line == "":
                body_start_index = i + 1
                break
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().lower()] = v.strip()

        body = "\n".join(lines[body_start_index:])
        return S40Response(headers, body, raw=raw_text)

    # -------------------------------------------------------------
    # Low-level Network Dispatcher
    # -------------------------------------------------------------
    def _request(self, endpoint, method="GET", s40_headers=None, body="", raw_body=None, content_type="text/plain; charset=utf-8"):
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        
        if raw_body is not None:
            data = raw_body
        elif s40_headers is not None or body:
            headers_dict = s40_headers or {}
            data = self.encode_s40(headers_dict, body)
        else:
            data = None

        req = Request(url, data=data)
        req.get_method = lambda: method
        req.add_header("User-Agent", "AIKON-N9/1.0 (MeeGo 1.2 Harmattan; Nokia N9)")
        if data is not None:
            req.add_header("Content-Type", content_type)

        if self.token:
            req.add_header("Authorization", "Bearer {0}".format(self.token))

        try:
            if self._ssl_context:
                resp = urlopen(req, context=self._ssl_context, timeout=45)
            else:
                resp = urlopen(req, timeout=45)
            raw_content = resp.read()
            return self.decode_s40(raw_content)
        except HTTPError as e:
            raw_content = e.read() if hasattr(e, "read") else ""
            parsed = self.decode_s40(raw_content)
            parsed.headers["http_status"] = str(e.code)
            return parsed
        except URLError as e:
            return S40Response({"status": "network_error", "error": str(e.reason)}, "")
        except Exception as e:
            return S40Response({"status": "error", "error": str(e)}, "")

    # -------------------------------------------------------------
    # AIKON API Endpoints
    # -------------------------------------------------------------
    def get_health(self):
        """GET /health - Verifies server status, TLS cipher, and app version."""
        return self._request("/health", method="GET")

    def test_echo(self, text="AIKON Nokia N9 bağlantı testi"):
        """POST /echo - Tests server UTF-8 connectivity."""
        return self._request("/echo", method="POST", raw_body=text.encode("utf-8") if sys.version_info[0] >= 3 else text)

    def pair_start(self):
        """POST /v1/pair/start - Generates 6-digit pairing code."""
        return self._request("/v1/pair/start", method="POST", s40_headers={})

    def pair_claim(self, pair_secret):
        """POST /v1/pair/claim - Exchanges pairing secret for permanent Bearer token."""
        return self._request("/v1/pair/claim", method="POST", s40_headers={"pair": pair_secret})

    def get_models(self):
        """
        POST /v1/models - Fetches list of available AI models.
        Returns list of dicts: [{'id', 'name', 'search', 'photos', 'provider', 'cost'}]
        """
        resp = self._request("/v1/models", method="POST", s40_headers={"costs": "1"})
        models = []
        default_model = resp.get("default", "")

        for line in resp.body.splitlines():
            parts = line.split("\t")
            if len(parts) >= 2:
                model_id = parts[0].strip()
                name = parts[1].strip()
                has_search = parts[2].strip() == "1" if len(parts) > 2 else False
                has_photos = parts[3].strip() == "1" if len(parts) > 3 else False
                provider = parts[4].strip() if len(parts) > 4 else "AI"
                cost = parts[5].strip() if len(parts) > 5 else ""

                models.append({
                    "id": model_id,
                    "name": name,
                    "search": has_search,
                    "photos": has_photos,
                    "provider": provider,
                    "cost": cost,
                    "is_default": (model_id == default_model)
                })

        return {"status": resp.status, "default": default_model, "models": models}

    def list_conversations(self):
        """
        POST /v1/conversations - Returns recent and pinned conversations.
        """
        resp = self._request("/v1/conversations", method="POST", s40_headers={"pins": "1", "models": "1"})
        convs = []
        for line in resp.body.splitlines():
            parts = line.split("\t")
            # Format: pinned \t id \t updated-ms \t messages \t model \t title
            if len(parts) >= 6:
                convs.append({
                    "pinned": parts[0].strip() == "1",
                    "id": parts[1].strip(),
                    "updated_ms": int(parts[2].strip()) if parts[2].strip().isdigit() else 0,
                    "messages": int(parts[3].strip()) if parts[3].strip().isdigit() else 0,
                    "model": parts[4].strip(),
                    "title": parts[5].strip()
                })
        return {"status": resp.status, "conversations": convs}

    def get_history(self, conversation_id):
        """
        POST /v1/history - Retrieves full message history of a conversation.
        """
        resp = self._request("/v1/history", method="POST", s40_headers={
            "conversation": conversation_id,
            "images": "1",
            "models": "1"
        })
        
        messages = []
        lines = resp.body.split("\n")
        idx = 0
        while idx < len(lines):
            header = lines[idx].strip()
            if not header:
                idx += 1
                continue
            # Header format: u <len> [i] or a <len> [m=<model>]
            tokens = header.split()
            role = "user" if tokens[0] == "u" else "assistant"
            has_photo = "i" in tokens
            model_id = ""
            for tok in tokens:
                if tok.startswith("m="):
                    model_id = tok[2:]

            idx += 1
            if idx < len(lines):
                text = lines[idx]
                messages.append({
                    "role": role,
                    "text": text,
                    "has_photo": has_photo,
                    "model": model_id
                })
                idx += 1

        return {
            "status": resp.status,
            "older": resp.get("older") == "1",
            "messages": messages
        }

    def send_chat(self, text, conversation_id=None, model=None, web_search=True, image_id=None, user_notes=None):
        """
        POST /v1/chat - Sends a message to the AI.
        Handles multi-part automatic pagination if reply exceeds 2000 chars (more: 1).
        """
        req_id = uuid.uuid4().hex[:16]
        headers = {
            "request": req_id,
            "calendar": "1",
            "local-time": time.strftime("%Y-%m-%d %H:%M"),
            "search": "1" if web_search else "0"
        }
        if conversation_id:
            headers["conversation"] = conversation_id
        if model:
            headers["model"] = model
        if image_id:
            headers["image"] = image_id
        if user_notes:
            headers["instructions"] = user_notes[:300]

        resp = self._request("/v1/chat", method="POST", s40_headers=headers, body=text)
        if not resp.is_ok():
            return {
                "ok": False,
                "status": resp.status,
                "error": resp.get("error", resp.status),
                "body": resp.body
            }

        full_reply = resp.body
        active_conv_id = resp.get("conversation", conversation_id)
        reply_model = resp.get("model", model or "")
        reply_model_name = resp.get("model-name", "")
        searches_done = int(resp.get("searched", "0")) if resp.get("searched", "").isdigit() else 0

        # Automatic paging fetch if response was cut into parts
        next_offset = resp.get("next")
        has_more = resp.get("more") == "1"

        while has_more and next_offset:
            more_resp = self._request("/v1/more", method="POST", s40_headers={
                "request": req_id,
                "offset": next_offset
            })
            if more_resp.is_ok():
                full_reply += more_resp.body
                has_more = more_resp.get("more") == "1"
                next_offset = more_resp.get("next")
            else:
                break

        return {
            "ok": True,
            "status": "ok",
            "conversation_id": active_conv_id,
            "model": reply_model,
            "model_name": reply_model_name,
            "reply": full_reply,
            "searches": searches_done,
            "replayed": resp.get("replayed") == "1"
        }

    def upload_image(self, file_path_or_bytes):
        """
        POST /v1/image - Uploads a JPEG/PNG picture. Returns image ID.
        """
        if isinstance(file_path_or_bytes, (str, bytes)) and os.path.exists(file_path_or_bytes):
            with open(file_path_or_bytes, "rb") as f:
                img_data = f.read()
        else:
            img_data = file_path_or_bytes

        resp = self._request("/v1/image", method="POST", raw_body=img_data, content_type="image/jpeg")
        return {
            "ok": resp.is_ok(),
            "status": resp.status,
            "image_id": resp.get("image", "")
        }

    def transcribe_audio(self, audio_bytes, language="tr"):
        """
        POST /v1/transcribe - Transcribes AMR/WAV audio using Whisper.
        """
        req_id = uuid.uuid4().hex[:16]
        endpoint = "/v1/transcribe?request={0}&lang={1}".format(req_id, quote(language))
        resp = self._request(endpoint, method="POST", raw_body=audio_bytes, content_type="audio/amr")
        return {
            "ok": resp.is_ok(),
            "status": resp.status,
            "text": resp.body.strip()
        }

    def delete_conversation(self, conversation_id):
        """POST /v1/delete - Deletes a conversation from server."""
        resp = self._request("/v1/delete", method="POST", s40_headers={"conversation": conversation_id})
        return resp.is_ok()

    def pin_conversation(self, conversation_id, pinned=True):
        """POST /v1/pin - Pins or unpins a conversation."""
        resp = self._request("/v1/pin", method="POST", s40_headers={
            "conversation": conversation_id,
            "pinned": "1" if pinned else "0"
        })
        return resp.is_ok()
