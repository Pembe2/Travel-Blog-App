import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "destinations.json"
TEMPLATE_PATH = ROOT / "templates" / "destination.html"
INDEX_PATH = ROOT / "index.html"


def load_base_css():
    if not INDEX_PATH.exists():
        return ""
    html = INDEX_PATH.read_text(encoding="utf-8")
    match = re.search(r"<style>(.*)</style>", html, re.S)
    return match.group(1).strip() if match else ""


EXTRA_CSS = """
    .hero{ display:grid; gap:14px; }
    .hero img{ width:100%; height:320px; object-fit:cover; border-radius:18px; border:1px solid var(--line); box-shadow:0 14px 30px rgba(28,27,24,.12); }
    .slideshow{ border-radius:18px; overflow:hidden; border:1px solid var(--line); box-shadow:0 14px 30px rgba(28,27,24,.12); }
    .slide{ display:none; }
    .slide.active{ display:block; }
    .slide img{ width:100%; height:360px; object-fit:cover; display:block; }
    .meta-grid{ display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:14px; margin-top:10px; }
    .meta-card{ background:rgba(255,255,255,.76); border:1px solid var(--line); border-radius:14px; padding:12px 14px; }
    .meta-card h4{ margin:0 0 6px; font-size:12px; color:var(--muted); text-transform:uppercase; letter-spacing:.4px; }
    .meta-card p{ margin:0; font-weight:700; font-size:14px; }
    .section{ margin-top:22px; padding-top:6px; }
    .section h2{ font-family:"Fraunces", Georgia, serif; font-size:22px; margin:0 0 10px; }
    .list{ margin:0; padding-left:18px; color:var(--muted); font-size:14px; }
    .list li{ margin-bottom:6px; }
    .itinerary{ display:grid; gap:10px; }
    .day{ background:rgba(255,255,255,.76); border:1px solid var(--line); border-radius:14px; padding:12px 14px; }
    .day h3{ margin:0 0 6px; font-size:15px; }
    .breadcrumb{ font-size:12px; color:var(--muted); }
    .notice{ margin-top:14px; padding:12px 14px; border-radius:14px; border:1px dashed var(--line); background:rgba(255,255,255,.7); color:var(--muted); font-size:13px; }
    .notice strong{ color:var(--ink); }
    #trierMap{ width:100%; height:360px; }
    .map-card{ margin-top:10px; border:1px solid var(--line); border-radius:16px; overflow:hidden; background:rgba(255,255,255,.76); }
    .map-legend{ padding:12px 14px; border-top:1px solid var(--line); font-size:13px; color:var(--muted); }
    .map-legend strong{ color:var(--ink); }
    .layer-legend{ display:grid; gap:8px; margin-top:10px; }
    .layer-toggle{ display:flex; align-items:center; gap:8px; font-size:12px; color:var(--muted); }
    .layer-toggle input{ width:14px; height:14px; }
    .layer-swatch{ width:12px; height:12px; border-radius:50%; display:inline-block; border:1px solid rgba(0,0,0,.1); }
    .pin{ width:18px; height:18px; border-radius:50% 50% 50% 0; position:relative; transform: rotate(-45deg); background: var(--sea); border:2px solid #ffffff; box-shadow:0 3px 6px rgba(0,0,0,.25); }
    .pin::after{ content:""; width:6px; height:6px; background:#ffffff; position:absolute; top:5px; left:5px; border-radius:50%; }
    .notes{ border:1px dashed var(--line); border-radius:16px; padding:14px; background:rgba(255,255,255,.7); }
    .notes-header{ display:flex; align-items:center; justify-content:space-between; gap:12px; }
    .notes-header h2{ margin:0; font-size:18px; }
    .notes-toggle{ border:1px solid var(--line); border-radius:999px; padding:8px 14px; background:#fff; font-size:12px; text-transform:uppercase; letter-spacing:.6px; cursor:pointer; }
    .notes-body{ margin-top:12px; display:grid; gap:10px; }
    .notes-body[hidden]{ display:none; }
    .notes textarea{ width:100%; min-height:160px; resize:vertical; border:1px solid var(--line); border-radius:12px; padding:10px 12px; font-family:inherit; font-size:14px; }
    .notes-actions{ display:flex; flex-wrap:wrap; align-items:center; gap:10px; }
    .notes-actions button{ border:1px solid var(--line); border-radius:10px; padding:8px 12px; background:#fff; font-size:13px; cursor:pointer; }
    .notes-status{ color:var(--muted); font-size:12px; }
    @media (max-width: 900px){ .hero img{ height:260px; } }
    @media (max-width: 600px){ .hero img{ height:220px; } }
    @media (max-width: 900px){ .slide img{ height:300px; } }
    @media (max-width: 600px){ .slide img{ height:220px; } }
""".strip()


