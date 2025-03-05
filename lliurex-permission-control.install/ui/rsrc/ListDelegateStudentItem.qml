import QtQuick
import QtQuick.Controls
import QtQml.Models
import org.kde.plasma.components as PC

PC.ItemDelegate{

    id: studentsListItem
    property string permissionId
    property bool isEnabled
    property int showResult

    enabled:true
    height:50

    Item{
        id: menuItem
        height:visible?45:0
        width:parent.width-15

        MouseArea {
           id: mouseAreaOption
           anchors.fill: parent
           hoverEnabled:true
           propagateComposedEvents:true

           onEntered: {
               studentsList.currentIndex=index
           }
        }
        PC.CheckBox {
            id:permissionCheck
            checked:isEnabled
            onToggled:{
                studentStackBridge.manageStudentsChecked([permissionId,checked])
            }
            anchors.left:parent.left
            anchors.leftMargin:5
            anchors.verticalCenter:parent.verticalCenter
            ToolTip{
                id:permissionCheckToolTip
                delay:1000
                timeout:3000
                visible:permissionCheck.hovered
                text:permissionCheck.checked?i18nd("lliurex-permission-control","Check to remove students users from this group"):i18nd("lliurex-permission-control","Check to add studentes users to this group")                   
                background:Rectangle{
                    color:"#ffffff"
                    border.color:"#b8b9ba"
                    radius:5.0
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
