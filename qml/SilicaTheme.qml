import QtQuick 1.1

Item {
    id: theme

    // AMOLED Deep Black & Translucent Glass Palette
    property color backgroundColor: "#000000"
    property color backgroundDarkColor: "#05070A"
    property color glassColor: "#1A222B"
    property color glassBorderColor: "#2A3A4A"
    
    // Message Bubbles
    property color userBubbleColor: "#15334E"
    property color userBubbleBorder: "#24527D"
    property color assistantBubbleColor: "#12171E"
    property color assistantBubbleBorder: "#1E2733"

    // Text & Accents
    property color primaryColor: "#FFFFFF"
    property color secondaryColor: "#9EAFBF"
    property color highlightColor: "#00D2FF"      // Silica Electric Cyan
    property color highlightDimColor: "#007A99"
    property color accentColor: "#FF6633"         // Claude Ember
    property color errorColor: "#FF4444"

    // Typography (Nokia Pure font on Harmattan)
    property string fontFamily: "Nokia Pure Text"
    property int fontSizeHuge: 32
    property int fontSizeLarge: 26
    property int fontSizeMedium: 21
    property int fontSizeNormal: 18
    property int fontSizeSmall: 15
    property int fontSizeTiny: 12

    // Layout Metrics for 854x480 AMOLED display
    property int horizontalMargin: 20
    property int verticalMargin: 16
    property int itemSpacing: 12
    property int cornerRadius: 10
}
