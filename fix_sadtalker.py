import os

def patch_sadtalker():
    # The specific file causing the crash
    target_file = "src/face3d/util/preprocess.py"
    
    if not os.path.exists(target_file):
        print(f"❌ File not found: {target_file}")
        print("Are you in the root 'Linly-Talker' folder?")
        return

    print(f"🔧 Patching {target_file}...")
    
    with open(target_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(target_file, "w", encoding="utf-8") as f:
        for line in lines:
            # Comment out the specific line causing the crash
            if "warnings.filterwarnings" in line and "VisibleDeprecationWarning" in line:
                f.write(f"# {line.strip()} # PATCHED FOR NUMPY 2.0+ COMPATIBILITY\n")
                print("✅ Found and disabled the broken warning filter.")
            else:
                f.write(line)
    
    print("✨ Patch complete! Upload the patched file to Hugging Face.")

if __name__ == "__main__":
    patch_sadtalker()
