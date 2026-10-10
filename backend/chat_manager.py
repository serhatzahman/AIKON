# -*- coding: utf-8 -*-
import sys
import os
import json
import sqlite3
import threading

from PySide.QtCore import QObject, Signal, Slot, Property
from .aikon_client import AikonClient


class ChatManager(QObject):
    newMessage = Signal()
    thinkingChanged = Signal()
    statusChanged = Signal()

    def __init__(self, parent=None):
        super(ChatManager, self).__init__(parent)
        self.config_dir = os.path.expanduser("~/.config/aikon-n9")
        if not os.path.exists(self.config_dir):
            try:
                os.makedirs(self.config_dir)
            except Exception:
                pass

        self.db_path = os.path.join(self.config_dir, "aikon_cache.db")
        self.settings_file = os.path.join(self.config_dir, "settings.json")

        self.settings = self._load_settings()
        self.client = AikonClient(
            base_url=self.settings.get("server_url", "http://192.168.8.137:5000"),
            token=self.settings.get("token", "")
        )

        self.active_conversation_id = ""
        self.active_model = self.settings.get("default_model", "anthropic:claude-3-5-sonnet")
        self.web_search_enabled = self.settings.get("web_search", True)

        self._latest_role = ""
        self._latest_text = ""
        self._latest_model = ""
        self._is_thinking = False
        self._status_text = "Hazir"

    def get_latest_role(self):
        return self._latest_role

    def get_latest_text(self):
        return self._latest_text

    def get_latest_model(self):
        return self._latest_model

    def get_is_thinking(self):
        return self._is_thinking

    def get_status_text(self):
        return self._status_text

    latestRole = Property(str, get_latest_role, notify=newMessage)
    latestText = Property(str, get_latest_text, notify=newMessage)
    latestModel = Property(str, get_latest_model, notify=newMessage)
    isThinking = Property(bool, get_is_thinking, notify=thinkingChanged)
    statusText = Property(str, get_status_text, notify=statusChanged)

    def _load_settings(self):
        default_settings = {
            "server_url": "http://192.168.8.137:5000",
            "token": "test",
            "default_model": "anthropic:claude-3-5-sonnet",
            "web_search": True
        }
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    default_settings.update(json.load(f))
            except Exception:
                pass
        return default_settings

    @Slot(str, str, str, bool)
    def save_settings(self, server_url, token, default_model, web_search):
        self.settings["server_url"] = server_url
        self.settings["token"] = token
        self.settings["default_model"] = default_model
        self.settings["web_search"] = web_search
        self.client.set_base_url(server_url)
        self.client.set_token(token)
        self.active_model = default_model
        self.web_search_enabled = web_search
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=2)
            self._status_text = "Ayarlar kaydedildi."
            self.statusChanged.emit()
        except Exception:
            pass

    @Slot(str)
    def sendMessage(self, text):
        if not text.strip():
            return

        conv_id = self.active_conversation_id
        model = self.active_model
        web_search = self.web_search_enabled

        print("[N9 Mesaj Gonderiyor]: " + text)
        print("[Hedef Sunucu]: " + self.client.base_url)

        self._latest_role = "user"
        self._latest_text = text
        self._latest_model = ""
        self._is_thinking = True
        self._status_text = "Dusunuyor..."

        self.newMessage.emit()
        self.thinkingChanged.emit()
        self.statusChanged.emit()

        def _worker():
            res = self.client.send_chat(
                text=text,
                conversation_id=conv_id,
                model=model,
                web_search=web_search
            )

            self._is_thinking = False
            self.thinkingChanged.emit()

            print("[Sunucu Yaniti]: " + str(res))

            if res.get("ok"):
                reply_text = res.get("reply", "")
                reply_model = res.get("model_name") or res.get("model", "")
                new_conv_id = res.get("conversation_id", conv_id)
                self.active_conversation_id = new_conv_id

                self._latest_role = "assistant"
                self._latest_text = reply_text
                self._latest_model = reply_model
                self._status_text = "Hazir"

                self.newMessage.emit()
                self.statusChanged.emit()
            else:
                err_msg = res.get("error", "Baglanti hatasi")
                self._status_text = "Hata: " + str(err_msg)[:20]
                self.statusChanged.emit()

        t = threading.Thread(target=_worker)
        t.daemon = True
        t.start()

    @Slot()
    def startNewChat(self):
        self.active_conversation_id = ""
        self._status_text = "Yeni sohbet baslatildi."
        self.statusChanged.emit()

    @Slot(str)
    def setActiveModel(self, model_id):
        self.active_model = model_id
        self._status_text = "Model: " + model_id.split(":")[-1]
        self.statusChanged.emit()