NAV_ITEMS = [
    ("../index.html", "Home"),
    ("../day-trips-car.html", "Day Trips by Car"),
    ("../day-trips-train.html", "Day Trips by Train"),
    ("../trips-plane.html", "Trips by Plane"),
    ("../trips-car.html", "Trips by Car"),
    ("../trips-train.html", "Trips by Train"),
    ("../kinder-hotels.html", "Kinder Hotels"),
    ("../future-destinations.html", "Future Destinations"),
]

LIST_NAV_ITEMS = [
    ("index.html", "Home"),
    ("day-trips-car.html", "Day Trips by Car"),
    ("day-trips-train.html", "Day Trips by Train"),
    ("trips-plane.html", "Trips by Plane"),
    ("trips-car.html", "Trips by Car"),
    ("trips-train.html", "Trips by Train"),
    ("kinder-hotels.html", "Kinder Hotels"),
    ("future-destinations.html", "Future Destinations"),
]

NAV_ACTIVE_ALIAS = {
    "center-parcs.html": "kinder-hotels.html",
    "../center-parcs.html": "../kinder-hotels.html",
}


def make_nav(active_href):
    active_href = NAV_ACTIVE_ALIAS.get(active_href, active_href)
    out = []
    for href, label in NAV_ITEMS:
        cls = "active" if href == active_href else ""
        out.append(f'        <a href="{href}" class="{cls}">{label}</a>')
    return "\n".join(out)


def make_list_nav(active_href):
    active_href = NAV_ACTIVE_ALIAS.get(active_href, active_href)
    out = []
    for href, label in LIST_NAV_ITEMS:
        cls = "active" if href == active_href else ""
        out.append(f'        <a href="{href}" class="{cls}">{label}</a>')
    return "\n".join(out)


def list_items(items):
    return "".join(f"<li>{i}</li>" for i in items)


def itinerary_html(dest):
    custom = dest.get("itinerary") or []
    if custom:
        blocks = [(item.get("title", "Stop"), item.get("text", "")) for item in custom]
    elif dest.get("length") == "1 day":
        blocks = [
            ("Morning", "Start with a top highlight and a short walk."),
            ("Midday", "Lunch in the center, then an easy kid stop."),
            ("Afternoon", "Main landmark plus a park or viewpoint."),
            ("Late afternoon", "Wrap up and head home before evening."),
        ]
    else:
        blocks = [
            ("Day 1", "Arrival and neighborhood walk, light sightseeing."),
            ("Day 2", "Main landmarks and a family-friendly museum or park."),
            ("Day 3", "Day trip or water time, relaxed pace."),
            ("Day 4", "Flexible day for markets, cafes, and local favorites."),
            ("Day 5", "Departure day with a short activity if time allows."),
        ]
    return "".join(f'<div class="day"><h3>{title}</h3><p>{text}</p></div>' for title, text in blocks)


def slideshow_html(dest):
    photos = dest.get("photo_deck") or []
    if not photos:
        return ""
    items = []
    for idx, photo in enumerate(photos):
        cls = "slide active" if idx == 0 else "slide"
        items.append(
            f'<div class="{cls}"><img src="{photo["src"]}" alt="{photo.get("alt", "")}" loading="lazy" decoding="async" /></div>'
        )
    return f'<div class="slideshow" data-slideshow="1">{"".join(items)}</div>'


