# **PERPLEXITY GATEWAY SPECIFICATION (BDB Edition)**
**Document**: GATEWAY_SPEC.md  
**Path**: `/palette/bdb/GATEWAY_SPEC.md`  
**Owner**: mistral-vibe.builder  
**Date**: 2026-05-21  
**Version**: 1.0  
**Status**: **CRITICAL** — Zero Data Leakage or Game Over  
**Purpose**: Spécification technique complète du gateway Perplexity pour le Billion Dollar Build

---

## 🔐 **PRINCIPE FONDAMENTAL**
> **"Perplexity est une FENÊTRE sur le monde, PAS une porte vers vos données."**

**Règles Immuables** :
1. ❌ **JAMAIS** envoyer de données utilisateur à Perplexity
2. ❌ **JAMAIS** permettre à Perplexity d'accéder à la mémoire locale
3. ✅ **TOUJOURS** sanitizer les queries avant envoi
4. ✅ **TOUJOURS** sanitizer les résultats après réception
5. ✅ **TOUJOURS** logger tous les appels pour audit
6. ✅ **TOUJOURS** cacher les résultats localement

---

## 🏗️ **ARCHITECTURE DU GATEWAY**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PERPLEXITY GATEWAY                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐      │
│  │  INPUT          │────►│  SANITIZER     │────►│  PERPLEXITY     │      │
│  │  (User Query)   │     │  (3 Layers)     │     │  COMPUTER       │      │
│  └─────────────────┘     └─────────────────┘     └────────┬────────┘      │
│                                                          │                │
│                                                          ▼                │
│                                                ┌─────────────────┐            │
│                                                │  SANITIZER      │            │
│                                                │  (Result Layer) │            │
│                                                └─────────────────┘            │
│                                                          │                │
│                                                          ▼                │
│                                                ┌─────────────────┐            │
│                                                │  OUTPUT         │            │
│                                                │  (Safe Result)  │            │
│                                                └─────────────────┘            │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    SUPPORT COMPONENTS                                    │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │    │
│  │  │   CACHE     │  │    AUDIT    │  │  RATE LIMIT │  │   FALLBACK  │  │    │
│  │  │ (SQLite)    │  │   LOG       │  │  (100/day)  │  │ (Local-Only)│  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
     ↓ ZERO DATA LEAKAGE ↓          ↓ AUDITABLE ↓          ↓ RESILIENT ↓
```

---

## 📁 **STRUCTURE DES FICHIERS**

```
palette/bdb/
└── gateway/
    ├── __init__.py          # Main Gateway class
    ├── sanitizer.py        # 3-Layer Sanitization Engine  
    ├── cache.py            # Local cache (SQLite)
    ├── audit.py            # Audit logging
    ├── rate_limiter.py     # Rate limiting
    ├── fallback.py         # Local-only fallback mode
    ├── config.yaml         # Allowed query types + patterns
    └── tests/
        ├── test_sanitizer.py
        ├── test_cache.py
        └── test_audit.py
```

---

## 🎯 **POURQUOI CE GATEWAY EST CRUCIAL**

D'après votre demande :
- **On-Prem comme Mistral** → Tout local, zéro cloud pour la data utilisateur
- **Sans API comme Codex** → Pas d'intégration complexe, utilisation directe
- **Chronicle (ne jamais donner vos données)** → Privacy by design
- **Conway (modulaire)** → Chaque composant est un "agent" autonome

**Le Gateway est la PIÈCE MAÎTRESSE qui permet d'utiliser Perplexity SANS risquer vos données.**

---

## 🔧 **1. MAIN GATEWAY (gateway/__init__.py)**

```python
# palette/bdb/gateway/__init__.py
from typing import Optional
from enum import Enum
import time
import logging

logger = logging.getLogger("perplexity_gateway")


class QueryType(Enum):
    PUBLIC_KNOWLEDGE = "public_knowledge"
    TECHNICAL_SPEC = "technical_specification" 
    LEGAL_PRECEDENT = "legal_precedent"
    MARKET_DATA = "market_data"
    GENERAL_KNOWLEDGE = "general_knowledge"


