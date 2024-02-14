#!/bin/bash

# If any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# Fail exit if one of your pipe command fails
set -o pipefail
# Exits if any of your variables is not set
set -o nounset

ansible-playbook -i $CONTROL_NODE_INVENTORIES_DIR/servers-init.yml $CONTROL_NODE_PLAYBOOKS_DIR/server-ssh-init.yml -vv

ansible-playbook -i $CONTROL_NODE_INVENTORIES_DIR/servers-init.yml $CONTROL_NODE_PLAYBOOKS_DIR/server-config.yml -vv

eval $(ssh-agent -s)

/usr/bin/expect <<EOF
spawn ssh-add $CONTROL_NODE_SSH_PRIVATE_KEY_LOCATION
expect {
    "Enter passphrase for $CONTROL_NODE_SSH_PRIVATE_KEY_LOCATION:" {
        send "$SERVER_03100_USER_SSH_PASS\r";
        exp_continue;
    }
    eof {
        exit 0;
    }
}
EOF

ansible-playbook -i $CONTROL_NODE_INVENTORIES_DIR/servers.yml $CONTROL_NODE_PLAYBOOKS_DIR/server-install.yml -vv

# Previous script had reboot
eval $(ssh-agent -s)

/usr/bin/expect <<EOF
spawn ssh-add $CONTROL_NODE_SSH_PRIVATE_KEY_LOCATION
expect {
    "Enter passphrase for $CONTROL_NODE_SSH_PRIVATE_KEY_LOCATION:" {
        send "$SERVER_03100_USER_SSH_PASS\r";
        exp_continue;
    }
    eof {
        exit 0;
    }
}
EOF

ansible-playbook -i $CONTROL_NODE_INVENTORIES_DIR/servers.yml $CONTROL_NODE_PLAYBOOKS_DIR/server-post-install.yml -vv

# Previous script had reboot
eval $(ssh-agent -s)

/usr/bin/expect <<EOF
spawn ssh-add $CONTROL_NODE_SSH_PRIVATE_KEY_LOCATION
expect {
    "Enter passphrase for $CONTROL_NODE_SSH_PRIVATE_KEY_LOCATION:" {
        send "$SERVER_03100_USER_SSH_PASS\r";
        exp_continue;
    }
    eof {
        exit 0;
    }
}
EOF

