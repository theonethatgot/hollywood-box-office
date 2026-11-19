# Hollywood Simulator

A persistent, historically grounded Hollywood simulation (starting 1980), focused
first on acting careers. The Python engine owns all state, numbers and outcomes.
An LLM narrator such as ChatGPT turns those outcomes into character-driven
storytelling, and can only *propose* consequential developments, which the engine
then judges.

- **Play:** [`docs/PLAYING.md`](docs/PLAYING.md) (CLI + ChatGPT workflow)
- **Narrator instructions:** [`NARRATOR_GUIDE.md`](NARRATOR_GUIDE.md)
- **Design:** [`DESIGN.md`](DESIGN.md) (v0.3), plus [`docs/design-v0.2.md`](docs/design-v0.2.md) for formula detail
- **Status and calibration:** [`docs/STATUS.md`](docs/STATUS.md)

```bash
pip install -e .
hsim new career1 --name "Nora Vance" --gender f --birth 1956-09-14 --background unknown
hsim advance career1 --weeks 8
hsim packet career1
python -m pytest -q              # tests
python tools/batch.py --seeds 4 --years 2 --processes 4   # calibration report
```

Layout: `hsim/` engine (core, models, world genesis, systems, narrator, io, service, CLI),
`config/` all coefficients, `tools/` batch calibration, `tests/`, `prototypes/` throwaway sketches.