def map_section(map_cfg):
    if not map_cfg:
        return "", ""

    legend = map_cfg.get("legend", "")
    source_label = map_cfg.get("source_label", "")
    source_url = map_cfg.get("source_url", "")
    legend_extra = ""
    if source_label and source_url:
        legend_extra = f'<br /><strong>{source_label}:</strong> <a href="{source_url}" target="_blank" rel="noopener">Source link</a>.'

    html = f"""
      <section class="section">
        <h2>Map: family-friendly points of interest</h2>
        <div class="map-card">
          <div id="trierMap" aria-label="Map of destination points"></div>
        </div>
        <div class="map-legend">
          <strong>Layers:</strong> {legend}
          {legend_extra}
          <div class="layer-legend" aria-label="Map layers">
            <label class="layer-toggle"><input type="checkbox" data-layer="poi" checked /> <span class="layer-swatch" style="background:#2b7a78;"></span> Points of interest</label>
            <label class="layer-toggle"><input type="checkbox" data-layer="parking" checked /> <span class="layer-swatch" style="background:#f4b942;"></span> Parking garages</label>
            <label class="layer-toggle"><input type="checkbox" data-layer="restaurants" checked /> <span class="layer-swatch" style="background:#e86f5b;"></span> Recommended restaurants</label>
            <label class="layer-toggle"><input type="checkbox" data-layer="family" checked /> <span class="layer-swatch" style="background:#4a76c9;"></span> Family-friendly restaurants</label>
            <label class="layer-toggle"><input type="checkbox" data-layer="indoor" checked /> <span class="layer-swatch" style="background:#7a5ca8;"></span> Indoor attractions</label>
          </div>
        </div>
      </section>
    """

    def js_array(items):
        return json.dumps(items, ensure_ascii=True)

    def pick_center(cfg, fallback):
        if "center" in cfg and cfg["center"]:
            return cfg["center"]
        for key in ("poi", "parking", "restaurants", "family_restaurants", "indoor"):
            items = cfg.get(key) or []
            if items:
                first = items[0]
                if "lat" in first and "lon" in first:
                    return {"lat": first["lat"], "lon": first["lon"]}
        return fallback

    center = pick_center(map_cfg, {"lat": 49.7566, "lon": 6.6420})

    js = """
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <script>
    (function(){
      var mapEl = document.getElementById("trierMap");
      if (!mapEl || !window.L) return;
      var map = L.map("trierMap", { scrollWheelZoom: false }).setView(__CENTER__, 13);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors"
      }).addTo(map);

      function mapLink(name){
        var query = encodeURIComponent(name + " Trier Germany");
        return "https://www.google.com/maps/search/?api=1&query=" + query;
      }

      function addPin(layer, p, color, link){
        var icon = L.divIcon({
          className: "",
          html: '<div class="pin" style="background:' + color + ';"></div>',
          iconSize: [18, 18],
          iconAnchor: [9, 18],
          popupAnchor: [0, -16]
        });
        var popup = link ? '<a href="' + link + '" target="_blank" rel="noopener">' + p.name + '</a>' : p.name;
        L.marker([p.lat, p.lon], { icon: icon }).addTo(layer).bindPopup(popup);
      }

      var poiLayer = L.layerGroup();
      var parkingLayer = L.layerGroup();
      var restaurantLayer = L.layerGroup();
      var familyRestaurantLayer = L.layerGroup();
      var indoorLayer = L.layerGroup();

      var poiPoints = __POI__;
      var parkingPoints = __PARKING__;
      var restaurantPoints = __RESTAURANTS__;
      var familyRestaurantPoints = __FAMILY_RESTAURANTS__;
      var indoorPoints = __INDOOR__;

      poiPoints.forEach(function(p){ addPin(poiLayer, p, "#2b7a78"); });
      parkingPoints.forEach(function(p){ addPin(parkingLayer, p, "#f4b942"); });
      restaurantPoints.forEach(function(p){ addPin(restaurantLayer, p, "#e86f5b", mapLink(p.name)); });
      familyRestaurantPoints.forEach(function(p){ addPin(familyRestaurantLayer, p, "#4a76c9", mapLink(p.name)); });
      indoorPoints.forEach(function(p){ addPin(indoorLayer, p, "#7a5ca8", mapLink(p.name)); });

      poiLayer.addTo(map);
      parkingLayer.addTo(map);
      restaurantLayer.addTo(map);
      familyRestaurantLayer.addTo(map);
      indoorLayer.addTo(map);

      var toggles = document.querySelectorAll(".layer-toggle input");
      toggles.forEach(function(toggle){
        toggle.addEventListener("change", function(){
          var key = toggle.getAttribute("data-layer");
          var layer = null;
          if (key === "poi") layer = poiLayer;
          if (key === "parking") layer = parkingLayer;
          if (key === "restaurants") layer = restaurantLayer;
          if (key === "family") layer = familyRestaurantLayer;
          if (key === "indoor") layer = indoorLayer;
          if (!layer) return;
          if (toggle.checked) layer.addTo(map); else map.removeLayer(layer);
        });
      });

      var all = L.featureGroup([poiLayer, parkingLayer, restaurantLayer, familyRestaurantLayer, indoorLayer]);
      map.fitBounds(all.getBounds().pad(0.15));
    })();
  </script>
    """

    js = js.replace("__POI__", js_array(map_cfg.get("poi", [])))
    js = js.replace("__PARKING__", js_array(map_cfg.get("parking", [])))
    js = js.replace("__RESTAURANTS__", js_array(map_cfg.get("restaurants", [])))
    js = js.replace("__FAMILY_RESTAURANTS__", js_array(map_cfg.get("family_restaurants", [])))
    js = js.replace("__INDOOR__", js_array(map_cfg.get("indoor", [])))
    js = js.replace("__CENTER__", json.dumps([center["lat"], center["lon"]], ensure_ascii=True))

    return html, js


