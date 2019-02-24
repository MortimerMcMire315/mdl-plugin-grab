#!/bin/bash
OLD_DIR="/var/www/totara_12.1"
NEW_DIR="/var/www/totara"

while read plugin; do
    OLD_PLUGIN_DIR="$OLD_DIR/$plugin"
    NEW_PLUGIN_DIR="$NEW_DIR/$plugin"
    if [ -d $OLD_PLUGIN_DIR ]; then
        if [ -d $NEW_PLUGIN_DIR ]; then
            echo "$NEW_PLUGIN_DIR already exists..."
        else
            cp -r $OLD_PLUGIN_DIR $NEW_PLUGIN_DIR
        fi
    else
        echo "Could not find $OLD_PLUGIN_DIR."
    fi

done < old_plugins
