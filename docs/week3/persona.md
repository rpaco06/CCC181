# VarsityQ: User Personas

---

## Marco, the PE student and intramural athlete (person waiting)    

> "We wasted 20 minutes of our 1-hour PE class waiting at the desk just to find out all the volleyballs were taken, so we ended up doing basic drills instead." *(interview)*

| | |
| --- | --- |
| **Photo or sketch** | 🏐 Icon only (not a photo of a real person) |
| **Age, role and background** | 19, 2nd-year Civil Engineering student, enrolled in PE 3 (Volleyball) on Tuesdays; plays intramural basketball on weekends. *(interview)* |
| **Goals** | 1. Get the sports gear before PE class starts so his group does not waste practice time. *(observation)*<br>2. Know whether a specific item (such as a regulation volleyball or a badminton set) is available before walking to the gym desk. |
| **Frustrations** | 1. Standing in a chaotic, unstructured crowd at the gym counter during the 10-minute rush between class periods. *(observation)*<br>2. Reaching the desk only to find the gear is out of stock, so the group cannot play. *(observation)*<br>3. No clear borrowing procedure for off-hour intramural practices. *(interview)* |
| **Devices and context** | Mid-range Android phone, used with one hand while holding a water bottle and a sports bag in the other; walking outdoors in sun glare, with spotty campus Wi-Fi near the courts. *(observation)* |
| **Tech comfort** | High: uses messaging, the student portal and mobile apps daily, but expects fast, single-screen feedback. |
| **Accessibility needs** | High visual contrast (sun glare near the open-air courts); large touch targets for one-handed use. |

### Scenario

Marco walks toward the MSU-IIT gym with his PE classmates, worried they won't get a volleyball in time for their 10:00 AM class. Instead of rushing into the crowd at the desk, he pulls out his phone with one hand, opens **VarsityQ**, and selects "Volleyball". He enters his Student ID (`2023-0412`), selects "Student ID Card" as his collateral, and ticks the "PE class" box. He submits the form and instantly sees his ticket number (#12) and his position ("2 people ahead of you"). As he reaches the counter, his screen changes to "Called", so he hands over his ID card and takes the ball without waiting in line.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Request sports gear and give collateral and student ID | Join | FR-01 |
| Check my ticket number and how many people are ahead | My place | FR-02 |
| Say that I am borrowing for an active PE class | Join | FR-05 |

### What this means for my interface

1. Because Marco checks his phone with one hand in outdoor sun glare, his ticket number, status and position must be the largest, highest-contrast things on My place. *(observation)*
2. Because mobile data near the courts is spotty and slow, My place must update by itself without a full page reload and must work without large images.
3. Because PE classes have strict start times, the Join form must include a clear "PE class" checkbox so that staff can see which borrowers are in an active class. *(interview)*

---

## Mang Bert, the campus gym caretaker (staff member)

> "When PE classes start at the top of the hour, dozens of students crowd the PE office door all at once shouting gear requests and dumping their IDs on my desk." *(interview)*

| | |
| --- | --- |
| **Photo or sketch** | 🔑 Icon only (not a photo of a real person) |
| **Age, role and background** | 52, gym caretaker and PE facility staff for 8 years; keeps the cabinet keys and manages the lending of sports equipment. *(interview)* |
| **Goals** | 1. Issue gear quickly and in order during the 10-minute class transitions.<br>2. Keep an accurate record of who holds which equipment and collect valid collateral for every item. *(observation)* |
| **Frustrations** | 1. Students crowd the desk all at once, so it is hard to hear requests or keep track of who is next. *(observation)*<br>2. Student IDs get mixed up on the counter during rushes. *(observation)* |
| **Devices and context** | Shared desktop PC at the counter with a 1080p monitor, under bright fluorescent lights, operated while standing in a noisy room. *(observation)* |
| **Tech comfort** | Medium: comfortable with basic web forms and spreadsheets, but needs clear visual controls and simple navigation. |
| **Accessibility needs** | Full keyboard use (Tab and Enter) so he does not keep switching to the mouse; high-contrast badges under the bright gym lights. |

### Scenario

At 9:55 AM, as dozens of students approach the gym counter, Mang Bert opens the **VarsityQ** staff dashboard on the counter PC. Instead of shouting over the noise, he clicks "Call next" at the top of the screen. The dashboard shows Ticket #12 (Marco) with a highlighted "PE class" badge. Mang Bert checks Marco's Student ID (`2023-0412`), collects his ID card as collateral, hands over the volleyball, and clicks "Issued" to finish the transaction in under 15 seconds.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| View the active queue, filtered by gear category, with rack locations | Staff dashboard | FR-03 |
| Call next, mark gear as issued, or mark a no-show | Staff dashboard | FR-04 |
| Check PE class highlights and the recorded collateral | Staff dashboard | FR-05 |

### What this means for my interface

1. Because Mang Bert handles severe rushes in the 10-minute gaps between classes, the main actions ("Call next", "Issued", "No-show") must sit at the top of the dashboard and work with one click or the keyboard. *(observation)*
2. Because he must check physical collateral before handing over gear, every ticket row must show the student ID number and collateral type in its own columns. *(interview)*
3. Because students in an active PE class are on a strict schedule, the dashboard must clearly highlight PE class tickets so they stand out in the waiting list. *(observation)*