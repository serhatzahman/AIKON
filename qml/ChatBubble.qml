import QtQuick 1.1

Item {
    id: bubbleRoot

    property string role: "assistant"
    property string messageText: ""
    property string modelName: ""
    property bool isUser: (role === "user")

    signal addToCalendarClicked(string eventDetails)
    signal copyTextRequested(string text)

    width: parent ? parent.width : 480
    height: bubbleRect.height + 16

    property bool hasCalendarEvent: !isUser && messageText.indexOf("EVENT:") !== -1

    Rectangle {
        id: bubbleRect
        anchors {
            left: isUser ? undefined : parent.left
            right: isUser ? parent.right : undefined
            leftMargin: isUser ? 0 : 14
            rightMargin: isUser ? 14 : 0
        }
        
        // Genis ve ferah Sailfish cam balonu (Ekranin %90ina kadar yayilir)
        width: Math.min(bubbleRoot.width * 0.90, Math.max(200, textMeasure.paintedWidth + 36))
        height: contentCol.height + 26
        radius: 18

        // Sailfish Silica Ambiance tonlari
        color: isUser ? "#18456E" : "#111A24"
        border.color: isUser ? "#2768A3" : "#1F3144"
        border.width: 1

        Text {
            id: textMeasure
            visible: false
            text: bubbleRoot.cleanDisplayMessage(bubbleRoot.messageText)
            font.pixelSize: 21
        }

        Column {
            id: contentCol
            anchors {
                left: parent.left
                right: parent.right
                top: parent.top
                margins: 14
            }
            spacing: 8

            // Model Rozeti
            Row {
                visible: !isUser && modelName.length > 0
                spacing: 8

                Rectangle {
                    width: 9
                    height: 9
                    radius: 4.5
                    color: "#00D2FF"
                    anchors.verticalCenter: parent.verticalCenter
                }

                Text {
                    text: modelName
                    font.pixelSize: 13
                    font.bold: true
                    color: "#00D2FF"
                }
            }

            // Buyuk ve Rahat Okunan Mesaj Metni (21 piksel)
            Text {
                id: mainText
                text: bubbleRoot.cleanDisplayMessage(bubbleRoot.messageText)
                font.pixelSize: 21
                color: isUser ? "#FFFFFF" : "#F0F4F8"
                wrapMode: Text.Wrap
                width: parent.width
                lineHeight: 1.3
            }

            // Takvim Aksiyon Butonu
            Rectangle {
                visible: bubbleRoot.hasCalendarEvent
                width: parent.width
                height: 40
                radius: 10
                color: "#163826"
                border.color: "#2C804D"
                border.width: 1

                Text {
                    anchors.centerIn: parent
                    text: "+ N9 Takvimine Ekle"
                    font.pixelSize: 15
                    font.bold: true
                    color: "#4ADE80"
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: { bubbleRoot.addToCalendarClicked(bubbleRoot.messageText); }
                }
            }
        }

        MouseArea {
            anchors.fill: parent
            z: -1
            onPressAndHold: { bubbleRoot.copyTextRequested(mainText.text); }
        }
    }

    function cleanDisplayMessage(raw) {
        if (!raw) return "";
        var lines = raw.split("\n");
        var filtered = [];
        for (var i = 0; i < lines.length; i++) {
            var l = lines[i];
            if (l.indexOf("EVENT:") === 0) continue;
            filtered.push(l);
        }
        return filtered.join("\n").trim();
    }
}
