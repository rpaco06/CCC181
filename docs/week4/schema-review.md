# Schema self-review

I reviewed the ERD and `schema.md` against the six questions from Part 3. Each entry says what works, one problem I found, and what I changed or why I kept it.

## 1. Coverage

> **Works well:** Every requirement marked *Stores data? = Yes* has a table or column in the nouns table in `schema.md` (2a). Marco's top tasks (join, see his place, say he is borrowing for a PE class) are covered by `users`, `tickets` and `tickets.pe_class`. Mang Bert's top tasks (see the queue with rack locations, call next, mark issued or no-show, check collateral and PE highlights) are covered by `tickets`, `services.rack`, `collateral_types` and `tickets.called_at`.
> **Problem:** I had put an `is_active` column in the first version of `services`, but FR-12 (active status) is something I build this week in Part 9 as a second migration on a table that already has rows. With the column already in the first table there would be nothing to migrate. I also checked every column for one that no requirement needs: `called_at` is set by Call next (FR-04) and `avg_minutes` is needed by FR-11 and FR-12, so both stay.
> **Change:** I renamed the column to `active`, and in `schema.md` and the ERD I mark it as added by the second migration. The first migration creates `services` with id, name, rack and avg_minutes only.

## 2. One fact in one place

> **Works well:** A student's name and ID are stored once in `users`, a gear category's name and rack once in `services`, and a collateral label once in `collateral_types`. Tickets only hold facts about one visit, so a rack that moves is one update.
> **Problem:** If the same student types a different spelling of their name on a later visit, the database has to decide which name wins.
> **Change:** I kept the name from the first visit. The join form looks the student up by Student ID and does not overwrite the name. This is written under "Decisions I am still open about" in `schema.md`.

## 3. Facts, not results

> **Works well:** There is no position column and no count of waiting people. The position is a query: the number of tickets with status `waiting` that were created before this one.
> **Problem:** Two tickets could be created at the same instant and share a `created_at`, which would make "who is ahead" ambiguous.
> **Change:** I kept the schema, and the rule is now to order by `created_at` and then by `id`, since `id` is unique and always increasing. `schema.md` already says this in the rules after the nouns table.

## 4. Bad data

> **Works well:** Each mistake my personas could make is stopped by a constraint. A double tap or a second tab with the same Student ID is stopped by the partial unique index on `tickets(user_id)`. A typo in the Student ID is stopped by the format CHECK. A blank name is stopped by the name CHECK. A wrong or missing gear or collateral is stopped by the foreign keys. A zero or negative average time is stopped by the avg_minutes CHECK.
> **Problem:** A foreign key only checks that the gear category exists. It does not check that the category is switched on, so the database would accept a ticket for a category with `active = false`.
> **Change:** The database cannot enforce this alone, so the join route in Flask treats an inactive service as if it did not exist, and I will test it in Part 10. I added a section "Rules the database cannot enforce alone" to `schema.md`. It also notes that the one-active-ticket index may need to change when return tracking (FR-15) is built.

## 5. Deletes

> **Works well:** Every foreign key uses RESTRICT on purpose. Deleting a service that has tickets is refused, which is exactly FR-13. Deleting one ticket removes only a leaf row, so no history is lost by accident. Leaving the queue is a status change (`left`), not a delete.
> **Problem:** RESTRICT on `tickets.user_id` also blocks deleting a student who has tickets. A student could ask for their data to be removed, which conflicts with keeping the gym's history (the Data Privacy Act of 2012, RA 10173, applies to student records).
> **Change:** I kept RESTRICT because history matters for the reports. If a removal request ever has to be honored, the plan is to blank out the name and ID in `users` and keep the ticket rows. No requirement asks for this now, so I did not build it.

## 6. Types

> **Works well:** Every moment in time is a `timestamptz`. `pe_class` and `active` are booleans, not text. The Student ID is `varchar(9)` and not a number, because it is an identifier with a hyphen and the format is enforced by a CHECK.
> **Problem:** `services.name` was `varchar(50)`, but the Flask check I plan to use allows names up to 60 characters. Flask would accept a 55-character name and the database would reject it with an ugly error.
> **Change:** I changed `services.name` to `varchar(60)` in `schema.md` and the ERD. The Flask limits will match the database limits (100 for `users.name`, 60 for `services.name`).
