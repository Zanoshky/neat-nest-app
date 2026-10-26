"""Builds the guide pages in docs/ from the bodies below, so they share one head, bar and footer, and refuses any
dash used as punctuation. python3 build.py"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).parent / 'docs'
PLAY = 'https://play.google.com/store/apps/details?id=com.zanoshky.neatnest'
SITE = 'https://neatnest.zanoski.com'
REPO = 'https://github.com/Zanoshky/neat-nest-app'
PAGES = [('index.html', 'Home'), ('guide.html', 'Guide'), ('faq.html', 'Questions'), ('report.html', 'Report a bug')]

def shell(file, title, desc, body):
    nav = ''.join(f'<a href="{f}"{" aria-current=\"page\"" if f == file else ""}>{n}</a>' for f, n in PAGES)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Neat Nest user guide</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} · Neat Nest user guide">
<meta property="og:description" content="{desc}">
<link rel="icon" href="img/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="img/icon.svg" alt="" width="34" height="34"><span>Neat Nest</span></a>
    <nav aria-label="Guide pages">{nav}</nav>
  </div>
</header>
<main id="main" class="page">
  <div class="wrap">
{body}
  </div>
</main>
<footer>
  <div class="wrap">
    <span>Guide text and images are shared under CC BY 4.0. The Neat Nest app itself is proprietary. Made by Marko Zanoski.</span>
    <nav aria-label="Footer"><a href="{PLAY}">Google Play</a><a href="{SITE}">neatnest.zanoski.com</a><a href="{REPO}/issues">Issues</a><a href="{SITE}/privacy">Privacy</a></nav>
  </div>
</footer>
</body>
</html>
'''

def shot(name, alt, cap):
    return f'<figure><img src="img/{name}.jpg" alt="{alt}" width="540" height="1200" loading="lazy"><figcaption>{cap}</figcaption></figure>'

INDEX = f'''    <p class="kicker">User guide</p>
    <h1>Neat Nest</h1>
    <p class="sub" style="margin-top:12px;color:var(--soft);font-size:1.15rem;max-width:40em">A text editor for Android that turns into a JSON viewer, formatter and compare tool. Text, Tree and Table views, a JSONPath filter, and a structural compare. Pay once, no ads, works offline.</p>
    <div class="shots">
      {shot("1-text", "The Text view with line numbers and JSON colours, and the Text, Tree and Table tabs above it.", "Text view")}
      {shot("2-tree", "The Tree view with objects opened, each value coloured by type.", "Tree view")}
      {shot("3-compare", "Compare: two versions of a file, with a changed version number, an added key and a removed key marked.", "Compare")}
      {shot("4-table", "The Table view of an array of orders, with id, customer and city columns.", "Table view")}
    </div>
    <div class="cta">
      <a class="btn main" href="guide.html">Read the guide</a>
      <a class="btn" href="report.html">Report a bug or ask for a feature</a>
    </div>'''

GUIDE = '''    <p class="kicker">Guide</p>
    <h1>How Neat Nest works</h1>
    <article>
    <h2>Open a file</h2>
    <p>On the home screen, tap Open a file and pick it in Android's file picker. Or start from another app: tap a .json or .txt file in your file manager, mail or cloud app and pick Neat Nest. When Android asks, tap Always to open such files in Neat Nest every time. If another app already opens JSON files, the home screen names it and has a button to its app info, where Open by default, Clear defaults sets it free.</p>
    <p>You can also Share a file or some text to Neat Nest, and select JSON in any app and pick Open in Neat Nest from the menu that appears. New JSON, New text and Paste start a document without a file.</p>
    <h2>Saving</h2>
    <p>Everything you type is kept on the phone as you type. The line under the name says whether the file has it yet: Saved, or Changes not saved. Tap the save button to write back to the same file. Save as in the menu writes a copy wherever you pick. A document that came without a file asks where to save the first time. Close this document in the menu, or on the home screen, removes it from Neat Nest; your file stays where it is.</p>
    <h2>The Text view</h2>
    <dl>
      <dt>Line numbers and colours</dt><dd>Keys, strings, numbers and true, false and null each have a colour. Turn colours or line numbers off in Settings.</dd>
      <dt>Status bar</dt><dd>Valid JSON, or the line and column of the first error with what is wrong. Tap an error to jump to it. Below it, the path of the value under the cursor, like <code>$.orders[3].total</code>, with a copy button.</dd>
      <dt>Key row</dt><dd>Over the keyboard: undo, redo, { } [ ] : , " and Tab.</dd>
      <dt>Wrap</dt><dd>The wrap button folds long lines to the screen. Turn it off and each line stays one line, and the text scrolls sideways as well as up and down.</dd>
      <dt>Find and replace</dt><dd>The search button opens find and replace, with Previous, Next, Replace and All.</dd>
      <dt>Format, Compact, Sort keys</dt><dd>Format indents with 2 spaces (or 4, in Settings), Compact removes the spaces, Sort keys orders every object's keys. They work from any view. Numbers keep their exact digits.</dd>
    </dl>
    <h2>The Tree view</h2>
    <p>Tap an object or array to open or close it. Tap a value, or the three dots on any row, for Edit value, Copy value, Copy path and Delete. Typed values keep their type: <code>42</code> is a number, <code>true</code> a boolean, <code>null</code> null, anything else text. Expand all and Collapse all are in the toolbar. Arrays show 200 items at a time, with Show more at the end. A tree edit writes the whole file back formatted.</p>
    <h2>The Table view</h2>
    <p>An array of objects, or an object that holds one, becomes a table. Nested keys become dotted columns like <code>customer.city</code>. Tap a column header to sort it up, again for down, again to go back. Tap a cell to see all of it and copy it. Tables show the first 1,000 rows.</p>
    <h2>JSONPath filter</h2>
    <p>In the Tree and Table views, type a query in the filter box:</p>
    <dl>
      <dt>$.store.book[0].title</dt><dd>names and indexes; the leading $ is optional</dd>
      <dt>items[-1] and items[1:3]</dt><dd>from the end, and slices</dd>
      <dt>$.a[*] and $..id</dt><dd>every child, and every id at any depth</dd>
      <dt>users[?(@.age &gt;= 18)]</dt><dd>filters with == != &lt; &lt;= &gt; &gt;=, =~ /regex/i, &amp;&amp;, || and !</dd>
    </dl>
    <p>Tap a match for Show in the tree, Copy value and Copy path. In the Table view the matches become the rows.</p>
    <h2>Compare</h2>
    <p>Tap the compare button at the top and pick the second JSON: a file, the clipboard, or another open document. The Tree view then shows both. Key order and formatting do not count; array items are lined up by value. Changed values are marked with a tilde, added with a plus, removed with a minus, each with its own colour. The counts at the top list them; tap one to see where. The arrows step through every difference. Swap puts the sides the other way round. On a tablet or in landscape the sides sit next to each other.</p>
    <h2>Big files</h2>
    <p>Neat Nest opens files up to 20 MB. Up to about 800 KB the Text view edits everything. Past that, the Text view reads the file and scrolls it smoothly (drag the right edge to move fast), and you change values in the Tree view or with Format, Sort keys and Replace all.</p>
    <h2>Widgets and shortcuts</h2>
    <p>Two widgets: Quick actions (Open, New, Paste, Compare) and Recent files. Add them from the home screen's widget list, or from the buttons on Neat Nest's home screen. Touch and hold the app icon for the same shortcuts.</p>
    <h2>Settings</h2>
    <p>Theme (follow the phone, light, dark or black), text size, indent, wrap, line numbers, colours, the key row, and a reading font for plain text files. Neat Nest follows Android's own font size up to 200 percent and works with TalkBack.</p>
    </article>'''

FAQ = '''    <p class="kicker">Questions</p>
    <h1>Questions and fixes</h1>
    <article>
    <h2>Neat Nest is not in the list when I tap a file</h2>
    <p>Some apps send JSON files as an unknown type. Open Neat Nest and use Open a file instead, or Share the file to Neat Nest.</p>
    <h2>Another app keeps opening my JSON files</h2>
    <p>Neat Nest's home screen names that app. Open its app info, tap Open by default, then Clear defaults. Next time, pick Neat Nest and Always.</p>
    <h2>It says the file is read only here</h2>
    <p>The app that handed over the file did not allow writing to it. Save makes a copy where you pick. Opening the file with Open a file instead usually allows saving back.</p>
    <h2>The Tree view says the document is not valid JSON</h2>
    <p>Go to the Text view; the status bar shows the line and column of the first problem. Tap it to jump there. Common ones are a comma before } or ], single quotes, and comments, which JSON does not allow.</p>
    <h2>A warning says a number may be rounded</h2>
    <p>Numbers over 9007199254740991, or with more than 17 digits, cannot be kept exactly by many other apps and languages. Neat Nest keeps them as written; the warning is for whatever reads the file next.</p>
    <h2>Copy says the text is too big for the clipboard</h2>
    <p>Android's clipboard holds about a megabyte. Use Share or Save as for bigger text.</p>
    <h2>Does Neat Nest send my files anywhere?</h2>
    <p>No. It has no internet access at all. See the <a href="https://neatnest.zanoski.com/privacy">privacy policy</a>.</p>
    </article>'''

REPORT = f'''    <p class="kicker">Report</p>
    <h1>Report a bug or ask for a feature</h1>
    <p>Found something broken, or have an idea? Tell us on GitHub. A free GitHub account is all you need.</p>
    <div class="grid">
      <div class="card"><h3>Bug report</h3><p>Something does not work, looks wrong or crashes.</p><p style="margin-top:16px"><a class="btn main" href="{REPO}/issues/new?template=bug_report.yml">Report a bug</a></p></div>
      <div class="card"><h3>Feature request</h3><p>Something you would like Neat Nest to do.</p><p style="margin-top:16px"><a class="btn" href="{REPO}/issues/new?template=feature_request.yml">Ask for a feature</a></p></div>
    </div>
    <article>
    <h2>Before you write</h2>
    <ul>
      <li>Search the <a href="{REPO}/issues">open issues</a> first. If yours is there, add a thumbs up or a comment.</li>
      <li>Check the <a href="faq.html">questions and fixes</a>.</li>
      <li>One problem per report makes it faster to fix.</li>
    </ul>
    <h2>What helps</h2>
    <dl>
      <dt>App version</dt><dd>Neat Nest, Settings, at the bottom.</dd>
      <dt>Phone model and Android version</dt><dd>Android settings, About phone.</dd>
      <dt>Which view</dt><dd>Text, Tree, Table, Compare, the filter, find and replace, a widget or Settings.</dd>
      <dt>Steps</dt><dd>What you did, one step per line.</dd>
      <dt>A small file that shows it</dt><dd>Only if it holds nothing private.</dd>
    </dl>
    <p>Issues on GitHub are public. Never paste private data, keys or passwords, and crop screenshots.</p>
    <h2>Other ways</h2>
    <p>Prefer not to use GitHub? Write to zanoski.marko@gmail.com (<a href="mailto:zanoski.marko@gmail.com">write an email</a>).</p>
    </article>'''

bad = 0
for (file, title), desc, body in zip(PAGES,
        ['The user guide for Neat Nest, the JSON and text editor for Android.', 'How to use Neat Nest: opening and saving files, Text, Tree and Table views, JSONPath, Compare and widgets.',
         'Answers to common questions about Neat Nest.', 'How to report a Neat Nest bug or ask for a feature.'],
        [INDEX, GUIDE, FAQ, REPORT]):
    html = shell(file, title, desc, body)
    text = re.sub(r'<[^>]+>', ' ', html)
    for m in re.finditer(r'\s[-–—]\s|–|—', text):
        bad += 1; print(file, 'dash near', text[max(0, m.start() - 30):m.end() + 30].replace('\n', ' '))
    (ROOT / file).write_text(html)
    print('built', file)
sys.exit(1 if bad else 0)