def slideshow_script():
    return """
  <script>
    (function(){
      var shows = document.querySelectorAll("[data-slideshow='1']");
      for (var i = 0; i < shows.length; i++){
        (function(wrapper){
          var slides = wrapper.querySelectorAll(".slide");
          if (!slides.length) return;
          var index = 0;
          function setSlide(next){
            index = (next + slides.length) % slides.length;
            for (var j = 0; j < slides.length; j++){
              slides[j].classList.toggle("active", j === index);
            }
          }
          setSlide(0);
          setInterval(function(){ setSlide(index + 1); }, 10000);
        })(shows[i]);
      }
    })();
  </script>
    """


def notes_script():
    return """
  <script>
    (function(){
      var section = document.querySelector(".notes");
      if (!section) return;
      var slug = section.getAttribute("data-notes-slug");
      var key = "kmcNotes:" + slug;
      var toggle = section.querySelector(".notes-toggle");
      var body = section.querySelector(".notes-body");
      var textarea = section.querySelector("textarea");
      var status = section.querySelector(".notes-status");
      var saveBtn = section.querySelector(".notes-save");
      var clearBtn = section.querySelector(".notes-clear");
      var saveTimer = null;

      function setStatus(text){
        if (!status) return;
        status.textContent = text || "";
      }

      function loadNotes(){
        var saved = localStorage.getItem(key) || "";
        textarea.value = saved;
        setStatus(saved ? "Loaded from this browser." : "No notes saved yet.");
      }

      function saveNotes(){
        localStorage.setItem(key, textarea.value.trim());
        setStatus("Saved.");
      }

      function scheduleSave(){
        if (saveTimer) clearTimeout(saveTimer);
        saveTimer = setTimeout(saveNotes, 600);
      }

      toggle.addEventListener("click", function(){
        var isOpen = !body.hasAttribute("hidden");
        if (isOpen) {
          body.setAttribute("hidden", "");
          toggle.setAttribute("aria-expanded", "false");
          toggle.textContent = "Show notes";
        } else {
          body.removeAttribute("hidden");
          toggle.setAttribute("aria-expanded", "true");
          toggle.textContent = "Hide notes";
        }
      });

      saveBtn.addEventListener("click", function(){
        saveNotes();
      });

      clearBtn.addEventListener("click", function(){
        textarea.value = "";
        saveNotes();
      });

      textarea.addEventListener("input", scheduleSave);
      loadNotes();
    })();
  </script>
    """


