import QtQuick 1.1

Item {
    id: pulleyMenu

    property variant flickable: parent
    property bool active: false
    property int selectedIndex: -1
    property variant items: []

    signal itemTriggered(int index, string actionId)

    width: flickable ? flickable.width : 480
    height: Math.max(0, -flickable.contentY)
    y: flickable.contentY
    z: 100
    clip: true

    // Pull distance calculation
    property real pullDistance: -flickable.contentY
    property real itemHeight: 48
    property int totalItems: menuColumn.children.length - 1 // minus pulley cue

    onPullDistanceChanged: {
        if (!flickable.dragging) return;
        if (pullDistance > 30) {
            var idx = Math.floor((pullDistance - 30) / itemHeight);
            if (idx >= 0 && idx < totalItems) {
                selectedIndex = idx;
            } else if (idx >= totalItems) {
                selectedIndex = totalItems - 1;
            }
        } else {
            selectedIndex = -1;
        }
    }

    Connections {
        target: flickable
        onMovementEnded: {
            if (selectedIndex >= 0 && selectedIndex < totalItems) {
                var chosenItem = menuColumn.children[selectedIndex];
                if (chosenItem && chosenItem.actionId) {
                    pulleyMenu.itemTriggered(selectedIndex, chosenItem.actionId);
                }
            }
            selectedIndex = -1;
        }
    }

    Column {
        id: menuColumn
        anchors.bottom: parent.bottom
        width: parent.width

        // Children MenuItem elements are placed here dynamically or statically
        Repeater {
            model: pulleyMenu.items
            delegate: Rectangle {
                property string actionId: modelData.actionId
                width: pulleyMenu.width
                height: 44
                color: (index === pulleyMenu.selectedIndex) ? "#2600D2FF" : "transparent"
                border.color: (index === pulleyMenu.selectedIndex) ? "#5500D2FF" : "transparent"
                border.width: 1
                radius: 6

                Text {
                    anchors.centerIn: parent
                    text: modelData.label
                    font.family: "Nokia Pure Text"
                    font.pixelSize: (index === pulleyMenu.selectedIndex) ? 22 : 18
                    font.bold: (index === pulleyMenu.selectedIndex)
                    color: (index === pulleyMenu.selectedIndex) ? "#00D2FF" : "#B0C0D0"
                    opacity: (index === pulleyMenu.selectedIndex) ? 1.0 : 0.7
                }
            }
        }

        // Pulley indicator bar at the bottom of menu
        Item {
            width: parent.width
            height: 16

            Rectangle {
                anchors.centerIn: parent
                width: 48
                height: 3
                radius: 1.5
                color: "#00D2FF"
                opacity: Math.min(1.0, pullDistance / 60.0)
            }
        }
    }
}
