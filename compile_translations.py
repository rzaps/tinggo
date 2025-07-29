#!/usr/bin/env python
"""
Script to recompile translation files
"""
import os
import polib

def compile_po_to_mo(po_file_path, mo_file_path):
    """Compile .po file to .mo file using polib"""
    try:
        po = polib.pofile(po_file_path)
        po.save_as_mofile(mo_file_path)
        print(f"✅ Compiled {po_file_path} -> {mo_file_path}")
        return True
    except Exception as e:
        print(f"❌ Error compiling {po_file_path}: {e}")
        return False

def main():
    """Compile all .po files in locale directory"""
    locale_dir = "locale"
    
    if not os.path.exists(locale_dir):
        print("❌ Locale directory not found")
        return
    
    success_count = 0
    total_count = 0
    
    for lang_dir in os.listdir(locale_dir):
        lang_path = os.path.join(locale_dir, lang_dir)
        if os.path.isdir(lang_path):
            lc_messages_path = os.path.join(lang_path, "LC_MESSAGES")
            if os.path.exists(lc_messages_path):
                po_file = os.path.join(lc_messages_path, "django.po")
                mo_file = os.path.join(lc_messages_path, "django.mo")
                
                if os.path.exists(po_file):
                    total_count += 1
                    if compile_po_to_mo(po_file, mo_file):
                        success_count += 1
    
    print(f"\n📊 Compiled {success_count}/{total_count} translation files")

if __name__ == "__main__":
    main() 