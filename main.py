import sys
import os
from gui import JokerSigmaTerminal

def main():
    if not os.path.exists("reports"):
        os.makedirs("reports")
    try:
        app = JokerSigmaTerminal()
        app.mainloop()
    except Exception as e:
        print(f"[FATAL ERROR]: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