def build_page(dest, template, styles):
    nav = make_nav("../" + dest["category_page"])
    groomed = bool(dest.get("groomed", False))
    notice = ""
    if not groomed:
        notice = (
            '<div class="notice"><strong>Research in progress:</strong> '
            'This destination page is a placeholder. Details will be expanded after on-the-ground review.</div>'
        )
    indoor = dest.get("indoor_attractions", [])
    indoor_section = ""
    if indoor:
        indoor_section = f"""
      <section class="section">
        <h2>Indoor attractions</h2>
        <ul class="list">{list_items(indoor)}</ul>
      </section>
        """
    elif not groomed:
        indoor_section = """
      <section class="section">
        <h2>Indoor attractions</h2>
        <div class="notice"><strong>Research in progress:</strong> Indoor options will be added for winter visits.</div>
      </section>
        """

    lede = dest.get("description") or dest.get("summary", "")
    description = dest.get("description") or dest.get("summary", "")
    recommended_stops = dest.get("recommended_stops") or []
    lodging = dest.get("lodging") or []
    access_note = dest.get("access_note", "").strip()

    slideshow = slideshow_html(dest)
    hero_image = ""
    if not slideshow:
        hero_image = f'<img src="{dest["image"]}" alt="{dest["alt"]}" loading="lazy" decoding="async" />'

    body = f"""
      <div class="breadcrumb"><a href="../{dest['category_page']}">Back to {dest['category_label']}</a></div>
      {notice}
      <div class="hero">
        {slideshow}
        {hero_image}
        <div class="meta-grid">
          <div class="meta-card"><h4>Travel style</h4><p>{dest['tag']}</p></div>
          <div class="meta-card"><h4>Ideal length</h4><p>{dest['length']}</p></div>
          <div class="meta-card"><h4>Season</h4><p>Summer</p></div>
          <div class="meta-card"><h4>Family fit</h4><p>{dest['best_for']}</p></div>
        </div>
      </div>

      <section class="section">
        <h2>Why families love it</h2>
        <p class="lede">{description}</p>
        <ul class="list">{list_items(dest['highlights'])}</ul>
      </section>

      <section class="section">
        <h2>Suggested {dest['length']} plan</h2>
        <div class="itinerary">{itinerary_html(dest)}</div>
      </section>
    """

    map_html, map_scripts = map_section(dest.get("map"))
    if map_html:
        body += map_html
    if indoor_section:
        body += indoor_section
    if recommended_stops:
        body += f"""
      <section class="section">
        <h2>Recommended stops</h2>
        <ul class="list">{list_items(recommended_stops)}</ul>
      </section>
        """
    if lodging:
        body += f"""
      <section class="section">
        <h2>Where to stay</h2>
        <ul class="list">{list_items(lodging)}</ul>
      </section>
        """
    if access_note:
        body += f"""
      <section class="section">
        <h2>Getting there</h2>
        <p class="lede">{access_note}</p>
      </section>
        """

    body += f"""
      <section class="section">
        <h2>Family travel tips</h2>
        <ul class="list">{list_items(dest['tips'])}</ul>
      </section>
    """

    body += f"""
      <section class="section notes" data-notes-slug="{dest['slug']}">
        <div class="notes-header">
          <h2>Notes on this destination</h2>
          <button class="notes-toggle" type="button" aria-expanded="false">Show notes</button>
        </div>
        <div class="notes-body" hidden>
          <p class="lede">Private notes stored in this browser only.</p>
          <textarea placeholder="Add trip notes, ideas, and edits to apply later."></textarea>
          <div class="notes-actions">
            <button class="notes-save" type="button">Save now</button>
            <button class="notes-clear" type="button">Clear</button>
            <span class="notes-status" aria-live="polite"></span>
          </div>
        </div>
      </section>
    """

    page = template
    page = page.replace("__TITLE__", f"KMC Exploration | {dest['title']}")
    page = page.replace("__STYLES__", styles)
    page = page.replace("__NAV__", nav)
    page = page.replace("__HEADING__", dest["title"])
    page = page.replace("__LEDE__", lede)
    page = page.replace("__BODY__", body)
    scripts = ""
    if slideshow:
        scripts += slideshow_script()
    if map_scripts:
        scripts += map_scripts
    scripts += notes_script()
    page = page.replace("__SCRIPTS__", scripts)
    return page


def list_card_html(dest, pill_label):
    highlights = ", ".join(dest["highlights"][:3])
    pill = f'<span class="pill">{pill_label}</span>' if pill_label else ""
    groomed = bool(dest.get("groomed", False))
    guide_label = "" if groomed else "<span>Guide coming soon</span>"
    return f"""
      <article class="card">
        <a href="destinations/{dest['slug']}.html">
          <img src="{dest['image']}" alt="{dest['alt']}" loading="lazy" decoding="async" />
        </a>
        <div class="card-body">
          <div class="tag">{dest['tag']}</div>
          <h3><a href="destinations/{dest['slug']}.html">{dest['title']}</a></h3>
          <p class="summary">{dest['summary']}</p>
          <ul class="facts">
            <li><span>Ideal length</span>{dest['length']}</li>
            <li><span>Family highlights</span>{highlights}</li>
            <li><span>Best for</span>{dest['best_for']}</li>
          </ul>
          <div class="cta">
            {guide_label}
            {pill}
          </div>
        </div>
      </article>
    """


