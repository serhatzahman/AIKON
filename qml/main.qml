import QtQuick 1.1
import com.nokia.meego 1.0

PageStackWindow {
    id: appWindow
    showStatusBar: true
    showToolBar: false
    initialPage: chatPage

    SilicaTheme { id: theme }

    ChatPage {
        id: chatPage
        orientationLock: PageOrientation.LockPortrait
        tools: null
        chatManager: pyChatManager

        onOpenConversationsRequested: { convsPage.open() }
        onOpenModelSelectorRequested: { modelDialog.open() }
        onOpenSettingsRequested: { settingsDialog.open() }
        onToastRequested: { appWindow.showToast(message) }
    }

    ConversationsPage {
        id: convsPage
        chatManager: pyChatManager
        onConversationSelected: {
            pyChatManager.loadConversationHistory(convId);
            appWindow.showToast("Sohbet: " + title);
        }
        onBackRequested: { convsPage.visible = false }
    }

    ModelSelectorDialog {
        id: modelDialog
        chatManager: pyChatManager
        onModelSelected: {
            chatPage.currentModelName = displayName;
            appWindow.showToast("Model: " + displayName);
        }
    }

    SettingsDialog {
        id: settingsDialog
        chatManager: pyChatManager
    }

    Rectangle {
        id: toast
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 90
        width: Math.min(parent.width - 40, toastText.width + 36)
        height: 42
        radius: 21
        color: "#E600D2FF"
        opacity: 0.0
        z: 999

        Text {
            id: toastText
            anchors.centerIn: parent
            text: ""
            font.pixelSize: 15
            font.bold: true
            color: "#000000"
        }

        SequentialAnimation {
            id: toastAnim
            NumberAnimation { target: toast; property: "opacity"; to: 1.0; duration: 200 }
            PauseAnimation { duration: 2200 }
            NumberAnimation { target: toast; property: "opacity"; to: 0.0; duration: 300 }
        }
    }

    function showToast(msg) {
        if (msg) {
            toastText.text = msg;
            toastAnim.restart();
        }
    }
}
