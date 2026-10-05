# Affiliate Links for Alfred

Search [Affiliate Links.txt](#the-links-file) from Alfred and copy the link you want.

The keyword is `aff`. Return puts the URL on the clipboard. A notification confirms the copy. The workflow reads a text file on disk. It does not send that file, or the link you copy, anywhere.

| | |
|---|---|
| Keyword | `aff` |
| Bundle ID | `com.retrocombs.affiliate-links` |
| Alfred | 5, with the Powerpack |
| Version | 1.0.0 |
| Source | https://github.com/stevencombs/alfred-affiliate-links |

On the Macs that already sync Alfred preferences through Google Drive, the workflow is already installed. This repository is the source copy: the script, the Alfred package, and these instructions.

## Table of contents

1. [What you can copy](#what-you-can-copy)
2. [Requirements](#requirements)
3. [Repository layout](#repository-layout)
4. [Where the files live](#where-the-files-live)
5. [Install](#install)
6. [Use it](#use-it)
7. [The links file](#the-links-file)
8. [How search matches](#how-search-matches)
9. [Examples](#examples)
10. [Configuration](#configuration)
11. [Keep the repo and Alfred in step](#keep-the-repo-and-alfred-in-step)
12. [Other Macs](#other-macs)
13. [Troubleshooting](#troubleshooting)
14. [Uninstall](#uninstall)

## What you can copy

Select a row, then use one of these keys.

| Key | Copies |
|---|---|
| Return | The URL for that row |
| ⌘Return | The YouTube paste line: emoji, name, and URL. When the entry has a UK link, that full line is copied, UK URL included |
| ⌥Return | The UK URL, on a row that has one |
| ⌃Return | The promo note, on a row that has one |

⌘C copies the URL as well. That is Alfred's copy shortcut, and it uses the same URL as Return.

The workflow copies to the clipboard. It does not type the link into the frontmost app. Paste with ⌘V.

UK links and alternate URLs are their own rows. Return on a `(UK)` row copies the UK URL. Return on an `(alt)` row copies that alternate URL. ⌘Return on an alt row copies `emoji Name: <that alt URL>`. ⌘Return on the main row and the UK row copies the original line from the file, which is the canonical paste line.

A row titled like a sentence, with the subtitle `Note · … · no link to copy`, is a note from the file. Return does nothing on that row.

## Requirements

- macOS with Alfred 5 and the Powerpack. Script Filters are a Powerpack feature.
- `/usr/bin/python3`. macOS provides this with the Xcode Command Line Tools. Check with `python3 --version`. If the command is missing, install the tools with `xcode-select --install`.
- A links file. The default path is below. Google Drive for desktop has to be running for that path to exist.
- Alfred's preferences sync, if you want the installed workflow to appear on your other Macs without installing it again. Sync is already pointed at `~/Google Drive (Home)/Computers/Mac/MacSyncing/Alfred` on this setup.

The default links file is:

```text
~/Google Drive (Home)/Grok Ops/YouTube/Affiliate Links.txt
```

## Repository layout

```text
alfred-affiliate-links/
├── README.md
├── Affiliate.Links.alfredworkflow    ← double-click to install
├── scripts/
│   ├── install.sh                    ← copy workflow/ into Alfred
│   ├── export-from-alfred.sh         ← copy Alfred's copy back here
│   └── package.sh                    ← rebuild the .alfredworkflow
└── workflow/
    ├── info.plist                    ← keyword, objects, configuration
    ├── search.py                     ← reads the file and builds the list
    └── icon.png
```

`Affiliate.Links.alfredworkflow` is a zip of `info.plist`, `search.py`, and `icon.png`. Alfred imports that zip. The README stays in the repository and is not part of the package.

## Where the files live

There are two copies, on purpose.

| Copy | Path | What it is for |
|---|---|---|
| Running workflow | Alfred's synced preferences, folder `user.workflow.4301CFFB-5B17-4B17-8CD6-C398E2DCCC84` | What Alfred runs. Google Drive syncs this folder to your other Macs. |
| Source | `~/Google Drive (Home)/GitHub Repos/stevencombs/alfred-affiliate-links` | This git repository. `~/src/github.com/stevencombs/alfred-affiliate-links` is a shortcut to the same folder after `repos-sync`. |

The running folder on this Mac is:

```text
~/Google Drive (Home)/Computers/Mac/MacSyncing/Alfred/Alfred.alfredpreferences/workflows/user.workflow.4301CFFB-5B17-4B17-8CD6-C398E2DCCC84
```

Editing the workflow in Alfred Preferences changes the running copy. Editing `workflow/` in this repository changes the source. [Keep the repo and Alfred in step](#keep-the-repo-and-alfred-in-step) explains how to copy either way.

The links file is not in this repository. Your URLs stay in `Affiliate Links.txt`.

## Install

### Already installed

If Alfred preferences are syncing through Google Drive, open Alfred and type `aff`. The workflow is there. You only need the steps below to reinstall it, or to install it on a Mac that does not use that sync folder.

### Double-click the package

1. Download [Affiliate.Links.alfredworkflow](https://github.com/stevencombs/alfred-affiliate-links/raw/main/Affiliate.Links.alfredworkflow), or use the copy in a clone of this repository.
2. Double-click it. Alfred asks to import the workflow.
3. If Alfred says a workflow with bundle ID `com.retrocombs.affiliate-links` is already installed, replace it.

Importing can give the workflow a new folder name inside `workflows/`. The keyword, bundle ID, and behavior stay the same. `scripts/install.sh` is the path that keeps the original folder name, which matters if you want the synced copy to stay one workflow instead of a second copy.

### Install from a clone

```bash
git clone https://github.com/stevencombs/alfred-affiliate-links.git
cd alfred-affiliate-links
./scripts/install.sh
```

On this Mac the checkout already lives in Google Drive:

```bash
cd "$HOME/Google Drive (Home)/GitHub Repos/stevencombs/alfred-affiliate-links"
./scripts/install.sh
```

`install.sh` does three things:

1. Reads Alfred's sync folder from `com.runningwithcrayons.Alfred-Preferences`. On this setup that is `~/Google Drive (Home)/Computers/Mac/MacSyncing/Alfred`.
2. Copies `info.plist`, `search.py`, and `icon.png` into `workflows/user.workflow.4301CFFB-5B17-4B17-8CD6-C398E2DCCC84`.
3. Tells Alfred to reload bundle ID `com.retrocombs.affiliate-links`.

If the sync folder is not set, or that folder is missing, the script uses `~/Library/Application Support/Alfred/Alfred.alfredpreferences` instead.

## Use it

1. Open Alfred.
2. Type `aff` and a space. A space is required. `affelgato` does not search. `aff elgato` does.
3. Keep typing. The list narrows as you type.
4. Highlight a row and press Return.

`aff` followed by a space, with nothing after it, lists every link in the file, in file order. Cleanup notes stay hidden until your query matches them.

The subtitle under each product shows the URL, the section, and which modifier keys apply to that row:

| Hint in the subtitle | Meaning |
|---|---|
| `⌘ paste line` | ⌘Return copies the paste line |
| `⌥ UK` | ⌥Return copies the UK URL |
| `⌃ promo` | ⌃Return copies the promo note |
| `UK` on a `(UK)` row | Return copies the UK URL |
| `alt` on an `(alt)` row | Return copies that alternate URL |

Hold the modifier before you press Return. The subtitle changes to the exact text that will be copied.

Alfred remembers rows you accept, using each row's stable id, and can move frequent links up the list.

## The links file

The file is plain text, UTF-8. The workflow understands the layout already used in `Affiliate Links.txt`.

### Section

A line that starts with `#` is a section name. The name is shown in the subtitle. A blank line, or a new section, ends the product above it, so a note only attaches to the product directly above the note.

```text
# Cameras

📷 Example Camera: https://example.com/camera
```

### Product

```text
EMOJI Product Name: https://example.com/product
```

The label is everything before the colon that introduces the URL. The first URL is the link Return copies. The whole line is the paste line ⌘Return copies.

### UK, or another region

```text
⚡ Example Hub: https://example.com/us | UK: https://example.com/uk
```

Return on the main row copies the first URL. ⌥Return on that row copies the UK URL. A second row, `Example Hub (UK)`, copies the UK URL on Return. ⌘Return on either row copies the whole original line, which is the paste format `US URL | UK: URL` with the emoji and name in front.

A region label is a short word, then a colon, then a URL, in the part after `|`. `UK` is the usual label. Another short label is treated the same way and gets its own row.

### Alternate URLs

Indent the line with spaces or a tab, directly under the product, with no blank line between them.

```text
📀 Example Recorder: https://example.com/first
   Alt: https://example.com/second
   Alts: https://example.com/third | https://example.com/fourth
```

Each alternate URL is a row titled `Example Recorder (alt)`. The main row stays the first URL. The file's own rule is to use the first URL until you pick a canonical one. The alt rows are there when you want a different link on purpose.

### Promo and other notes

```text
⚡ Example Cable: https://example.com/cable
   Promo: save 10% with code EXAMPLE
```

The promo is shown in the subtitle. ⌃Return copies the promo line, including the word `Promo:`. Several promo lines are copied together, one per line.

Any other indented line is shown in the subtitle and is not given its own copy action.

### Cleanup notes

A line that starts with `- ` is a note, not a product. These are the lines under `# Notes to Clean Later`.

```text
# Notes to Clean Later

- Example Product: the short link may point at the older model. Confirm before the next use.
```

The note appears when your query matches its text. It is not a link. Return does not copy it.

### Lines the workflow skips

- The introductory lines at the top of the file, because they are not a product, a heading, or a `- ` note.
- The disclosure paragraph, because it has no URL.
- Blank lines. They only separate entries.
- An indented line that does not sit directly under a product.

A product line Alfred cannot parse as `Name: https://…` still appears if it contains a URL. The first URL is the link, and further URLs on that line become alt rows.

## How search matches

The query is the text after `aff `.

- Matching is case insensitive.
- `RØDE` matches `rode`. `ø`, `æ`, `ł`, `đ`, and `ß` are folded, and accents are ignored.
- Every word has to appear somewhere in that product: the name, the section, any URL, the promo, or an attached note.
- A query with the spaces removed matches a name with the spaces removed, when the squashed query is at least 3 characters. `aff streamdeck` finds `Stream Deck`.
- Products whose name contains the words rank above products that only match in the URL or the section.
- A name that contains the whole phrase ranks above a name that only contains the words separately.
- With no query, results stay in file order: the main link, then each region, then each alt.
- Cleanup notes are added at the bottom, and only when the query matches them.

The list is built by `workflow/search.py`. Alfred does not filter again. What the script prints is the list you see.

## Examples

```text
aff
aff elgato
aff stream deck
aff streamdeck
aff sabrent
aff uk joystick
aff gitryin
aff rode
aff B08965JV8D
```

| You type | You get |
|---|---|
| `aff elgato` | Each Elgato product. Return copies that product's URL. ⌘Return copies `emoji Elgato …: URL`. |
| `aff sabrent` | The hub, then a `(UK)` row. Return on the first row copies the US URL. ⌥Return, or Return on the UK row, copies the UK URL. ⌘Return copies the full paste line with both URLs. |
| `aff gitryin` | The direct link and the Amazon color links. The direct row shows the promo. ⌃Return copies `Promo: save 10% with code retrocombs`. |
| `aff rode` | The VideoMic row, typed without `ø`, plus the cleanup note that asks you to confirm the product. The note cannot be copied as a link. |
| `aff wireless` | The wireless keyboard, plus the VideoMic cleanup note, because that note contains "Wireless". |
| `aff pocket` | The main Box Pro Pocket URL, then each alt URL, plus the cleanup note about multiple links. |

A query that matches nothing shows one row, `No affiliate links match`. That row cannot be copied.

## Configuration

The path to the text file is a workflow variable named `links_file`.

1. Open Alfred Preferences → Workflows.
2. Select **Affiliate Links**.
3. Click **Configure Workflow** (the button at the upper right of the workflow). The field is labeled **Links file**.
4. Set the path. A leading `~` is expanded. Save.

The default is `~/Google Drive (Home)/Grok Ops/YouTube/Affiliate Links.txt`. Leave it alone when that file is the list you want. Change it when a Mac mounts Google Drive under a different folder name.

If the file is missing, Alfred shows `Affiliate Links.txt not found` and the path it tried. Fix the path, or wait until Google Drive has finished downloading the file.

The same variable can be set from the command line:

```bash
osascript -e 'tell application "Alfred" to set configuration "links_file" to "~/Google Drive (Home)/Grok Ops/YouTube/Affiliate Links.txt" in workflow "com.retrocombs.affiliate-links" exportable true'
```

`exportable true` stores the value with the workflow so it is included when Alfred syncs.

## Keep the repo and Alfred in step

### You edited the repository

Rebuild the package, install it over the running copy, then commit.

```bash
cd "$HOME/Google Drive (Home)/GitHub Repos/stevencombs/alfred-affiliate-links"
./scripts/package.sh
./scripts/install.sh
git add -A
git status
git commit -m "Describe the change"
git push
```

`package.sh` writes `Affiliate.Links.alfredworkflow` next to this README. Commit that file when you change `workflow/`, so the downloadable package matches the source.

### You edited the workflow inside Alfred

Alfred writes the running copy, not this repository. Bring those edits back before you commit:

```bash
cd "$HOME/Google Drive (Home)/GitHub Repos/stevencombs/alfred-affiliate-links"
./scripts/export-from-alfred.sh
git diff
```

`export-from-alfred.sh` copies `info.plist`, `search.py`, and `icon.png` from the installed workflow into `workflow/`, then rebuilds the package. It looks in the Alfred sync folder first.

### What each script touches

| Script | Reads | Writes |
|---|---|---|
| `scripts/package.sh` | `workflow/` | `Affiliate.Links.alfredworkflow` |
| `scripts/install.sh` | `workflow/` | The installed workflow in Alfred's preferences |
| `scripts/export-from-alfred.sh` | The installed workflow | `workflow/` and the `.alfredworkflow` package |

None of the scripts read or write `Affiliate Links.txt`.

## Other Macs

Two different syncs are involved.

**Alfred preferences sync** carries the installed workflow. After Google Drive finishes syncing `Computers/Mac/MacSyncing/Alfred`, the other Mac's Alfred sees **Affiliate Links**. Type `aff`. The links file has to be at the configured path on that Mac too. The default path is the same Google Drive file, so it appears when Drive has synced `Grok Ops/YouTube/Affiliate Links.txt`.

**This git repository** is stored with the other checkouts:

```text
~/Google Drive (Home)/GitHub Repos/stevencombs/alfred-affiliate-links
```

It is listed in `~/.local/share/repos/github.txt`. On another Mac:

1. Wait until Drive has finished syncing `GitHub Repos` and the Alfred preferences folder.
2. Update dotfiles with `dpull`, so `github.txt` includes this repository.
3. Run `repos-sync`.

`repos-sync` creates the shortcut:

```text
~/src/github.com/stevencombs/alfred-affiliate-links
```

That shortcut points at the Google Drive checkout. Do not commit this repository from two Macs while Drive is still syncing the `.git` folder.

You do not need the git checkout to use the workflow. You need it to change the source, reinstall from the package, or read these instructions offline.

## Troubleshooting

**`aff` shows nothing.**

Alfred Preferences → Workflows → Affiliate Links. Confirm the workflow is enabled. Confirm the keyword is `aff`. Powerpack has to be active. Script Filters do not run without it.

**`affelgato` shows nothing useful.**

Type a space after `aff`. The keyword is `aff`, and the rest is the query.

**The row says the file was not found.**

The path in [Configuration](#configuration) has to be a real file. In Terminal:

```bash
ls -l "$HOME/Google Drive (Home)/Grok Ops/YouTube/Affiliate Links.txt"
```

If `ls` fails, Google Drive has not mounted that folder, or the file is still online-only and has not been downloaded. Open the file once in Finder, or change **Links file** to where the file actually is.

**A product you know is in the file does not appear.**

The product line needs a URL. A line with no `http` is skipped, unless it is a `#` section or a `- ` note. A promo or alt line only attaches when it is indented and there is no blank line between it and the product.

**The wrong URL was copied.**

Return copies the row you highlighted. The main row is the first URL. A `(UK)` row is the region URL. An `(alt)` row is an alternate. ⌘Return copies the paste line, which is longer than the URL. The notification shows the exact clipboard text.

**The link was not pasted into the document.**

The workflow only copies. Click the document and press ⌘V.

**A note appeared and Return did nothing.**

That is a cleanup note. It is shown so you see the warning. Pick the product row above it when you want the link.

**Search feels out of date after you edit the text file.**

The script reads the file on every query. Save the text file and type the query again. There is no separate index.

**`/usr/bin/python3` is missing.**

Install the Xcode Command Line Tools (`xcode-select --install`). The Script Filter calls `/usr/bin/python3` directly. A Homebrew Python on your `PATH` is not used.

**The other Mac has an older copy, or two Affiliate Links workflows.**

Wait for Google Drive to finish the Alfred preferences folder. If a double-click import created a second copy, disable or delete the extra one in Alfred Preferences and keep the synced workflow. Then run `./scripts/install.sh` from this repository if you want the running files replaced with the git version.

**Alfred did not reload after install.**

Quit Alfred with ⌘Q and open it again. `install.sh` prints the folder it wrote. You can also reload from Terminal:

```bash
osascript -e 'tell application "Alfred" to reload workflow "com.retrocombs.affiliate-links"'
```

## Uninstall

1. Alfred Preferences → Workflows → Affiliate Links → right-click → Remove.
2. Removing the workflow does not change `Affiliate Links.txt`.

To drop the git checkout as well, delete `stevencombs/alfred-affiliate-links` from `~/.local/share/repos/github.txt` (and from the chezmoi source of that file), run `repos-sync`, and delete the Google Drive checkout when you are sure you want it gone. The GitHub repository stays until you delete it on GitHub.
