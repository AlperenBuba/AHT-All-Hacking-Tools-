# AHT 1.0b (All Hacking Tools)

It is a toolkit that allows you to easily use the best cybersecurity and hacking tools via terminal menus.

**Youtube Kanalı:** [Alperen Buba](https://www.youtube.com/@Alperenbuba/videos)

## ⚠️ Legal Disclaimer (Yasal Uyarı)
**NOTE:** This tool is developed strictly for **educational purposes, cybersecurity awareness, and authorized penetration testing.** The entire legal responsibility arising from the usage of this tool against unauthorized systems or unpermitted networks belongs solely to the end-user. The developer assumes no liability and is not responsible for any misuse, data loss, or legal violations caused by this program. By using this software, you agree to these terms.

## 🚀 Environment Setup
Clone the repository and install the Python dependencies:

\`\`\`bash
git clone https://github.com/AlperenBuba/AHT-All-Hacking-Tools-.git
cd AHT
pip install -r requirements.txt
\`\`\`

## 💻 Execution
Launch the primary interface with root privileges:

\`\`\`bash
sudo python3 main.py
\`\`\`

## 🎮 User Interface Workflow
To maintain a high-speed workflow, AHT utilizes specific input patterns:

* **Menu Navigation:** Enter \`0\` at any menu prompt to navigate back to the previous screen.
* **Data Entry:** When asked for inputs (IP, Phone, BSSID, Interface), pressing **ENTER** (leaving the field blank) will immediately cancel the current operation and redirect you to the main menu.

## 🛡 Security Warnings
* **Wireless Interface:** Ensure your network adapter supports "Monitor Mode."
* **Privileges:** Always run the tool with \`sudo\` permissions to avoid permission-denied errors.
* **Data Safety:** Ensure your \`.gitignore\` is correctly configured to avoid pushing sensitive logs to GitHub.

## 👤 Development
* **Lead Developer:** Alperen Buba
* **Project Name:** AHT (All Hacking Tools)
* **License:** MIT

> “Knowledge is the ultimate security vulnerability.”
