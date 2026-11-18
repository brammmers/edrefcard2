# Controller Mapping Guide

How a new controller gets its own reference card on EDRefCard, and how to help as a mapper.

> [!NOTE]
> The January 2026 guide, from before the mapping editor, is kept in
> [docs/legacy/CONTROLLER_MAPPING_GUIDE_2026-01.md](docs/legacy/CONTROLLER_MAPPING_GUIDE_2026-01.md) for the record.
> Its process (coordinates typed into `bindingsData.py`) is no longer used for new controllers.

## How it works

A **mapping** ties a clean photo of a controller to its physical controls. Each box groups the rows of one
physical control (a button, a hat, a trigger, an axis...) and points to it with a leader line. When a player
uploads a `.binds` file, the renderer fills the boxes with that player's commands and hides the boxes they
did not bind.

Mappings are data, not code: they are drawn in the admin **Mapping Editor**, stored in the database with their
image, versioned, and published without a code change or a redeploy. When a published mapping exists for a
controller, it takes over the older hand-coded template of `bindingsData.py`.

Controllers without a mapping and without a legacy template still get a card: a photo-less text layout listing
the bindings by group, so no upload ends in an error.

## Becoming a mapper

Mapping is done in the admin panel with a **mapper** account. Mappers can use the Controllers page, the
Mapping Editor and the mapper guide; they cannot see players' configurations, users or backups.

To get an account, contact the maintainers on the
[Frontier forum thread](https://forums.frontier.co.uk/threads/627609/)
or by direct message. An admin creates it from **Users**.

## Workflow

1. **Pick the controller** on the **Controllers** page.
   - *Unknown devices* lists hardware IDs seen in real uploads that have no card yet, most seen first. Click
     **Scaffold**: the editor opens pre-filled with the inputs found in a real `.binds`. When the ID is only a
     variant of a known controller (same hardware, same numbering), **Attach** it to that controller instead.
   - *Legacy controllers* are the hand-coded templates. They can be redrawn as a mapping.
   - **+ New (editor)** starts from scratch. **Blank scaffold** generates the rows from button, POV and axis
     counts taken from the manual.
   - **Duplicate** with the mirror option gives a starting point for the other hand of a left/right pair.
2. **Upload a clean product photo**: manufacturer press shot or your own, neutral background, straight-on,
   high resolution, no overlay or watermark. Keep *side margins* ticked so the boxes have room on both sides.
3. **Place the controls.** Pick a stamp, then click the physical control on the photo, once per control.
   For scaffolded boxes, use **Set btn** to anchor the leader line on the control.
4. **Import a manufacturer sheet** when one exists: Virpil fillable PDFs and VKB worksheets can be imported,
   with a review of the inputs they declare before anything is kept.
5. **Arrange** sorts the boxes into two columns by anchor position to limit line crossings. Then adjust:
   multi-select, alignment and spacing tools, snapping guides, movable title and URL.
6. **Check the inputs** in the right-hand panel against the manual or a real `.binds`: labels, numbering,
   `Joy_N` and axis codes. Live checks flag duplicates and inconsistencies as you edit.
7. **Preview with a real profile.** Enter a saved card's reference (the part after `/binds/` in its URL) and
   click **Preview**: the editor renders that player's commands in every game mode, without saving anything,
   and reports the inputs the mapping does not cover.
8. **Save draft.** Every save is a draft, an admin's included. If the controller is already published, its
   public card does not change.
9. **Review and publish** (admin). The review page shows the changes against the published version with
   layout previews; **Publish draft** releases it. Every version is kept in **History**, with a rollback.

### Stamps

| Stamp | One click gives you |
|-------|---------------------|
| Button | 1 row (press), `Joy_N` auto-incremented |
| Hat 4-way | 4 rows (up, right, down, left), `Joy_N` to `Joy_N+3` |
| Hat 4-way + push | 5 rows, `Joy_N` to `Joy_N+4` |
| POV | 4 rows, `Joy_POVnUp/Right/Down/Left` |
| 2-stage trigger | stage 1 and stage 2 rows |
| Stick (X+Y) | 2 analogue rows, `Joy_XAxis` and `Joy_YAxis` |
| Axis | 1 analogue row, axis code to set |

### Safety nets

- Undo and redo cover 100 full-document steps, imports included.
- Unsaved work is kept in the browser and offered back after a crash or a refresh.
- If someone else saved the same mapping while you were editing, your save is refused instead of
  overwriting their work.
- Saving a draft never changes anything public.

## Ground rules

- **Exhaustive beats personal.** Map every physical control, not only the ones you bind: players with other
  profiles must be able to use the card.
- **One box per physical control.** A 4-way hat with its push, a toggle, a rotary encoder or a mode selector is
  one box with several rows, not one box per direction.
- **Cite your source.** Manufacturer manual or callout sheet preferred; your own hardware is even better.
- **Check the codes.** Axis assignments vary between controllers, and a `.binds` file only contains the inputs
  a player assigned, so it cannot prove an unused button's number. Keep the `Neg_` and `Pos_` prefixes when an
  axis is split into two digital directions.
- **Left and right variants** share a layout but not always their hardware IDs, button numbers or axes:
  verify the mirrored variant before it is published.
- **Photos** must be usable: ask if you are unsure about the rights. No AI-generated images.

The full in-app version of this guide is at `/admin/help`, linked from the editor.

## Legacy templates

The controllers of the original site are still defined in `www/scripts/bindingsData.py` (device IDs and
template names) with their box coordinates and images under `www/res/`. They keep working unchanged. Editing
them requires a code change and a deploy, which is why new controllers go through the Mapping Editor instead.
