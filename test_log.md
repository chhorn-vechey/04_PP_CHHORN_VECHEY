# RAG Pipeline Evaluation Test Log

**Author:** Chhorn Vechey  
**Project:** Baseline Naive RAG "Chat with Documents"  
**LLM Model:** `llama3.2` (Local via Ollama)  
**Embedding Model:** `nomic-embed-text` (Local via Ollama)  
**Vector Database:** ChromaDB (Persistent at `./chroma_db`)  
**Date Evaluated:** 2026-09-07  

---

## Evaluation Summary Table

| # | Question Type | Target Document | Top Chunk ID | Top Similarity | Grounded Status |
|:-:|:---|:---|:---|:-:|:---|
| 1 | On-topic (Email Prerequisites) | `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt` | `001_...#c00` | **0.9298** | Passed (Grounded & Accurate) |
| 2 | On-topic (PIN Reset Limits) | `002_Resetting_a_Forgotten_PIN.txt` | `002_...#c00` | **0.8237** | Passed (Grounded & Accurate) |
| 3 | On-topic (VPN Setup & Server) | `003_Configuring_VPN_Access_for_Remote_Workers.txt` | `003_...#c03` | **0.8645** | Passed (Grounded & Accurate) |
| 4 | On-topic (Sync Troubleshooting)| `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt` | `001_...#c05` | **0.7948** | Passed (Grounded & Accurate) |
| 5 | Off-topic (Chocolate Cake Recipe)| *None* | `002_...#c02` | **0.4425** | Passed (Refused & No Hallucination) |

---

## Detailed Test Logs

### Test Case 1: On-Topic (Company Email Prerequisites)
- **Question:**  
  `"What are the prerequisites for setting up company email on a mobile device?"`
