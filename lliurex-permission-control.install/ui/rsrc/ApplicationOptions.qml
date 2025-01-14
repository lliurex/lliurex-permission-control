import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12


GridLayout{
    id: optionsGrid
    columns: 2
    flow: GridLayout.LeftToRight
    columnSpacing:10

    Rectangle{
        width:160
        height:230
        border.color: "#d3d3d3"

        GridLayout{
            id: menuGrid
            rows:4 
            flow: GridLayout.TopToBottom
            rowSpacing:0

            MenuOptionBtn {
                id:settingsItem
                optionText:i18nd("lliurex-permission-control","Settings")
                optionIcon:"/usr/share/icons/breeze/actions/22/configure.svg"
                optionEnabled:true
                Connections{
                    function onMenuOptionClicked(){
                        permissionControlBridge.manageTransitions(0)
                    }
                }
            }

            MenuOptionBtn {
                id:helpItem
                optionText:i18nd("lliurex-permission-control","Help")
                optionIcon:"/usr/share/icons/breeze/actions/22/help-contents.svg"
                Connections{
                    function onMenuOptionClicked(){
                        permissionControlBridge.openHelp();
                    }
                }
            }
        }
    }

    StackView{
        id: optionsView
        property int currentIndex:permissionControlBridge.currentOptionsStack
        implicitHeight: 230
        Layout.fillWidth:true
        Layout.fillHeight: true
        
        initialItem:settingsView

        onCurrentIndexChanged:{
            switch (currentIndex){
                case 0:
                    optionsView.replace(settingsView)
                    break;
           }
        }

        replaceEnter: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 0
                to:1
                duration: 600
            }
        }
        replaceExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to:0
                duration: 600
            }
        }

        Component{
            id:settingsView
            Settings{
                id:settings
            }
        }

    }
}

