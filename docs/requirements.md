# VarsityQ requirements

**Setting:** MSU-IIT gym counter, during weekday PE classes and intramural hours
**People who wait:** PE students and intramural athletes borrowing sports gear ([Marco](week3/personas.md))
**People who serve:** Campus gym caretakers issuing and tracking sports gear ([Mang Bert](week3/personas.md))

**Problem statement:** A student borrowing sports gear between PE classes needs a way to join the line and see an accurate live wait count without crowding the gym counter, because dozens of students arriving at the top of the hour currently shout requests and pile IDs on the desk without knowing whether gear is still available.

## Functional requirements

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | A student can join the queue for a sports gear category by entering their full name and MSU-IIT Student ID. | Must | **Yes** | Built (Week 3) |
| FR-02 | A student can view their ticket number, current status, and the exact count of waiting borrowers ahead of them in arrival order. | Must | **Yes** | Built (Week 3) |
| FR-03 | A gym caretaker can view all waiting and called tickets in arrival order along with each gear item's rack location. | Must | **Yes** | Built (Week 3) |
| FR-04 | A gym caretaker can call the next waiting borrower in arrival order. | Must | **Yes** | Built (Week 3) |
| FR-05 ★ | A student can indicate whether they are borrowing for a scheduled PE class when joining the queue. | Must | **Yes** | Built (Week 3) |
| FR-06 ★ | A student can select which collateral item they will leave at the gym counter when joining the queue. | Must | **Yes** | Built (Week 3) |
| FR-07 | A gym caretaker can mark a called ticket as issued. | Must | **Yes** | Built (Week 3) |
| FR-08 | A gym caretaker can mark a called ticket as no-show. | Must | **Yes** | Built (Week 3) |
| FR-09 | A student can leave the queue and cancel their ticket while its status is waiting. | Must | **Yes** | Built (Week 3) |
| FR-10 ★ | A student with an active waiting or called ticket cannot submit a second ticket using the same Student ID. | Must | **Yes** | This week |
| FR-11 | A gym caretaker can add a new sports gear category with its rack location and average issue time. | Must | **Yes** | This week |
| FR-12 | A gym caretaker can edit an existing sports gear category's name, rack location, average issue time, and active status. | Must | **Yes** | This week |
| FR-13 | A gym caretaker can delete a sports gear category that has no tickets attached to it. | Must | **Yes** | This week |
| FR-14 ★ | A gym caretaker can filter the staff queue view by sports gear category. | Should | **Yes** | This week |
| FR-15 ★ | A gym caretaker can record when issued sports gear is returned and collateral is released. | Should | **Yes** | Later |
| FR-16 | A gym caretaker can log in with a password before accessing staff pages. | Should | **Yes** | Later |
| FR-17 | A gym caretaker can view a daily summary of issued gear, no-shows, and early departures per gear category. | Could | **Yes** | Later |

## Non-functional requirements

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | No ticket, student record, or gear category is lost when the Flask server or PostgreSQL container restarts. | Reliability | Must |
| NFR-02 | Two borrowers can never receive the same ticket number or register duplicate Student ID records, even if they submit at the exact same second. | Data integrity | Must |
| NFR-03 | The My place status screen and its 10-second auto-refresh respond in under 2 seconds on campus mobile data. | Performance | Should |
| NFR-04 | Every student and staff screen scores 90 or higher in Google Lighthouse mobile accessibility audits and maintains visible keyboard focus outlines. | Accessibility | Must |
| NFR-05 | No database passwords, `.env` files, or secret keys are committed to the public GitHub repository. | Security | Must |

## MVP and scope

- **MVP:** `FR-01`, `FR-02`, `FR-03`, `FR-04`, `FR-05`, `FR-06`, `FR-07`, `FR-08`, `FR-09`, `FR-10`, `FR-11`, `FR-12`, `FR-13`, `NFR-01`, `NFR-02`, `NFR-04`, and `NFR-05`. This is the smallest working system that replaces crowding at the MSU-IIT gym counter with an ordered digital queue, tracks PE class status and collateral, prevents duplicate active tickets per Student ID, allows staff to manage gear availability, and persists all records across restarts.
- **Out of scope:**
  - **Automated SMS or Messenger push notifications:** Sending texts requires third-party telecom APIs and paid credits; students can already check live status on the auto-refreshing My place screen.
  - **Real-time barcode or RFID scanner integration for individual balls and rackets:** The gym counter tracks gear by category and rack location rather than individual serialized equipment tags, so hardware scanning is unnecessary this semester.

## Stakeholder check

| Who (role only, no full name) | What they said | What I changed |
| --- | --- | --- |
| MSU-IIT PE student and intramural player | "Students sometimes line up twice using two tabs so they can grab whichever gear opens first, and we also need a way to cancel if our PE professor dismisses us early." | Added **FR-10 ★** (block duplicate active tickets per Student ID) and **FR-09** (allow waiting students to leave the queue). |