"""Clean up cmd_noi from source"""
import re, os

src_dir = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\packaging\than_thong'

# Remove from inline_commands.py
path = os.path.join(src_dir, 'inline_commands.py')
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove cmd_noi function completely
content = re.sub(
    r"def cmd_noi\(text: str = \"\"\) -> dict:.*?(?=\ndef cmd_|\nimport string)",
    '',
    content,
    flags=re.DOTALL
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Cleaned cmd_noi from inline_commands.py')

# Remove from router.py
path2 = os.path.join(src_dir, 'router.py')
with open(path2, 'r', encoding='utf-8') as f:
    content = f.read()

for item in ['    cmd_noi,\n']:
    content = content.replace(item, '')

for item in ['    "noi": cmd_noi,\n', '    "speak": cmd_noi,\n', '    "doc": cmd_noi,\n']:
    content = content.replace(item, '')

with open(path2, 'w', encoding='utf-8') as f:
    f.write(content)
print('Cleaned cmd_noi from router.py')

print('\nDone! All voice app references removed.')
