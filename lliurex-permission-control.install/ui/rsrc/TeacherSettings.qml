import org.kde.plasma.core 2.1 as PlasmaCore
import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3
import org.kde.plasma.components 3.0 as PC3

Rectangle{
    color:"transparent"
    Text{ 
        text:i18nd("lliurex-permission-control","Permission available for teachers")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout{
        id:generalLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        anchors.left:parent.left
        width:parent.width-10
        height:parent.height-90
        enabled:true
        Kirigami.InlineMessage {
            id: messageLabel
            visible:teacherStackBridge.showTeacherSettingsMessage[0]
            text:getMessageText(teacherStackBridge.showTeacherSettingsMessage[1])
            type:getMessageType(teacherStackBridge.showTeacherSettingsMessage[2])
            Layout.fillWidth:true
            Layout.topMargin: 40
        }

        GridLayout{
            id: optionsGrid
            rows: 1
            flow: GridLayout.TopToBottom
            rowSpacing:5
            Layout.topMargin: messageLabel.visible?0:50

           TeacherList{
                id:teacherList
                structModel:teacherStackBridge.teachersModel
                Layout.fillHeight:true
                Layout.fillWidth:true
 
            }
        }
    }
    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.right:parent.right
        anchors.bottomMargin:15
        anchors.rightMargin:10
        spacing:10

        PC3.Button {
            id:applyBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok"
            text:i18nd("lliurex-permission-control","Apply")
            Layout.preferredHeight:40
            enabled:teacherStackBridge.teacherSettingsChanged
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:{
                applyChanges()
                teacherStackBridge.applyTeachersChanges()
            }
        }
        PC3.Button {
            id:cancelBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-cancel"
            text:i18nd("lliurex-permission-control","Cancel")
            Layout.preferredHeight: 40
            enabled:teacherStackBridge.teacherSettingsChanged
            Keys.onReturnPressed: cancelBtn.clicked()
            Keys.onEnterPressed: cancelBtn.clicked()
            onClicked:{
                discardChanges()
                teacherStackBridge.cancelTeachersChanges()
            }
        }
    } 

     ChangesDialog{
        id:changesDialog
        dialogTitle:"Lliurex Permission Control"+" - "+i18nd("lliurex-permission-control","Permission for Teachers")
        dialogVisible:teacherStackBridge.showTeacherChangesDialog
        dialogMsg:i18nd("lliurex-permission-control","The are pending changes to apply.\nDo you want apply the changes or discard them?")
        Connections{
            target:changesDialog
            function onDialogApplyClicked(){
                applyChanges()
                
            }
            function onDiscardDialogClicked(){
                discardChanges()
            }
            function onCancelDialogClicked(){
                closeTimer.stop()
            }

        }
    }
    CustomPopup{
        id:synchronizePopup
     }

    Timer{
        id:changesTimer
    }

  
    function delayT(delayTime,cb){
        changesTimer.interval=delayTime;
        changesTimer.repeat=true;
        changesTimer.triggered.connect(cb);
        changesTimer.start()
    }


    
    function getMessageText(code){

        var msg="";
        switch (code){
            case 0:
                msg=i18nd("lliurex-permission-control","Changes applied successfully");
                break;
            case -1:
                msg=i18nd("lliurex-permission-control","An error ocurred while applying changes");
                break;
           default:
                break;
        }
        return msg;

    }

    function getMessageType(type){

        switch (type){
            case "Info":
                return Kirigami.MessageType.Information
            case "Ok":
                return Kirigami.MessageType.Positive
            case "Error":
                return Kirigami.MessageType.Error
        }

    } 

    function applyChanges(){
        synchronizePopup.open()
        synchronizePopup.popupMessage=i18nd("lliurex-permission-control", "Apply changes. Wait a moment...")
        delayT(500, function() {
            if (mainStackBridge.closePopUp){
                synchronizePopup.close(),
                changesTimer.stop()
            }
        })
    } 

    function discardChanges(){
        synchronizePopup.open()
        synchronizePopup.popupMessage=i18nd("lliurex-permission-control", "Restoring previous values. Wait a moment...")
        delayT(1000, function() {
            if (mainStackBridge.closePopUp){
                synchronizePopup.close(),
                changesTimer.stop()

            }
        })
    }  
} 