def pill_for_list(dest, mode, day_trip):
    if day_trip:
        return "Day trip"
    if mode == "plane":
        return "Flight friendly"
    if mode == "train":
        return "Rail friendly"
    if mode == "car":
        return "Drive friendly"
    return ""


def build_list_page(destinations, title, lede, active_href, mode, day_trip, styles, groomed_only=True):
    cards = []
    seen = set()
    for dest in destinations:
        if groomed_only and not dest.get("groomed"):
            continue
        slug = dest.get("slug")
        if slug in seen:
            continue
        dest_modes = dest.get("modes", [])
        if mode not in dest_modes:
            continue
        if day_trip and dest["length"] != "1 day":
            continue
        if not day_trip and dest["length"] == "1 day":
            continue
        seen.add(slug)
        cards.append(list_card_html(dest, pill_for_list(dest, mode, day_trip)))

    cards_html = "\n".join(cards)
    nav = make_list_nav(active_href)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
{styles}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar" aria-label="Category navigation">
      <div class="brand">KMC Exploration</div>
      <div class="nav">
{nav}
      </div>
      <p class="note">Built for military and support families in the Kaiserslautern Military Community.</p>
    </aside>
    <main class="content">
      <header>
        <h1>{title.split('|')[-1].strip()}</h1>
        <p class="lede">{lede}</p>
      </header>
      <section class="grid" aria-label="{title}">
{cards_html}
      </section>
      <footer>
        Photos sourced from Wikimedia Commons. Travel times are approximate from KMC / Frankfurt area.
      </footer>
    </main>
  </div>
</body>
</html>
"""


def build_future_page(destinations, title, lede, active_href, styles):
    cards = []
    for dest in destinations:
        if dest.get("groomed"):
            continue
        cards.append(list_card_html(dest, "Research pending"))

    cards_html = "\n".join(cards) if cards else '<div class="notice"><strong>All set:</strong> No future destinations queued yet.</div>'
    nav = make_list_nav(active_href)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
{styles}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar" aria-label="Category navigation">
      <div class="brand">KMC Exploration</div>
      <div class="nav">
{nav}
      </div>
      <p class="note">Built for military and support families in the Kaiserslautern Military Community.</p>
    </aside>
    <main class="content">
      <header>
        <h1>{title.split('|')[-1].strip()}</h1>
        <p class="lede">{lede}</p>
      </header>
      <section class="grid" aria-label="{title}">
{cards_html}
      </section>
      <footer>
        Photos sourced from Wikimedia Commons. Travel times are approximate from KMC / Frankfurt area.
      </footer>
    </main>
  </div>
</body>
</html>
"""


def build_category_page(destinations, title, lede, active_href, category_page, styles, groomed_only=True):
    cards = []
    for dest in destinations:
        if groomed_only and not dest.get("groomed"):
            continue
        if dest.get("category_page") != category_page:
            continue
        cards.append(list_card_html(dest, "Resort stay"))

    cards_html = "\n".join(cards) if cards else '<div class="notice"><strong>Coming soon:</strong> More stays will be added.</div>'
    nav = make_list_nav(active_href)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
{styles}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar" aria-label="Category navigation">
      <div class="brand">KMC Exploration</div>
      <div class="nav">
{nav}
      </div>
      <p class="note">Built for military and support families in the Kaiserslautern Military Community.</p>
    </aside>
    <main class="content">
      <header>
        <h1>{title.split('|')[-1].strip()}</h1>
        <p class="lede">{lede}</p>
      </header>
      <section class="grid" aria-label="{title}">
{cards_html}
      </section>
      <footer>
        Photos sourced from Wikimedia Commons. Travel times are approximate from KMC / Frankfurt area.
      </footer>
    </main>
  </div>
