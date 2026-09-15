# Bavaria Dental Video Asset Library

Remote visual asset library for the Bavaria Dental HyperFrames video engine.

## Locked rules

- HyperFrames CSS/UX is the primary visual language.
- Existing approved assets are preferred over new generation.
- Maximum **2 newly generated images per video**.
- During test operation, generation is locked to **gpt-image-1-mini**.
- Generated images are supporting visual motifs, never complete ad layouts.
- Text, CTA, cards, backgrounds, gradients, diagrams, masks and motion belong to HyperFrames/CSS.
- A scene may deliberately use no image.
- Bavaria Dental works with a partner clinic; imagery must not imply ownership of a clinic or an in-house medical team.

## Brand

Main text: `#0D1117`  
Background: `#F3F1EB`  
Panel: `#F9F9F9`  
Gold: `#B6965E`  
Dark gold: `#4E4028`  
Display: Playfair Display  
Body: Inter

The former `#295970` secondary color is retained only as legacy metadata and is disabled by default.

## Asset resolution order

1. CSS/UX only
2. Existing approved library asset
3. New image generation, only if materially useful

Asset metadata lives in `asset-manifest.json`.
