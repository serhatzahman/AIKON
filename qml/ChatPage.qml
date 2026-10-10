import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    id: chatPage
    orientationLock: PageOrientation.LockPortrait
    tools: null

    property variant chatManager
    property string currentModelName: "Claude 3.5 Sonnet"

    signal openConversationsRequested()
    signal openModelSelectorRequested()
    signal openSettingsRequested()
    signal toastRequested(string message)

    // Sailfish Ambiance Derin Koyu Gradyan
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#0B1624" }
            GradientStop { position: 0.5; color: "#070E18" }
            GradientStop { position: 1.0; color: "#03060B" }
        }
    }

    // Ust Baslik Cubugu (Silica PageHeader)
    Item {
        id: headerBar
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 64
        z: 10

        Rectangle {
            anchors.fill: parent
            color: "#0F1B28"
            border.color: "#1B3047"
            border.width: 1
        }

        Row {
            anchors.left: parent.left
            anchors.leftMargin: 16
            anchors.verticalCenter: parent.verticalCenter
            spacing: 12

            Text {
                text: "Claude"
                font.pixelSize: 24
                font.bold: true
                color: "#FFFFFF"
            }

            Rectangle {
                id: modelButton
                width: 155
                height: 30
                radius: 15
                color: "#15273B"
                border.color: "#00D2FF"
                border.width: 1
                anchors.verticalCenter: parent.verticalCenter

                Text {
                    anchors.centerIn: parent
                    text: chatPage.currentModelName
                    font.pixelSize: 13
                    font.bold: true
                    color: "#00D2FF"
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: { chatPage.openModelSelectorRequested(); }
                }
            }
        }

        Row {
            anchors.right: parent.right
            anchors.rightMargin: 16
            anchors.verticalCenter: parent.verticalCenter
            spacing: 6

            Rectangle {
                width: 8
                height: 8
                radius: 4
                color: thinkingBar.visible ? "#00D2FF" : "#4ADE80"
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                id: statusLabel
                text: thinkingBar.visible ? "Dusunuyor..." : "Cevrimici"
                font.pixelSize: 14
                color: thinkingBar.visible ? "#00D2FF" : "#8EA4B8"
            }
        }
    }

    // Mesaj Listesi
    ListView {
        id: messageListView
        anchors.top: headerBar.bottom
        anchors.bottom: inputDock.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.topMargin: 6
        anchors.bottomMargin: 8
        clip: true
        spacing: 16

        model: ListModel { id: messagesModel }

        PulleyMenu {
            id: pulley
            flickable: messageListView
            items: [
                { actionId: "new_chat", label: "Yeni Sohbet" },
                { actionId: "select_model", label: "Model Degistir" },
                { actionId: "history", label: "Sohbet Gecmisi" },
                { actionId: "settings", label: "Sunucu ve Ayarlar" }
            ]

            onItemTriggered: {
                if (actionId === "new_chat") {
                    messagesModel.clear();
                    chatManager.startNewChat();
                    chatPage.toastRequested("Yeni sohbet baslatildi.");
                } else if (actionId === "select_model") {
                    chatPage.openModelSelectorRequested();
                } else if (actionId === "history") {
                    chatPage.openConversationsRequested();
                } else if (actionId === "settings") {
                    chatPage.openSettingsRequested();
                }
            }
        }

        delegate: ChatBubble {
            role: model.role
            messageText: model.text
            modelName: model.modelName || ""
            onCopyTextRequested: { chatPage.toastRequested("Metin kopyalandi."); }
            onAddToCalendarClicked: { chatPage.toastRequested("Takvime kaydedildi!"); }
        }

        onCountChanged: {
            messageListView.positionViewAtEnd();
        }
    }

    // Dusunme Animasyon Cubugu
    Rectangle {
        id: thinkingBar
        anchors.bottom: inputDock.top
        width: parent.width
        height: 3
        color: "#00D2FF"
        visible: false

        SequentialAnimation on opacity {
            loops: Animation.Infinite
            running: thinkingBar.visible
            NumberAnimation { from: 0.2; to: 1.0; duration: 500 }
            NumberAnimation { from: 1.0; to: 0.2; duration: 500 }
        }
    }

    // Alt Mesaj Giris Paneli (Buyuk font, genis dokunma alani, 70px yukarida)
    Item {
        id: inputDock
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 70
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        height: 56
        z: 20

        Rectangle {
            anchors.fill: parent
            color: "#111C28"
            border.color: "#1E344A"
            border.width: 1
            radius: 16
        }

        Item {
            anchors.fill: parent
            anchors.margins: 6

            Rectangle {
                anchors.left: parent.left
                anchors.right: sendBtn.left
                anchors.rightMargin: 10
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                color: "#172738"
                radius: 12
                border.color: inputField.activeFocus ? "#00D2FF" : "#244260"
                border.width: 1

                TextInput {
                    id: inputField
                    anchors.fill: parent
                    anchors.margins: 8
                    font.pixelSize: 19
                    color: "#FFFFFF"
                    selectByMouse: true

                    Text {
                        anchors.fill: parent
                        text: "Mesajinizi yazin..."
                        font.pixelSize: 19
                        color: "#6D8EAE"
                        visible: !inputField.text.length && !inputField.activeFocus
                    }

                    onAccepted: {
                        var text = inputField.text.trim();
                        if (text.length > 0) {
                            chatManager.sendMessage(text);
                            inputField.text = "";
                        }
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    z: -1
                    onClicked: {
                        inputField.forceActiveFocus();
                        inputField.openSoftwareInputPanel();
                    }
                }
            }

            Rectangle {
                id: sendBtn
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                width: 44
                height: 44
                radius: 22
                color: inputField.text.trim().length > 0 ? "#00D2FF" : "#1C2B3A"

                Text {
                    anchors.centerIn: parent
                    text: ">"
                    font.pixelSize: 22
                    font.bold: true
                    color: inputField.text.trim().length > 0 ? "#000000" : "#557088"
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        var text = inputField.text.trim();
                        if (text.length > 0) {
                            chatManager.sendMessage(text);
                            inputField.text = "";
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: chatManager
        onNewMessage: {
            if (chatManager.latestText) {
                messagesModel.append({
                    role: chatManager.latestRole,
                    text: chatManager.latestText,
                    modelName: chatManager.latestModel
                });
            }
        }
        onThinkingChanged: {
            thinkingBar.visible = chatManager.isThinking;
        }
        onStatusChanged: {
            statusLabel.text = chatManager.statusText;
        }
    }
}
