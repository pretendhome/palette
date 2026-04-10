---
tags:
  - dashboard
---

# Project Dashboard

## Active Decisions by Mode

### Committed
```dataview
TABLE convergence.route AS Route, convergence.confidence AS "Conf %", convergence.next_action AS "Next Action"
FROM "projects"
WHERE convergence.mode = "commit"
SORT convergence.confidence DESC
```

### Converging
```dataview
TABLE convergence.route AS Route, convergence.confidence AS "Conf %", convergence.next_action AS "Next Action"
FROM "projects"
WHERE convergence.mode = "converge"
SORT convergence.confidence DESC
```

### Exploring
```dataview
TABLE convergence.route AS Route, convergence.confidence AS "Conf %", convergence.next_action AS "Next Action"
FROM "projects"
WHERE convergence.mode = "explore"
SORT convergence.confidence DESC
```

## What Needs Attention

### Low Confidence (< 50%)
```dataview
LIST convergence.next_action
FROM "projects"
WHERE convergence.confidence < 50
SORT convergence.confidence ASC
```

### Has Blockers
```dataview
TABLE convergence.blocked AS Blockers
FROM "projects"
WHERE length(convergence.blocked) > 0
```

### Missing Evidence
```dataview
TABLE length(convergence.missing) AS "Missing Count", convergence.missing AS "What's Missing"
FROM "projects"
WHERE length(convergence.missing) > 2
SORT length(convergence.missing) DESC
```

## Full Overview

```dataview
TABLE convergence.mode AS Mode, convergence.route AS Route, convergence.confidence AS "Conf %", convergence.updated AS Updated
FROM "projects"
WHERE convergence.mode
SORT convergence.mode ASC, convergence.confidence DESC
```
