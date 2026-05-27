# Search recipes

Use Tavily by default for web verification. If `tvly` is unavailable, follow the `tavily-search` skill.

## Principles

- Verify product facts on official domains first.
- Do not mix product name and company name when they are ambiguous.
- Use secondary sources for context, not as the first source of truth for core product facts.
- Distinguish “shown in video” from “confirmed on web”.

## Minimum verification set

At minimum, check:

1. official homepage
2. official docs / help center
3. official pricing or packaging page if relevant
4. official changelog / release notes / blog when new behavior is shown

## Tavily query patterns

### Official site

```bash
tvly search "\"<product name>\" official site" --max-results 5 --json
```

If the official domain is known:

```bash
tvly search "\"<product name>\"" --include-domains <official_domain> --max-results 8 --json
```

### Docs / help

```bash
tvly search "\"<product name>\" docs OR help OR documentation" --include-domains <official_domain> --max-results 8 --json
```

### Pricing / packaging

```bash
tvly search "\"<product name>\" pricing OR plans" --include-domains <official_domain> --max-results 8 --json
```

### Changelog / release notes

```bash
tvly search "\"<product name>\" changelog OR release notes OR blog" --include-domains <official_domain> --max-results 8 --json
```

### Reddit

```bash
tvly search "site:reddit.com \"<product name>\"" --max-results 8 --json
```

### ProductHunt

```bash
tvly search "site:producthunt.com \"<product name>\"" --max-results 5 --json
```

### G2

```bash
tvly search "site:g2.com \"<product name>\"" --max-results 5 --json
```

### Company background

```bash
tvly search "\"<company name>\" founder funding" --max-results 8 --json
```

## What to verify vs. what to treat cautiously

Verify on official sources whenever possible:

- product name
- feature name
- pricing
- plan limits
- integrations
- platform support
- release timing

Treat cautiously unless strongly corroborated:

- total user count
- growth claims
- “AI-powered” marketing language
- comparison claims from the company itself
