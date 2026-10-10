import QtQuick 1.1

Rectangle {
    id: coverRoot
    width: 240
    height: 360
    color: "#070C12"

    property string modelName: "Claude 3.5"
    property string lastMessage: "Hazir"
    property bool isThinking: false

    Rectangle {
        anchors.fill: parent
        anchors.margins: 8
        radius: 12
        color: "#0F1620"
        border.color: "#00D2FF"
        border.width: 1

        Column {
            anchors.fill: parent
            anchors.margins: 14
            spacing: 10

            // Header in Cover
            Row {
                spacing: 8
                Rectangle {
                    width: 10
                    height: 10
                    radius: 5
                    color: isThinking ? "#00D2FF" : "#4ADE80"
                    anchors.verticalCenter: parent.verticalCenter
                }
                Text {
                    text: "AIKON"
                    font.family: "Nokia Pure Text"
                    font.pixelSize: 18
                    font.bold: true
                    color: "#FFFFFF"
                }
            }

            Text {
                text: modelName
                font.family: "Nokia Pure Text"
                font.pixelSize: 13
                color: "#00D2FF"
            }

            Rectangle {
                width: parent.width
                height: 1
                color: "#1B2735"
            }

            Text {
                text: isThinking ? "Claude dusunuyor..." : lastMessage
                font.family: "Nokia Pure Text"
                font.pixelSize: 14
                color: "#C2D2E2"
                wrapMode: Text.Wrap
                maximumLineCount: 7
                elide: Text.ElideRight
                width: parent.width
            }
        }
    }
}
