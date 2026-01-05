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
    .pin{ width:18px; height:18px; border-radius:50% 50% 50% 0; position:relative; transform: rotate(-45deg); background: var(--sea); border:2px solid #ffffff; box-shadow:0 3px 6px rgba(0,0,0,.25); }
    .pin::after{ content:""; width:6px; height:6px; background:#ffffff; position:absolute; top:5px; left:5px; border-radius:50%; }
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
]

LIST_NAV_ITEMS = [
    ("index.html", "Home"),
    ("day-trips-car.html", "Day Trips by Car"),
    ("day-trips-train.html", "Day Trips by Train"),
    ("trips-plane.html", "Trips by Plane"),
    ("trips-car.html", "Trips by Car"),
    ("trips-train.html", "Trips by Train"),
]


def make_nav(active_href):
    out = []
    for href, label in NAV_ITEMS:
        cls = "active" if href == active_href else ""
        out.append(f'        <a href="{href}" class="{cls}">{label}</a>')
    return "\n".join(out)


def make_list_nav(active_href):
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
          <div class="map-legend">
            <strong>Layers:</strong> {legend}
            {legend_extra}
          </div>
        </div>
      </section>
    """

    def js_array(items):
        return json.dumps(items, ensure_ascii=True)

    js = """
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <script>
    (function(){
      var mapEl = document.getElementById("trierMap");
      if (!mapEl || !window.L) return;
      var map = L.map("trierMap", { scrollWheelZoom: false }).setView([49.7566, 6.6420], 13);
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
      L.control.layers(null, {
        "Points of interest": poiLayer,
        "Parking garages": parkingLayer,
        "Recommended restaurants": restaurantLayer,
        "Family-friendly restaurants": familyRestaurantLayer,
        "Indoor attractions": indoorLayer
      }, { collapsed: false }).addTo(map);

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
    page = page.replace("__SCRIPTS__", scripts)
    return page


def list_card_html(dest, pill_label):
    highlights = ", ".join(dest["highlights"][:3])
    pill = f'<span class="pill">{pill_label}</span>' if pill_label else ""
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
            <span>Guide coming soon</span>
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


def build_list_page(destinations, title, lede, active_href, mode, day_trip, styles):
    cards = []
    for dest in destinations:
        dest_modes = dest.get("modes", [])
        if mode not in dest_modes:
            continue
        if day_trip and dest["length"] != "1 day":
            continue
        if not day_trip and dest["length"] == "1 day":
            continue
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
        )
        (ROOT / page["filename"]).write_text(html, encoding="utf-8")

    print(f"Generated {len(data)} destination pages and {len(list_pages)} list pages")


if __name__ == "__main__":
    main()