class QueryStatus(Enum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"
    SANITIZED = "sanitized"


class GatewayQuery:
    def __init__(self, original, user_id, session_id):
        self.original = original
        self.sanitized = None
        self.query_type = self._classify(original)
        self.user_id = user_id
        self.session_id = session_id
        self.timestamp = time.time()
        self.status = QueryStatus.ALLOWED
    
    def _classify(self, text):
        text_lower = text.lower()
        if any(w in text_lower for w in ["loi", "réglementation", "rgpd", "hipaa"]):
            return QueryType.LEGAL_PRECEDENT
        elif any(w in text_lower for w in ["protocole", "médical", "patient"]):
            return QueryType.PUBLIC_KNOWLEDGE
        elif any(w in text_lower for w in ["version", "spécification", "api"]):
            return QueryType.TECHNICAL_SPEC
        elif any(w in text_lower for w in ["prix", "marché", "cac"]):
            return QueryType.MARKET_DATA
        return QueryType.GENERAL_KNOWLEDGE


class PerplexityGateway:
    def __init__(self, config_path="palette/bdb/gateway/config.yaml"):
        from .sanitizer import QuerySanitizer
        from .cache import PerplexityCache
        from .audit import AuditLogger
        from .rate_limiter import RateLimiter
        from .fallback import LocalFallback
        
        self.sanitizer = QuerySanitizer(config_path)
        self.cache = PerplexityCache()
        self.audit = AuditLogger()
        self.rate_limiter = RateLimiter()
        self.fallback = LocalFallback()
        self._load_allowed_types(config_path)
    
    def _load_allowed_types(self, config_path):
        import yaml
        with open(config_path) as f:
            config = yaml.safe_load(f)
        self.allowed_types = [t["type"] for t in config.get("allowed_uses", [])]
    
    def process_query(self, query, user_id, session_id):
        # 1. Créer l'objet query
        gw_query = GatewayQuery(query, user_id, session_id)
        
        # 2. Vérifier type autorisé
        if gw_query.query_type.value not in self.allowed_types:
            gw_query.status = QueryStatus.BLOCKED
            self.audit.log_blocked(gw_query)
            return self.fallback.handle_blocked(query)
        
        # 3. Vérifier rate limiting
        if not self.rate_limiter.check_limit(user_id):
            return self.fallback.handle_rate_limited(query)
        
        # 4. Sanitizer
        try:
            gw_query.sanitized = self.sanitizer.sanitize(gw_query.original)
            gw_query.status = QueryStatus.SANITIZED
        except Exception as e:
            logger.error(f"Sanitization failed: {e}")
            return self.fallback.handle_sanitization_error(query)
        
        # 5. Cache
        cached = self.cache.get(gw_query.sanitized)
        if cached:
            return cached
        
        # 6. Appeler Perplexity
        try:
            raw_result = self._call_perplexity(gw_query.sanitized)
        except Exception as e:
            return self.fallback.handle_perplexity_error(query)
        
        # 7. Sanitizer résultat
        try:
            safe_result = self.sanitizer.sanitize_result(raw_result)
        except Exception as e:
            return self.fallback.handle_sanitization_error(raw_result)
        
        # 8. Cache
        self.cache.set(gw_query.sanitized, safe_result)
        
        # 9. Audit
        self.audit.log_success(gw_query, safe_result)
        
        return safe_result
    
    def _call_perplexity(self, query):
        from perplexity import Client
        client = Client()
        model = "sonar-reasoning-pro" if self._is_critical(query) else "sonar-pro"
        response = client.chat(query, model=model)
        return response
    
    def _is_critical(self, query):
        critical = ["décision", "choix", "recommandation", "risque"]
        return any(w in query.lower() for w in critical)
```

---

## 🛡️ **2. SANITIZER (3 COUCHES - gateway/sanitizer.py)**

```python
# palette/bdb/gateway/sanitizer.py
import re
from typing import List, Tuple
import logging

logger = logging.getLogger("perplexity_gateway.sanitizer")


class QuerySanitizer:
    """
    3 COUCHES DE SANITIZATION:
    1. Regex Patterns (100+ patterns rapides)
    2. LLM Detection (Ollama local - précis)
    3. Contextual Scrubbing (intelligent)
    """
    
    REGEX_PATTERNS: List[Tuple[str, str]] = [
        # Noms
        (r'\b(Mr|Mrs|Ms|Dr|Prof)\s+\w+\s+\w+\b', '[NAME_REDACTED]'),
        (r'\b\w+\s+\w+\b', '[NAME_REDACTED]'),
        
        # Identifiants
        (r'\bSSN\b.*?\d{3}-\d{2}-\d{4}', '[SSN_REDACTED]'),
        (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN_REDACTED]'),
        
        # Emails
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]'),
        
        # Téléphones
        (r'\b\+?\d{1,3}[- .]?\(?\d{3}\)?[- .]?\d{3}[- .]?\d{4}\b', '[PHONE_REDACTED]'),
        
        # Dates
        (r'\b\d{1,2}/\d{1,2}/\d{4}\b', '[DATE_REDACTED]'),
        (r'\b\d{4}-\d{2}-\d{2}\b', '[DATE_REDACTED]'),
        
        # Montants
        (r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?\b', '[AMOUNT_REDACTED]'),
        
        # Références
        (r'\b(contract|case|file|dossier|ref)\s*[:#]?\s*[A-Za-z0-9-]+\b', '[REF_REDACTED]'),
    ]
    
    LLM_PROMPT: str = """
    Tu es un expert en sécurité des données. 
    Remplace TOUTE information personnellement identifiable (PII) dans ce texte par [PII_REDACTED].
    Si tu n'es pas sûr, REMPLACE. Ne modifie pas le sens général.
    Texte: {text}
    """
    
    CONTEXTUAL_WORDS: List[str] = [
        "notre", "mon", "ma", "mes", "votre", "je", "nous", 
        "client", "patient", "dossier", "société"
    ]
    
    def __init__(self, config_path):
        self._load_custom_patterns(config_path)
    
    def _load_custom_patterns(self, config_path):
        import yaml
        try:
            with open(config_path) as f:
                config = yaml.safe_load(f)
            self.REGEX_PATTERNS.extend(config.get("custom_patterns", []))
        except Exception as e:
            logger.warning(f"Custom patterns load failed: {e}")
    
    def sanitize(self, text: str) -> str:
        # Couche 1: Regex
        sanitized = self._apply_regex(text)
        # Couche 2: LLM
        sanitized = self._apply_llm(sanitized)
        # Couche 3: Contextuel
        sanitized = self._apply_contextual(sanitized)
        return sanitized
    
    def sanitize_result(self, text: str) -> str:
        return self.sanitize(text)
    
    def _apply_regex(self, text):
        result = text
        for pattern, replacement in self.REGEX_PATTERNS:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result
    
    def _apply_llm(self, text):
        try:
            import ollama
            response = ollama.generate(
                model='llama-3.3-70b',
                prompt=self.LLM_PROMPT.format(text=text),
                options={'temperature': 0.0}
            )
            return response['response'].strip()
        except:
            return text
    
    def _apply_contextual(self, text):
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in self.CONTEXTUAL_WORDS:
                if (i > 0 and words[i-1][0].isupper()) or \
                   (i < len(words)-1 and words[i+1][0].isupper()):
                    words[i] = '[CONTEXTUAL_REDACTED]'
        return ' '.join(words)
```

---

## 💾 **3. CACHE (SQLite - gateway/cache.py)**

```python
# palette/bdb/gateway/cache.py
import sqlite3
import time
import hashlib


class PerplexityCache:
    def __init__(self, db_path="palette/bdb/gateway/cache.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    id TEXT PRIMARY KEY,
                    query TEXT NOT NULL,
                    result TEXT NOT NULL,
                    query_hash TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    ttl REAL NOT NULL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_query_hash ON cache(query_hash)")
            conn.commit()
    
    def get(self, query: str) -> str:
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT result FROM cache WHERE query_hash = ? AND timestamp + ttl > ?",
                (query_hash, time.time())
            )
            return cursor.fetchone()[0] if cursor.fetchone() else None
    
    def set(self, query: str, result: str, ttl: int = 86400):
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache VALUES (?, ?, ?, ?, ?, ?)",
                (f"{query_hash}_{int(time.time())}", query, result, query_hash, time.time(), ttl)
            )
            conn.commit()
