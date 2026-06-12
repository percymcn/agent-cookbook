---
name: creative-visual-artifacts
description: "Creative visual artifacts umbrella: quick HTML mockups, one-off landing/deck/prototype designs, architecture diagrams, design-token specs, ASCII art, hand-drawn diagrams, and browser-based generative sketches. Use to choose a visual artifact workflow and produce polished visual outputs."
---

# Creative Visual Artifacts

Use this umbrella to route visual/creative artifact requests. Choose the smallest workflow that produces the desired artifact, then verify by opening/rendering/exporting the output.

## Quick HTML/UI artifacts

For one-off landing pages, decks, prototypes, and mockups, create self-contained HTML/CSS/JS when possible. Offer 2-3 variants when the user is comparing directions. Favor real layout, typography, spacing, and responsive behavior over placeholder text.

## Architecture and diagram artifacts

For infrastructure or system diagrams, use SVG/HTML or Excalidraw-style JSON depending on requested aesthetics. Include labeled nodes, directional edges, boundaries, and a legend when helpful. For dark-themed cloud/infra diagrams, ensure contrast and readable labels.

## Design systems and tokens

For DESIGN.md/token specs, keep tokens semantic and exportable. Separate color, typography, spacing, radii, shadows, and component tokens. Validate the spec before treating it as complete.

## ASCII and text-based art

Use ASCII art for banners, terminal visuals, cowsay/boxes-style decorations, or image-to-ASCII. Keep output width appropriate for the destination. For animated/video ASCII, route to the heavier ASCII-video workflow rather than this quick-art section.

## Generative browser sketches

Use p5.js or pretext-style browser demos for generative art, shaders, kinetic typography, text-as-geometry, and interactive sketches. Default to a single-file HTML demo unless the project requires a bundled app.

## Heavy creative systems left standalone

Some creative workflows have large support packages and should remain as their own skills when needed: ComfyUI, Manim, TouchDesigner, Baoyu infographic/comic/illustration, popular design-template libraries, and full ASCII-video production.

## Verification

- Render/open generated HTML/SVG/JSON when feasible.
- For images/video, inspect output files or run a conversion/export command.
- Deliver local media with `MEDIA:/absolute/path` when appropriate.
