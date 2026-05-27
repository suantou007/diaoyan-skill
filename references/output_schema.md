# Output schema

The default deliverable is a **local research package**.

## Recommended folder layout

```text
<product>_video_analysis/
├── frames_10s/
├── contact_sheets/   # optional
├── selected_screenshots/
├── notes.md
└── analysis_manifest.json
```

## `notes.md` structure

Use a structure like this:

```markdown
# <Product name>

- Official URL:
- Source video:
- Analysis date:

## 1. Executive summary

## 2. Product snapshot

## 3. Evidence-backed feature breakdown

### 3.1 <Feature title>
- Timestamp:
- Screenshot:
- Observed in video:
- Confirmed on web:
- Inference / open question:
- Competitive significance:

## 4. Key workflow / user journey

## 5. Pricing / packaging

## 6. Market or review signals

## 7. Open questions and unverified claims

## 8. Asset paths
```

## `analysis_manifest.json`

Keep one entry per feature candidate. Minimum fields:

```json
{
  "product": "Example Product",
  "official_url": "https://example.com",
  "video": {
    "path": "/path/to/video.mp4",
    "duration_seconds": 540
  },
  "features": [
    {
      "id": "03_asset_library",
      "title": "Asset library with category filtering",
      "timestamp_start": "00:02:34",
      "timestamp_end": "00:02:50",
      "screenshots": [
        "selected_screenshots/03_asset_library.jpg"
      ],
      "observed_ui": [
        "Left sidebar shows asset categories",
        "Dragging an item places it into the scene"
      ],
      "confirmed_facts": [
        "Official site describes a reusable asset library"
      ],
      "inferences": [
        "Category taxonomy may also influence recommendation quality"
      ],
      "web_sources": [
        "official-homepage",
        "official-docs"
      ],
      "confidence": "high"
    }
  ]
}
```

Critical rule: keep `observed_ui`, `confirmed_facts`, and `inferences` separate.
