"""Extract lecture pptx decks into plain text + media the chapter writers can read.

Why: agents cannot open .pptx, and a naive <a:t> scrape drops the OMML equations
and speaker notes, which is exactly the background a chapter must restore.

Usage (from repo root):  python3 book_intro_2_ds/tools/extract_slides.py [deck.pptx ...]
Output: book_intro_2_ds/notes_text/<deck>/slides.md and media/<file> per deck.
Re-run it whenever a new deck lands in notes/.
"""
import glob
import html
import os
import re
import sys
import zipfile

OUT_ROOT = "book_intro_2_ds/notes_text"

# One token per text run (<a:t>) or math run (<m:t>), in document order.
TOKEN = re.compile(r"<(a|m):t(?:\s[^>]*)?>(.*?)</\1:t>", re.S)
PARA = re.compile(r"<a:p>(.*?)</a:p>", re.S)
MATH = re.compile(r"<m:oMath(?:\s[^>]*)?>(.*?)</m:oMath>", re.S)


def para_lines(xml: str) -> list[str]:
    """Paragraph texts; math runs are wrapped in [MATH: ...] so the writer knows to rebuild them."""
    lines = []
    for p in PARA.findall(xml):
        # Collapse each oMath block into one marked token before scanning runs.
        p = MATH.sub(lambda m: "<a:t>[MATH: " + "".join(t for _, t in TOKEN.findall(m.group(1))) + "]</a:t>", p)
        text = html.unescape("".join(t for _, t in TOKEN.findall(p))).strip()
        if text:
            lines.append(text)
    return lines


def slide_media(z: zipfile.ZipFile, n: int) -> list[str]:
    rels = f"ppt/slides/_rels/slide{n}.xml.rels"
    if rels not in z.namelist():
        return []
    targets = re.findall(r'Target="\.\./media/([^"]+)"', z.read(rels).decode("utf8"))
    return sorted(set(targets))


def notes_for(z: zipfile.ZipFile, n: int) -> list[str]:
    rels = f"ppt/slides/_rels/slide{n}.xml.rels"
    if rels not in z.namelist():
        return []
    m = re.search(r'Target="\.\./notesSlides/(notesSlide\d+\.xml)"', z.read(rels).decode("utf8"))
    if not m:
        return []
    lines = para_lines(z.read("ppt/notesSlides/" + m.group(1)).decode("utf8"))
    # The notes page repeats the slide number as a lone digit; drop it.
    return [l for l in lines if not l.isdigit()]


def extract(path: str) -> None:
    deck = os.path.splitext(os.path.basename(path))[0].replace(" ", "_")
    out_dir = os.path.join(OUT_ROOT, deck)
    os.makedirs(os.path.join(out_dir, "media"), exist_ok=True)
    z = zipfile.ZipFile(path)
    slides = sorted(
        (n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
        key=lambda n: int(re.search(r"\d+", n).group()),
    )
    parts = [f"# {deck}\n\nsource: `{path}` ({len(slides)} slides)\n"]
    for s in slides:
        n = int(re.search(r"\d+", s).group())
        parts.append(f"\n## Slide {n}\n")
        parts.extend(f"- {l}" for l in para_lines(z.read(s).decode("utf8")))
        media = slide_media(z, n)
        if media:
            parts.append("\nmedia: " + ", ".join(f"`media/{m}`" for m in media))
        notes = notes_for(z, n)
        if notes:
            parts.append("\nspeaker notes:")
            parts.extend(f"> {l}" for l in notes)
    for name in z.namelist():
        if name.startswith("ppt/media/"):
            with open(os.path.join(out_dir, "media", os.path.basename(name)), "wb") as f:
                f.write(z.read(name))
    with open(os.path.join(out_dir, "slides.md"), "w") as f:
        f.write("\n".join(parts) + "\n")
    print(f"{deck}: {len(slides)} slides -> {out_dir}")


if __name__ == "__main__":
    for p in sys.argv[1:] or sorted(glob.glob("notes/*.pptx")):
        extract(p)
