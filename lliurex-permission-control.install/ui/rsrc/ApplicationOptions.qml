import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


GridLayout{
    id: optionsGrid
    columns: 2
    flow: GridLayout.LeftToRight
    columnSpacing:10

    Rectangle{
        width:185
        Layout.minimumHeight:370
        Layout.preferredHeight:370
        Layout.fillHeight:true
        border.color: "#d3d3d3"

        GridLayout{
            id: menuGrid
            rows:4 
            flow: GridLayout.TopToBottom
            rowSpacing:0

            MenuOptionBtn {
                id:studentsItem
                optionText:i18nd("lliurex-permission-control","Permission for Students")
                optionIcon:"/usr/share/icons/breeze/actions/22/group.svg"
                optionEnabled:true
                Connections{
                    function onMenuOptionClicked(){
                        mainStackBridge.manageTransitions(0)
                    }
                }
            }

            MenuOptionBtn {
                id:teachersItem
                optionText:i18nd("lliurex-permission-control","Permission for Teachers")
                optionIcon:"/usr/share/icons/breeze/actions/22/user.svg"
                visible:mainStackBridge.isAdminUser
                Connections{
                    function onMenuOptionClicked(){
                        mainStackBridge.manageTransitions(1)
                   
                    }
                }
            }

            MenuOptionBtn {
                id:helpItem
                optionText:i18nd("lliurex-permission-control","Help")
                optionIcon:"/usr/share/icons/breeze/actions/22/help-contents.svg"
                Connections{
                    function onMenuOptionClicked(){
                        mainStackBridge.openHelp();
                    }
                }
            }
        }
    }

    StackView{
        id: optionsView
        property int currentIndex:mainStackBridge.currentOptionsStack
        Layout.fillWidth:true
        Layout.fillHeight: true
        Layout.alignment:Qt.AlignHCenter
       
        initialItem:studentsView

        onCurrentIndexChanged:{
            switch (currentIndex){
                case 0:
                    optionsView.replace(studentsView)
                    break;
                case 1:
                    optionsView.replace(teachersView)
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
            id:studentsView
            StudentSettings{
                id:studentSettings
            }
        }
        Component{
            id:teachersView
            TeacherSettings{
                id:teacherSettings
            }
        }
       
    }
}