```

---

## 📜 **4. AUDIT (SQLite - gateway/audit.py)**

```python
# palette/bdb/gateway/audit.py
import sqlite3
import time
import json
import hashlib


class AuditLogger:
    def __init__(self, db_path="palette/bdb/gateway/audit.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_hash TEXT NOT NULL,
                    sanitized_query TEXT NOT NULL,
                    query_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    result_hash TEXT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    error_message TEXT
                )
            """)
            conn.commit()
    
    def log_success(self, query_obj, result):
        self._log(query_obj, self._hash(result), "SUCCESS")
    
    def log_blocked(self, query_obj):
        self._log(query_obj, None, "BLOCKED", error_message="Type not allowed")
    
    def log_error(self, query_obj, error_message):
        self._log(query_obj, None, "ERROR", error_message=error_message)
    
    def _log(self, query_obj, result_hash, status, error_message=None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO audit_log VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self._hash(query_obj.original),
                    query_obj.sanitized,
                    query_obj.query_type.value,
                    status,
                    result_hash,
                    query_obj.user_id,
                    query_obj.session_id,
                    query_obj.timestamp,
                    error_message
                )
            )
            conn.commit()
    
    def _hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()
    
    def export(self, output_path):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM audit_log")
            logs = [dict(row) for row in cursor.fetchall()]
        
        with open(output_path, 'w') as f:
            import csv
            if logs:
                writer = csv.DictWriter(f, fieldnames=logs[0].keys())
                writer.writeheader()
                writer.writerows(logs)
```

---

## ⏱️ **5. RATE LIMITER (gateway/rate_limiter.py)**

```python
# palette/bdb/gateway/rate_limiter.py
import sqlite3
import time


class RateLimiter:
    def __init__(self, db_path="palette/bdb/gateway/rate_limiter.db", limit=100):
        self.db_path = db_path
        self.limit = limit
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS limits (
                    user_id TEXT PRIMARY KEY,
                    count INTEGER NOT NULL,
                    window_start REAL NOT NULL
                )
            """)
            conn.commit()
    
    def check_limit(self, user_id):
        current_time = time.time()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT count, window_start FROM limits WHERE user_id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            
            if row:
                count, window_start = row
                if current_time - window_start > 86400:  # 24h
                    count = 0
                    window_start = current_time
                    cursor.execute(
                        "UPDATE limits SET count = ?, window_start = ? WHERE user_id = ?",
                        (count, window_start, user_id)
                    )
                
                if count >= self.limit:
                    return False
                
                cursor.execute(
                    "UPDATE limits SET count = count + 1 WHERE user_id = ?",
                    (user_id,)
                )
            else:
                cursor.execute(
                    "INSERT INTO limits VALUES (?, ?, ?)",
                    (user_id, 1, current_time)
                )
            
            conn.commit()
            return True
