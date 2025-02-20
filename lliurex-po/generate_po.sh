#!/bin/bash
xgettext --join-existing -L python ../lliurex-permission-control.install/ui/lliurex-permission-control -o ../lliurex-po/lliurex-permission-control/lliurex-permission-control.pot
xgettext -kde -ki18nd:2 ../lliurex-permission-control.install/ui/rsrc/lliurex-permission-control.qml -o ../lliurex-po/lliurex-permission-control/lliurex-permission-control.pot
xgettext --join-existing -kde -ki18nd:2 ../lliurex-permission-control.install/ui/rsrc/ApplicationOptions.qml -o ../lliurex-po/lliurex-permission-control/lliurex-permission-control.pot
xgettext --join-existing -kde -ki18nd:2 ../lliurex-permission-control.install/ui/rsrc/StudentSettings.qml -o ../lliurex-po/lliurex-permission-control/lliurex-permission-control.pot
xgettext --join-existing -kde -ki18nd:2 ../lliurex-permission-control.install/ui/rsrc/TeacherSettings.qml -o ../lliurex-po/lliurex-permission-control/lliurex-permission-control.pot
xgettext --join-existing -kde -ki18nd:2 ../lliurex-permission-control.install/ui/rsrc/Loading.qml -o ../lliurex-po/lliurex-permission-control/lliurex-permission-control.pot
xgettext --join-existing -kde -ki18nd:2 ../lliurex-permission-control.install/ui/rsrc/ChangesDialog.qml -o ../lliurex-po/lliurex-permission-control/lliurex-permission-control.pot
