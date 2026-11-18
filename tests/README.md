## What I learned

I built this project to practise Python on a realistic data-quality problem:
checking raw text files line by line and deciding whether each line is Valid,
a Warning (fixable) or an Error (unusable).

- **Git and GitHub:** I set up a virtual environment, made small commits and
  pushed them to GitHub. I also fixed mistakes with files in the wrong folder.
- **Encoding:** Files are bytes, and the encoding decides how they become
  text. I detect it first with charset-normalizer instead of guessing.
- **Validation:** I defined my own Valid/Warning/Error rules first, then
  turned them into code. My first attempt got two lines wrong (an impossible
  time and extra spaces), which taught me to check values and not just format.
- **SQLite:** I store every result and keep the original raw line unchanged,
  so the data stays traceable.
- **Testing:** I wrote 9 pytest tests, one for each rule, so I notice
  immediately if a change breaks something.
- **Debugging:** Excel on my PC splits CSV columns at commas, not semicolons,
  so I reverted my first export setting after testing it.

Next I want to add an Excel export and charts with Matplotlib.