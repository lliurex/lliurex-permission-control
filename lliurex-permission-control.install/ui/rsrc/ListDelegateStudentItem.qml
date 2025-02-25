import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQml.Models 2.8
import org.kde.plasma.components 2.0 as Components
import org.kde.plasma.components 3.0 as PC3


Components.ListItem{

    id: studentsListItem
    property string permissionId
    property bool isEnabled
    property int showResult

    enabled:true

    onContainsMouseChanged: {
        if (containsMouse) {
           studentsList.currentIndex = index
        } else {
           studentsList.currentIndex = -1
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
                studentStackBridge.manageStudentsChecked([permissionId,checked])
            }
            anchors.left:parent.left
            anchors.leftMargin:5
            anchors.verticalCenter:parent.verticalCenter
            ToolTip.delay: 1000
            ToolTip.timeout: 3000
            ToolTip.visible: hovered
            ToolTip.text:{
                if (permissionCheck.checked){
                    i18nd("lliurex-permission-control","Check to remove students users from this group")
                }else{
                    i18nd("lliurex-permission-control","Check to add studentes users to this group")                   
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
                    "/usr/share/icons/breeze/status/24/data-success.svg"
                }else{
                    "/usr/share/icons/breeze/status/24/data-error.svg"
                                 
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
