import QtQuick 1.1

Rectangle {
    id: settingsDialog
    anchors.fill: parent
    color: "#F0000000"
    visible: false
    z: 100

    property variant chatManager

    Rectangle {
        width: parent.width - 32
        height: Math.min(parent.height - 60, 620)
        anchors.centerIn: parent
        color: "#0D131A"
        border.color: "#00D2FF"
        border.width: 1
        radius: 14

        Flickable {
            anchors.fill: parent
            anchors.margins: 18
            contentHeight: contentCol.height + 20
            clip: true

            Column {
                id: contentCol
                width: parent.width
                spacing: 16

                Text {
                    text: "AIKON Sunucu & Ayarlar"
                    font.family: "Nokia Pure Text"
                    font.pixelSize: 22
                    font.bold: true
                    color: "#FFFFFF"
                }

                // Server URL Field
                Column {
                    width: parent.width
                    spacing: 6

                    Text {
                        text: "Sunucu Adresi (Gateway URL):"
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 14
                        color: "#8FA3B8"
                    }

                    Rectangle {
                        width: parent.width
                        height: 48
                        radius: 8
                        color: "#151F2A"
                        border.color: serverInput.focus ? "#00D2FF" : "#243242"
                        border.width: 1

                        TextInput {
                            id: serverInput
                            anchors.fill: parent
                            anchors.margins: 10
                            text: "https://localhost:443"
                            font.family: "Nokia Pure Text"
                            font.pixelSize: 16
                            color: "#FFFFFF"
                            selectByMouse: true
                        }
                    }
                }

                // Bearer Token / Pairing Field
                Column {
                    width: parent.width
                    spacing: 6

                    Text {
                        text: "Erisim Anahtari (Bearer Token):"
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 14
                        color: "#8FA3B8"
                    }

                    Rectangle {
                        width: parent.width
                        height: 48
                        radius: 8
                        color: "#151F2A"
                        border.color: tokenInput.focus ? "#00D2FF" : "#243242"
                        border.width: 1

                        TextInput {
                            id: tokenInput
                            anchors.fill: parent
                            anchors.margins: 10
                            text: ""
                            echoMode: TextInput.Password
                            font.family: "Nokia Pure Text"
                            font.pixelSize: 16
                            color: "#FFFFFF"
                            selectByMouse: true
                        }
                    }
                }

                // Web Search Toggle Switch
                Row {
                    width: parent.width
                    spacing: 14

                    Rectangle {
                        id: searchSwitch
                        width: 54
                        height: 32
                        radius: 16
                        color: searchActive ? "#00D2FF" : "#202C38"
                        property bool searchActive: true

                        Rectangle {
                            width: 26
                            height: 26
                            radius: 13
                            color: "#FFFFFF"
                            anchors.verticalCenter: parent.verticalCenter
                            x: searchSwitch.searchActive ? parent.width - width - 3 : 3
                            Behavior on x { NumberAnimation { duration: 150 } }
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: { searchSwitch.searchActive = !searchSwitch.searchActive }
                        }
                    }

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: "Web Aramasi Aktif"
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 16
                        color: "#E2E8F0"
                    }
                }

                // Action Buttons
                Row {
                    width: parent.width
                    spacing: 12

                    // Save Button
                    Rectangle {
                        width: (parent.width - 12) / 2
                        height: 46
                        radius: 8
                        color: "#00D2FF"

                        Text {
                            anchors.centerIn: parent
                            text: "Kaydet"
                            font.family: "Nokia Pure Text"
                            font.pixelSize: 16
                            font.bold: true
                            color: "#000000"
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                chatManager.save_settings(
                                    serverInput.text.trim(),
                                    tokenInput.text.trim(),
                                    chatManager.active_model,
                                    searchSwitch.searchActive
                                );
                                settingsDialog.visible = false;
                            }
                        }
                    }

                    // Close Button
                    Rectangle {
                        width: (parent.width - 12) / 2
                        height: 46
                        radius: 8
                        color: "#1B2735"

                        Text {
                            anchors.centerIn: parent
                            text: "Kapat"
                            font.family: "Nokia Pure Text"
                            font.pixelSize: 16
                            font.bold: true
                            color: "#FFFFFF"
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: { settingsDialog.visible = false }
                        }
                    }
                }
            }
        }
    }

    function open() {
        if (chatManager) {
            serverInput.text = chatManager.settings.server_url || "";
            tokenInput.text = chatManager.settings.token || "";
            searchSwitch.searchActive = chatManager.web_search_enabled;
        }
        visible = true;
    }
}
