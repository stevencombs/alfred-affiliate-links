# Affiliate Links for Alfred

Search your Affiliate Links file from Alfred and copy the line you need into a YouTube description, script, or document.

**Keyword:** `aff`  
**Bundle ID:** `com.retrocombs.affiliate-links`  
**Alfred:** 5 or later, with the Powerpack  
**Source:** https://github.com/stevencombs/alfred-affiliate-links

## Attribution

This workflow was built by:

- **Steven Combs (retroCombs)** — workflow design, the product list, ongoing maintenance, and the real-world use case for YouTube descriptions and documents. YouTube: [@retrocombs](https://www.youtube.com/@retrocombs) and [@retroCombs-tech](https://www.youtube.com/@retroCombs-tech). Site: [retrocombs.com](https://www.retrocombs.com).
- **Grok (xAI)** — Script Filter logic, path handling, packaging, Python compatibility fixes, and this documentation. Built in collaboration with Steven.

Use and modify freely. Attribution to both is appreciated.

## What it does

Type `aff` plus a product, brand, or section. Alfred lists matching rows from your `Affiliate Links.txt`.

| Key | Copies |
|---|---|
| Return | Full line: emoji, product name, and URL |
| ⌘Return | URL only |
| ⌥Return | UK line (emoji, name, and UK URL) when one exists |
| ⌃Return | Promo note when one exists |

The workflow copies to the clipboard and shows a notification. Paste with ⌘V. It does not type into the frontmost app, and it does not send your links file anywhere.

## Requirements

- macOS
- Alfred 5 or later with the Powerpack (Script Filters require the Powerpack)
- Python 3. `/usr/bin/python3` is used. If it is missing, install the Xcode Command Line Tools: `xcode-select --install`
- An `Affiliate Links.txt` file. The default path is below. Google Drive for desktop must be running for that path to exist, or you can point the workflow at any other file.

## Setup on any Mac

### 1. Install the workflow

Double-click [`Affiliate.Links.alfredworkflow`](https://github.com/stevencombs/alfred-affiliate-links/raw/main/Affiliate.Links.alfredworkflow).

Alfred asks to import it. If a workflow with the same bundle ID is already installed, replace it.

Or from a clone:

```bash
git clone https://github.com/stevencombs/alfred-affiliate-links.git
cd alfred-affiliate-links
./scripts/install.sh
```

### 2. Confirm the links file path

The default path is:

```text
~/Google Drive (Home)/Grok Ops/00 Common/Affiliates/Affiliate Links.txt
```

On another Mac, Google Drive may mount under a different folder name. Set the path:

1. Open Alfred Preferences → Workflows.
2. Select **Affiliate Links**.
3. Click **Configure Workflow** (upper right).
4. Set **Links file** to the full path of your `Affiliate Links.txt`. A leading `~` is expanded. Save.

If the file is missing, Alfred shows “Affiliate Links.txt not found” and the path it tried. Fix the path or wait until Google Drive finishes downloading the file.

### 3. Try it

1. Open Alfred.
2. Type `aff` and a space, then part of a product name (`aff elgato`, `aff sabrent`, `aff streamdeck`).
3. Highlight a row and press Return.
4. Paste into your document with ⌘V.

A space after `aff` is required. `affelgato` does not search. `aff elgato` does.

## Links file format

Plain UTF-8 text. The workflow understands the layout used in `Affiliate Links.txt`:

- `# Section name` starts a section.
- `EMOJI Product Name: https://…` is a product.
- `… | UK: https://…` adds a UK (or other short region) link.
- Indented lines under a product are promos or alternate URLs.
- Lines starting with `- ` are notes. They appear when they match, and they are not copied.

## Troubleshooting

**`aff` shows nothing.**  
Confirm the workflow is enabled in Alfred Preferences, the keyword is `aff`, and the Powerpack is active.

**File not found.**  
Check the path in Configure Workflow. In Terminal:

```bash
ls -l "$HOME/Google Drive (Home)/Grok Ops/00 Common/Affiliates/Affiliate Links.txt"
```

**Wrong text copied.**  
Return copies the full line for the highlighted row. A `(UK)` row is the UK line. An `(alt)` row is that alternate URL. ⌘Return always copies the URL alone.

**Nothing pasted into the document.**  
The workflow only copies. Click the document and press ⌘V.

**`/usr/bin/python3` is missing.**  
Install the Xcode Command Line Tools (`xcode-select --install`).

## Uninstall

Alfred Preferences → Workflows → Affiliate Links → right-click → Remove.  
This does not change your `Affiliate Links.txt`.

## License

Use and modify freely. Attribution to Steven Combs (retroCombs) and Grok (xAI) is appreciated.
