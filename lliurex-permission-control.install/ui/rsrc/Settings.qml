import org.kde.plasma.core 2.1 as PlasmaCore
import org.kde.kirigami 2.6 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3
import org.kde.plasma.components 3.0 as PC3

Rectangle{
    color:"transparent"
    Text{ 
        text:i18nd("lliurex-permission-control","Permissions configured")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout{
        id:generalLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        Layout.fillWidth: true
        anchors.left:parent.left

        Kirigami.InlineMessage {
            id: messageLabel
            visible:permissionControlBridge.showSettingsMessage[0]
            text:getMessageText(permissionControlBridge.showSettingsMessage[1])
            type:getMessageType(permissionControlBridge.showSettingsMessage[2])
            Layout.minimumWidth:490
            Layout.maximumWidth:490
            Layout.topMargin: 40
        }

        GridLayout{
            id: optionsGrid
            rows: 1
            flow: GridLayout.TopToBottom
            rowSpacing:5
            Layout.topMargin: messageLabel.visible?0:50

            PC3.CheckBox {
                id:dockerControlCb
                text:i18nd("lliurex-permission-control","Allow teachers and students groups to use docker")
                checked:permissionControlBridge.isDockerEnabled
                enabled:true
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                Keys.onReturnPressed: dockerControlCb.toggled()
                Keys.onEnterPressed: dockerControlCb.toggled()
                onToggled:{
                   permissionControlBridge.manageDockerChanges(checked)
                }

                Layout.alignment:Qt.AlignLeft
                Layout.bottomMargin:15
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
            enabled:permissionControlBridge.settingsChanged
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:{
                applyChanges()
                closeTimer.stop()
                permissionControlBridge.applyChanges()
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
            enabled:permissionControlBridge.settingsChanged
            Keys.onReturnPressed: cancelBtn.clicked()
            Keys.onEnterPressed: cancelBtn.clicked()
            onClicked:{
                discardChanges()
                closeTimer.stop()
                permissionControlBridge.cancelChanges()
            }
        }
    } 

    ChangesDialog{
        id:changesDialog
        dialogTitle:"Lliurex Permission Control"+" - "+i18nd("lliurex-permission-control","Settings")
        dialogVisible:permissionControlBridge.showChangesDialog
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
                permissionControlBridge.manageSettingsDialog("Cancel")
            }

        }
    }
    CustomPopup{
        id:synchronizePopup
     }

    Timer{
        id:delayTimer
    }

    function delay(delayTime,cb){
        delayTimer.interval=delayTime;
        delayTimer.repeat=true;
        delayTimer.triggered.connect(cb);
        delayTimer.start()
    }

    Timer{
        id:waitTimer
    }

    function wait(delayTime,cb){
        waitTimer.interval=delayTime;
        waitTimer.repeat=true;
        waitTimer.triggered.connect(cb);
        waitTimer.start()
    }


    function getMessageText(code){

        var msg="";
        switch (code){
            case 0:
                msg=i18nd("lliurex-permission-control","Changes applied successfully");
                break;
            case -1:
                msg=i18nd("lliurex-permission-control","Unable to activate permissions to usr docker");
                break;
            case -2:
                msg=i18nd("lliurex-permission-control","Unable to disable permissions to use docker");
                break;
            case -3:
                msg=i18nd("lliurex-permission-control","Unable to read permissions configuration")
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
            if (permissionControlBridge.closePopUp){
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
            if (permissionControlBridge.closePopUp){
                synchronizePopup.close(),
                delayTimer.stop()

            }
        })
    }  
} 
