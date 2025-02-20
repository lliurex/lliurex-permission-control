import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQml.Models 2.8
import org.kde.plasma.components 2.0 as Components
import org.kde.plasma.components 3.0 as PC3
import org.kde.kirigami 2.16 as Kirigami



Rectangle {
    property alias structModel:teachersList.model
    property alias listCount:teachersList.count
    property alias structEnabled:teachersList.enabled

    id:teacherTable
    visible: true
    width: 335; height: 125
    color:"white"
    border.color: "#d3d3d3"

    ListModel{
        id: teachersModel
    } 
    PC3.ScrollView{
        implicitWidth:parent.width
        implicitHeight:parent.height
        anchors.leftMargin:10
   
        ListView{
            id: teachersList
            anchors.fill:parent
            height: parent.height
            model:structModel
            enabled:true
            currentIndex:-1
            clip: true
            focus: true
            boundsBehavior: Flickable.StopAtBounds
            highlight: Rectangle { color: "#add8e6"; opacity:0.8;border.color:"#53a1c9" }
            highlightMoveDuration: 0
            highlightResizeDuration: 0
            delegate: ListDelegateTeacherItem{
                width:teacherTable.width
                permissionId:model.permissionId
                isEnabled:model.isEnabled
                showResult:model.showResult
            }
            Kirigami.PlaceholderMessage { 
                id: emptyStudentHint
                anchors.centerIn: parent
                width: parent.width - (units.largeSpacing * 4)
                visible:teachersList.count>0?false:true
                text:i18nd("lliurex-permission-control","No permission found to configure")
            }
      } 
    }
}

