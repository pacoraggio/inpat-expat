# A Corto Muso — Article Plan

## Project identity

**Series:** Reinventing the Wheel
**Working title:** A Corto Muso — Massimiliano Allegri and the Statistics of Grinding

**The question:** Does Massimiliano Allegri genuinely manage differently from his peers
— specifically, does he systematically produce narrow-margin victories, low scoring,
and defensive solidity — or is *a corto muso* a narrative the Italian football
culture has built around results that any title-winning manager would produce?

**The vehicle:** Football. The real subject: what statistical analysis can and
cannot tell us in messy, non-reproducible real-world conditions.

**Two readers simultaneously:**
- The football fan who wants to know if Allegri is really a *corto muso* manager
- The data-curious reader learning what statistical analysis can and cannot do in the wild

Both get something. Neither feels talked down to.

## Editorial line

Caveats are not collected at the end — they are woven into the analysis,
flagged at the moment each chart or result is shown. The epistemological
contract is set in the introduction and honoured throughout.

Underlying position: it is OK, useful, and genuinely fun to use statistics
in football — once you know the caveats and limitations. Every limitation
flagged is not a weakness in the analysis. It is the lesson.

## Narrative arc

1. **Introduce *a corto muso*** — what it means culturally in Italian football.
   Allegri as the archetype. The phrase as a style, a philosophy, a provocation.

2. **The epistemological contract** — the cognac party paragraph. Set the terms
   of the analysis before showing a single number. Correlation is not causation;
   here is why that matters, and here is why we proceed anyway.

3. **What we can measure** — the three signatures of *a corto muso*:
   - Higher share of 1-0 and 2-1 wins (narrow margin victories)
   - Lower goals against (defensive solidity)
   - Lower goals scored (not chasing goals when ahead)

4. **Allegri's overall distribution** — career-long, Big 5 only.
   The 1-0 modal scoreline as the opening exhibit.

5. **The natural experiment** — before/during/after the Juventus spells.
   Two separate spells means two natural experiments on the same club.
   This is the methodological backbone of the article.

6. **Position-matched baseline** — is this just what title-winning teams
   look like? Compare Allegri's Juventus to other Serie A title winners
   across different years. Controls for league position and expected dominance.

7. **Widening the lens** — how Allegri compares to the other managers
   in the dataset. Is he an outlier or is narrow-margin winning common
   among elite managers?

8. **Honest conclusion** — what the pattern suggests, what it cannot prove,
   and why that is fine. No lab in football. That is why we love it.

## Analytical design

### Managers in scope

| Manager | Primary league |
|---|---|
| Massimiliano Allegri | Serie A |
| Pep Guardiola | Premier League, Bundesliga, La Liga |
| José Mourinho | Premier League, La Liga, Serie A |
| Antonio Conte | Serie A, Premier League |
| Carlo Ancelotti | Serie A, La Liga, Premier League, Bundesliga |
| Roberto De Zerbi | Premier League |
| Vincenzo Italiano | Serie A |
| Simone Inzaghi | Serie A |
| Maurizio Sarri | Serie A, Premier League |

Scope: Big 5 domestic leagues only (GB1, IT1, ES1, L1, FR1).
Turkish and Portuguese spells excluded by design.

### The three comparisons

**1. Career distribution**
One row per manager per match. Goals for, goals against, goal difference,
result (W/D/L), home/away flag. Source: `manager_matches.csv`.

**2. Before/during/after spell**
For each manager-club spell: pull the club's result distribution in the
season immediately before and immediately after the spell.
- One season on each side (extendable later if patterns warrant it)
- Two separate spells treated as two separate natural experiments
- If no before/after season exists in the DB, that boundary is skipped gracefully
- Source: `game_index` table in `tm_football.db`

**3. Position-matched league baseline**
For each league-season in which a manager appears, calculate the result
distribution of all teams that finished in the same final position across
other years. Controls for the fact that dominant teams naturally produce
different scoreline distributions.
- Final Serie A standings: available for last 80 seasons (separate dataset)
- Other leagues: to be derived from `game_index` match results

### Data files

| File | Content | Status |
|---|---|---|
| `tm_football.db` | Raw data lake, SQLite | Done |
| `manager_matches.csv` | One row per manager per match | Done |
| `league_baselines.csv` | Full league distributions by season | To build |
| `spell_comparisons.csv` | Before/during/after per manager-club spell | To build |
| `position_baselines.csv` | Position-matched distributions | To build |

## Scientific concerns and how they feed the narrative

These are not disclaimers to collect at the end. Each concern is flagged
at the moment the relevant chart or result appears.

### 1. Sample size within spells
A single Allegri season at Juventus is ~38 matches. Confidence intervals
on scoreline distributions will be wide. Show them explicitly — readers
who know statistics will respect it, readers who don't won't notice.

### 2. The "after" comparison is noisy by design
The manager who replaces Allegri inherits his squad, his tactical inertia,
sometimes his captain. If the distribution does not change immediately after
he leaves, that could mean the effect persists — or it could mean the next
manager has not changed things yet. Flag this at the moment the after-spell
charts appear.

### 3. Selection bias in the manager list
All nine managers are successful, mostly at big clubs. The comparison group
is not a random sample. De Zerbi at Brighton is the interesting outlier —
the exception that tests the rule.

### 4. Dominant teams can afford to defend a lead
Narrow wins might be a consequence of squad quality, not philosophy. A team
good enough to score once and shut the game down is different from a team
that wins 1-0 because that is the only way they know how to play. The
position-matched baseline partially addresses this — but only partially.
Flag the residual ambiguity explicitly.

### 5. No lab in football
To establish causation you need to replicate an experiment under the same
conditions, changing only one parameter. That is impossible in football.
What we can do is compare in plausibly similar scenarios. This is not a
weakness — it is the honest condition of all sports analysis. It is also
why we love it.

### 6. Correlation is not causation — step 1 and step 2
Knowing that correlation is not causation is step 1. Knowing how you would
actually check for causation is step 2. The article lives in the honest
space between the two.

## Notebooks and next steps

### Notebooks in scope

| Notebook | Purpose | Status |
|---|---|---|
| `tm_scraper.ipynb` | Build `tm_football.db` from Transfermarkt | Done |
| `validate_managers.ipynb` | Validate manager names and match counts | Done |
| `build_manager_matches.ipynb` | Build `manager_matches.csv` | Done |
| `build_league_baselines.ipynb` | Build `league_baselines.csv` | To build |
| `build_spell_comparisons.ipynb` | Build `spell_comparisons.csv` | To build |
| `build_position_baselines.ipynb` | Build `position_baselines.csv` | To build |
| `analysis_allegri.ipynb` | Allegri-focused analysis and charts | To build |
| `analysis_comparison.ipynb` | Cross-manager comparison | To build |

### Immediate next steps

1. Build `build_league_baselines.ipynb` — full league distributions by season
2. Build `build_spell_comparisons.ipynb` — before/during/after per manager-club spell
3. Decide whether position-matched baseline uses the existing Serie A standings
   dataset or is derived from `game_index` for non-Italian leagues
4. Start `analysis_allegri.ipynb` once the three data files are ready

### Open questions

- Time-of-goal data: flagged as low priority, potential future article
- Extending before/after to two seasons: revisit if one-season patterns
  are interesting enough to warrant it
- Statistical testing: chi-square on scoreline distributions to confirm
  patterns are distinguishable from noise — planned for analysis notebooks