"""Script de correction automatique des erreurs flake8 les plus courantes."""
import re
from pathlib import Path
from typing import List


def get_indentation(line: str) -> str:
    """Retourne l'indentation d'une ligne."""
    return line[: len(line) - len(line.lstrip())]


def fix_docstring(line: str) -> str:
    """Corrige les docstrings pour respecter D400/D401."""
    indent = get_indentation(line)

    if line.strip().startswith('"""'):
        # Vérifie si c'est une docstring multi-lignes
        if '"""' in line.strip()[3:]:
            # Single line docstring
            content = line.strip()[3:-3].strip()
            if not content.endswith("."):
                content += "."
            return f'{indent}"""{content}."""\n'  # Note le double point
        else:
            # Multi-line docstring
            content = line.strip()[3:].strip()
            if not content.endswith("."):
                content += "."
            return f'{indent}"""{content}."""\n'  # Note le double point
    return line


def fix_line_length(line: str) -> List[str]:
    """Découpe intelligemment les lignes trop longues (E501)."""
    if len(line) <= 79:
        return [line]

    indent = get_indentation(line)

    # Cas des retours de fonction avec dictionnaire
    if "return" in line and "{" in line:
        match = re.search(
            r'return\s*{\s*"message":\s*"([^"]+)"\s*},\s*(\d+)', line
        )
        if match:
            message, status = match.groups()
            return [
                f"{indent}return {{\n",
                f'{indent}    "message": "{message}"\n',
                f"{indent}}}, {status}\n",
            ]

    # Cas des descriptions de champs flask-restx
    if "fields.String" in line and "description=" in line:
        # Extrait les parties de la ligne
        match = re.search(
            r'(.*fields\.String\([^)]*description=")([^"]+)(")\),?', line
        )
        if match:
            prefix, desc, suffix = match.groups()
            return [f"{indent}{prefix}\n", f'{indent}    {desc}"),\n']

    # Découpage standard avec indentation
    return [line[:79] + "\n", indent + "    " + line[79:] + "\n"]


def analyze_imports(lines: List[str]) -> set:
    """Analyse les imports utilisés dans le code."""
    used_imports = set()
    for line in lines:
        # Cherche les noms utilisés dans le code
        words = re.findall(r"\b\w+\b", line)
        used_imports.update(words)
    return used_imports


def fix_code(file_path: Path) -> None:
    """Corrige le code du fichier donné."""
    print(f"🔧 Fixing {file_path}")

    with open(file_path, "r") as file:
        lines = file.readlines()

    # Analyse des imports utilisés
    used_names = analyze_imports(lines)

    new_lines = []
    in_multiline_docstring = False

    for line in lines:
        # Gestion des docstrings
        if '"""' in line:
            in_multiline_docstring = not in_multiline_docstring
            if not in_multiline_docstring:
                line = fix_docstring(line)

        # Gestion des imports
        if "import" in line:
            imported_name = re.search(r"from .* import (\w+)", line)
            if imported_name and imported_name.group(1) not in used_names:
                continue

        # Gestion de la longueur des lignes
        if len(line) > 79:
            new_lines.extend(fix_line_length(line))
        else:
            new_lines.append(line)

    with open(file_path, "w") as file:
        file.writelines(new_lines)


# def main():
#     """Point d'entrée principal."""
#     part3_path = Path('part3')

#     for filepath in part3_path.rglob('*.py'):
#         if filepath.is_file():
#             fix_code(filepath)

#     print("✨ All files have been processed!")


def main():
    """Point d'entrée principal."""
    file_path = Path("app/api/v1/auth.py")
    if file_path.exists():
        fix_code(file_path)
        print("✨ File has been processed!")
    else:
        print("❌ File not found!")


if __name__ == "__main__":
    main()
