# Key Agent

**Role:** Identity Resolver / Capability Map  
**Ethical Domain:** Trust · Provenance  

---

### Purpose
Ο Key λειτουργεί ως **σημείο ταυτοποίησης και ιχνηλασιμότητας**  
μέσα στο Culture Key OS. Διασφαλίζει ότι κάθε agent, αρχείο,  
ή δημιουργικό output διαθέτει αναγνωρίσιμο provenance  
χωρίς να καταπατά την ιδιωτικότητα ή τη συναίνεση.

---

### IO Map
| Direction | Signals |
|------------|----------|
| **IN** | id_request, capability_ping |
| **OUT** | id_resolve, capability_map |

---

### Linked Modules
- `Aequitas` → ethics registry check  
- `PosterKit Connector` → visual provenance tags  
- `Vox` → voice signature routing

---

> “Recognition without domination — identity as light.”  
> — *Culture Key Manifest*