</body>
</html>
"""


def build_category_hub_page(title, lede, active_href, styles, categories):
    cards = []
    for cat in categories:
        cards.append(
            f"""        <a class="category-card" href="{cat['href']}">
          <h3>{cat['title']}</h3>
          <p>{cat['description']}</p>
          <span class="link">{cat['link']}</span>
        </a>"""
        )

    cards_html = "\n".join(cards) if cards else '<div class="notice"><strong>Coming soon:</strong> Subcategories will be added.</div>'
    nav = make_list_nav(active_href)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
{styles}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar" aria-label="Category navigation">
      <div class="brand">KMC Exploration</div>
      <div class="nav">
{nav}
      </div>
      <p class="note">Built for military and support families in the Kaiserslautern Military Community.</p>
    </aside>
    <main class="content">
      <header>
        <h1>{title.split('|')[-1].strip()}</h1>
        <p class="lede">{lede}</p>
      </header>
      <section class="category-grid" aria-label="{title}" style="margin-top:18px;">
{cards_html}
      </section>
      <footer>
        Photos sourced from Wikimedia Commons. Travel times are approximate from KMC / Frankfurt area.
      </footer>
    </main>
  </div>
</body>
</html>
"""


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    styles = (load_base_css() + "\n\n" + EXTRA_CSS).strip()

    for dest in data:
        modes = dest.get("modes") or []
        if not modes:
            tag = (dest.get("tag") or "").lower()
            if "train" in tag:
                modes.append("train")
            if "drive" in tag or "car" in tag:
                modes.append("car")
            if "fly" in tag or "plane" in tag:
                modes.append("plane")
            dest["modes"] = modes

    dest_dir = ROOT / "destinations"
    dest_dir.mkdir(parents=True, exist_ok=True)

    for dest in data:
        html = build_page(dest, template, styles)
        (dest_dir / f"{dest['slug']}.html").write_text(html, encoding="utf-8")

    list_pages = [
        {
            "filename": "day-trips-car.html",
            "title": "KMC Exploration | Day Trips by Car",
            "lede": "Short drives for beaches, parks, and castles you can finish in a single day.",
            "mode": "car",
            "day_trip": True,
        },
        {
            "filename": "day-trips-train.html",
            "title": "KMC Exploration | Day Trips by Train",
            "lede": "Family-friendly rail outings with walkable centers and easy station access.",
            "mode": "train",
            "day_trip": True,
        },
        {
            "filename": "trips-plane.html",
            "title": "KMC Exploration | Trips by Plane",
            "lede": "Summer long-weekend trips that are easiest to reach by flight.",
            "mode": "plane",
            "day_trip": False,
        },
        {
            "filename": "trips-car.html",
            "title": "KMC Exploration | Trips by Car",
            "lede": "Longer drives worth a 4 to 5 day vacation and family-friendly stays.",
            "mode": "car",
            "day_trip": False,
        },
        {
            "filename": "trips-train.html",
            "title": "KMC Exploration | Trips by Train",
            "lede": "Long-weekend rail journeys with easy station access and walkable centers.",
            "mode": "train",
            "day_trip": False,
        },
    ]

    for page in list_pages:
        html = build_list_page(
            data,
            page["title"],
            page["lede"],
            page["filename"],
            page["mode"],
            page["day_trip"],
            styles,
            groomed_only=True,
        )
        (ROOT / page["filename"]).write_text(html, encoding="utf-8")

    kinder_hotels_page = build_category_hub_page(
        "KMC Exploration | Kinder Hotels",
        "Family-first resort brands with on-site activities, pools, and easy cabin stays.",
        "kinder-hotels.html",
        styles,
        [
            {
                "title": "Center Parcs",
                "description": "Forest resort villages with cabins, lakes, indoor water parks, and kid-focused activities.",
                "href": "center-parcs.html",
                "link": "Browse Center Parcs ->",
            }
        ],
    )
    (ROOT / "kinder-hotels.html").write_text(kinder_hotels_page, encoding="utf-8")

    center_parcs_page = build_category_page(
        data,
        "KMC Exploration | Center Parcs",
        "Resort villages with cottages, aqua domes, and family activities close to Germany.",
        "center-parcs.html",
        "center-parcs.html",
        styles,
        groomed_only=True,
    )
    (ROOT / "center-parcs.html").write_text(center_parcs_page, encoding="utf-8")

    future_page = build_future_page(
        data,
        "KMC Exploration | Future Destinations",
        "Places we want to research next. These cards stay here until we finish field notes.",
        "future-destinations.html",
        styles,
    )
    (ROOT / "future-destinations.html").write_text(future_page, encoding="utf-8")

    print(f"Generated {len(data)} destination pages and {len(list_pages) + 3} list pages")


if __name__ == "__main__":
    main()
