# References, Task List, ...
## Poetry
- [Poetry - Python dependency management and packaging made easy](https://python-poetry.org/).
- [Python Poetry in 8 Minutes](https://youtu.be/Ji2XDxmXSOM).
- [How to Create and Use Virtual Environments in Python With Poetry](https://youtu.be/0f3moPe_bhk).

```bash
poetry install
poetry shell
python main.py
exit
```
`.venv` folder and `poetry.lock` file. See [Basic usage](https://python-poetry.org/basic-usage/).

## data/
### loader.py
- [polars.read_csv](https://docs.pola.rs/api/python/stable/reference/api/polars.read_csv.html).

### cleaner.py
- [ ] re
- [ ] e.g., `condition1`
- [ ] `na_to_none`, useless?

### descriptor.py
- [ ] list comprehensions

## agent_based_model/
### houses.py
- [ ] `get_quality_score` thresholds

### house_market.py
- [ ] `get_houses_that_meet_requirements` availability

### consumers.py
- [x] ~~`consumer.savings`~~ or ~~`is None`~~ (main.py)

`initial_savings` or `is not None`.

### simulation.py