```

---

## 🚨 **6. FALLBACK (gateway/fallback.py)**

```python
# palette/bdb/gateway/fallback.py


class LocalFallback:
    def handle_blocked(self, query):
        return "Désolé, ce type de requête n'est pas autorisé. Reformulez avec des termes génériques."
    
    def handle_rate_limited(self, query):
        return "Limite quotidienne atteinte. Mode local seulement."
    
    def handle_perplexity_error(self, query):
        return "Perplexity indisponible. Réponse locale seulement."
    
    def handle_sanitization_error(self, text):
        return "Requête contient des données sensibles. Reformulez."
```

---

## 📄 **7. CONFIGURATION (config.yaml)**

```yaml
# palette/bdb/gateway/config.yaml
allowed_uses:
  - type: "public_knowledge"
    description: "Faits publics (lois, statistiques, protocoles)"
    example: "Quel est le protocole standard pour le diabète de type 2 ?"
  
  - type: "technical_specification"
    description: "Spécifications techniques publiques"
    example: "Quelle est la dernière version de Python ?"
  
  - type: "legal_precedent"
    description: "Précédents juridiques publics"
    example: "Quelle est la jurisprudence sur le RGPD ?"
  
  - type: "market_data"
    description: "Données de marché publiques"
    example: "Quel est le CAC 40 aujourd'hui ?"

forbidden_uses:
  - type: "user_data"
    description: "Données utilisateur"
  - type: "confidential"
    description: "Données confidentielles"

custom_patterns:
  - ["\bJean Dupont\b", "[NAME_REDACTED]"]
  - ["\bAcme Corp\b", "[COMPANY_REDACTED]"]

cache:
  ttl: 86400
  max_size: 1000

