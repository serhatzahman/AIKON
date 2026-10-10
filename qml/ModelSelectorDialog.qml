import QtQuick 1.1

Rectangle {
    id: modelDialog
    anchors.fill: parent
    color: "#E6000000" // Modal overlay
    visible: false
    z: 100

    property variant chatManager
    signal modelSelected(string modelId, string displayName)

    // Inner Dialog Card
    Rectangle {
        id: card
        width: parent.width - 32
        height: Math.min(parent.height - 80, 520)
        anchors.centerIn: parent
        color: "#0F161E"
        border.color: "#00D2FF"
        border.width: 1
        radius: 14

        Column {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 12

            Text {
                text: "Yapay Zeka Modeli Secin"
                font.family: "Nokia Pure Text"
                font.pixelSize: 22
                font.bold: true
                color: "#FFFFFF"
            }

            Text {
                text: "Tum saglayicilar AIKON ag gecidi uzerinden sunulur."
                font.family: "Nokia Pure Text"
                font.pixelSize: 14
                color: "#8FA3B8"
            }

            Rectangle {
                width: parent.width
                height: 1
                color: "#1E2A38"
            }

            ListView {
                id: modelList
                width: parent.width
                height: parent.height - 110
                clip: true
                spacing: 8

                model: ListModel {
                    id: defaultModelsModel
                    ListElement { modelId: "anthropic:claude-3-5-sonnet"; name: "Claude 3.5 Sonnet"; provider: "Anthropic"; hasSearch: true; hasVision: true }
                    ListElement { modelId: "anthropic:claude-3-haiku"; name: "Claude 3.5 Haiku"; provider: "Anthropic"; hasSearch: true; hasVision: false }
                    ListElement { modelId: "openai:gpt-4o"; name: "GPT-4o"; provider: "OpenAI"; hasSearch: true; hasVision: true }
                    ListElement { modelId: "gemini:gemini-1-5-pro"; name: "Gemini 1.5 Pro"; provider: "Google"; hasSearch: true; hasVision: true }
                    ListElement { modelId: "xai:grok-2"; name: "Grok 2"; provider: "xAI"; hasSearch: true; hasVision: false }
                }

                delegate: Rectangle {
                    width: modelList.width
                    height: 56
                    radius: 8
                    color: itemMouseArea.pressed ? "#1E2D3D" : "#141D26"
                    border.color: "#202E3D"
                    border.width: 1

                    Row {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 10

                        Column {
                            width: parent.width - 70
                            spacing: 4

                            Text {
                                text: model.name
                                font.family: "Nokia Pure Text"
                                font.pixelSize: 17
                                font.bold: true
                                color: "#FFFFFF"
                            }

                            Text {
                                text: model.provider + (model.hasSearch ? " - Web Aramasi" : "") + (model.hasVision ? " - Gorme" : "")
                                font.family: "Nokia Pure Text"
                                font.pixelSize: 12
                                color: "#00D2FF"
                            }
                        }

                        Text {
                            anchors.verticalCenter: parent.verticalCenter
                            text: "Sec"
                            font.family: "Nokia Pure Text"
                            font.pixelSize: 15
                            font.bold: true
                            color: "#8FA3B8"
                        }
                    }

                    MouseArea {
                        id: itemMouseArea
                        anchors.fill: parent
                        onClicked: {
                            chatManager.setActiveModel(model.modelId);
                            modelDialog.modelSelected(model.modelId, model.name);
                            modelDialog.visible = false;
                        }
                    }
                }
            }
        }
    }

    // Dismiss on background tap
    MouseArea {
        anchors.fill: parent
        z: -1
        onClicked: { modelDialog.visible = false }
    }

    function open() {
        visible = true;
    }
}
