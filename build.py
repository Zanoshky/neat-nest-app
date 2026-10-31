"""Builds the guide pages in docs/ from the bodies below, so they share one head, bar and footer, writes docs/style.css
from src/tokens.css (the shared Zanoshky Standard tokens) and src/style.css, and refuses any dash used as punctuation
or any local file a page names that is not there. python3 build.py"""
import pathlib, re, sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE / 'docs'
PLAY = 'https://play.google.com/store/apps/details?id=com.zanoshky.neatnest'
SITE = 'https://neatnest.zanoski.com'
REPO = 'https://github.com/Zanoshky/neat-nest-app'
PAGES = [('index.html', 'Home'), ('guide.html', 'Guide'), ('faq.html', 'Questions'), ('report.html', 'Report a bug')]
CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>'
TICK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
PLAYICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 2.8v18.4c0 .6.7 1 1.2.7l15.6-9.2c.5-.3.5-1.1 0-1.4L5.2 2.1C4.7 1.8 4 2.2 4 2.8z"/></svg>'
LOOKS = [('auto', 'Follow the phone'), ('light', 'Light'), ('dark', 'Dark'), ('black', 'Black')]


def shell(file, title, desc, body):
    nav = ''.join(f'<a href="{f}"{" aria-current=\"page\"" if f == file else ""}>{n}</a>' for f, n in PAGES[1:])
    looks = ''.join(f'<button type="button" data-look="{i}" aria-pressed="false">{TICK}{n}</button>' for i, n in LOOKS)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Neat Nest user guide</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#f6f7f9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<script>try{{var l=localStorage.getItem('look');if(l==='light'||l==='dark'||l==='black')document.documentElement.dataset.look=l}}catch(e){{}}</script>
<meta property="og:title" content="{title} · Neat Nest user guide">
<meta property="og:description" content="{desc}">
<link rel="icon" href="img/icon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/JetBrainsMono-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/inter-regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <div class="wrap">
    <a class="brand" href="index.html"{" aria-current=\"page\"" if file == "index.html" else ""}><img src="img/icon.svg" alt="" width="34" height="34"><span>Neat Nest</span></a>
    <nav class="pages" aria-label="Guide pages">{nav}</nav>
    <a class="key filled get" href="{PLAY}">Get the app</a>
  </div>
</header>
<main id="main" class="page">
  <div class="wrap">
{body}
  </div>
</main>
<footer>
  <div class="wrap">
    <span class="by">Neat Nest by <a href="https://zanoski.com">Marko Zanoski</a></span>
    <nav aria-label="Footer"><a href="{SITE}">Home</a><a href="index.html"{" aria-current=\"page\"" if file in ("index.html", "guide.html", "faq.html") else ""}>User guide</a><a href="report.html"{" aria-current=\"page\"" if file == "report.html" else ""}>Report a bug</a><a href="{SITE}/privacy">Privacy</a><a href="{SITE}/terms">Terms</a></nav>
    <div class="looks" role="group" aria-label="Look"><span aria-hidden="true">Look</span>{looks}</div>
    <p class="lic">Guide text and images are shared under CC BY 4.0. The Neat Nest app itself is proprietary.</p>
  </div>
