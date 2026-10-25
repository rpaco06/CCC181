# Design review: personas and wireframes

I reviewed each screen at phone and laptop width against Marco (student waiting) and Mang Bert (gym caretaker), and against my "Because..., my interface must..." rules.

## Screen 1: Join (FR-01, FR-05)

**Works well:** The form has only the five things the gym needs (name, student ID, gear, collateral, PE class), and GET MY TICKET is a large black button at the bottom. Marco can tell what to do within 5 seconds, and the button is easy to hit with one thumb on the phone.

**Problem:** The gear category and collateral dropdowns start with "Basketball" and "Student ID Card" already selected, so a rushed student can submit without noticing and get the wrong gear or collateral recorded. This breaks *error prevention*. The subtitle ("Complete student identity verification and gear requisition parameters...") is also not how students talk, and the phone frame has a "KIOSK" label even though Marco uses his own phone. Both break *match with the real world*.

**Change:** I will change both dropdowns to start on "Choose gear..." and "Choose collateral...", so the student has to pick. I will change the subtitle to "Pick your gear and get a ticket." and remove the KIOSK label. The top navigation shows a "Staff Dashboard" link to students, which I will keep for testing but hide from students later.

## Screen 2: My place (FR-02)

**Works well:** The ticket number #12 is the largest thing on the page, and the black STATUS bar and "2 people ahead of you" come right after it. This follows my rule that Marco checks his phone with one hand in sun glare, so the most important facts must be biggest. The note "This page updates by itself" follows my rule about slow mobile data.

**Problem:** The same ticket shows two identifiers, "#12" and "TKT-8842", which is confusing because Marco does not know which one staff will call (*consistency*). The wireframe also only shows the WAITING state. When Marco is called, or marked no-show, the screen must look clearly different, otherwise he may miss it (*visibility of system status*).

**Change:** I will keep only "#12". I will build three status states in Part 6 (waiting, called, served or no-show), and "CALLED" will use different wording and a different style with the words "Go to the counter". I will remove the progress bar, because the number already says it.

## Screen 3: Staff dashboard (FR-03, FR-04, FR-05)

**Works well:** CALL NEXT is the biggest button, placed at the top, because it is what Mang Bert does most often. Student ID and collateral are in their own columns, and PE class tickets are highlighted with a label. This follows all three of my Mang Bert rules.

**Problem:** The NO-SHOW button is light gray with thin text while ISSUED is bold, and Mang Bert works under bright gym lights and needs high contrast, so it is easy to miss or mis-tap (*error prevention*). Both buttons also appear on rows that have not been called yet, so staff could mark someone as issued before calling them (*visibility of status*). The navigation also differs between frames: a sidebar on the laptop, tabs on the phone, and a top bar on the other screens (*consistency*). Staff see "Rack B-04" while students see "Rack B" (*match*).

**Change:** I will give NO-SHOW the same size and contrast as ISSUED, with an outline style so the two still look different. I will show ISSUED and NO-SHOW only on the ticket that has been called. I will use one simple top navigation on every screen and "Rack B" everywhere. My persona also needs full keyboard use (Tab and Enter), which a wireframe cannot show, so I will check it when I build the page in Part 7.

## Parts of the wireframes I will not build

The Stitch wireframes include features that are not in my requirements (FR-01 to FR-05), so I am leaving them out of the app: the "TKT-8842" code, "ISSUED AT" time, "REPORT COUNTER", CONNECTED indicator and LEAVE LINE button on My place; the PRIORITY FILTER (PE classes only), the desk station box and the lockers, wait-time and rack-lock boxes on the staff dashboard; and the INVENTORY and HISTORY tabs on the staff phone. An SMS alert was also considered and removed, because it needs phone numbers and an SMS service.

## Decision on the wireframes

I kept the layouts, because they match my personas' rules. The changes above are small (dropdown text, status states, button contrast, button visibility, one navigation), so I will apply them in the HTML build and compare the finished screens in Part 10.