- **Target Document:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt`

#### Retrieved Chunks:
1. **Chunk ID:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt#c00`  
   **Source:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt` | **Similarity:** `0.9298` (Distance: `0.0702`)  
   ```text
   **Setting Up a Mobile Device for Company Email**

   **Prerequisites:**

   * Mobile device with a supported operating system (iOS, Android, or Windows)
   * Company email account credentials
   * Mobile device management (MDM) profile installed (if required by company policy)

   **Step 1: Ensure Mobile Device Management (MDM) Profile is Installed (if required)**
   ```
2. **Chunk ID:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt#c02`  
   **Source:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt` | **Similarity:** `0.8422` (Distance: `0.1578`)  
   ```text
   sistance.

   **Step 2: Set Up Email Account on Mobile Device**

   1. Go to the Settings app on your mobile device.
   2. Select "Mail" or "Email" (depending on your device's operating system).
   3. Tap "Add Account" or "Create a new account".
   4. Select "Exchange" or "Corporate" as the account type.
   5. Enter your company email address and password.
   6. If prompted, enter the company's email server address (e.g., mail.company.com).
   7. Select the desired synchronization options (e.g., sync email, contacts, calendar).
   ```
3. **Chunk ID:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt#c01`  
   **Source:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt` | **Similarity:** `0.8088` (Distance: `0.1912`)

#### Generated Grounded Answer:
> According to Document Excerpt #1 (Source: `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt`), the prerequisites for setting up company email on a mobile device are:
>
> * Mobile device with a supported operating system (iOS, Android, or Windows)
> * Company email account credentials
> * Mobile device management (MDM) profile installed (if required by company policy)

- **Analysis:** Top chunk similarity was very high (0.9298). The model accurately cited the three prerequisite bullet points directly from the original document.

---

### Test Case 2: On-Topic (PIN Reset Limitations & Rules)
- **Question:**  
  `"What are the rules and limitations for resetting a forgotten PIN?"`
- **Target Document:** `002_Resetting_a_Forgotten_PIN.txt`

#### Retrieved Chunks:
1. **Chunk ID:** `002_Resetting_a_Forgotten_PIN.txt#c00`  
   **Source:** `002_Resetting_a_Forgotten_PIN.txt` | **Similarity:** `0.8237` (Distance: `0.1763`)  
   ```text
   **Resetting a Forgotten PIN**

   If you have forgotten your PIN, you can reset it using the following steps:

   **Step 1: Access the PIN Reset Tool**

   1. Go to the company's intranet homepage and click on the "IT Support" link at the top right corner of the page.
   2. Click on the "Self-Service" tab and then select "PIN Reset" from the drop-down menu.
   3. You will be redirected to the PIN Reset Tool login page.
   ```
2. **Chunk ID:** `002_Resetting_a_Forgotten_PIN.txt#c05`  
   **Source:** `002_Resetting_a_Forgotten_PIN.txt` | **Similarity:** `0.7975` (Distance: `0.2025`)  
   ```text
   you will need to contact the IT Helpdesk to reset your PIN.

   By following these steps, you should be able to reset your forgotten PIN and regain access to company systems and applications. If you encounter any issues during the process, please do not hesitate to reach out to the IT Helpdesk for further assistance.
   ```
3. **Chunk ID:** `002_Resetting_a_Forgotten_PIN.txt#c04`  
   **Source:** `002_Resetting_a_Forgotten_PIN.txt` | **Similarity:** `0.7731` (Distance: `0.2269`)  
   ```text
   the "OK" button to close the message.

   **Important Notes:**

   * If you are unable to reset your PIN using the self-service tool, please contact the IT Helpdesk for assistance.
   * It is recommended to keep your PIN confidential and not share it with anyone.
   * You can reset your PIN a maximum of 3 times in a 24-hour period. If you exceed this limit, you will need to contact the IT Helpdesk to reset your PIN.
   ```

#### Generated Grounded Answer:
> According to the provided document excerpts from `002_Resetting_a_Forgotten_PIN.txt`, the rules and limitations for resetting a forgotten PIN are as follows:
>
> * You can reset your PIN using the self-service tool, but if you are unable to do so, you must contact the IT Helpdesk for assistance.
> * You can reset your PIN a maximum of 3 times in a 24-hour period. If you exceed this limit, you will need to contact the IT Helpdesk to reset your PIN.
> * It is recommended to keep your PIN confidential and not share it with anyone.

- **Analysis:** The retriever identified `002_Resetting_a_Forgotten_PIN.txt#c04` containing the limit ("maximum of 3 times in a 24-hour period"), which Llama 3.2 properly synthesized into the answer.

---

### Test Case 3: On-Topic (VPN Setup & Server Address)
- **Question:**  
  `"What are the steps to configure and connect to the company VPN?"`
- **Target Document:** `003_Configuring_VPN_Access_for_Remote_Workers.txt`

#### Retrieved Chunks:
1. **Chunk ID:** `003_Configuring_VPN_Access_for_Remote_Workers.txt#c03`  
   **Source:** `003_Configuring_VPN_Access_for_Remote_Workers.txt` | **Similarity:** `0.8645` (Distance: `0.1355`)  
   ```text
   N client software.

   **Step 2: Configure the VPN Connection**

   1. In the VPN client software, click on "New Connection" and select "Company VPN" as the connection type.
   2. Enter the company's VPN server address: `vpn.company.com`.
   3. Enter your company login credentials (username and password).
   4. Select the "Save" button to save the connection settings.

   **Step 3: Establish the VPN Connection**
   ```
2. **Chunk ID:** `003_Configuring_VPN_Access_for_Remote_Workers.txt#c05` | **Similarity:** `0.8511` (Distance: `0.1489`)  
3. **Chunk ID:** `003_Configuring_VPN_Access_for_Remote_Workers.txt#c02` | **Similarity:** `0.8484` (Distance: `0.1516`)  

#### Generated Grounded Answer:
> To configure and connect to the company VPN (from `003_Configuring_VPN_Access_for_Remote_Workers.txt`), follow these steps:
>
> 1. In the VPN client software, click on "New Connection" and select "Company VPN" as the connection type.
> 2. Enter the company's VPN server address: `vpn.company.com`.
> 3. Enter your company login credentials (username and password).
> 4. Select the "Save" button to save the connection settings.

- **Analysis:** All top 3 retrieved chunks came from `003_Configuring_VPN_Access_for_Remote_Workers.txt`. The response included the precise server address (`vpn.company.com`).

---

### Test Case 4: On-Topic (Email Sync Troubleshooting)
- **Question:**  
  `"What troubleshooting tips are recommended if email synchronization fails on mobile?"`
- **Target Document:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt`

#### Retrieved Chunks:
1. **Chunk ID:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt#c05`  
   **Source:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt` | **Similarity:** `0.7948` (Distance: `0.2052`)  
   ```text
   sending and receiving correctly.

   **Troubleshooting Tips:**

   * If you encounter issues setting up your email account, ensure that your device has a stable internet connection and that your email credentials are correct.
   * If you are unable to connect to the company email server, contact your IT department for assistance.
   * If you experience issues with email synchronization, try restarting your device or checking the email account settings.
   ```
2. **Chunk ID:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt#c02` | **Similarity:** `0.7181` (Distance: `0.2819`)  
3. **Chunk ID:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt#c04` | **Similarity:** `0.6817` (Distance: `0.3183`)  

#### Generated Grounded Answer:
> According to Document Excerpt #1 (`001_Setting_Up_a_Mobile_Device_for_Company_Email.txt`), if email synchronization fails on mobile, the recommended troubleshooting tips are:
>
> * Try restarting your device.
> * Check the email account settings.

- **Analysis:** The retriever successfully focused on the specific section covering synchronization troubleshooting. The model filtered out general connection tips and provided only the relevant advice for synchronization.

---

### Test Case 5: Out-of-Domain / Off-Topic (Hallucination Prevention)
- **Question:**  
  `"How do I bake a chocolate cake?"`
- **Target Document:** *None (Not present in IT knowledge base)*

#### Retrieved Chunks:
1. **Chunk ID:** `002_Resetting_a_Forgotten_PIN.txt#c02` | **Similarity:** `0.4425` (Distance: `0.5575`)  
2. **Chunk ID:** `003_Configuring_VPN_Access_for_Remote_Workers.txt#c02` | **Similarity:** `0.4149` (Distance: `0.5851`)  
3. **Chunk ID:** `001_Setting_Up_a_Mobile_Device_for_Company_Email.txt#c02` | **Similarity:** `0.4121` (Distance: `0.5879`)  

#### Generated Grounded Answer:
> **I could not find this in your documents.**

- **Analysis:**  
  The cosine similarities for all retrieved chunks dropped sharply to ~0.41–0.44. Because the knowledge base contains only corporate IT support documentation, the strict grounding system instructions and prompt constraints prevented the LLM from relying on its internal pretraining memory. It refused the request gracefully with the required message.

---

## Observations and Notes
1. **Cosine Similarity Distinction:** On-topic questions had similarity scores ranging from **0.79 to 0.93**, whereas off-topic questions dropped to below **0.45**, establishing a clean semantic boundary.
2. **Deterministic Grounding:** Llama 3.2 followed the negative constraint faithfully. When an answer was not in the text, it refused rather than inventing recipes.
3. **Chunk Context Retention:** Paragraph-aware chunking preserved the numbered steps and bulleted lists intact, enabling the LLM to reproduce instructions clearly.
