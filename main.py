import sys

if "--reminder" in sys.argv:
    from reminders.notifier import main
    main()
    sys.exit()

from app import ThoughtInbox

app = ThoughtInbox()
app.mainloop()