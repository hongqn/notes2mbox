Restore Notes from iOS backup
=============================

This script helps to restore iOS notes from a device backup.

It read the notes.sqlite database from the backup, and translate it into a mbox file, which can be imported into Mail.app and syncs to iOS devices later.

Usage
-----

#. Extract your backup using `iPhone Backup Extractor
   <http://supercrazyawesome.com/>`_.

#. Navigate to iOS Files > Library > Notes and copy notes.sqlite to the
   directory holding notes2mbox.py.

#. cd /path/to/notes2mbox

#. Run the following command::

        python notes2mbox.py notes.sqlite notes.mbox --device-name="My iPhone"

   where "My iPhone" could be replaced with your device's name.  A new file
   named notes.mbox will be generated under the current directory.

#. Open Mail.app and choose File > Import Mailbox... to import the generated
   notes.mbox.

Now your lost notes will be shown in your Mail.app.  At the next time syncing
with your iOS device with iTunes, make sure you checked "sync notes" option and
the recovered notes will be back in your device.
