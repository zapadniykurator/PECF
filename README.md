# PECF
<div align="center">
  <img src="PECF.png" alt="Pecf logo">
</div>
**PECF** (Python Easy Configuration Files) is a lightweight configuration language for Python.  
It combines human‑friendly syntax with the power of executable expressions – without sacrificing safety.

PECF started as a small experiment 4 years ago, and then was abandoned.  
Today, with **MPECFGA** (Make PECF Great Again), it has evolved into a fast, convenient, and practical tool.

---

## Why PECF?

- ✅ **Readable** – clean syntax, no unnecessary brackets or quotes   
- ✅ **Flexible** – automatic type handling, no need to declare types  
- ✅ **Powerful** – `do:` lets you compute values on the fly  
- ✅ **Convenient** – load configs from files, URLs, or raw strings with one method  


## Syntax comparison

**PECF:**

```hello: world;```


**JSON:**
```json
{"hello": "world"}
```

ey features
🔁 No type declaration required
text
name: PECF;
version: 1.0;
enabled: true;
PECF automatically understands strings, numbers, and booleans.

🧠 On‑the‑fly evaluation with do:
text
calculated: do: 1000 - 7;
message: do: "Hello, " + "World!";
Useful for dynamic configuration values, small expressions, or derived data.

📁 Load from anything – with .upload()
python
import pecf

# From a raw string
pecf.upload("answer: do: 40 + 2;")

# From a local .pecf file
pecf.upload("config/config.pecf")

# From a remote URL (HTML or raw PECF)
pecf.upload("https://example.com/api")

# Quick start
Install PECF: **pip install pecf**

```python
import pecf
pecf.upload("name_variable: str: you variable meaning there!;")
print(pecf.get("name_variable"))

Result: "you variable meaning there!"
```
# Documentation
Current MPECFGA branch (reccomended for using)
- <a href="">Wiki for PECF 1.0.0 </a>

Older not stable versions (Not reccomend for use)

- <a href="https://github.com/Zedikon/PECF/wiki/PECF-WIKI-PAGE-(version-1.0.25)">Wiki for 1.0.25</a>



- <a href="https://github.com/Zedikon/PECF/wiki/PECF-WIKI-PAGE-(version-1.0.26)"> Wiki for 1.0.26</a>


# MPECFGA
Note: the language has evolved significantly since those versions.
The new syntax is more human, faster, and more reliable.

Status
PECF is actively developed under MPECFGA (Make PECF Great Again).
It is stable enough for real projects, but still welcomes constructive feedback.