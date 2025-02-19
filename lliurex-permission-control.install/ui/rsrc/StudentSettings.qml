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
        text:i18nd("lliurex-permission-control","Permission available for students")
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
            visible:studentStackBridge.showStudentSettingsMessage[0]
            text:getMessageText(studentStackBridge.showStudentSettingsMessage[1])
            type:getMessageType(studentStackBridge.showStudentSettingsMessage[2])
            Layout.fillWidth:true
            Layout.topMargin: 40
        }

        GridLayout{
            id: optionsGrid
            rows: 1
            flow: GridLayout.TopToBottom
            rowSpacing:5
            Layout.topMargin: messageLabel.visible?0:50

            StudentList{
                id:studentList
                structModel:studentStackBridge.studentsModel
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
            enabled:studentStackBridge.studentSettingsChanged
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:{
                applyChanges()
                closeTimer.stop()
                studentStackBridge.applyStudentsChanges()
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
            enabled:studentStackBridge.studentSettingsChanged
            Keys.onReturnPressed: cancelBtn.clicked()
            Keys.onEnterPressed: cancelBtn.clicked()
            onClicked:{
                discardChanges()
                closeTimer.stop()
                studentStackBridge.cancelStudentsChanges()
            }
        }
    } 

     ChangesDialog{
        id:changesDialog
        dialogTitle:"Lliurex Permission Control"+" - "+i18nd("lliurex-permission-control","Permission for Students")
        dialogVisible:studentStackBridge.showStudentChangesDialog
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
                mainStackBridge.manageSettingsDialog("Cancel")
            }

        }
    }
    CustomPopup{
        id:synchronizePopup
     }

    Timer{
        id:timer
    }

    Timer{
        id:delayTimer
    }

    function delay(delayTime,cb){
        timer.interval=delayTime;
        timer.repeat=true;
        timer.triggered.connect(cb);
        timer.start()
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
        delayTimer.stop()
        delay(500, function() {
            if (mainStackBridge.closePopUp){
                synchronizePopup.close(),
                delayTimer.stop()
            }
        })
    } 

    function discardChanges(){
        synchronizePopup.open()
        synchronizePopup.popupMessage=i18nd("lliurex-permission-control", "Restoring previous values. Wait a moment...")
        delayTimer.stop()
        delay(1000, function() {
            if (mainStackBridge.closePopUp){
                synchronizePopup.close(),
                delayTimer.stop()

            }
        })
    }  
} 
