# zipcode-street-distance
Calculated the street driving distance between zip codes using Google Cloud API 

Ensure all dataset files do not end with a newline otherwise the code will break.

## Create Conda ENV

### To make a requirements file

pip3 freeze > requirements.txt

### To use a requirements file

Replace `foo_env` with desired environment

```bash
conda create --name foo_env --file requirements.txt
```

### Force VS code to use this by default

Make a directory called `.vscode`
inside this directory make one file `settings.json` containing the following
information tailored to your environment.

```json
{
    "python.pythonPath": "/usr/local/anaconda3/envs/foo_env/bin/python"
}
```