</footer>
<script>
(function () {{
  var html = document.documentElement, bs = document.querySelectorAll('.looks button');
  function show() {{ var cur = html.dataset.look || 'auto'; bs.forEach(function (b) {{ b.setAttribute('aria-pressed', String(b.dataset.look === cur)); }}); }}
  bs.forEach(function (b) {{ b.addEventListener('click', function () {{
    var l = b.dataset.look;
    if (l === 'auto') delete html.dataset.look; else html.dataset.look = l;
    try {{ if (l === 'auto') localStorage.removeItem('look'); else localStorage.setItem('look', l); }} catch (e) {{}}
    show();
  }}); }});
  show();
}})();
</script>
</body>
</html>
'''


def shot(name, alt, cap, lazy=True):
    return (f'<figure><img src="img/{name}-360.jpg" srcset="img/{name}-360.jpg 360w, img/{name}.jpg 720w" '
            f'sizes="(min-width: 1000px) 175px, (min-width: 600px) 30vw, 45vw" width="360" height="800"'
            f'{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} alt="{alt}"><figcaption>{cap}</figcaption></figure>')


def pair(*shots):
    return '<div class="fig">' + ''.join(shot(*s) for s in shots) + '</div>'


def toc(items):
    return '<ul class="plate toc">' + ''.join(f'<li><a href="{h}"><span>{n}</span>{CHEV}</a></li>' for h, n in items) + '</ul>'


INDEX = f'''    <p class="kicker">User guide</p>
    <h1>Neat Nest</h1>
    <p class="lead">A text editor for Android that turns into a JSON viewer, formatter and compare tool. Text, Tree and Table views, a JSONPath filter, and a structural compare. Pay once, no ads, works offline. This guide is for Neat Nest 1.1.0.</p>
    <div class="shots">
      {shot("0-home", "The home screen: Open a file, tiles for New JSON, New text, Paste and Compare JSON, and the open documents.", "Home", False)}
      {shot("1-text", "The Text view with line numbers and JSON colours, the tool row above and undo and redo below.", "Text view", False)}
      {shot("2-tree", "The Tree view with the JSONPath filter box and objects opened, each value coloured by type.", "Tree view")}
      {shot("3-compare", "Compare: two versions of a file, 1 added, 2 removed and 3 changed, with the changed version number marked.", "Compare")}
      {shot("4-table", "The Table view of an array of orders, with id, customer name and customer city columns.", "Table view")}
      {shot("7-settings", "Settings: the Look tiles Follow the phone, Default Light, Default Dark and Black, and the editor themes.", "Settings")}
    </div>
    <div class="keys cta">
      <a class="key filled" href="guide.html">Read the guide</a>
      <a class="key tonal" href="report.html">Report a bug or ask for a feature</a>
    </div>
    <h2 style="margin-top:48px">In this guide</h2>
    {toc([("guide.html#home", "The home screen"), ("guide.html#open", "Open and save a file"), ("guide.html#text", "The Text view"), ("guide.html#tree", "The Tree view"), ("guide.html#table", "The Table view"), ("guide.html#filter", "JSONPath filter"), ("guide.html#compare", "Compare two JSON files"), ("guide.html#big", "Big files"), ("guide.html#widgets", "Widgets and shortcuts"), ("guide.html#settings", "Settings")])}'''

GUIDE = f'''    <p class="kicker">Guide</p>
    <h1>How Neat Nest works</h1>
    <p class="lead">Every screen of Neat Nest 1.1.0, in the order you meet them.</p>
    <article>
    <h2 id="home">The home screen</h2>
    <p>The name sits at the top with Settings at the far right. Below it, Open a file, then four tiles: New JSON, New text, Paste and Compare JSON. Paste starts a document from what you copied last.</p>
    <p>Open documents lists what you are working on, each with whether it is saved. Its three dots give Open, Compare with another JSON and Close. Recent files shows the last four files you opened (six on a tablet) and ends in a See all row with the whole list. A recent file's three dots can remove it from the list. On the very first start there is nothing open yet, and Try the sample opens a small JSON file to try the views on.</p>
    <p>On your home screen holds the two widget keys, Quick actions widget and Recent files widget. On a tablet, the open and recent files sit in a column on the right.</p>
    {pair(("0-home", "The home screen with four open documents.", "Home"), ("9-more", "The More menu as a sheet from the bottom.", "The More menu"))}

    <h2 id="open">Open and save a file</h2>
    <p>Tap Open a file and pick it in Android's file picker. Or start from another app: tap a .json or .txt file in Files, Gmail or Drive and pick Neat Nest. When Android asks, tap Always to open such files in Neat Nest every time. If another app already opens JSON files, the home screen names it and has a button to its app info, where Open by default, Clear defaults sets it free. Show me how explains the steps; Got it hides the card.</p>
    <p>You can also Share a file or some text to Neat Nest, and select JSON in any app and pick Open in Neat Nest from the menu that appears.</p>
    <p>Everything you type is kept on the phone as you type. The line under the name says where the file stands: Saved, Changes not saved, or Not saved to a file. The save button at the top writes back to the same file. The three dots at the top right open More, a sheet from the bottom:</p>
    <dl class="plate">
      <dt>Save and Save as</dt><dd>Save writes back to the file; Save as writes a copy wherever you pick. A document that came without a file asks where to save the first time. In Compare there is also Save the right side.</dd>
      <dt>Share</dt><dd>Sends the text to another app.</dd>
      <dt>Find and replace</dt><dd>Opens the find bar, see the Text view.</dd>
      <dt>Compare with another JSON</dt><dd>Starts Compare, or Exit compare while it is on.</dd>
      <dt>Treat as plain text, or Treat as JSON</dt><dd>Switches a file between the JSON views and plain text.</dd>
      <dt>Wrap long lines</dt><dd>On when it has a tick.</dd>
      <dt>Settings</dt><dd>Opens Settings.</dd>
      <dt>Close this document</dt><dd>Last, in red. It removes the document from Neat Nest; your file stays where it is. A text that was never saved to a file asks first.</dd>
    </dl>
    <p>A document that was never saved to a file gets its name from you: tap the name at the top to change it.</p>

    <h2 id="text">The Text view</h2>
    <p>For JSON, the Text, Tree and Table tabs sit under the top bar, with the tools in a row under them: Format, Compact, Sort keys, Wrap, Find and Copy all (Expand all and Collapse all in the Tree view). On a phone the tools are icons; touch and hold one to see its name. On a wide screen they carry their names.</p>
    <dl class="plate">
      <dt>Line numbers and colours</dt><dd>Keys, strings, numbers and true, false and null each have a colour. Turn colours or line numbers off in Settings.</dd>
      <dt>Status</dt><dd>At the bottom: Valid JSON, or the line and column of the first error with what is wrong, plus the line count and size. Tap an error to jump to it.</dd>
      <dt>Undo, redo and the path</dt><dd>Under the status: undo and redo, then the path of the value under the cursor, like <code>$.orders[3].total</code>, with a copy button. While the keyboard is up the two rows fold into one.</dd>
      <dt>Key row</dt><dd>Over the keyboard: {{ }} [ ] : , " and Tab. Turn it off in Settings.</dd>
      <dt>Wrap</dt><dd>Folds long lines to the screen. Turn it off and each line stays one line, and the text scrolls sideways as well as up and down.</dd>
      <dt>Find and replace</dt><dd>The search tool opens find and replace, with Previous, Next, Replace and All.</dd>
      <dt>Format, Compact, Sort keys</dt><dd>Format indents with 2 spaces (or 4, in Settings), Compact removes the spaces, Sort keys orders every object's keys. They work from any view. Numbers keep their exact digits.</dd>
    </dl>
    {pair(("1-text", "The Text view of a JSON file.", "Text view"), ("6-error", "Invalid JSON: line 7 is marked and the status says a comma before a closing brace is not allowed.", "An error, with its line and column"))}

    <h2 id="tree">The Tree view</h2>
    <p>Tap an object or array to open or close it. Tap a value, or the three dots on any row, for Edit value, Copy value, Copy path, Open everything inside (on an object or array) and Delete, last in red. Typed values keep their type: <code>42</code> is a number, <code>true</code> a boolean, <code>null</code> null, anything else text. Expand all and Collapse all are in the tool row. Arrays show 200 items at a time, with a Show more row at the end. A tree edit writes the whole file back formatted.</p>

    <h2 id="table">The Table view</h2>
    <p>An array of objects, or an object that holds one, becomes a table. Nested keys become dotted columns like <code>customer.city</code>. Tap a column header to sort it up, again for down, again to go back. Tap a cell to see all of it and copy it. Tables show the first 1,000 rows.</p>
    {pair(("2-tree", "The Tree view with the filter box.", "Tree view"), ("4-table", "The Table view of an array of orders.", "Table view"))}

    <h2 id="filter">JSONPath filter</h2>
    <p>In the Tree and Table views, type a query in the filter box at the top:</p>
    <dl class="plate">
      <dt>$.store.book[0].title</dt><dd>names and indexes; the leading $ is optional</dd>
      <dt>items[-1] and items[1:3]</dt><dd>from the end, and slices</dd>
      <dt>$.a[*] and $..id</dt><dd>every child, and every id at any depth</dd>
      <dt>users[?(@.age &gt;= 18)]</dt><dd>filters with == != &lt; &lt;= &gt; &gt;=, =~ /regex/i, &amp;&amp;, || and !</dd>
    </dl>
    <p>The box shows how many match. Tap a match for Show in the tree, Copy value and Copy path. In the Table view the matches become the rows. The cross clears the filter.</p>
    {pair(("5-query", "A filter for open orders in the Table view, with 12 matches as rows.", "A filter in the Table view"), ("2-tree", "The filter box over the Tree view.", "The filter box in the Tree view"))}

    <h2 id="compare">Compare two JSON files</h2>
    <p>Start it from More, Compare with another JSON, from the Compare JSON tile on the home screen, or from the Quick actions widget. Pick the second JSON: Open a file, Paste from the clipboard, another open document, or Empty, I will type or paste. Key order and formatting do not count as a change, and array items are lined up by value.</p>
    <p>A bar under the top bar holds Exit, Swap sides, and once there is a difference, Previous and Next with where you are, like 1 of 6. Under it the counts: added, removed, changed and the same. Tap a count to list those changes and go to one. In the Tree view changed values are marked with a tilde, added with a plus and removed with a minus, each with its own colour. On a tablet or in landscape the two sides sit next to each other; on a phone, Left and Right tabs switch between them.</p>
    {pair(("3a-compare-pick", "Compare with: Open a file, or Empty, I will type or paste.", "Pick the second JSON"), ("3-compare", "Compare with the counts and the changed version number marked.", "Compare"))}

    <h2 id="big">Big files</h2>
    <p>Neat Nest opens files up to 20 MB. Up to about 800 KB the Text view edits everything. Past that, the Text view reads the file and scrolls it smoothly (drag the right edge to move fast), and you change values in the Tree view or with Format, Sort keys and Replace all.</p>

    <h2 id="widgets">Widgets and shortcuts</h2>
    <p>Two widgets: Quick actions (Open, New, Paste, Compare) and Recent files. Add them with the keys on Neat Nest's home screen or in Settings, Widgets, or from your home screen's widget list. Touch and hold the app icon for the same shortcuts.</p>

    <h2 id="settings">Settings</h2>
    <p>Settings fills the screen, with Back at the top. In order:</p>
    <dl class="plate">
      <dt>Look</dt><dd>Four tiles: Follow the phone (Light by day, Dark at night), Default Light, Default Dark and Black (true black for OLED). These three are held to 7:1 contrast. Under them, Editor themes, in their own colours: a list of 20 popular editor themes such as Dracula, One Dark Pro, Nord and Solarized, with a sample of the editor below.</dd>
      <dt>Editor</dt><dd>Text size from 10 to 20 (14 is the default), indent when formatting (2 or 4 spaces), Wrap long lines, Line numbers, JSON colours, Bracket and quote keys over the keyboard, and Plain text files in a reading font, not mono.</dd>
      <dt>Opening files</dt><dd>Which app opens JSON files on this phone right now, and How to open files.</dd>
      <dt>Widgets</dt><dd>Quick actions and Recent files.</dd>
      <dt>Privacy</dt><dd>The promises on red ban chips (No ads, No tracking, No analytics, No crash reports, No error reports, No account, No AI, No internet), and the permissions Neat Nest never asks for. It asks for none at all.</dd>
      <dt>Help</dt><dd>User guide, Report a bug or ask for a feature, and Privacy policy.</dd>
      <dt>Support the developer</dt><dd>A link to buymeacoffee.com/zanoshky.</dd>
      <dt>About</dt><dd>Neat Nest and its version, the privacy line, and the font and icon credits.</dd>
    </dl>
    <p>Neat Nest follows Android's own font size up to 200 percent and works with TalkBack.</p>
    {pair(("7-settings", "Settings: the Look tiles and the editor themes list.", "Look"), ("8-privacy", "Settings, Privacy: the promises on red ban chips, and Help.", "Privacy and Help"))}
    </article>'''

FAQ = '''    <p class="kicker">Questions</p>
    <h1>Questions and fixes</h1>
    <article>
    <h2>Neat Nest is not in the list when I tap a file</h2>
    <p>Some apps send JSON files as an unknown type. Open Neat Nest and use Open a file instead, or Share the file to Neat Nest.</p>
    <h2>Another app keeps opening my JSON files</h2>
    <p>Neat Nest's home screen names that app. Open its app info, tap Open by default, then Clear defaults. Next time, pick Neat Nest and Always. Settings, Opening files says which app opens them now.</p>
    <h2>It says the file is read only here</h2>
    <p>The app that handed over the file did not allow writing to it. Save makes a copy where you pick. Opening the file with Open a file instead usually allows saving back.</p>
    <h2>The Tree view says the document is not valid JSON</h2>
    <p>Go to the Text view; the status at the bottom shows the line and column of the first problem. Tap it to jump there. Common ones are a comma before } or ], single quotes, and comments, which JSON does not allow.</p>
    <h2>A warning says a number may be rounded</h2>
    <p>Numbers over 9007199254740991, or with more than 17 digits, cannot be kept exactly by many other apps and languages. Neat Nest keeps them as written; the warning is for whatever reads the file next.</p>
    <h2>Copy says the text is too big for the clipboard</h2>
    <p>Android's clipboard holds about a megabyte. Use Share or Save as for bigger text.</p>
    <h2>Where did the compare button go?</h2>
    <p>Since 1.1.0 the top bar of the editor holds only Save and More. Compare is in More, Compare with another JSON, on the home screen's Compare JSON tile and in the Quick actions widget.</p>
    <h2>Does Neat Nest send my files anywhere?</h2>
    <p>No. It has no internet access at all. See the <a href="https://neatnest.zanoski.com/privacy">privacy policy</a>.</p>
    </article>'''

REPORT = f'''    <p class="kicker">Report</p>
    <h1>Report a bug or ask for a feature</h1>
    <p class="lead">Found something broken, or have an idea? Tell us on GitHub. A free GitHub account is all you need.</p>
    <ul class="plate feat report">
      <li class="fr"><span class="tile"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m8 2 1.9 1.9M14.1 3.9 16 2M9 7.1v-1a3 3 0 1 1 6 0v1"/><path d="M12 20c-3.3 0-6-2.7-6-6v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3c0 3.3-2.7 6-6 6M12 20v-9M6.5 13H3M21 13h-3.5"/></svg></span><div><b>Bug report</b><span>Something does not work, looks wrong or crashes.</span></div><a class="key filled" href="{REPO}/issues/new?template=bug_report.yml">Report a bug</a></li>
      <li class="fr"><span class="tile"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5M9 18h6M10 22h4"/></svg></span><div><b>Feature request</b><span>Something you would like Neat Nest to do.</span></div><a class="key tonal" href="{REPO}/issues/new?template=feature_request.yml">Ask for a feature</a></li>
    </ul>
    <article>
    <h2>Before you write</h2>
    <ul>
      <li>Search the <a href="{REPO}/issues">open issues</a> first. If yours is there, add a thumbs up or a comment.</li>
      <li>Check the <a href="faq.html">questions and fixes</a>.</li>
      <li>One problem per report makes it faster to fix.</li>
    </ul>
    <h2>What helps</h2>
    <dl class="plate">
      <dt>App version</dt><dd>Neat Nest, Settings, the About card at the bottom.</dd>
      <dt>Phone model and Android version</dt><dd>Android settings, About phone.</dd>
      <dt>Which view</dt><dd>Text, Tree, Table, Compare, the filter, find and replace, a widget or Settings.</dd>
      <dt>Steps</dt><dd>What you did, one step per line.</dd>
      <dt>A small file that shows it</dt><dd>Only if it holds nothing private.</dd>
    </dl>
    <p>Issues on GitHub are public. Never paste private data, keys or passwords, and crop screenshots.</p>
    <h2>Other ways</h2>
    <p>Prefer not to use GitHub? Write to zanoski.marko@gmail.com (<a href="mailto:zanoski.marko@gmail.com">write an email</a>).</p>
    </article>'''

(ROOT / 'style.css').write_text((HERE / 'src/tokens.css').read_text() + '\n' + (HERE / 'src/style.css').read_text())
print('built style.css')

bad = 0
for (file, title), desc, body in zip(PAGES,
        ['The user guide for Neat Nest, the JSON and text editor for Android.', 'How to use Neat Nest 1.1.0: the home screen, opening and saving files, Text, Tree and Table views, JSONPath, Compare, widgets and Settings.',
         'Answers to common questions about Neat Nest.', 'How to report a Neat Nest bug or ask for a feature.'],
        [INDEX, GUIDE, FAQ, REPORT]):
    html = shell(file, title, desc, body)
    text = re.sub(r'<[^>]+>', ' ', re.sub(r'<(style|script)[\s\S]*?</\1>', '', html))
    for m in re.finditer(r'\s[-–—]\s|–|—', text):
        bad += 1; print(file, 'dash near', text[max(0, m.start() - 30):m.end() + 30].replace('\n', ' '))
    for m in re.finditer(r'(?:src|href|srcset)="([^"#?:]+)"', html):
        for part in m.group(1).split(','):
            f = part.strip().split(' ')[0]
            if f and '.' in f and not (ROOT / f).exists():
                bad += 1; print(file, 'missing', f)
    (ROOT / file).write_text(html)
    print('built', file)
sys.exit(1 if bad else 0)