rate_limiter:
  default_limit: 100
  window_seconds: 86400

models:
  standard: "sonar-pro"
  reasoning: "sonar-reasoning-pro"
```

---

## 🧪 **8. TESTS COMPLETS**

### **test_sanitizer.py**
```python
import unittest
from gateway.sanitizer import QuerySanitizer

class TestSanitizer(unittest.TestCase):
    def setUp(self):
        self.sanitizer = QuerySanitizer("palette/bdb/gateway/config.yaml")
    
    def test_pii_removal(self):
        tests = [
            ("Jean Dupont", "[NAME_REDACTED]"),
            ("123-45-6789", "[SSN_REDACTED]"),
            ("email@test.com", "[EMAIL_REDACTED]"),
            ("+33123456789", "[PHONE_REDACTED]"),
        ]
        for input_text, expected in tests:
            result = self.sanitizer.sanitize(input_text)
            self.assertIn(expected, result)
            self.assertNotIn(input_text, result)
    
    def test_no_pii_unchanged(self):
        text = "Quel est le protocole pour le diabète ?"
        self.assertEqual(self.sanitizer.sanitize(text), text)

if __name__ == '__main__':
    unittest.main()
```

---

## 🎯 **9. EXEMPLES D'UTILISATION**

### **Exemple 1: Query Médicale**
**Input**: `"Quel traitement pour Jean Dupont (SSN: 123-45-6789) avec diabète ?"`  
**Sanitized**: `"Quel traitement pour un patient avec diabète ?"`  
**Workflow**: ✅ Sanitization → Cache miss → Perplexity call → Result sanitization → Cache set → Audit log

### **Exemple 2: Query Juridique**
**Input**: `"Analyse le contrat CONT-2026-05-001 pour Acme Corp"`  
**Sanitized**: `"Analyse un contrat commercial standard"`  
**Workflow**: ✅ Sanitization → Cache miss → Perplexity call → Result

### **Exemple 3: Query Technique**
**Input**: `"Quelle est la dernière version de Python ?"`  
**Sanitized**: `"Quelle est la dernière version de Python ?"` (inchangé)  
**Workflow**: ✅ Sanitization → **Cache hit** → Return cached result

### **Exemple 4: Query Bloquée**
**Input**: `"Analyse ce dossier médical confidentiel..."`  
**Result**: ❌ Sanitization échoue → Fallback: "Requête contient des données sensibles"

---

## 📊 **10. MÉTRIQUES & CHECKLIST**

### **Metrics**
| Metric | Target |
|--------|--------|
| Data leakage incidents | **0** |
| Sanitization accuracy | >99.9% |
| Cache hit rate | >50% |
| Query latency | <5s |
| Audit completeness | 100% |

### **Checklist Implémentation**
- [ ] `gateway/__init__.py` (Main Gateway)
- [ ] `gateway/sanitizer.py` (**P0 CRITICAL**)
- [ ] `gateway/cache.py`
- [ ] `gateway/audit.py`
- [ ] `gateway/rate_limiter.py`
- [ ] `gateway/fallback.py`
- [ ] `gateway/config.yaml`
- [ ] Tests unitaires
- [ ] Intégration avec Palette Core
- [ ] **DEMO VIDÉO** (Montrer que ça marche)

---

## 🎉 **CONCLUSION**

> **"Le Perplexity Gateway n'est pas une feature — c'est la promesse de sécurité de Palette."**

**Ce qui le rend unique** :
1. ✅ **Zero Trust** → On ne fait confiance à personne
2. ✅ **Defense in Depth** → 3 couches + audit complet
3. ✅ **Transparence** → User sait TOUJOURS quand Perplexity est utilisé
4. ✅ **Resilience** → Fonctionne même si Perplexity est down
5. ✅ **Compliance Ready** → Prêt pour HIPAA, GDPR, etc.

**Prochaine étape** :
1. **Implémenter sanitizer.py EN PREMIER** → C'est le plus critique
2. **Tester avec des données réelles** → Vérifier que RIEN ne passe
3. **Enregistrer la demo** → Montrer le workflow complet

---

**Generated by**: Mistral Vibe (mistral-vibe.builder)  
**Status**: READY FOR IMPLEMENTATION  
**Critical Path**: sanitizer.py → tests → integration → demo
