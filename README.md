# Reto
Reto is a simple Python app that scrapes job in Indeed and exports it into a readable `.xlsx` file. Currently it is based upon the results given by *Indeed*. This is heavily inspired of the growing layoffs in the tech industry and using this app might help them get a job much more easier than the traditional way.

`Reto` is a Filipino word meaning to **recommend** or **suggest**.

## Installation

Reto is dependent with [Textual](https://github.com/Textualize/textual) and [Selenium](https://pypi.org/project/selenium/) for web scraping so check them first if you already have them!

### Textual
```
pip install "textual[dev]"
```

### Selenium
```
pip install selenium
```

## Running the Program

**Reto** has 2 version namely, `reto.py` and `reto-lite.py`. Both have the same functionality but `reto.py` has a more user-friendly **TUI** while the "lite" version is only terminal-based.

After installing all the dependencies, you can simply run:

```
python reto.py
```

or

```
python reto-lite.py
```

## More Information

**Reto** only asks for `4` vital information.

| Input        | Description                               | Example             |
| ------------ | ----------------------------------------- | -------------       |
| Job Title    | The title of job                          | Software Engineer   |
| Job Location | The location for the job                  | Austin, TX          |
| Page         | entries of jobs. 1 page is ~13 entries.   | 3                   |
| Filename     | Name of the file to save the job listing  | joblisting-se       |

## Demonstration

![demo of reto](reto-demo.gif)
