import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQml.Models 2.8
import org.kde.plasma.components 2.0 as Components
import org.kde.plasma.components 3.0 as PC3


Components.ListItem{

    id: teachersListItem
    property string permissionId
    property bool isEnabled
    property int showResult

    enabled:true

    onContainsMouseChanged: {
        if (containsMouse) {
           teachersList.currentIndex = index
        } else {
           teachersList.currentIndex = -1
        }

    }

    Item{
        id: menuItem
        height:visible?45:0
        width:parent.width-15
        PC3.CheckBox {
            id:permissionCheck
            checked:isEnabled
            onToggled:{
                teacherStackBridge.manageTeachersChecked([permissionId,checked])
            }
            anchors.left:parent.left
            anchors.leftMargin:5
            anchors.verticalCenter:parent.verticalCenter
            ToolTip.delay: 1000
            ToolTip.timeout: 3000
            ToolTip.visible: hovered
            ToolTip.text:{
                if (permissionCheck.checked){
                    i18nd("lliurex-permission-control","Check to deny users in teachers groups to use this application")
                }else{
                    i18nd("lliurex-permission-control","Check to allow users in teachers groups to use this application")                   
                }
            }

        }

        Text{
            id: text
            text: permissionId
            width:parent.width-resultImg.width-40
            clip: true
            anchors.left:permissionCheck.right
            anchors.leftMargin:5
            anchors.verticalCenter:parent.verticalCenter
        }

        Image {
            id: resultImg
            source:{
                if (showResult==0){
                    "/usr/share/lliurex-permission-control/rsrc/ok.png"
                }else{
                    "/usr/share/lliurex-permission-control/rsrc/error.png"
                                 
                }
            }
            visible:{
                if (showResult!=-1){
                    true
                }else{
                    false
                }
            }
            sourceSize.width:32
            sourceSize.height:32
            anchors.leftMargin:10
            anchors.left:text.right
            anchors.verticalCenter:parent.verticalCenter
        }

    }
}
