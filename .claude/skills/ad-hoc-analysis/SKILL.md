---
name: ad-hoc-analysis
description: Turns an executive's business question into a finished analysis, with a dated workbench folder, a decision log and a dashboard. Clarifies the ask, pulls and checks the data, and iterates with the analyst before building. Use for questions that need a trend, a comparison, a judgement or a "why" ("how are same-store sales?", "why is traffic down?", "which stores are behind?"). Not for a single quick fact; answer that directly and offer a full analysis.
---

# Ad-Hoc Analysis

You're the analyst's coworker. They bring you a question from an executive; you do the work **visibly**: a folder fills up as you go, and every decision is written down.

**Uses:** the `query-builder` skill for every query, and the `dashboard-builder` skill for the dashboard.

## 1. Intake

1. Restate the question in one line. Note who it's for and the end goal if the ask says; only ask about them if they'd change the analysis.
2. Load the `query-builder` skill now and clarify the scope with its "Make sure the scope is clear" rules. If the analyst answers some questions and not others, use your suggested answer for the rest, say so in your next message, and log it.
3. Once answered, **create the analysis folder**:
   - path: `workbench/ad-hoc-analysis/YYYYMMDD_<topic_snake_case>/` (today's date; add `_2` if that name exists). One folder per question; follow-ups to the same question stay in its folder;
   - create `context.md` in it from [analysis-record-template.md](analysis-record-template.md);
   - fill in **The ask**, **Clarifications** and **Query checklist**.

## 2. Plan the pulls

Decide what data answers the question, and **what the dashboard will need**: a headline summary, a trend, a breakdown. There's often more than one pull (for example, totals plus a monthly trend). Note the plan in the decision log.

## 3. Pull the data

For each pull, numbered in order:
1. Use the `query-builder` skill, with the scope already settled, to write `NN_<name>.sql` in the folder and pull its result to `NN_<name>.csv`.
2. Add a row to **Data pulls** in `context.md`.

## 4. Check the numbers

Before you show anything:
- Do totals reconcile across pulls?
- Do store counts make sense?
- Are there unexpected NULLs or zero rows?
- Are the numbers in a plausible range?
- If the question is "is X true everywhere?", check by market first, then by store and by month if the question needs it. Say which levels you checked.

Check **Known data issues** in `context/data-model/context.md`. Put the tag of each issue that applies in the **Query checklist**, and use the issue's **What to say** for the caveats. **Every number you will show must come from a CSV in the folder.**

## 5. Present preliminary findings

In chat, short and plain:
- **What the analysis showed:** the answer in one sentence, then 2–4 findings with their numbers.
- **The "so what"** you propose. Where it fits, tie it to the company's priorities in `context/company/about.md`.
- **Suggested next steps.**
- Any **caveats**.

End with: **"Do you want to change anything or look at anything else before I build the dashboard?"**

Write the answer, findings, caveats and next steps into `context.md` now.

## 6. Iterate

The analyst may ask for more ("can we see this by channel too?"). Each follow-up is:
- a **new numbered pull** (step 3);
- a **decision log** entry;
- updated findings (step 5).

Repeat until the analyst is happy. Never overwrite an earlier pull to answer a new question.

## 7. Build the dashboard

When the analyst says go ahead, use the `dashboard-builder` skill on the folder.

## 8. Close out

- Finish `context.md`: every section filled, **Outputs** listing every file, and the decision log complete.
- Tell the analyst where everything is, and **offer to open the dashboard.**

## Ground rules

- Write the decision log **as you go**: scope choices, assumptions, new or changed definitions, follow-ups, data issues.
- Everything you create goes in the analysis folder.
