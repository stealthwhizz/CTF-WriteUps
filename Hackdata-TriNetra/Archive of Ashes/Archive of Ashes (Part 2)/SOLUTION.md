# Archive of Ashes (Part 2) - Solution

## Challenge: "Any guesses who did it?"

### Evidence Analysis:

#### 1. Document Metadata
```bash
unzip -p "Abernathy Archives/Evidence_Bag_Site04/Recovered_Doc_Abernathy.docx" docProps/core.xml
```
**Creator:** Dr. Dubsky

#### 2. Letter Content
- From: Silas Abernathy to Dr. Alistair Dubsky
- Exposes fraud: Dubsky's "grant" for Aethelgard Institute was actually a fraudulent payout
- Abernathy threatens to report to District Attorney

#### 3. Recovery Log (DELETED_NOTE_RECOVERY.txt)
Journal entries showing the perpetrator's actions:
- **09/12**: Moved Green and Morgan to use as scapegoats
- **10/10**: "Abernathy is getting close. He keeps asking about the 2004 ledgers. I can't let him publish."
- **10/14**: The Archive burned, Logan Anderson framed
- **10/15**: Police accept false narrative blaming Green and Morgan

### Conclusion:

**The Culprit: Dr. Alistair Dubsky**

Motive: Destroy evidence of the 1999 Blackwood Vale fraud before Abernathy could expose him
Method: Burned the archive, drugged and manipulated Logan Anderson to make him appear guilty, used Green and Morgan as phantom suspects

## Flag Format:
Likely variations:
- `TriNetra{Dr_Dubsky}`
- `TriNetra{Dubsky}`
- `TriNetra{Dr. Dubsky}`
- `TriNetra{Alistair_Dubsky}`
- `TriNetra{Dr.Dubsky}`
