import re
import sys

def remove_empty_try_catch(content):
    changed = True
    while changed:
        orig = content

        # Pattern 1a: Allman style, single-line empty catch
        content = re.sub(
            r'\n[ \t]*try\n([ \t]+)\{\n((?:(?!\1\})[^\n]*\n)*)\1\}\n\1catch \(\\Throwable \$th\) \{\}',
            lambda m: '\n' + re.sub(r'^    ', '', m.group(2), flags=re.MULTILINE),
            content
        )

        # Pattern 1b: Allman style, multi-line empty catch
        content = re.sub(
            r'\n[ \t]*try\n([ \t]+)\{\n((?:(?!\1\})[^\n]*\n)*)\1\}\n\1catch \(\\Throwable \$th\) \{\n\1\}',
            lambda m: '\n' + re.sub(r'^    ', '', m.group(2), flags=re.MULTILINE),
            content
        )

        # Pattern 2: Compact try{} with }catch(\Throwable $th){ whitespace-only-line }
        content = re.sub(
            r'\n([ \t]+)try\{\n((?:(?!\1\})[^\n]*\n)*)\1\}catch\(\\Throwable \$th\)\{[ \t]*\n[ \t]*\n\1\}',
            lambda m: '\n' + re.sub(r'^    ', '', m.group(2), flags=re.MULTILINE),
            content
        )

        # Pattern 3: Compact try{} with } catch (\Throwable $th){}
        content = re.sub(
            r'\n([ \t]+)try\{\n((?:(?!\1\})[^\n]*\n)*)\1\} catch \(\\Throwable \$th\)\{\}',
            lambda m: '\n' + re.sub(r'^    ', '', m.group(2), flags=re.MULTILINE),
            content
        )

        changed = content != orig

    return content

files = sys.argv[1:]
for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
    new_content = remove_empty_try_catch(content)
    with open(filepath, 'w') as f:
        f.write(new_content)
    print(f"Done: {filepath}")
