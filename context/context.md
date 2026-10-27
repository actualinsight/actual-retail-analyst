# Context

Everything the agent needs to know before answering a question. Nothing here runs: it's the company's knowledge, written down so the agent never has to guess.

| Folder | What's in it | Read it when |
|---|---|---|
| [company/](company/about.md) | Who Actual Burger Co. is: concept, guests, markets, channels, priorities | You need business background: who the guests are, how they order, what leadership is focused on |
| [data-model/](data-model/context.md) | Every table and column, how they join, the rules for every query, the **known data issues**, and the standard definitions and SQL for every metric | Before writing any SQL or calculating any number |

**For a new question,** start with `data-model/context.md`: it sets the reading order for the data. Read `company/about.md` for the business background.
