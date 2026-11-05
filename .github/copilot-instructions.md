# Instructions for GitHub Copilot

## Design System

This project uses DESIGN.md as the source of truth for visual decisions.

Before generating any UI component, form, page or style:
1. Read the DESIGN.md file at the project root
2. Use exclusively the colors, typography and spacing defined there
3. Follow the documented component patterns (buttons, cards, inputs)
4. Respect the constraints listed in the "Constraints" section

### Mandatory rules

- Colors: use only tokens from DESIGN.md, never hardcoded values
- Typography: respect the defined scale, no invented sizes
- Spacing: use multiples of the base (8px)
- Components: follow documented states (hover, focus, disabled)
- Never violate the Constraints section

### When there's no definition

If DESIGN.md doesn't cover a specific case, ask before inventing.
Prefer consistency with existing patterns over novel decisions.