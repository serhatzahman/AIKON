import QtQuick 1.1

Rectangle {
    id: convsPage
    anchors.fill: parent
    color: "#05070A"
    visible: false
    z: 50

    property variant chatManager
    signal conversationSelected(string convId, string title)
    signal backRequested()

    Column {
        anchors.fill: parent

        // Header
        Item {
            width: parent.width
            height: 64

            Rectangle {
                anchors.fill: parent
                color: "#0B1117"
                border.color: "#18222D"
                border.width: 1
            }

            Row {
                anchors.left: parent.left
                anchors.leftMargin: 16
                anchors.verticalCenter: parent.verticalCenter
                spacing: 12

                Text {
                    text: "<- Geri"
                    font.family: "Nokia Pure Text"
                    font.pixelSize: 18
                    font.bold: true
                    color: "#00D2FF"

                    MouseArea {
                        anchors.fill: parent
                        onClicked: { convsPage.backRequested() }
                    }
                }

                Text {
                    text: "Gecmis Sohbetler"
                    font.family: "Nokia Pure Text"
                    font.pixelSize: 20
                    font.bold: true
                    color: "#FFFFFF"
                }
            }
        }

        // Conversation List
        ListView {
            id: convList
            width: parent.width
            height: parent.height - 64
            clip: true
            spacing: 8

            model: ListModel { id: convListModel }

            delegate: Rectangle {
                width: convList.width - 24
                anchors.horizontalCenter: parent.horizontalCenter
                height: 64
                radius: 10
                color: convMouse.pressed ? "#1A2533" : "#111821"
                border.color: "#1B2735"
                border.width: 1

                Column {
                    anchors.fill: parent
                    anchors.margins: 10
                    spacing: 4

                    Text {
                        text: model.title || "Adsiz Sohbet"
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 16
                        font.bold: true
                        color: "#FFFFFF"
                        elide: Text.ElideRight
                        width: parent.width
                    }

                    Text {
                        text: (model.model ? model.model.split(":")[1] : "Claude") + " - " + (model.messages || 1) + " mesaj"
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 12
                        color: "#00D2FF"
                    }
                }

                MouseArea {
                    id: convMouse
                    anchors.fill: parent
                    onClicked: {
                        convsPage.conversationSelected(model.id, model.title);
                        convsPage.visible = false;
                    }
                }
            }
        }
    }

    Connections {
        target: chatManager
        onConversationsUpdated: {
            convListModel.clear();
            try {
                var list = JSON.parse(conversationsJson);
                for (var i = 0; i < list.length; i++) {
                    convListModel.append(list[i]);
                }
            } catch (e) {
                console.log("JSON parse error: " + e);
            }
        }
    }

    function open() {
        if (chatManager) {
            chatManager.fetchConversations();
        }
        visible = true;
    }
}
