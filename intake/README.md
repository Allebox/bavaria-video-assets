# Asset intake queue

This directory is the cloud-side handoff point for Bavaria Dental visual assets.

The ingest workflow accepts a temporary or durable HTTPS source URL, normalizes the image to WebP, stores it under `assets/approved/<category>/`, updates `asset-manifest.json`, commits, and pushes.

## Important

The source URL only needs to remain valid while the workflow is downloading it. The final video engine must use the repository asset path, not the intake URL.

## Categories

- planning
- clinical
- human
- aftercare
- location
- editorial
- brand
- comparison

## Usage

- video
- magazine
- both
- reference

Text-heavy posters should normally be `reference`; clean reusable visual material can be `video` or `both`.
